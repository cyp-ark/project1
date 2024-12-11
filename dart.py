import streamlit as st
from dotenv import load_dotenv
import OpenDartReader
import os
import matplotlib.pyplot as plt
import pandas as pd

# 환경 변수 로드
load_dotenv()

# DART API 초기화
dart_api_key = os.environ["DART_API_KEY"]
dart = OpenDartReader(dart_api_key)

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# Streamlit UI 설정
st.title("기업 손익계산서 조회 및 시각화")

# 사용자 입력
company_name = st.text_input("기업 이름을 입력하세요:", value="삼성전자")
report_year = st.number_input("보고서 연도 입력:", min_value=2000, max_value=2023, value=2023, step=1)

if st.button("조회하기"):
    if company_name and report_year:
        try:
            # 기업 코드 조회
            corp_code = dart.find_corp_code(company_name)

            if corp_code is None:
                st.error(f"기업 이름 '{company_name}'에 해당하는 정보를 찾을 수 없습니다.")
            else:
                st.success(f"'{company_name}'의 회사 코드: {corp_code}")

                # 손익계산서 데이터 조회
                st.info("손익계산서 데이터를 가져오는 중입니다...")
                fs = dart.finstate_all(corp_code, report_year, fs_div='CFS')  # 연결재무제표

                if fs is None or fs.empty:
                    st.warning(f"{report_year}년도의 손익계산서 데이터를 찾을 수 없습니다.")
                else:
                    st.success(f"{company_name}의 {report_year}년도 손익계산서 데이터를 조회했습니다.")
                    st.dataframe(fs)

                    # 컬럼 이름 정리
                    fs.columns = fs.columns.str.strip()

                    # 손익계산서 주요 항목 추출
                    income_statement_items = ['매출액', '영업이익', '당기순이익']
                    available_items = [item for item in income_statement_items if item in fs['account_nm'].values]

                    if available_items:
                        # 시각화 데이터 준비
                        viz_data = fs[fs['account_nm'].isin(available_items)][['account_nm', 'thstrm_amount']]
                        viz_data.set_index('account_nm', inplace=True)
                        viz_data = viz_data.astype(float)

                        # 막대 그래프 시각화
                        st.subheader("손익계산서 주요 항목 시각화")
                        try:
                            fig, ax = plt.subplots()
                            viz_data.plot(kind='bar', ax=ax, legend=False)
                            ax.set_title(f"{company_name} {report_year} 손익계산서 주요 항목")
                            ax.set_ylabel("금액")
                            ax.set_xlabel("항목")
                            st.pyplot(fig)
                        except Exception as viz_error:
                            st.error(f"그래프 생성 중 오류가 발생했습니다: {viz_error}")
                    else:
                        st.warning("손익계산서 시각화를 위한 데이터가 부족합니다. 필수 항목이 누락되었습니다.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("기업 이름과 연도를 모두 입력하세요.")
