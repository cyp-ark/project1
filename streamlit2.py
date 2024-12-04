import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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

# Streamlit 앱 시작
st.title("산업은행 급여 데이터 시각화")
st.write("주어진 급여 데이터를 바탕으로 분석 결과를 시각화합니다.")

# 데이터프레임 표시
st.dataframe(df)

# 레이아웃 설정: 세 개의 그래프를 한 줄로 배치
col1, col2, col3 = st.columns(3)

# 기본급 변화 (히스토그램 스타일, Plotly로 확대)
with col1:
    st.subheader("기본급 변화 (확대)")
    basic_salary = df.set_index("구분").loc["기본급"]
    basic_salary_data = pd.DataFrame({
        "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
        "기본급": basic_salary.values
    })
    fig = go.Figure(data=[
        go.Bar(x=basic_salary_data["년도"], y=basic_salary_data["기본급"], marker_color='skyblue')
    ])
    fig.update_layout(
        yaxis=dict(range=[50000, 60000]),  # y축 범위 설정
        title="기본급 변화",
        xaxis_title="년도",
        yaxis_title="금액 (천 원)",
    )
    st.plotly_chart(fig)

# 성과상여금 변화 (선형 차트, Plotly로 확대)
with col2:
    st.subheader("성과상여금 변화 (확대)")
    performance_bonus = df.set_index("구분").loc["성과상여금"].replace("-", 0).astype(float)
    performance_data = pd.DataFrame({
        "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
        "성과상여금": performance_bonus.values
    })
    fig = go.Figure(data=[
        go.Scatter(x=performance_data["년도"], y=performance_data["성과상여금"], mode='lines+markers', line=dict(color='orange'))
    ])
    fig.update_layout(
        yaxis=dict(range=[25000, 40000]),  # y축 범위 설정
        title="성과상여금 변화",
        xaxis_title="년도",
        yaxis_title="금액 (천 원)",
    )
    st.plotly_chart(fig)

# 평균근속연수 변화 (선형 차트, Plotly로 확대)
with col3:
    st.subheader("평균근속연수 변화 (확대)")
    tenure = df.set_index("구분").loc["평균근속연수"]
    tenure_data = pd.DataFrame({
        "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
        "평균근속연수": tenure.values
    })
    fig = go.Figure(data=[
        go.Scatter(x=tenure_data["년도"], y=tenure_data["평균근속연수"], mode='lines+markers', line=dict(color='green'))
    ])
    fig.update_layout(
        yaxis=dict(range=[16, 18]),  # y축 범위 설정
        title="평균근속연수 변화",
        xaxis_title="년도",
        yaxis_title="근속연수 (년)",
    )
    st.plotly_chart(fig)
