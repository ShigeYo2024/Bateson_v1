
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
st.write("グレゴリー・ベイトソンの教育モデルに基づいて、ChatGPTによるコーチングを提供するサービスです")

user_input = st.text_input("どんな人生を過ごしたいのか、是非教えてください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
