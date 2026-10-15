import math
import datetime
import json

def calculate_panchang():
    # भारतीय मानक समय (IST = UTC + 5:30)
    utc_now = datetime.datetime.utcnow()
    ist_now = utc_now + datetime.timedelta(hours=5, minutes=30)
    today = ist_now.date()

    weekdays_hi = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
    months_hi = ["जनवरी", "फ़रवरी", "मार्च", "अप्रैल", "मई", "जून", "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]
    day_hi = weekdays_hi[today.weekday()]
    date_str_hi = f"{day_hi}, {today.day} {months_hi[today.month - 1]} {today.year}"

    # संवत गणना
    vikram_samvat = today.year + 57
    shak_samvat = today.year - 78
    samvat_str = f"विक्रम संवत {vikram_samvat} | शक संवत {shak_samvat}"

    # खगोलीय जूलियन गणना (Astronomical Algorithm)
    year, month, day = today.year, today.month, today.day
    dt_calc = datetime.datetime(year, month, day, 0, 30, 0)
    y, m, d = dt_calc.year, dt_calc.month, dt_calc.day
    if m <= 2:
        y -= 1
        m += 12
    A = math.floor(y / 100)
    B = 2 - A + math.floor(A / 4)
    jd = math.floor(365.25 * (y + 4716)) + math.floor(30.6001 * (m + 1)) + d + B - 1524.5
    jd += (dt_calc.hour + dt_calc.minute / 60.0) / 24.0

    T = (jd - 2451545.0) / 36525.0

    # सूर्य देशांतर
    L0 = (280.46646 + 36000.76983 * T) % 360
    M = (357.52911 + 35999.05029 * T) % 360
    M_rad = math.radians(M)
    C = (1.914602 - 0.004817 * T) * math.sin(M_rad) + 0.019993 * math.sin(2 * M_rad)
    sun_lon = (L0 + C) % 360

    # चंद्र देशांतर
    Lp = (218.3164477 + 481267.88123421 * T) % 360
    D = (297.8501921 + 445267.1114034 * T) % 360
    Mp = (134.9633964 + 477198.8675055 * T) % 360
    F = (93.2720950 + 483202.0175233 * T) % 360

    moon_lon = Lp + 6.288774 * math.sin(math.radians(Mp)) \
                  + 1.274027 * math.sin(math.radians(2*D - Mp)) \
                  + 0.658314 * math.sin(math.radians(2*D)) \
                  + 0.213618 * math.sin(math.radians(2*Mp)) \
                  - 0.185116 * math.sin(math.radians(M)) \
                  - 0.114332 * math.sin(math.radians(2*F))
    moon_lon = moon_lon % 360

    # लाहिड़ी अयनांश
    ayanamsha = 23.8561 + 1.3960 * T
    sun_sidereal = (sun_lon - ayanamsha) % 360
    moon_sidereal = (moon_lon - ayanamsha) % 360

    # तिथि गणना
    diff = (moon_lon - sun_lon) % 360
    tithi_index = int(diff / 12) + 1

    tithi_names = [
        "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी", 
        "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी", 
        "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी"
    ]
    if tithi_index <= 15:
        paksha = "शुक्ल पक्ष"
        tithi_name = tithi_names[tithi_index - 1] if tithi_index <= 14 else "पूर्णिमा"
    else:
        paksha = "कृष्ण पक्ष"
        tithi_name = tithi_names[tithi_index - 16] if tithi_index <= 29 else "अमावस्या"

    # नक्षत्र गणना
    nakshatra_names = [
        "अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा",
        "पुनर्वसु", "पुष्य", "आश्लेषा", "मघा", "पूर्व फाल्गुनी", "उत्तर फाल्गुनी",
        "हस्त", "चित्रा", "स्वाति", "विशाखा", "अनुराधा", "ज्येष्ठा",
        "मूल", "पूर्वाषाढ़ा", "उत्तराषाढ़ा", "श्रवण", "धनिष्ठा", "शतभिषा",
        "पूर्व भाद्रपद", "उत्तर भाद्रपद", "रेवती"
    ]
    nakshatra_idx = int(moon_sidereal / (360.0 / 27.0)) % 27
    nakshatra_name = nakshatra_names[nakshatra_idx]

    # योग गणना
    yoga_names = [
        "विष्कम्भ", "प्रीति", "आयुष्मान", "सौभाग्य", "शोभन", "अतिगण्ड",
        "सुकर्मा", "धृति", "शूल", "गण्ड", "वृद्धि", "ध्रुव",
        "व्याघात", "हर्षण", "वज्र", "सिद्धि", "व्यतीपात", "वरीयान",
        "परिघ", "शिव", "सिद्ध", "साध्य", "शुभ", "शुक्ल",
        "ब्रह्म", "इन्द्र", "वैधृति"
    ]
    yoga_idx = int((sun_sidereal + moon_sidereal) % 360 / (360.0 / 27.0)) % 27
    yoga_name = yoga_names[yoga_idx]

    # करण गणना
    karana_idx = int(diff / 6)
    fixed_karanas = {0: "किस्तुघ्न", 57: "शकुनि", 58: "चतुष्पद", 59: "नाग"}
    repeating_karanas = ["बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टि (भद्रा)"]
    if karana_idx in fixed_karanas:
        karana_name = fixed_karanas[karana_idx]
    else:
        karana_name = repeating_karanas[(karana_idx - 1) % 7]

    # सूर्योदय और सूर्यास्त (भारत मानक केंद्र अक्षांश/देशांतर)
    day_of_year = today.timetuple().tm_yday
    gamma = 2 * math.pi / 365 * (day_of_year - 1)
    eqtime = 229.18 * (0.000075 + 0.001868 * math.cos(gamma) - 0.032077 * math.sin(gamma) \
             - 0.014615 * math.cos(2 * gamma) - 0.040849 * math.sin(2 * gamma))
    decl = 0.006918 - 0.399912 * math.cos(gamma) + 0.070257 * math.sin(gamma) \
           - 0.006758 * math.cos(2 * gamma) + 0.000907 * math.sin(2 * gamma)

    lat_rad = math.radians(28.6139)
    zenith = math.radians(90.833)
    cos_ha = (math.cos(zenith) / (math.cos(lat_rad) * math.cos(decl))) - (math.tan(lat_rad) * math.tan(decl))
    cos_ha = max(-1.0, min(1.0, cos_ha))
    ha_deg = math.degrees(math.acos(cos_ha))

    sunrise_utc_min = 720 - 4 * 77.2090 - eqtime - ha_deg * 4
    sunset_utc_min = 720 - 4 * 77.2090 - eqtime + ha_deg * 4

    sr_m = (sunrise_utc_min + 5.5 * 60) % 1440
    ss_m = (sunset_utc_min + 5.5 * 60) % 1440

    def min_to_str(m):
        hh = int(m // 60)
        mm = int(m % 60)
        ampm = "AM" if hh < 12 else "PM"
        d_hh = hh if 1 <= hh <= 12 else (hh - 12 if hh > 12 else 12)
        return f"{d_hh:02d}:{mm:02d} {ampm}"

    sr_str = min_to_str(sr_m)
    ss_str = min_to_str(ss_m)

    # मुहूर्त और राहुकाल
    day_len = ss_m - sr_m
    part_8 = day_len / 8.0
    w = today.weekday() # Mon=0, Sun=6
    rahu_parts = {0: 2, 1: 7, 2: 5, 3: 6, 4: 4, 5: 3, 6: 8}
    yama_parts = {0: 4, 1: 3, 2: 2, 3: 1, 4: 7, 5: 6, 6: 5}
    guli_parts = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 7}

    def format_part(p):
        st = sr_m + (p - 1) * part_8
        en = sr_m + p * part_8
        return f"{min_to_str(st)} - {min_to_str(en)}"

    part_15 = day_len / 15.0
    abhijit_str = f"{min_to_str(sr_m + 7 * part_15)} - {min_to_str(sr_m + 8 * part_15)}"
    brahma_str = f"{min_to_str((sr_m - 96) % 1440)} - {min_to_str((sr_m - 48) % 1440)}"
    amrit_str = f"{min_to_str(sr_m + 4.5 * part_8)} - {min_to_str(sr_m + 6 * part_8)}"

    # चंद्रोदय / चंद्रास्त का लगभग समय
    moon_offset = (diff / 360.0) * 1440
    mr_m = (sr_m + moon_offset) % 1440
    ms_m = (ss_m + moon_offset) % 1440

    data = {
        "date_hi": date_str_hi,
        "date_en": today.strftime("%Y-%m-%d"),
        "samvat": samvat_str,
        "day": day_hi,
        "sunrise": sr_str,
        "sunset": ss_str,
        "moonrise": min_to_str(mr_m),
        "moonset": min_to_str(ms_m),
        "tithi": tithi_name,
        "paksha": paksha,
        "nakshatra": nakshatra_name,
        "yoga": yoga_name,
        "karana": karana_name,
        "abhijit": abhijit_str,
        "amrit": amrit_str,
        "brahma": brahma_str,
        "rahukaal": format_part(rahu_parts[w]),
        "yamaganda": format_part(yama_parts[w]),
        "gulika": format_part(guli_parts[w]),
        "last_updated": ist_now.strftime("%Y-%m-%d %H:%M:%S IST")
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("data.json सफलतापूर्वक जनरेट हो गई है!")

if __name__ == "__main__":
    calculate_panchang()
