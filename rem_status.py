import requests
from bs4 import BeautifulSoup

REM_URL = "https://web.archive.org/web/20260218020902/https://rem.info/en/travelling/network-status#tab-service"

def get_rem_status():
    r = requests.get(REM_URL, timeout=10)
    r.raise_for_status()
    file = open("out.txt", "w")
    file.write(r.text)
    file.close()
    soup = BeautifulSoup(r.text, "html.parser")

    status = soup.find("span", {"aria-label": True})

    if status:
        return status["aria-label"]

    return "unknown"
    
if __name__ == "__main__":
    print(get_rem_status())