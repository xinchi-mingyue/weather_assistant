from http_client import request_json, GEOCODING_URL, WEATHER_URL, AIR_QUALITY_URL


def search_city(city_name):
    cleaned_name = city_name.strip()
    if not cleaned_name:
        return {'ok': False, 'error': 'empty_city_name'}

    response = request_json(
        GEOCODING_URL,
        {
            'name': cleaned_name,
            'count': 5,
            'language': 'zh',
            'format': 'json',
        }
    )

    if not response['ok']:
        return response

    raw_results = response['data'].get('results') or []
    if not raw_results:
        return {'ok': False, 'error': 'city_not_found', 'city_name': cleaned_name}

    candidates = []
    for item in raw_results:
        required = {'name', 'latitude', 'longitude', 'timezone'}
        if not required.issubset(item):
            continue

        candidates.append(
            {
                "name": item["name"],
                "country": item.get("country"),
                "admin1": item.get("admin1"),
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "timezone": item["timezone"],
            }
        )

    if not candidates:
        return {'ok': False, 'error': 'city_data_incomplete'}

    if len(candidates) == 1:
        c = candidates[0]
        return {
            "ok": True,
            'query': cleaned_name,
            'city': c['name'],
            'country': c['country'],
            'admin1': c['admin1'],
            'latitude': c['latitude'],
            'longitude': c['longitude'],
            'timezone': c['timezone'],
        }

    return {
        'ok': True,
        'query': cleaned_name,
        'unique': False,
        'candidates': candidates
    }

def get_current_weather(
        latitude: float,
        longitude: float,
        timezone: str,
):
    response = request_json(
        WEATHER_URL,
        {
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone,
            'current': (
                'temperature_2m,'
                'apparent_temperature,'
                'precipitation,'
                'weather_code,'
                'wind_speed_10m'
            ),
        },
    )

    if not response['ok']:
        return response

    data = response['data']
    current = data.get('current')
    units = data.get('current_units')

    if not isinstance(current, dict) or not isinstance(units, dict):
        return {'ok': False, 'error': 'weather_fields_missing'}

    required = {
        'time',
        'temperature_2m',
        'apparent_temperature',
        'precipitation',
        'weather_code',
        'wind_speed_10m',
    }
    if not required.issubset(current):
        return {'ok': False, 'error': 'weather_fields_missing'}

    return {
        "ok": True,
        "data_time": current["time"],
        "temperature": current["temperature_2m"],
        "temperature_unit": units.get("temperature_2m"),
        "apparent_temperature": current["apparent_temperature"],
        "precipitation": current["precipitation"],
        "precipitation_unit": units.get("precipitation"),
        "weather_code": current["weather_code"],
        "wind_speed": current["wind_speed_10m"],
        "wind_speed_unit": units.get("wind_speed_10m"),
    }

def get_current_air_quality(
        latitude: float,
        longitude: float,
        timezone: str,
):
    response = request_json(
        AIR_QUALITY_URL,
        {
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone,
            'current': 'pm2_5,pm10,us_aqi'
        },
    )

    if not response['ok']:
        return response

    data = response['data']
    current = data.get('current')
    units = data.get('current_units')
    if not isinstance(current, dict) or not isinstance(units, dict):
        return {'ok': False, 'error': 'air_quality_fields_missing'}

    required = {'time', 'pm2_5', 'pm10', 'us_aqi'}
    if not required.issubset(current):
        return {'ok': False, 'error': 'air_quality_fields_missing'}

    return {
        'ok': True,
        'data_time': current['time'],
        'pm2_5': current['pm2_5'],
        'pm10': current['pm10'],
        'us_aqi': current['us_aqi'],
        'pm2_5_unit': units.get('pm2_5'),
        'pm10_unit': units.get('pm10'),
        'api_standard': 'US AQI',
    }


# if __name__ == "__main__":
#     print("=" * 60)
#     print("🧪 直接运行 tools.py 验证模块三（三个业务工具）")
#     print("=" * 60)
#
#     # ------ 测试 1：空输入拦截 ------
#     print("\n📌 测试 1：空输入拦截")
#     empty_result = search_city("   ")
#     if empty_result.get("error") == "empty_city_name":
#         print("   ✅ 空输入拦截成功")
#     else:
#         print(f"   ⚠️ 空输入返回异常: {empty_result}")
#
#     # ------ 测试 2：真实城市搜索（上海） ------
#     print("\n📌 测试 2：真实城市搜索（上海）")
#     city_result = search_city("上海")
#
#     if not city_result.get("ok"):
#         print(f"   ❌ 搜索失败: {city_result.get('error')}")
#         print("   → 请检查网络或模块二是否正常")
#         exit(1)  # 搜不到城市，后面的测试没必要继续了
#
#     city = city_result["candidates"][0]
#     print(f"   ✅ 搜索成功！首选: {city['name']}, {city.get('country', '未知')}")
#     print(f"      - 纬度: {city['latitude']}")
#     print(f"      - 经度: {city['longitude']}")
#     print(f"      - 时区: {city['timezone']}")
#
#     lat = city["latitude"]
#     lon = city["longitude"]
#     tz = city["timezone"]
#
#     # ------ 测试 3：当前天气查询 ------
#     print("\n📌 测试 3：当前天气查询")
#     weather = get_current_weather(lat, lon, tz)
#
#     if weather.get("ok"):
#         print("   ✅ 天气查询成功！")
#         print(f"      - 数据时间: {weather['data_time']}")
#         print(f"      - 温度: {weather['temperature']} {weather['temperature_unit']}")
#         print(f"      - 体感温度: {weather['apparent_temperature']}")
#         print(f"      - 风速: {weather['wind_speed']} {weather['wind_speed_unit']}")
#         print(f"      - 天气代码: {weather['weather_code']}")
#     else:
#         print(f"   ❌ 天气查询失败: {weather.get('error')}")
#         print("   → 提示：如果报 request_timeout，说明网络不通，请检查 VPN 或调大 config.py 的超时。")
#
#     # ------ 测试 4：当前空气质量查询 ------
#     print("\n📌 测试 4：当前空气质量查询")
#     air = get_current_air_quality(lat, lon, tz)
#
#     if air.get("ok"):
#         print("   ✅ 空气质量查询成功！")
#         print(f"      - 数据时间: {air['data_time']}")
#         print(f"      - PM2.5: {air['pm2_5']} {air['pm2_5_unit']}")
#         print(f"      - PM10: {air['pm10']} {air['pm10_unit']}")
#         print(f"      - US AQI: {air['us_aqi']} ({air['aqi_standard']})")
#     else:
#         print(f"   ❌ 空气质量查询失败: {air.get('error')}")
#         print("   → 提示：如果报 request_timeout，说明网络不通，请检查 VPN 或调大 config.py 的超时。")
#
#     # ------ 最终汇总 ------
#     print("\n" + "=" * 60)
#     if weather.get("ok") and air.get("ok"):
#         print("🎉 模块三全部通过！天气和空气质量数据都获取成功！")
#     elif weather.get("ok") or air.get("ok"):
#         print("⚠️ 模块三部分成功（天气或空气质量只拿到了一个）。")
#     else:
#         print("❌ 模块三测试失败。请检查网络连接或确认 config.py 中的超时设置。")
#











