import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
import OpenDartReader
from langchain.chat_models import ChatOpenAI

# 한글 폰트 설정
rc('font', family='Malgun Gothic')  # Windows 사용 시

# OpenDART API 및 OpenAI API 설정
dart_api_key = 'a1d84099f486d7c1158e8471e54d1c63695397e2'
openai_api_key = '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'

dart = OpenDartReader(dart_api_key)
llm = ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key)

# Streamlit 페이지 설정
st.set_page_config(page_title="재무제표 시각화 및 분석", layout="wide")

# 제목
st.title("재무제표 시각화 및 AI 분석")
st.write("금융감독원 API를 활용하여 여러 기업의 재무제표를 시각화하고 분석합니다.")

# 회사명 입력
company_name = st.sidebar.text_input("회사명을 입력하세요 (예: 삼성전자)", value="삼성전자")

# 데이터 선택 옵션
option = st.sidebar.selectbox(
    "시각화할 항목을 선택하세요",
    ("재무상태표", "포괄손익계산서")
)

# 보고 연도 선택
report_year = st.sidebar.number_input("보고 연도를 입력하세요 (예: 2023)", min_value=2010, max_value=2023, value=2023)

# 회사 코드 가져오기
try:
    corp_code = dart.find_corp_code(company_name)
    st.sidebar.write(f"**{company_name}의 종목 코드**: {corp_code}")

    # 재무제표 데이터 가져오기
    if option == "재무상태표":
        fs = dart.finstate(corp_code, report_year)
        data = fs[fs['account_nm'].isin(['자산', '부채', '자본'])][['account_nm', 'thstrm_amount']]
        data.columns = ['항목', '금액 (백만원)']

    elif option == "포괄손익계산서":
        fs = dart.finstate_all(corp_code, report_year)
        data = fs[fs['sj_nm'] == '포괄손익계산서'][['account_nm', 'thstrm_amount']]
        data.columns = ['항목', '금액 (백만원)']

    # 데이터프레임 생성
    df = pd.DataFrame(data)
    df['금액 (백만원)'] = pd.to_numeric(df['금액 (백만원)'], errors='coerce')

    # 2단 레이아웃
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{option} 데이터")
        st.table(df)

        # AI 분석 버튼
        if st.button("AI 분석 실행"):
            with st.spinner("AI가 데이터를 분석 중입니다..."):
                # 데이터를 텍스트로 변환하여 AI 모델에 전달
                prompt = f"""
                아래는 {company_name}의 {report_year}년도 {option} 데이터입니다. 주요 패턴과 인사이트를 분석하세요:
                {df.to_string(index=False)}
                """
                result = llm.predict(prompt)
                st.write("### AI 분석 결과")
                st.write(result)

    with col2:
        st.subheader(f"{option} 그래프")
        fig, ax = plt.subplots()

        if option == "재무상태표":
            # 막대 그래프
            ax.bar(df["항목"], df["금액 (백만원)"], color="skyblue")
            ax.set_xlabel("항목")
            ax.set_ylabel("금액 (백만원)")
            ax.set_title(f"{company_name} - 자산 분포 ({report_year})")
            plt.xticks(rotation=45)

        elif option == "포괄손익계산서":
            # 원형 그래프
            ax.pie(df["금액 (백만원)"], labels=df["항목"], autopct='%1.1f%%', startangle=90)
            ax.set_title(f"{company_name} - 손익 분포 ({report_year})")

        st.pyplot(fig)

except Exception as e:
    st.error(f"오류 발생: {e}")
    st.write("회사명을 정확히 입력했는지 확인하거나 해당 연도의 데이터를 확인하세요.")
