import sqlite3, json
from datetime import datetime, timedelta

DB_PATH = "db.sqlite3"
OUTPUT_FILE = "data.json"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# 直近30日分のデータを抽出
to_date = datetime.now()
from_date = to_date - timedelta(days=30)

cur.execute("SELECT DISTINCT device_name, device_type FROM sensor_data")
devices = cur.fetchall()

result = {}

for name, dtype in devices:
    cur.execute("""
        SELECT timestamp, temperature, humidity, absolute_humidity, dew_point, vpd,
               power, voltage, electricity, current
        FROM sensor_data
        WHERE device_name=? AND timestamp BETWEEN ? AND ?
        ORDER BY timestamp
    """, (name, from_date.strftime("%Y-%m-%d %H:%M:%S"), to_date.strftime("%Y-%m-%d %H:%M:%S")))
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
                "electricity": r[8],
                "current": r[9],
            } for r in rows
        ]
    }

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

conn.close()
