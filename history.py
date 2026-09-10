import os
import json

from config import Config

def load_history():
    """
    从硬盘 JSON 文件中加载历史对话记录。

    返回：
        历史消息列表（列表中的每一项是 {"role": "user", "content": "..."}
        或 {"role": "assistant", "content": "..."}）。
        如果文件不存在或损坏，返回空列表。
    """

    if not os.path.exists(Config.history_path):
        return []

    try:
        with open(Config.history_path, "r", encoding="utf-8") as f:
            history = json.load(f)

        if not isinstance(history, list):
            return []
        return history
    except(json.JSONDecodeError, IOError):
        return []


def save_history(history):
    """
        将历史记录保存到硬盘 JSON 文件。
        会自动创建目标文件夹（如果不存在）。
    """
    os.makedirs(os.path.dirname(Config.history_path), exist_ok=True)

    with open(Config.history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def trim_history(history):
    """
        截断历史记录，只保留最近 MAX_HISTORY_TURNS 轮对话。

        每轮对话包含 2 条消息（一条 user，一条 assistant），
        所以最大消息数为 MAX_HISTORY_TURNS * 2。
    """
    max_messages = Config.MAX_HISTORY_TURNS * 2
    if len(history) > max_messages:
        return history[-max_messages:]
    return history


def append_turn(history, user_msg, assistant_reply):
    """
        向历史记录中追加一轮完整的对话（用户问题 + 助手回答）。
        该函数会自动调用 trim_history 进行截断处理。

        参数：
            history: 当前的历史记录列表
            user_msg: 用户本轮输入的问题
            assistant_reply: 助手本轮返回的最终回答

        返回：
            更新并截断后的新历史记录列表
    """

    history.append(
        {
            'role': 'user',
            'content': user_msg,
        }
    )
    history.append(
        {
            'role': 'assistant',
            'content': assistant_reply,
        }
    )

    trimmed_history = trim_history(history)

    save_history(trimmed_history)

    return trimmed_history






































