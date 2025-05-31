
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
);
