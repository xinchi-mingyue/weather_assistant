import sys
from assistant import run_assistant
from history import load_history,append_turn
from config import Config

HELP_MESSAGE = '''
/help       查看帮助
/history    查看历史信息
/clear      清空历史信息
/exit       退出系统
'''

def main():
    print("=" * 60)
    print(" 天气与空气质量助手（多轮对话）")
    print(f"  最大工具调用轮次: {Config.MAX_TOOL_ROUNDS}")
    print(" 提示：输入 '/help' 查看命令，'exit' 退出程序")
    history = load_history()
    if history:
        print(f"📚 已加载 {len(history) // 2} 轮历史对话")
    print("=" * 60)

    while True:
        try:
            user_input = input("\n你: ").strip()

            if not user_input:
                continue

            if user_input == '/help':
                print(HELP_MESSAGE)
                continue

            if user_input == '/history':
                if not history:
                    print('暂无历史记录')
                else:
                    for i, msg in enumerate(history):
                        role = '你' if msg['role'] == 'user' else '助手'
                        print(f'[{i+1}]{role}: {msg["content"]}')
                continue

            if user_input == '/clear':
                confirm = input('请输入 yes 以确认清空: ').strip().lower()
                if confirm == 'yes':
                    from history import save_history
                    save_history({})
                    history = []
                    print('✅ 历史记录已清空')
                continue

            if user_input.lower() in ["exit", "quit"]:
                print('再见')
                break

            print('思考中...（可能调用工具获取数据）')
            result = run_assistant(user_input, history=history)

            final_answer = result.get("final_answer","（模型没有返回任何内容）" )
            print(f"助手: {final_answer}")

            rounds = result.get("rounds",[])
            if rounds:
                print(f'调试共进行了 {len(rounds)} 轮工具调用')
                for round in rounds:
                    tool_names = [tc["name"] for tc in round["tool_calls"]]
                    print(f"      第 {round['round']} 轮: 调用了 {', '.join(tool_names)}")
            else:
                print("调试未调用任何工具，直接回答了问题")

            if final_answer and len(final_answer) > 3:
                history = append_turn(history, user_input, final_answer)

        except KeyboardInterrupt:
            print("检测到中断信号，退出程序。")
            break
        except Exception as e:
            # 捕获所有其他未预料的异常（如网络突然断开、JSON解析错误等）
            print(f"发生未预料的错误: {e}")
            print("程序将继续运行，请重新输入你的问题。")


if __name__ == "__main__":
    main()



































