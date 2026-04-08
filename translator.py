import streamlit as st
from groq import Groq

# Groq API 설정
API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("AI 번역기")
st.caption("한국어를 입력하면 영어로 번역해드립니다.")

# 번역 기록 저장
if "translations" not in st.session_state:
    st.session_state.translations = []

# 입력
st.header("번역할 내용 입력")
korean_text = st.text_area("한국어 입력", height=150, placeholder="번역할 한국어 문장을 입력하세요...")

if st.button("번역하기"):
    if korean_text:
        with st.spinner("번역 중..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "당신은 전문 번역가입니다. 한국어를 자연스러운 영어로 번역해주세요. 번역 결과만 출력하고 다른 설명은 하지 마세요."},
                    {"role": "user", "content": f"다음 한국어를 영어로 번역해주세요:\n{korean_text}"}
                ]
            )
            english_text = response.choices[0].message.content

            # 결과 표시
            st.header("번역 결과")
            st.success(english_text)

            # 번역 기록 저장
            st.session_state.translations.append({
                "한국어": korean_text,
                "영어": english_text
            })
    else:
        st.warning("번역할 내용을 입력해주세요.")

# 번역 기록
if st.session_state.translations:
    st.header("번역 기록")
    for i, t in enumerate(reversed(st.session_state.translations)):
        with st.expander(f"번역 {len(st.session_state.translations) - i}"):
            st.write("**한국어:**", t["한국어"])
            st.write("**영어:**", t["영어"])