import streamlit as st
from groq import Groq

API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("회의록 요약기")
st.caption("회의록을 붙여넣으면 AI가 핵심 내용을 요약해드립니다.")

meeting_text = st.text_area("회의록 입력", height=250,
    placeholder="회의록 내용을 여기에 붙여넣으세요...")

col1, col2 = st.columns(2)
with col1:
    summary_type = st.selectbox("요약 유형", [
        "전체 요약",
        "핵심 결정사항만",
        "액션아이템만",
        "전체 요약 + 액션아이템"
    ])
with col2:
    language = st.selectbox("출력 언어", ["한국어", "영어"])

if st.button("요약하기"):
    if meeting_text:
        with st.spinner("AI가 요약 중입니다..."):
            prompt_map = {
                "전체 요약": "회의 내용을 간결하게 요약해줘. 주요 논의사항, 결정사항을 포함해줘.",
                "핵심 결정사항만": "회의에서 결정된 사항만 번호 목록으로 정리해줘.",
                "액션아이템만": "회의에서 나온 액션아이템을 담당자와 함께 번호 목록으로 정리해줘. 담당자가 없으면 미정으로 표시해줘.",
                "전체 요약 + 액션아이템": "1) 회의 전체 요약 2) 결정사항 3) 액션아이템(담당자 포함) 순서로 정리해줘.",
            }
            lang = "한국어" if language == "한국어" else "English"
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"당신은 전문 비서입니다. 회의록을 분석해서 {lang}로 명확하게 정리해주세요."},
                    {"role": "user", "content": f"{prompt_map[summary_type]}\n\n회의록:\n{meeting_text}"}
                ]
            )
            result = response.choices[0].message.content

            st.header("요약 결과")
            st.write(result)

            # 복사 버튼
            st.text_area("결과 복사용", value=result, height=200)
    else:
        st.warning("회의록을 입력해주세요.")