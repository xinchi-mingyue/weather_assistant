from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional

class CitySearchArgs(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    city_name:str = Field(min_length=2, max_length=60)

    @field_validator('city_name')
    @classmethod
    def strip_city_name(cls, value):
        cleaned = value.strip()
        if len(cleaned) < 2:
            raise ValueError('城市名称不能为空且至少包含 2 个字符')
        return cleaned

class CoordinatesArgs(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    timezone: str = Field(min_length=1, max_length=60)


def build_tool_schema(name, description, args_model):
    return {
        'type': 'function',
        'function': {
            'name': name,
            'description': description,
            'parameters': args_model.model_json_schema(),
            'strict': True,
        }
    }

TOOL_SCHEMAS =[
    build_tool_schema(
        'search_city',
        (
            "根据城市名称查询候选地点、经纬度和时区。"
            "用户只提供城市名称时先调用此工具；"
            "如果用户同时提到多个城市（例如'比较北京和上海'），"
            "请在同一轮中多次调用本工具，分别查询每个城市的坐标。"
            "如果返回多个候选（unique=false），请列出候选让用户确认。"
        ),
        CitySearchArgs,
    ),
    build_tool_schema(
        'get_current_weather',

         "根据已确认的经纬度和时区查询当前天气。"
            "如果用户想对比多个城市，可以对每个城市同时调用本工具。",
        CoordinatesArgs,
    ),
    build_tool_schema(
        'get_current_air_quality',
         "根据已确认的经纬度和时区查询当前空气质量（US AQI 标准）。"
            "如果用户想对比多个城市，可以对每个城市同时调用本工具。",
        CoordinatesArgs,
    ),
]












