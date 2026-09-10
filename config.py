import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class Config:
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("BASE_URL")
    openai_model = os.getenv("OPENAI_MODEL")
    history_path = os.getenv("HISTORY_PATH")

    MAX_CITIES_PER_REQUEST = 3          #单次查询最多允许的城市数量
    MAX_TOOL_CALLS_PER_ROUND = 6        #单轮对话中，模型最多可以调用多少个工具
    MAX_CONCURRENT_REQUESTS = 4         #最大并发请求数。
    TOOL_BATCH_TIMEOUT = 30             #整批工具调用的最大等待时间（秒）
    HTTP_TIMEOUT = (10, 30)               # 单个 HTTP 请求的超时设置（连接超时=3秒，读取超时=8秒）
    MAX_HISTORY_TURNS = 6               #长期记忆最多保留多少轮对话
    MAX_TOOL_ROUNDS = 6                 #一次用户提问，程序最多允许模型进行几轮工具调用循环

def create_client():

    base_url = os.getenv('BASE_URL')
    api_key = os.getenv('OPENAI_API_KEY')
    openai_model = os.getenv('OPENAI_MODEL')

    if not base_url or not api_key or not openai_model:
        raise RuntimeError('请先配置环境变量')

    client = OpenAI(
        base_url=base_url,
        api_key=api_key,
        timeout=60.0,
        max_retries=2
    )

    return client, openai_model



# if __name__ == "__main__":
#     print("=" * 60)
#     print("🧪 直接运行 config.py 验证模块一本身")
#     print("=" * 60)
#
#     # ✅ 修正：通过 Config 类访问，而不是直接写变量名
#     print(f"OPENAI_API_KEY: {'已配置' if Config.api_key else '未配置'}")
#     print(f"OPENAI_MODEL: {Config.openai_model}")
#     print(f"BASE_URL: {Config.base_url or '使用官方'}")
#     print(f"HTTP_TIMEOUT: {Config.HTTP_TIMEOUT}")
#
#     try:
#         client, model = create_client()
#         print(f"✅ 客户端创建成功: {model}")
#     except RuntimeError as e:
#         print(f"⚠️ 客户端创建失败（如缺Key是预期行为）: {e}")

















