# 🌤️ 城市天气与空气质量助手（函数式版）

一个基于 **OpenAI Tool Calling** 的多城市天气与空气质量查询助手。使用 **函数式编程风格**，模块间通过函数调用协作，代码更直观、更易上手。

## ✨ 核心功能

- 🌍 **自然语言交互**：用户说话，AI 理解并调用工具
- 📍 **多城市并发**：一句话查询多个城市，自动并发执行
- 🎯 **歧义处理**：城市名有多个候选时，询问用户确认
- ⚡ **受控并发**：线程池 + 批次超时，效率与稳定兼得
- 💾 **多轮记忆**：支持“那上海呢？”的追问
- 🛡️ **Pydantic 严格校验**：参数类型、范围、额外字段全拦截
- 🔄 **自动重试**：OpenAI 客户端内置重试，网络抖动不怕

## 🏗️ 项目架构

```text
weather_assistant/
├── config.py             # 配置与客户端工厂
├── http_client.py        # HTTP 安全通道
├── tools.py              # 三个业务函数
├── schemas.py            # Pydantic 参数模型
├── registry.py           # 工具注册表
├── executor.py           # 并发执行器
├── assistant.py          # Tool Calling 循环
├── history.py            # 历史存储
├── app.py                # 命令行入口
└── data/
    └── history.json
