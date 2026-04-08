import streamlit as st
from groq import Groq

API_KEY = ""
client = Groq(api_key=API_KEY)

st.title("SQL 쿼리 생성기")
st.caption("원하는 데이터를 말로 설명하면 AI가 SQL을 작성해드립니다.")

col1, col2 = st.columns(2)
with col1:
    db_type = st.selectbox("데이터베이스", [
        "MySQL", "Oracle", "PostgreSQL", "MS SQL Server", "SQLite"
    ])
with col2:
    query_type = st.selectbox("쿼리 유형", [
        "SELECT (조회)",
        "INSERT (입력)",
        "UPDATE (수정)",
        "DELETE (삭제)",
        "CREATE TABLE (테이블 생성)",
    ])

table_info = st.text_area("테이블 구조 입력", height=120,
    placeholder="""예:
customers 테이블: id, name, email, phone, created_at
orders 테이블: id, customer_id, product, amount, order_date, status""")

request = st.text_area("원하는 데이터 설명", height=100,
    placeholder="예: 이번 달에 주문한 고객 중 주문금액이 100만원 이상인 고객의 이름과 이메일을 조회해줘")

if st.button("SQL 생성"):
    if request:
        with st.spinner("AI가 SQL을 생성 중입니다..."):
            table_context = f"테이블 구조:\n{table_info}\n\n" if table_info else ""
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": f"당신은 {db_type} 전문 DBA입니다. 요청에 맞는 SQL 쿼리를 작성해주세요. SQL 코드와 함께 각 부분에 대한 한국어 설명도 제공해주세요."},
                    {"role": "user", "content": f"{table_context}쿼리 유형: {query_type}\n요청: {request}"}
                ]
            )
            result = response.choices[0].message.content

            st.header("생성된 SQL")
            st.write(result)
            st.text_area("SQL 복사용", value=result, height=200)
    else:
        st.warning("원하는 데이터를 설명해주세요.")