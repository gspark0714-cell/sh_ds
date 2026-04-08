import streamlit as st
from groq import Groq

API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("업무 이메일 작성기")
st.caption("상황을 설명하면 AI가 업무 이메일 초안을 작성해드립니다.")

col1, col2 = st.columns(2)
with col1:
    email_type = st.selectbox("이메일 유형", [
        "업무 요청",
        "일정 조율",
        "결과 보고",
        "사과/양해 요청",
        "감사 인사",
        "회의 소집",
    ])
with col2:
    tone = st.selectbox("말투", ["격식체 (공식적)", "일반 (보통)", "친근체 (편안한)"])

receiver = st.text_input("받는 사람", placeholder="예: 김철수 팀장님")
situation = st.text_area("상황 설명", height=150,
    placeholder="예: 모바일뱅킹 프로젝트 일정이 2주 지연될 것 같아서 팀장님께 보고하는 이메일")

if st.button("이메일 작성"):
    if situation and receiver:
        with st.spinner("AI가 이메일을 작성 중입니다..."):
            tone_map = {
                "격식체 (공식적)": "매우 격식 있고 공식적인",
                "일반 (보통)": "적당히 격식 있는",
                "친근체 (편안한)": "친근하고 편안한",
            }
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"당신은 전문 비서입니다. {tone_map[tone]} 말투로 한국어 업무 이메일을 작성해주세요. 제목과 본문을 모두 작성해주세요."},
                    {"role": "user", "content": f"받는 사람: {receiver}\n이메일 유형: {email_type}\n상황: {situation}\n\n위 내용으로 업무 이메일을 작성해줘."}
                ]
            )
            result = response.choices[0].message.content

            st.header("작성된 이메일")
            st.write(result)
            st.text_area("복사용", value=result, height=250)
    else:
        st.warning("받는 사람과 상황을 입력해주세요.")