import json
from typing import Any, Dict
from pydantic import ValidationError


from schemas import CitySearchArgs, CoordinatesArgs

from tools import search_city, get_current_weather, get_current_air_quality

TOOL_REGISTRY:Dict[str,Dict[str, Any]] = {
    'search_city': {
        'args_model': CitySearchArgs,
        'handler': search_city,
    },
    'get_current_weather': {
        'args_model': CoordinatesArgs,
        'handler': get_current_weather,
    },
    'get_current_air_quality': {
        'args_model': CoordinatesArgs,
        'handler': get_current_air_quality,
    },
}

def execute_tool_call(tool_call: Any):
    tool_name = tool_call.function.name
    if tool_name not in TOOL_REGISTRY:
        return {'ok': False, 'error': 'tool not found'}

    entry = TOOL_REGISTRY[tool_name]
    args_model = entry['args_model']
    handler = entry['handler']

    try:
        raw_agrs = json.loads(tool_call.function.arguments)
    except json.JSONDecodeError:
        return {'ok': False, 'error': 'invalid_args_json'}

    try:
        validated_agrs = args_model(**raw_agrs)
    except ValidationError as e:
        error_messages = ';'.join([err['msg'] for err in e.errors()])
        return {'ok': False, 'error': f'validation error: {error_messages}'}

    try:
        result = handler(**validated_agrs.model_dump())
    except Exception as e:
        return {'ok': False, 'error': f'tool_execution_failed: {str(e)}'}

    return result

















































