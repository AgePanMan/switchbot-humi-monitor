import requests, json, sqlite3, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("SWITCHBOT_TOKEN")
DEVICE_LIST = json.loads(os.getenv("DEVICE_LIST"))

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json; charset=utf8"
}

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id TEXT,
    device_name TEXT,
    timestamp TEXT,
    temperature REAL,
    humidity REAL
)
""")

for device in DEVICE_LIST:
    device_id = device["id"]
    name = device["name"]
    url = f"https://api.switch-bot.com/v1.1/devices/{device_id}/status"
    res = requests.get(url, headers=headers).json()

    if res["message"] != "success":
        print(f"[WARN] Failed to get data from {name}")
        continue

    body = res["body"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO sensor_data (device_id, device_name, timestamp, temperature, humidity)
        VALUES (?, ?, ?, ?, ?)
    """, (device_id, name, timestamp, body["temperature"], body["humidity"]))

conn.commit()
conn.close()
