import streamlit as st
import pandas as pd
from datetime import date

st.title("신한DS IT 프로젝트 관리")
st.caption("프로젝트 현황을 등록하고 조회합니다.")

# 데이터 저장
if "projects" not in st.session_state:
    st.session_state.projects = []

# ── 입력 폼 ──────────────────────────
st.header("프로젝트 등록")

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("프로젝트명")
    manager = st.text_input("담당자")
with col2:
    status = st.selectbox("상태", ["진행중", "완료", "지연", "대기"])
    deadline = st.date_input("마감일", value=date.today())

if st.button("등록"):
    if name and manager:
        st.session_state.projects.append({
            "프로젝트명": name,
            "담당자": manager,
            "상태": status,
            "마감일": str(deadline)
        })
        st.success(f"'{name}' 프로젝트가 등록됐습니다!")
    else:
        st.warning("프로젝트명과 담당자를 입력해주세요.")

# ── 목록 조회 ──────────────────────────
st.header("프로젝트 목록")

if st.session_state.projects:
    df = pd.DataFrame(st.session_state.projects)

    # 상태별 색상 표시
    status_filter = st.selectbox("상태 필터", ["전체", "진행중", "완료", "지연", "대기"])
    if status_filter != "전체":
        df = df[df["상태"] == status_filter]

    st.dataframe(df, use_container_width=True)

    # 상태별 현황 차트
    st.header("상태별 현황")
    status_counts = pd.DataFrame(st.session_state.projects)["상태"].value_counts()
    st.bar_chart(status_counts)

else:
    st.info("등록된 프로젝트가 없습니다.")