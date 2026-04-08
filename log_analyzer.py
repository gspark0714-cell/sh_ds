import streamlit as st
from groq import Groq

API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("장애 로그 분석기")
st.caption("서버 로그를 붙여넣으면 AI가 원인을 분석하고 대응 방법을 알려드립니다.")

col1, col2 = st.columns(2)
with col1:
    system_type = st.selectbox("시스템 유형", [
        "웹 서버 (Nginx/Apache)",
        "애플리케이션 서버",
        "데이터베이스 (MySQL/Oracle)",
        "Java/Spring",
        "Python",
        "기타",
    ])
with col2:
    analysis_type = st.selectbox("분석 유형", [
        "원인 분석 + 해결 방법",
        "오류 요약만",
        "긴급도 평가",
        "재발 방지 방안",
    ])

log_text = st.text_area("로그 입력", height=250,
    placeholder="분석할 로그를 여기에 붙여넣으세요...")

if st.button("로그 분석"):
    if log_text:
        with st.spinner("AI가 로그를 분석 중입니다..."):
            analysis_map = {
                "원인 분석 + 해결 방법": "로그에서 오류 원인을 분석하고 해결 방법을 단계별로 알려줘.",
                "오류 요약만": "로그에서 발생한 오류들을 간단히 요약해줘.",
                "긴급도 평가": "로그를 보고 장애 긴급도를 평가해줘. (긴급/주의/정보) 그리고 즉시 조치가 필요한 항목을 알려줘.",
                "재발 방지 방안": "이런 오류가 재발하지 않도록 방지 방안을 알려줘.",
            }
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"당신은 {system_type} 전문 시스템 엔지니어입니다. 로그를 분석하고 한국어로 명확하게 설명해주세요. 기술적인 내용은 쉽게 풀어서 설명해주세요."},
                    {"role": "user", "content": f"{analysis_map[analysis_type]}\n\n로그:\n{log_text}"}
                ]
            )
            result = response.choices[0].message.content

            st.header("분석 결과")
            st.write(result)

            # 장애 보고서 생성
            if analysis_type == "원인 분석 + 해결 방법":
                st.header("장애 보고서 초안")
                report_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "당신은 IT 운영팀 전문가입니다. 장애 보고서를 한국어로 작성해주세요."},
                        {"role": "user", "content": f"아래 로그 분석 결과를 바탕으로 장애 보고서를 작성해줘.\n분석결과: {result}"}
                    ]
                )
                st.text_area("보고서 복사용",
                    value=report_response.choices[0].message.content,
                    height=200)
    else:
        st.warning("로그를 입력해주세요.")