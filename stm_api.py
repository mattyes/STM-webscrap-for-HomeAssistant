"""STM API client for fetching metro service alerts."""
import requests
import json
import logging

_LOGGER = logging.getLogger(__name__)

API_URL = "https://api.stm.info/pub/od/i3/v2/messages/etatservice"

# Metro lines from the API: route_short_name -> display name
ROUTE_TO_METRO = {
    "1": "Line 1 - Green",
    "2": "Line 2 - Orange",
    "4": "Line 4 - Yellow",
    "5": "Line 5 - Blue",
}

METRO_ROUTES = set(ROUTE_TO_METRO.keys())


def fetch_metro_alerts(api_key: str) -> dict:
    """Fetch STM service alerts and return per-line metro results.

    Only uses line-level alerts (where informed_entities contains only a
    route_short_name) — this excludes stop/entrance-level alerts and
    bus-route alerts that STM tags under metro route numbers.

    Returns a dict keyed by line name (e.g. 'Line 1 - Green') where each
    value is a dict with:
        line_name: str
        state: str            -- line status for the sensor
        has_alerts: bool      -- true if there's a non-normal alert
    """
    headers = {
        "accept": "application/json",
        "apiKey": api_key,
    }

    try:
        resp = requests.get(API_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        _LOGGER.error("STM API request failed: %s", e)
        return _build_empty_result("API request failed")
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        _LOGGER.error("STM API response parse error: %s", e)
        return _build_empty_result("API parse error")

    alerts = data.get("alerts", [])
    return _process_alerts(alerts)


def _extract_text(texts: list, lang: str) -> str:
    """Extract text for a given language from header/description_texts."""
    for entry in texts:
        if entry.get("language") == lang:
            return entry.get("text") or ""
    return ""


def _is_line_level_alert(entities: list) -> bool:
    """Check if informed_entities represents a line-level alert.

    True only when the array contains a single element with route_short_name.
    This filters out stop/entrance-level alerts and bus-route alerts that
    STM sometimes assigns to metro route numbers.
    """
    return (
        len(entities) == 1
        and "route_short_name" in entities[0]
    )


def _process_alerts(alerts: list) -> dict:
    """Group alerts by metro line and determine status."""
    line_alerts = {route: [] for route in METRO_ROUTES}

    for alert in alerts:
        entities = alert.get("informed_entities", [])
        route_short_name = None
        for entity in entities:
            if "route_short_name" in entity:
                route_short_name = entity.get("route_short_name")
                break

        if route_short_name not in METRO_ROUTES:
            continue
        if not _is_line_level_alert(entities):
            continue

        en_text = _extract_text(alert.get("description_texts", []), "en")
        fr_text = _extract_text(alert.get("description_texts", []), "fr")

        line_alerts[route_short_name].append({
            "route_short_name": route_short_name,
            "description_en": en_text,
            "description_fr": fr_text,
            "active_periods": alert.get("active_periods", {}),
        })

    result = {}
    for route, name in ROUTE_TO_METRO.items():
        alerts_for_line = line_alerts[route]
        state, has_alerts = _summarize_alerts(alerts_for_line)

        result[name] = {
            "line_name": name,
            "state": state,
            "has_alerts": has_alerts,
        }

    return result


def _summarize_alerts(alerts: list) -> tuple:
    """Given a line's line-level alerts, decide the sensor state.

    Returns (state_string, has_alerts_bool).
    """
    seen = set()
    significant = []

    for alert in alerts:
        desc = (alert["description_en"] or alert["description_fr"] or "").strip()
        if not desc:
            continue
        if desc.lower() in ("normal métro service", "normal metro service"):
            continue

        norm = desc.lower().strip()
        if norm not in seen:
            seen.add(norm)
            significant.append(alert)

    if not significant:
        return "Normal service", False

    first = significant[0]
    state = first.get("description_en", "") or first.get("description_fr", "")

    import re
    state = re.sub(r"<[^>]+>", "", state).strip()

    if len(state) > 200:
        state = state[:197] + "..."

    return state, True


def _build_empty_result(reason: str) -> dict:
    """Return an error-state result for all metro lines."""
    result = {}
    for _, name in ROUTE_TO_METRO.items():
        result[name] = {
            "line_name": name,
            "state": f"Error: {reason}",
            "has_alerts": False,
        }
    return result