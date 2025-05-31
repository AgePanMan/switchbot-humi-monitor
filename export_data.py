import sqlite3, json

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

cur.execute("SELECT DISTINCT device_name FROM sensor_data")
devices = [row[0] for row in cur.fetchall()]
result = {}

for device in devices:
    cur.execute("""
        SELECT timestamp, temperature, humidity
        FROM (
            SELECT * FROM sensor_data
            WHERE device_name = ?
            ORDER BY id DESC LIMIT 100
        ) ORDER BY timestamp ASC
    """, (device,))
    rows = cur.fetchall()
    result[device] = [
        {"timestamp": r[0], "temperature": r[1], "humidity": r[2]}
        for r in rows
    ]

with open("data.json", "w") as f:
    json.dump(result, f, indent=2)

conn.close()
