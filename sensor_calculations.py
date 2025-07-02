import math

def calc_absolute_humidity(temp_c, rh):
    temp_k = temp_c + 273.15
    es = 6.112 * math.exp((17.67 * temp_c) / (temp_c + 243.5))
    e = rh * es / 100.0
    ah = 216.7 * (e / temp_k)
    return round(ah, 2)

def calc_dew_point(temp_c, rh):
    a = 17.27
    b = 237.7
    alpha = ((a * temp_c) / (b + temp_c)) + math.log(rh / 100.0)
    dp = (b * alpha) / (a - alpha)
    return round(dp, 2)

def calc_vpd(temp_c, rh):
    es = 0.6108 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    e = rh / 100.0 * es
    vpd = es - e
    return round(vpd, 2)
