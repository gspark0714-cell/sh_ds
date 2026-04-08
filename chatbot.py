import streamlit as st
from groq import Groq

# Groq API 설정
API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("신한DS AI 업무 어시스턴트")
st.caption("업무 관련 질문을 입력하면 AI가 답변해드립니다.")

# 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 표시
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 입력창
user_input = st.chat_input("질문을 입력하세요...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("답변 생성 중..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "당신은 신한DS의 IT 업무 전문 AI 어시스턴트입니다. 친절하고 전문적으로 한국어로 답변해주세요."},
                    {"role": "user", "content": user_input}
                ]
            )
            answer = response.choices[0].message.content
            st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})