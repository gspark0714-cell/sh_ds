import streamlit as st
import requests

st.title("학생 관리 시스템")

# 학생 추가
st.header("학생 정보 입력")
name = st.text_input("이름")
age = st.number_input("나이", min_value=1, max_value=100)
score = st.number_input("점수", min_value=0, max_value=100)

if st.button("추가"):
    response = requests.post("http://localhost:8000/students",
                            json={"name": name, "age": int(age), "score": float(score)})
    result = response.json()
    st.success(result["message"])

# 학생 목록 조회
st.header("학생 목록")
if st.button("목록 새로고침"):
    response = requests.get("http://localhost:8000/students")
    students = response.json()
    if students:
        st.table(students)
    else:
        st.info("등록된 학생이 없습니다.")