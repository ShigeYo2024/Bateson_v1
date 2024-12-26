
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": """あなたはグレゴリー・ベイトソンの教育モデルに習熟した教育コーチです。以下のプロセスを基にユーザーと対話してください：
1. 現在の状況を理解する質問をする。
2. 学習モデルに基づき、適切な助言を提供する。
3. 次のステップを提案し、内省を促す。"""}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("AI Coach SHIGERU")
st.write("グレゴリー・ベイトソンの教育モデルに基づいて、ChatGPTによる”メタ認知”を提供するサービスです")

user_input = st.text_input("どんなことを学びたいのか、是非教えてください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

import json

# 保存機能
def save_history():
    with open("chat_history.json", "w") as file:
        json.dump(st.session_state["messages"], file)

# ロード機能
def load_history():
    try:
        with open("chat_history.json", "r") as file:
            st.session_state["messages"] = json.load(file)
    except FileNotFoundError:
        st.session_state["messages"] = [
            {"role": "system", "content": """あなたはグレゴリー・ベイトソンの教育モデルに習熟した教育コーチです。..."""}
        ]

# 起動時に履歴をロード
if "messages" not in st.session_state:
    load_history()

# セッション終了時に保存
if st.button("終了して履歴を保存"):
    save_history()
    st.success("履歴を保存しました。")

# UI追加　感じを変えてランダム性を持たせる
import streamlit as st
import openai
import json

# OpenAI APIキーを設定
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# 初期メッセージの設定
DEFAULT_MESSAGE = {
    "role": "system",
    "content": """あなたはグレゴリー・ベイトソンの教育モデルに習熟した教育コーチです。以下のプロセスを基にユーザーと対話してください：
1. 現在の状況を理解する質問をする。
2. 学習モデルに基づき、適切な助言を提供する。
3. 次のステップを提案し、内省を促す。"""
}

# セッションステートの初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = [DEFAULT_MESSAGE]

# チャット履歴を保存する関数
def save_history():
    with open("chat_history.json", "w") as file:
        json.dump(st.session_state["messages"], file)

# チャット履歴を読み込む関数
def load_history():
    try:
        with open("chat_history.json", "r") as file:
            st.session_state["messages"] = json.load(file)
    except FileNotFoundError:
        st.session_state["messages"] = [DEFAULT_MESSAGE]

# メッセージを送信して応答を受け取る関数
def communicate():
    if not st.session_state["user_input"].strip():
        st.warning("入力が空です。メッセージを入力してください。")
        return

    # ユーザーメッセージを追加
    user_message = {"role": "user", "content": st.session_state["user_input"]}
    st.session_state["messages"].append(user_message)

    # OpenAI APIを使用して応答を取得
    try:
        response = openai.ChatCompletion.create(
            model=st.session_state["selected_model"],
            messages=st.session_state["messages"],
            temperature=st.session_state["temperature"]
        )
        bot_message = response["choices"][0]["message"]
        st.session_state["messages"].append(bot_message)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    # 入力欄をクリア
    st.session_state["user_input"] = ""

# 学習レベルを分析する関数
def analyze_messages():
    levels = {"zero_learning": 0, "first_learning": 0, "second_learning": 0, "third_learning": 0}
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            if "基本知識" in msg["content"]:
                levels["zero_learning"] += 1
            elif "新しい方法" in msg["content"]:
                levels["first_learning"] += 1
            elif "考え方やパターン" in msg["content"]:
                levels["second_learning"] += 1
            elif "世界観" in msg["content"]:
                levels["third_learning"] += 1
    return levels

# UI構築
st.title("AI Coach SHIGERU")
st.write("グレゴリー・ベイトソンの教育モデルに基づいて、ChatGPTによる”メタ認知”を提供するサービスです")

# モデル選択と設定

# ユーザー入力
st.text_input("どんなことを学びたいのか、是非教えてください。", key="user_input", on_change=communicate)

# チャット履歴表示
if st.session_state["messages"]:
    for message in reversed(st.session_state["messages"][1:]):  # 最新のメッセージを上に表示
        speaker = "🙂" if message["role"] == "user" else "🤖"
        st.write(f"{speaker}: {message['content']}")

# 対話のサマリー表示
if st.button("対話のサマリーを見る"):
    analysis = analyze_messages()
    st.write("学習レベルごとのやり取り数:", analysis)

# 履歴保存ボタン
if st.button("終了して履歴を保存"):
    save_history()
    st.success("履歴を保存しました。")

# communicate関数でモデルと温度を使用
response = openai.ChatCompletion.create(
    model=model,
    messages=messages,
    temperature=temperature
)

# プログラムのエラーハンドリング
def communicate():
    messages = st.session_state["messages"]
    
    # 入力が空の場合
    if not st.session_state["user_input"].strip():
        st.warning("入力が空です。メッセージを入力してください。")
        return

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages
        )
        bot_message = response["choices"][0]["message"]
        messages.append(bot_message)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

    st.session_state["user_input"] = ""

# 分析と学習サマリーの提供
def analyze_messages():
    levels = {"zero_learning": 0, "first_learning": 0, "second_learning": 0, "third_learning": 0}
    for msg in st.session_state["messages"]:
        if msg["role"] == "assistant":
            # メッセージ内容に応じて分類 (仮の例)
            if "基本知識" in msg["content"]:
                levels["zero_learning"] += 1
            elif "新しい方法" in msg["content"]:
                levels["first_learning"] += 1
            elif "考え方やパターン" in msg["content"]:
                levels["second_learning"] += 1
            elif "世界観" in msg["content"]:
                levels["third_learning"] += 1
    return levels

if st.button("対話のサマリーを見る"):
    analysis = analyze_messages()
    st.write("学習レベルごとのやり取り数:", analysis)

