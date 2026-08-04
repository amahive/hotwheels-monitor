import json
import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

HEADERS = {
    "User-Agent":"Mozilla/5.0"
}

SEEN_FILE = "products_seen.json"

if os.path.exists(SEEN_FILE):
    with open(SEEN_FILE,"r") as f:
        seen = set(json.load(f))
else:
    seen = set()

new_seen = set(seen)

def telegram(msg):
    url=f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    requests.post(url,json={
        "chat_id":CHAT_ID,
        "text":msg
    })

def get_firstcry():

    url="https://www.firstcry.com/search?query=hot%20wheels"

    r=requests.get(url,headers=HEADERS)

    soup=BeautifulSoup(r.text,"lxml")

    items=[]

    for a in soup.select("a"):

        href=a.get("href","")

        text=a.get_text(" ",strip=True)

        if "hot wheels" in text.lower():

            items.append({
                "name":text,
                "url":"https://www.firstcry.com"+href if href.startswith("/") else href
            })

    return items

def get_hamleys():

    url="https://www.hamleys.in/search?q=hot+wheels"

    r=requests.get(url,headers=HEADERS)

    soup=BeautifulSoup(r.text,"lxml")

    items=[]

    for a in soup.select("a"):

        txt=a.get_text(" ",strip=True)

        if "hot wheels" in txt.lower():

            href=a.get("href","")

            items.append({
                "name":txt,
                "url":"https://www.hamleys.in"+href if href.startswith("/") else href
            })

    return items

def get_crossword():

    url="https://www.crossword.in/search?q=hot+wheels"

    r=requests.get(url,headers=HEADERS)

    soup=BeautifulSoup(r.text,"lxml")

    items=[]

    for a in soup.select("a"):

        txt=a.get_text(" ",strip=True)

        if "hot wheels" in txt.lower():

            href=a.get("href","")

            items.append({
                "name":txt,
                "url":"https://www.crossword.in"+href if href.startswith("/") else href
            })

    return items

stores=[
    ("FirstCry",get_firstcry),
    ("Hamleys",get_hamleys),
    ("Crossword",get_crossword)
]

for store,func in stores:

    try:

        for item in func():

            uid=item["url"]

            if uid not in seen:

                new_seen.add(uid)

                telegram(
f"""🚗 New Hot Wheels

Store: {store}

{item['name']}

{item['url']}

Check delivery for PIN 421201."""
                )

    except Exception as e:

        print(e)

with open(SEEN_FILE,"w") as f:
    json.dump(list(new_seen),f)