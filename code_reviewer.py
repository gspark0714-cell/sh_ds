import streamlit as st
from groq import Groq

API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("AI 코드 리뷰어")
st.caption("코드를 붙여넣으면 AI가 문제점과 개선사항을 알려드립니다.")

col1, col2 = st.columns(2)
with col1:
    language = st.selectbox("프로그래밍 언어", [
        "Python", "Java", "JavaScript", "SQL", "기타"
    ])
with col2:
    review_type = st.selectbox("리뷰 유형", [
        "전체 리뷰",
        "버그 찾기",
        "성능 개선",
        "보안 취약점",
        "코드 설명",
    ])

code = st.text_area("코드 입력", height=250,
    placeholder="리뷰받을 코드를 여기에 붙여넣으세요...")

if st.button("리뷰 시작"):
    if code:
        with st.spinner("AI가 코드를 분석 중입니다..."):
            review_map = {
                "전체 리뷰": "코드 품질, 버그, 성능, 가독성 전반을 리뷰해줘.",
                "버그 찾기": "코드에서 버그나 오류가 발생할 수 있는 부분을 찾아줘.",
                "성능 개선": "코드의 성능을 개선할 수 있는 부분을 알려줘.",
                "보안 취약점": "코드에서 보안 취약점이 있는 부분을 찾아줘.",
                "코드 설명": "코드가 어떻게 동작하는지 비전공자도 이해할 수 있게 설명해줘.",
            }
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"당신은 {language} 전문 시니어 개발자입니다. 코드를 분석하고 한국어로 명확하게 피드백해주세요. 문제점은 구체적으로, 개선 코드도 함께 제시해주세요."},
                    {"role": "user", "content": f"{review_map[review_type]}\n\n```{language.lower()}\n{code}\n```"}
                ]
            )
            result = response.choices[0].message.content

            st.header("리뷰 결과")
            st.write(result)
    else:
        st.warning("코드를 입력해주세요.")