import math

def calc_absolute_humidity(temp_c, rh_percent):
    # 絶対湿度 (g/m³)
    es = 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))
    e = es * rh_percent / 100
    ah = 216.7 * e / (temp_c + 273.15)
    return round(ah, 2)

def calc_dew_point(temp_c, rh_percent):
    # 露点温度 (°C)
    a = 17.27
    b = 237.7
    alpha = ((a * temp_c) / (b + temp_c)) + math.log(rh_percent / 100.0)
    dp = (b * alpha) / (a - alpha)
    return round(dp, 2)

def calc_vpd(temp_c, rh_percent):
    # 飽差 (VPD, kPa)
    es = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))  # 飽和水蒸気圧
    ea = es * rh_percent / 100  # 実効水蒸気圧
    vpd = es - ea
    return round(vpd, 2)
