"""第1回: 素のLLMに1回だけ質問するスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

ツールも会話履歴も持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, chat=None) -> str:
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        response = client.models.generate_content(model=MODEL, contents=question)
    else:
        response = chat.send_message(question)

    # 第1回 演習：トークン使用量の表示
    usage = response.usage_metadata

    if usage is not None:
        print("\n========== トークン使用量 ==========")
        print(f"入力トークン数：{usage.prompt_token_count}")
        print(f"出力トークン数：{usage.candidates_token_count}")

        # 思考トークン数（対応モデルの場合）
        if usage.thoughts_token_count is not None:
            print(f"思考トークン数：{usage.thoughts_token_count}")

        print(f"合計トークン数：{usage.total_token_count}")
        print("====================================\n")
        
    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="LLMと会話する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    # 会話セッションを作成（履歴は自動保持）
    client = genai.Client(api_key=get_api_key())
    chat = client.chats.create(model=MODEL)

    print(f"[model] {MODEL}")
    print(f"[質問] {args.question}\n")

    try:
        question = args.question

        while True:
            if question:
                print(ask(question, chat))

            # 次の質問を受け付ける
            question = input("\n[次の質問]（exitで終了）> ").strip()

            if question.lower() in {"exit", "quit", "終了"}:
                break

    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)

    except (KeyboardInterrupt, EOFError):
        print("\n会話を終了しました。")


if __name__ == "__main__":
    main()
