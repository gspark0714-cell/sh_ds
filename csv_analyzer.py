import streamlit as st
import pandas as pd
from groq import Groq

# Groq API 설정
API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("AI CSV 분석기")
st.caption("CSV 파일을 업로드하면 AI가 분석해드립니다.")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.header("데이터 미리보기")
    st.dataframe(df.head(10), use_container_width=True)

    st.header("기본 통계")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 행 수", f"{len(df):,}개")
    with col2:
        st.metric("컬럼 수", f"{len(df.columns)}개")
    with col3:
        st.metric("결측값", f"{df.isnull().sum().sum()}개")

    # 컬럼 목록 표시
    st.write("**컬럼 목록:**", ", ".join(df.columns.tolist()))

    st.header("AI 분석 요청")
    question = st.text_input(
        "데이터에 대해 궁금한 것을 물어보세요",
        placeholder="예: 이 데이터의 주요 특징을 분석해줘"
    )

    if st.button("AI 분석 시작"):
        if question:
            with st.spinner("AI가 분석 중입니다..."):
                # 데이터 요약 정보 생성
                data_summary = f"""
데이터 정보:
- 행 수: {len(df)}
- 컬럼: {', '.join(df.columns.tolist())}
- 상위 5개 행:
{df.head().to_string()}
- 기본 통계:
{df.describe().to_string()}
"""
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "당신은 데이터 분석 전문가입니다. 주어진 데이터를 분석하고 한국어로 친절하게 설명해주세요."},
                        {"role": "user", "content": f"다음 데이터를 분석해주세요.\n{data_summary}\n\n질문: {question}"}
                    ]
                )
                answer = response.choices[0].message.content

                st.header("AI 분석 결과")
                st.write(answer)
        else:
            st.warning("질문을 입력해주세요.")
else:
    st.info("CSV 파일을 업로드해주세요.")