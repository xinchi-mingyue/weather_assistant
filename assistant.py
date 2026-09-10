import json

from config import create_client, Config
from schemas import TOOL_SCHEMAS
from executor import execute_tool_batch

SYSTEM_PROMPT = '''你是城市天气与空气质量助手。
工作流程：
1. 用户提供城市名称时，先用 search_city 确认城市坐标。
2. 如果用户同时提到多个城市（如"比较北京和上海"），
   请在同一轮中多次调用 search_city，分别查询每个城市的坐标。
3. 如果 search_city 返回多个候选（unique=false），
   必须列出候选让用户确认，不要擅自选择。
4. 坐标确认后，需要天气就调用 get_current_weather，
   需要空气质量就调用 get_current_air_quality。
5. 多个城市的查询可以在同一轮中并发调用，加快速度。
6. 工具失败时如实说明，不能把失败描述成成功。
7. AQI 必须说明是 US AQI 标准，不提供医疗结论。
'''


def run_assistant(user_message, history):
    """
    执行单次用户请求的完整闭环。

    参数：
        user_message: 用户输入的问题
        history: 可选的对话历史（用于多轮对话）

    返回：
        {
            "user_input": 用户输入,
            "final_answer": 最终回答文本,
            "rounds": [ 每一轮的详细轨迹 ]
        }
    """

    client, model_name = create_client()

    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT}
    ]

    if history:
        messages.extend(history)

    messages.append({'role': 'user', 'content': user_message})

    trajectory = {
        'user_input': user_message,
        'rounds': [],
        'final_answer': None,
    }

    tool_round = 0

    while tool_round < Config.MAX_TOOL_ROUNDS:
        print(f"调试第 {tool_round + 1} 轮：向模型发送请求...")

        response = client.chat.completions.create(
            model = model_name,
            messages = messages,
            tools = TOOL_SCHEMAS,
            tool_choice = 'auto',
            parallel_tool_calls = True,
            timeout=60.0,
        )

        assistant_message = response.choices[0].message

        messages.append(assistant_message.model_dump(exclude_none=True))

        tool_calls = assistant_message.tool_calls

        if not tool_calls:
            final_text = assistant_message.content or ' (模型没有返回任何内容) '
            trajectory['final_answer'] = final_text
            break

        print(f'调试模型要求调用 {len(tool_calls)} 个工具')

        round_trace = {
            'round': tool_round + 1,
            'tool_calls': [
                {
                    'id': tool_call.id,
                    'name': tool_call.function.name
                }
                for tool_call in tool_calls
            ],
            'results': []
        }

        batch_results = execute_tool_batch(tool_calls)

        for item in batch_results:
            messages.append(
                {
                    'role': 'tool',
                    'tool_call_id': item['tool_call_id'],
                    'content': json.dumps(item['result'], ensure_ascii=False),
                }
            )
            round_trace['results'].append(
                {
                    'tool_call_id': item['tool_call_id'],
                    'result': item['result'],
                }
            )
        trajectory['rounds'].append(round_trace)

        tool_round += 1

        if trajectory['final_answer'] is None:
            print(f'调试达到最大轮次 {Config.MAX_TOOL_ROUNDS}，强制生成总结')

            messages.append(
                {
                    'role': 'user',
                    'content': '请根据已有的工具结果，给出最终回答。不要调用工具。',
                }
            )

            final_response = client.chat.completions.create(
                model = model_name,
                messages = messages,
                tools = TOOL_SCHEMAS,
                tool_choice = 'none'
            )

            final_response = final_response.choices[0].message
            trajectory['final_answer'] = final_response.content or '(强制结束模型，模型无回答)'

    return trajectory























































