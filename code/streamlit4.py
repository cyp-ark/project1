import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from PIL import Image
import os
from langchain_openai import ChatOpenAI
import plotly.graph_objects as go

# 한글 폰트 설정
rc('font', family='Malgun Gothic')  # Windows 사용 시

# OpenAI API Key 설정
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = openai_api_key

# LangChain ChatOpenAI 모델 설정
llm = ChatOpenAI(model="gpt-4")

# Streamlit 페이지 설정
st.set_page_config(page_title="데이터 분석 및 시각화", layout="wide")

# 제목
st.title("데이터 분석 및 시각화")
st.write("재무제표, KDB 합격자 통계, 산업은행 급여 데이터를 시각화하고 분석합니다.")

# 데이터 선택 옵션
option = st.selectbox(
    "분석할 데이터를 선택하세요",
    ("재무제표 시각화", "KDB 한국산업은행 합격자 통계", "산업은행 급여 데이터 분석")
)

if option == "재무제표 시각화":
    st.subheader("재무제표 시각화")
    financial_option = st.selectbox(
        "시각화할 항목을 선택하세요",
        ("재무상태표", "포괄손익계산서", "연결재무상태표", "연결포괄손익계산서")
    )

    # 데이터 입력
    if financial_option == "재무상태표":
        data = {
            "항목": ["현금 및 현금성 자산", "공정가치 측정 금융자산(FVTPL)", "기타포괄손익-공정가치 금융자산(FVOCI)", 
                    "상각후원가 측정 대출채권", "기타 자산"],
            "금액 (백만원)": [8659808, 16085556, 33888064, 19998120, 10177583]
        }
    elif financial_option == "포괄손익계산서":
        data = {
            "항목": ["이자수익", "수수료수익", "배당수익", 
                    "공정가치 측정 금융자산(FVTPL) 순손익", "기타 영업수익"],
            "금액 (백만원)": [1561519, 409836, 76370, 518808, 1386462]
        }
    elif financial_option == "연결재무상태표":
        data = {
            "항목": ["현금 및 현금성 자산", "기타포괄손익-공정가치 금융자산(FVOCI)", 
                    "상각후원가 측정 대출채권", "관계기업 투자", "기타 자산"],
            "금액 (백만원)": [8306382, 23770064, 21838747, 21086136, 11077694]
        }
    else:
        data = {
            "항목": ["이자수익", "배당수익", "공정가치 측정 금융상품(FVTPL) 순손익", 
                    "파생상품 순손익", "기타 영업수익"],
            "금액 (백만원)": [2435618, 316017, 743632, 49455, 2964399]
        }
    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{financial_option} 이미지")
        img_path = f'./image/{financial_option}.jpg'
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, caption=financial_option)

    with col2:
        st.subheader(f"{financial_option} 데이터")
        st.table(df)

        st.subheader(f"{financial_option} 그래프")
        fig, ax = plt.subplots()
        if financial_option in ["재무상태표", "연결재무상태표"]:
            ax.bar(df["항목"], df["금액 (백만원)"], color="skyblue")
            ax.set_xlabel("항목")
            ax.set_ylabel("금액 (백만원)")
            ax.set_title("자산 분포")
            plt.xticks(rotation=45)
        else:
            ax.pie(df["금액 (백만원)"], labels=df["항목"], autopct='%1.1f%%', startangle=90)
            ax.set_title("손익 분포")
        st.pyplot(fig)

elif option == "KDB 한국산업은행 합격자 통계":
    st.subheader("KDB 한국산업은행 합격자 통계 분석")
    data = {
        "년도": ["2023(상)", "2022(상)", "2021(상)", "2020(하)", "2020(상)", "2019(상)"],
        "서류전형 응시인원": [3416, 3357, 2611, 3576, 1802, 2841],
        "서류전형 합격인원": [2317, 1823, 1501, 1006, 627, 1294],
        "서류전형 경쟁률": [1.47, 1.84, 1.74, 3.55, 2.87, 2.20],
        "필기전형 응시율": [58.90, 70.80, 68.00, 82.10, 57.10, 49.60],
        "필기전형 합격률": [26.60, 23.30, 18.00, 19.40, 29.10, 34.30],
        "서류/최종 경쟁률": [29.7, 36.1, 43.52, 71.52, 60.07, 43.71]
    }
    df = pd.DataFrame(data)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("서류전형 응시인원 및 합격인원")
        st.bar_chart(df.set_index("년도")[["서류전형 응시인원", "서류전형 합격인원"]])
    with col2:
        st.subheader("필기전형 응시율 및 합격률")
        st.line_chart(df.set_index("년도")[["필기전형 응시율", "필기전형 합격률"]])
    with col3:
        st.subheader("경쟁률 비교")
        st.line_chart(df.set_index("년도")[["서류전형 경쟁률", "서류/최종 경쟁률"]])

    st.subheader("AI 분석 결과")
    with st.spinner("AI가 데이터를 분석 중입니다..."):
        prompt = f"다음 데이터를 분석하여 주요 패턴과 인사이트를 도출하세요:\n{df.to_string(index=False)}"
        result = llm.predict(prompt)
        st.write(result)

elif option == "산업은행 급여 데이터 분석":
    st.subheader("산업은행 급여 데이터 분석")
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
    df = pd.DataFrame(data)

    basic_salary_data = pd.DataFrame({
        "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
        "기본급": df.set_index("구분").loc["기본급"].values
    })

    performance_data = pd.DataFrame({
        "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
        "성과상여금": df.set_index("구분").loc["성과상여금"].replace("-", 0).astype(float).values
    })

    tenure_data = pd.DataFrame({
        "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
        "평균근속연수": df.set_index("구분").loc["평균근속연수"].values
    })

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("기본급 변화")
        fig1 = go.Figure(data=[
            go.Bar(x=basic_salary_data["년도"], y=basic_salary_data["기본급"], marker_color='skyblue')
        ])
        fig1.update_layout(title="", xaxis_title="년도", yaxis_title="금액 (백만원)")
        st.plotly_chart(fig1, use_container_width=True)
        
        if 'result' not in st.session_state:
            st.session_state.result = None

        if st.button("기본급 AI 분석"):
            with st.spinner("AI가 기본급 데이터를 분석 중입니다..."):
                prompt = "다음 기본급 데이터를 분석하고 주요 패턴을 두 문장으로 요약하세요:\n" + basic_salary_data.to_string(index=False)
                st.session_state.result = llm.predict(prompt)
        if st.session_state.result:
            st.write(st.session_state.result)

    with col2:
        st.subheader("성과상여금 변화")
        fig2 = go.Figure(data=[
            go.Scatter(x=performance_data["년도"], y=performance_data["성과상여금"], mode='lines+markers', line=dict(color='orange'))
        ])
        fig2.update_layout(title="", xaxis_title="년도", yaxis_title="금액 (백만원)")
        st.plotly_chart(fig2, use_container_width=True)
        
        if 'result' not in st.session_state:
            st.session_state.result = None

        if st.button("성과상여금 AI 분석"):
            with st.spinner("AI가 성과상여금 데이터를 분석 중입니다..."):
                prompt = "다음 성과상여금 데이터를 분석하고 주요 패턴을 두 문장으로 요약하세요:\n" + performance_data.to_string(index=False)
                st.session_state.result = llm.predict(prompt)
        if st.session_state.result:
            st.write(st.session_state.result)

    with col3:
        st.subheader("평균근속연수 변화")
        fig3 = go.Figure(data=[
            go.Scatter(x=tenure_data["년도"], y=tenure_data["평균근속연수"], mode='lines+markers', line=dict(color='green'))
        ])
        fig3.update_layout(title="", xaxis_title="년도", yaxis_title="근속연수 (년)")
        st.plotly_chart(fig3, use_container_width=True)

        if st.button("평균근속연수 AI 분석"):
            with st.spinner("AI가 평균근속연수 데이터를 분석 중입니다..."):
                prompt = "다음 평균근속연수 데이터를 분석하고 주요 패턴을 두 문장으로 요약하세요:\n" + tenure_data.to_string(index=False)
                result = llm.predict(prompt)
                st.write(result)
