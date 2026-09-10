import requests

from config import Config

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

ALLOWED_URLS = {
    GEOCODING_URL,
    WEATHER_URL,
    AIR_QUALITY_URL,
}

def request_json(url, params):
    if url not in ALLOWED_URLS:
        return {'ok': False, 'error': 'url_not_allowed'}

    try:
        response = requests.get(
            url,
            params=params,
            timeout=Config.HTTP_TIMEOUT
        )
        response.raise_for_status()

    except requests.Timeout:
        return {'ok': False, 'error': 'request_timeout'}
    except requests.RequestException:
        return {'ok': False, 'error': 'request_failed'}

    try:
        data = response.json()
    except ValueError:
        return {'ok': False, 'error': 'invalid_response_json'}

    if not  isinstance(data, dict):
        return {'ok':False, 'error': 'invalid_response_shape'}

    return {'ok':True, 'data':data}


# if __name__ == "__main__":
#     print("=" * 60)
#     print("🧪 直接运行 http_client.py 验证模块二（HTTP安全通道）")
#     print("=" * 60)
#
#     # 1. 展示白名单内容
#     print("\n📌 测试 1：展示白名单内容")
#     for url in ALLOWED_URLS:
#         print(f"   ✅ {url}")
#
#     # 2. 测试白名单拦截（访问百度）
#     print("\n📌 测试 2：白名单拦截（访问百度）")
#     result_block = request_json("https://www.baidu.com", {"q": "test"})
#     if result_block.get("error") == "url_not_allowed":
#         print("   ✅ 拦截成功！返回错误: url_not_allowed")
#     else:
#         print(f"   ❌ 拦截失败，返回: {result_block}")
#
#     # 3. 测试真实网络请求（查询北京坐标）
#     print("\n📌 测试 3：真实网络请求（查询北京坐标）")
#     result_geo = request_json(GEOCODING_URL, {
#         "name": "北京",
#         "count": 1,
#         "format": "json"
#     })
#
#     if result_geo.get("ok"):
#         data = result_geo["data"]
#         results = data.get("results", [])
#         if results:
#             first = results[0]
#             print("   ✅ 网络请求成功！")
#             print(f"      - 名称: {first.get('name')}")
#             print(f"      - 纬度: {first.get('latitude')}")
#             print(f"      - 经度: {first.get('longitude')}")
#             print(f"      - 时区: {first.get('timezone')}")
#             print("\n🎉 模块二验证通过！白名单和网络通道完全正常。")
#         else:
#             print("   ⚠️ 请求成功但无候选城市")
#     else:
#         print(f"   ❌ 网络请求失败: {result_geo.get('error')}")
#         print("   → 请检查网络连接或VPN设置")












