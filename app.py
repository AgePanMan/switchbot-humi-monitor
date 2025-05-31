from flask import Flask, request, jsonify, render_template, Response
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
import json
from sensor_calculations import calc_absolute_humidity, calc_dew_point, calc_vpd

app = Flask(__name__)
load_dotenv()

DB_PATH = "db.sqlite3"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            device_name TEXT,
            device_type TEXT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            absolute_humidity REAL,
            dew_point REAL,
            vpd REAL,
            power REAL,
            voltage REAL,
            electricity REAL,
            current REAL
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            device_name TEXT,
            device_type TEXT,
            timestamp TEXT,
            temperature REAL,
            humidity REAL,
            absolute_humidity REAL,
            dew_point REAL,
            vpd REAL,
            power REAL,
            voltage REAL,
            electricity REAL
        );
        """)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT device_name, device_type FROM sensor_data")
    devices = cur.fetchall()
    result = {}
    for name, dtype in devices:
        cur.execute("""
            SELECT timestamp, temperature, humidity, absolute_humidity, dew_point, vpd, power, voltage, electricity, current
            FROM sensor_data
            WHERE device_name=? AND timestamp BETWEEN ? AND ?
            ORDER BY timestamp
        """, (name, from_date + " 00:00:00", to_date + " 23:59:59"))
        rows = cur.fetchall()
        result[name] = {
            "type": dtype,
            "data": [
                {
                    "timestamp": r[0],
                    "temperature": r[1],
                    "humidity": r[2],
                    "absolute_humidity": r[3],
                    "dew_point": r[4],
                    "vpd": r[5],
                    "power": r[6],
                    "voltage": r[7],
                    "electricity": r[8], "current": r[9]
                } for r in rows
            ]
        }
    conn.close()
    return Response(json.dumps(result, ensure_ascii=False), content_type="application/json; charset=utf-8")

@app.route("/add", methods=["POST"])
def add():
    token = os.getenv("SWITCHBOT_TOKEN")
    headers = {"Authorization": token}
    res = requests.get("https://api.switch-bot.com/v1.1/devices", headers=headers).json()
    devices = res.get("body", {}).get("deviceList", [])
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    for dev in devices:
        dev_id = dev.get("deviceId")
        dev_name = dev.get("deviceName")
        dev_type = dev.get("deviceType")

        if not dev_type or not (dev_type.startswith("Meter") or dev_type.startswith("Plug")):
            continue

        status = requests.get(
            f"https://api.switch-bot.com/v1.1/devices/{dev_id}/status",
            headers=headers
        ).json().get("body", {})

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if dev_type.startswith("Meter"):
            temp = status.get("temperature")
            hum = status.get("humidity")
            if temp is not None and hum is not None:
                ah = calc_absolute_humidity(temp, hum)
                dp = calc_dew_point(temp, hum)
                vpd = calc_vpd(temp, hum)
                cur.execute("""
                    INSERT INTO sensor_data (
                        device_id, device_name, device_type, timestamp,
                        temperature, humidity, absolute_humidity, dew_point, vpd
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (dev_id, dev_name, dev_type, now, temp, hum, ah, dp, vpd))

        elif dev_type.startswith("Plug"):
            power = status.get("weight")  # 消費電力 (W)
            voltage = status.get("voltage")
            current = status.get("current")
            electricity = status.get("electricityOfDay")
            voltage = status.get("voltage")
            electricity = status.get("electricityOfDay")
            cur.execute("""
                INSERT INTO sensor_data (
                    device_id, device_name, device_type, timestamp,
                    power, voltage, electricity, current
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (dev_id, dev_name, dev_type, now, power, voltage, electricity, current))

    conn.commit()
    conn.close()
    return "OK"

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
