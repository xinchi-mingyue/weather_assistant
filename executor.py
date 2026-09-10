from concurrent.futures import ThreadPoolExecutor, wait
from config import Config
from registry import execute_tool_call
from typing import List, Any

def execute_tool_batch(tool_calls):
    if not tool_calls:
        return []
    city_search_calls = [
        tool_call
        for tool_call in tool_calls
        if tool_call.function.name == 'search_city'
    ]
    if len(city_search_calls) > Config.MAX_CITIES_PER_REQUEST:
        return [
            {
                'tool_call_id': tool_call.id,
                'result': {
                    'ok': False,
                    'error': 'too_many_cities'
                },
            }
            for tool_call in tool_calls
        ]

    accepted_calls = tool_calls[:Config.MAX_TOOL_CALLS_PER_ROUND]
    rejected_calls = tool_calls[Config.MAX_TOOL_CALLS_PER_ROUND:]

    results_by_id = {}

    if accepted_calls:
        max_workers = min(Config.MAX_CONCURRENT_REQUESTS, len(accepted_calls))

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_call = {
                executor.submit(execute_tool_call, tool_call): tool_call
                for tool_call in accepted_calls
            }

            done, not_done = wait(
                future_to_call,
                timeout = Config.TOOL_BATCH_TIMEOUT
            )

            for future in done:
                tool_call = future_to_call[future]
                try:
                    result = future.result()
                except Exception:
                    result = {'ok': False, 'error': 'tool_failed'}
                results_by_id[tool_call.id] = result

            for future in not_done:
                tool_call = future_to_call[future]
                future.cancel()
                results_by_id[tool_call.id] = {
                    'ok': False,
                    'error': 'batch_wait_timeout'
                }

        for tool_call in rejected_calls:
            results_by_id[tool_call.id] = {
                'ok': False,
                'error': 'tool_many_tool_calls'
            }

    return [
        {
            'tool_call_id': tool_call.id,
            'result': results_by_id[tool_call.id],
        }
        for tool_call in tool_calls
    ]













































