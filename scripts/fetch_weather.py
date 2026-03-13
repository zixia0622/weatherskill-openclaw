#!/usr/bin/env python3
"""
天气数据获取脚本 - 基于 Open-Meteo API（免费，无需 API Key）
支持多城市查询，输出结构化 JSON 或文字播报。

用法:
    python3 fetch_weather.py                          # 默认查北京
    python3 fetch_weather.py --city 北京              # 指定城市名
    python3 fetch_weather.py --lat 39.9042 --lon 116.4074  # 指定经纬度
    python3 fetch_weather.py --cities 北京,上海,广州   # 多城市查询
    python3 fetch_weather.py --json                   # JSON 输出
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime

CITY_COORDS = {
    "北京": (39.9042, 116.4074),
    "上海": (31.2304, 121.4737),
    "广州": (23.1291, 113.2644),
    "深圳": (22.5431, 114.0579),
    "成都": (30.5728, 104.0668),
    "杭州": (30.2741, 120.1551),
    "武汉": (30.5928, 114.3055),
    "南京": (32.0603, 118.7969),
    "西安": (34.3416, 108.9398),
    "重庆": (29.4316, 106.9123),
    "长沙": (28.2282, 112.9388),
    "天津": (39.0842, 117.2010),
    "苏州": (31.2990, 120.5853),
    "郑州": (34.7466, 113.6254),
    "厦门": (24.4798, 118.0894),
}

WMO_CODES = {
    0: "☀️ 晴", 1: "🌤️ 大部晴", 2: "⛅ 多云", 3: "☁️ 阴",
    45: "🌫️ 雾", 48: "🌫️ 冻雾",
    51: "🌦️ 小毛毛雨", 53: "🌦️ 毛毛雨", 55: "🌧️ 大毛毛雨",
    61: "🌧️ 小雨", 63: "🌧️ 中雨", 65: "🌧️ 大雨",
    71: "🌨️ 小雪", 73: "🌨️ 中雪", 75: "❄️ 大雪",
    80: "🌧️ 阵雨", 81: "🌧️ 中阵雨", 82: "⛈️ 强阵雨",
    95: "⛈️ 雷暴", 96: "⛈️ 雷暴+冰雹", 99: "⛈️ 强雷暴+冰雹",
}


def fetch_weather(lat, lon, city_name=""):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&daily=temperature_2m_max,temperature_2m_min,weathercode,"
        f"precipitation_sum,windspeed_10m_max,uv_index_max"
        f"&timezone=Asia/Shanghai&forecast_days=3"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "weather-push-skill/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError) as e:
        return {"error": str(e), "city": city_name}

    current = data.get("current_weather", {})
    daily = data.get("daily", {})
    wc = current.get("weathercode", -1)

    result = {
        "city": city_name, "fetch_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "current": {
            "temperature": current.get("temperature"),
            "windspeed": current.get("windspeed"),
            "weather_code": wc,
            "weather_desc": WMO_CODES.get(wc, f"未知({wc})"),
        },
        "today": {
            "date": daily.get("time", [None])[0],
            "temp_max": daily.get("temperature_2m_max", [None])[0],
            "temp_min": daily.get("temperature_2m_min", [None])[0],
            "weather_code": daily.get("weathercode", [None])[0],
            "weather_desc": WMO_CODES.get(daily.get("weathercode", [None])[0], ""),
            "precipitation": daily.get("precipitation_sum", [None])[0],
            "windspeed_max": daily.get("windspeed_10m_max", [None])[0],
            "uv_index_max": daily.get("uv_index_max", [None])[0],
        },
        "forecast": [],
    }
    for i in range(1, min(3, len(daily.get("time", [])))):
        result["forecast"].append({
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "weather_desc": WMO_CODES.get(daily["weathercode"][i], ""),
            "precipitation": daily["precipitation_sum"][i],
        })
    return result


def generate_report(d):
    if "error" in d:
        return f"❌ {d['city']} 天气获取失败: {d['error']}"
    c, t = d["current"], d["today"]
    lines = [
        f"🌤️ {d['city']}今日天气",
        f"当前: {c['weather_desc']} {c['temperature']}°C",
        f"最高 {t['temp_max']}°C | 最低 {t['temp_min']}°C",
        f"风速: {c['windspeed']} km/h",
    ]
    if t.get("precipitation") and t["precipitation"] > 0:
        lines.append(f"降水: {t['precipitation']}mm 💧")
    if t.get("uv_index_max") and t["uv_index_max"] >= 6:
        lines.append(f"紫外线: {t['uv_index_max']}（较强，注意防晒）🧴")
    temp = c["temperature"]
    if temp is not None:
        if temp <= 5: lines.append("🧥 天冷，注意保暖")
        elif temp >= 35: lines.append("🥵 高温，注意防暑")
        elif 20 <= temp <= 28: lines.append("😊 气温舒适，适合户外")
    if t.get("precipitation") and t["precipitation"] > 5:
        lines.append("☔ 记得带伞")
    if d.get("forecast"):
        lines.append("\n📅 未来预报:")
        for f in d["forecast"]:
            lines.append(f"  {f['date']} | {f['weather_desc']} | {f['temp_min']}~{f['temp_max']}°C")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="获取天气数据")
    parser.add_argument("--city", default="北京", help="城市名")
    parser.add_argument("--cities", help="多城市，逗号分隔")
    parser.add_argument("--lat", type=float, help="纬度")
    parser.add_argument("--lon", type=float, help="经度")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()

    queries = []
    if args.cities:
        for c in args.cities.split(","):
            c = c.strip()
            if c in CITY_COORDS:
                queries.append((c, *CITY_COORDS[c]))
            else:
                print(f"⚠️ 未知城市: {c}", file=sys.stderr)
    elif args.lat and args.lon:
        queries.append((args.city, args.lat, args.lon))
    else:
        if args.city in CITY_COORDS:
            queries.append((args.city, *CITY_COORDS[args.city]))
        else:
            print(f"❌ 未知城市: {args.city}。支持: {', '.join(CITY_COORDS.keys())}", file=sys.stderr)
            sys.exit(1)

    results = [fetch_weather(lat, lon, name) for name, lat, lon in queries]
    if args.json:
        print(json.dumps(results if len(results) > 1 else results[0], ensure_ascii=False, indent=2))
    else:
        print("\n---\n".join(generate_report(r) for r in results))


if __name__ == "__main__":
    main()
