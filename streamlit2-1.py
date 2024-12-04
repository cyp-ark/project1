import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from langchain.chat_models import ChatOpenAI
import os

# OpenAI API Key 설정
openai_api_key = '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'
os.environ['OPENAI_API_KEY'] = openai_api_key

# LangChain 모델 설정
llm = ChatOpenAI(model="gpt-4")

# 데이터 입력
data = {
    "구분": [
        "기본급", "고정수당", "실적수당", "급여성 복리후생비", 
        "성과상여금", "경영평가 성과금", "기타", 
        "1인당 평균 보수액", "평균근속연수"
    ],
    "2020년 결산": [54954, 11996, 5110, 1227, 38656, "-", 56, 111999, 16.3],
    "2021년 결산": [54481, 12119, 6255, 1312, 39458, "-", 78, 113703, 16.6],
    "2022년 결산": [54761, 12238, 5966, 1374, 38475, "-", 76, 112890, 16.8],
    "2023년 결산": [54924, 12268, 5423, 1415, 38875, "-", 94, 112999, 16.4],
    "2024년 예산": [56297, 12575, 5558, 1451, 29510, "-", 97, 105488, 17.4]
}

# 데이터프레임 생성
df = pd.DataFrame(data)

# 세션 상태 초기화
if "basic_salary_analysis" not in st.session_state:
    st.session_state["basic_salary_analysis"] = None
if "performance_bonus_analysis" not in st.session_state:
    st.session_state["performance_bonus_analysis"] = None
if "tenure_analysis" not in st.session_state:
    st.session_state["tenure_analysis"] = None

# Streamlit 앱 시작
st.title("산업은행 급여 데이터 시각화 및 AI 분석")
st.write("급여 데이터를 바탕으로 주요 변화를 분석하고 시각화합니다.")

# 데이터 준비
basic_salary = df.set_index("구분").loc["기본급"]
basic_salary_data = pd.DataFrame({
    "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
    "기본급": basic_salary.values
})

performance_bonus = df.set_index("구분").loc["성과상여금"].replace("-", 0).astype(float)
performance_data = pd.DataFrame({
    "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
    "성과상여금": performance_bonus.values
})

tenure = df.set_index("구분").loc["평균근속연수"]
tenure_data = pd.DataFrame({
    "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
    "평균근속연수": tenure.values
})

# 한 줄에 세 개의 그래프 배치
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("기본급 변화")
    fig1 = go.Figure(data=[
        go.Bar(x=basic_salary_data["년도"], y=basic_salary_data["기본급"], marker_color='skyblue')
    ])
    fig1.update_layout(title="", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig1, use_container_width=True)

    if st.button("기본급 분석", key="basic_salary"):
        with st.spinner("AI가 기본급 데이터를 분석 중입니다..."):
            prompt = "다음 기본급 데이터를 분석하고, 두 문장으로 요약하세요:\n" + basic_salary_data.to_string(index=False)
            st.session_state["basic_salary_analysis"] = llm.predict(prompt)

    if st.session_state["basic_salary_analysis"]:
        st.write(st.session_state["basic_salary_analysis"])

with col2:
    st.subheader("성과상여금 변화")
    fig2 = go.Figure(data=[
        go.Scatter(x=performance_data["년도"], y=performance_data["성과상여금"], mode='lines+markers', line=dict(color='orange'))
    ])
    fig2.update_layout(title="", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)

    if st.button("성과상여금 분석", key="performance_bonus"):
        with st.spinner("AI가 성과상여금 데이터를 분석 중입니다..."):
            prompt = "다음 성과상여금 데이터를 분석하고, 두 문장으로 요약하세요:\n" + performance_data.to_string(index=False)
            st.session_state["performance_bonus_analysis"] = llm.predict(prompt)

    if st.session_state["performance_bonus_analysis"]:
        st.write(st.session_state["performance_bonus_analysis"])

with col3:
    st.subheader("평균근속연수 변화")
    fig3 = go.Figure(data=[
        go.Scatter(x=tenure_data["년도"], y=tenure_data["평균근속연수"], mode='lines+markers', line=dict(color='green'))
    ])
    fig3.update_layout(title="", xaxis_title="", yaxis_title="")
    st.plotly_chart(fig3, use_container_width=True)

    if st.button("평균근속연수 분석", key="tenure"):
        with st.spinner("AI가 평균근속연수 데이터를 분석 중입니다..."):
            prompt = "다음 평균근속연수 데이터를 분석하고, 두 문장으로 요약하세요:\n" + tenure_data.to_string(index=False)
            st.session_state["tenure_analysis"] = llm.predict(prompt)

    if st.session_state["tenure_analysis"]:
        st.write(st.session_state["tenure_analysis"])
