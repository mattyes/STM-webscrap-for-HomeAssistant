ARG BUILD_FROM=ghcr.io/hassio-addons/base:16.3.2
FROM $BUILD_FROM

# Install Python and packages
RUN apk add --no-cache \
    python3 \
    py3-pip \
    py3-requests \
    py3-beautifulsoup4

WORKDIR /app

# Copy files
COPY src/ .

# Create simple run script using bashio
RUN echo '#!/usr/bin/with-contenv bashio' > /app/run.sh && \
    echo '' >> /app/run.sh && \
    echo 'HA_TOKEN_CONFIG=$(bashio::config "ha_token")' >> /app/run.sh && \
    echo 'UPDATE_INTERVAL=$(bashio::config "update_interval")' >> /app/run.sh && \
    echo '' >> /app/run.sh && \
    echo 'if [ -n "$HA_TOKEN_CONFIG" ] && [ "$HA_TOKEN_CONFIG" != "" ]; then' >> /app/run.sh && \
    echo '  export HA_TOKEN="$HA_TOKEN_CONFIG"' >> /app/run.sh && \
    echo '  bashio::log.info "Using configured token"' >> /app/run.sh && \
    echo 'else' >> /app/run.sh && \
    echo '  export HA_TOKEN="$SUPERVISOR_TOKEN"' >> /app/run.sh && \
    echo '  bashio::log.info "Using supervisor token"' >> /app/run.sh && \
    echo 'fi' >> /app/run.sh && \
    echo '' >> /app/run.sh && \
    echo 'export HA_URL="http://192.168.2.118:8123"' >> /app/run.sh && \
    echo '' >> /app/run.sh && \
    echo 'bashio::log.info "Starting STM Metro Status monitor..."' >> /app/run.sh && \
    echo 'bashio::log.info "Update interval: ${UPDATE_INTERVAL} seconds"' >> /app/run.sh && \
    echo '' >> /app/run.sh && \
    echo 'while true; do' >> /app/run.sh && \
    echo '  python3 metro_status.py' >> /app/run.sh && \
    echo '  sleep "${UPDATE_INTERVAL}"' >> /app/run.sh && \
    echo 'done' >> /app/run.sh && \
    chmod +x /app/run.sh

CMD ["/app/run.sh"]