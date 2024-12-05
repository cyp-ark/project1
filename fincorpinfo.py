import os
import pandas as pd
import streamlit as st
from KDB import KDBAnalysisApp

# 현재 디렉토리와 CSV 파일 경로 설정
base_dir = os.getcwd()
csv_file_path = os.path.join(base_dir, "corpinfo.csv")

# CSV 데이터 읽기 함수
def load_data_from_csv(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8-sig')
        return data[["기업명", "산업", "설립일", "자본금", "매출액", "대표자", "주력 사업", "최근 동향", "주소", "이미지 경로"]]
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 특정 기업 정보 표시 함수
def display_company_info(company_info):
    st.markdown(
        f"""
        <div>
            <h3>🏢 {company_info['기업명']}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div>
                <p><strong>산업:</strong> {company_info['산업']}</p>
                <p><strong>주소:</strong> {company_info['주소']}</p>
                <p><strong>설립일:</strong> {company_info['설립일']}</p>
                <p><strong>자본금:</strong> {company_info['자본금']}</p>
                <p><strong>매출액:</strong> {company_info['매출액']}</p>
                <p><strong>대표자:</strong> {company_info['대표자']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        if pd.notna(company_info['이미지 경로']):
            st.image(company_info['이미지 경로'], use_column_width=True)

    st.markdown(
        f"""
        <div>
            <p><strong>주력 사업:</strong> {company_info['주력 사업']}</p>
            <p><strong>최근 동향:</strong> {company_info['최근 동향']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.subheader(f"{company_info['기업명']} 최신 헤드라인")
    st.markdown(
                    f'''
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                        <p> 1. "글로벌 주요 증시, 미국 소비자물가 30년 만에 최고치 상승"</p>
                        <p> 2. "미국 신규 실업수당 신청, 예상치 상회"</p>
                        <p> 3. "중국 경제성장률, 전 분기 대비 하락세"</p>
                        <p> 4. "유럽 연합, 코로나19로 인한 경제 위기 극복을 위한 경제 지원안 추진"</p>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
    st.subheader(f"{company_info['기업명']} 키워드 분석")
    
    st.subheader(f"{company_info['기업명']} 합격자 통계")
    
    
    # 합격자, 급여 데이터 분석 앱 실행
    app = KDBAnalysisApp()
    app.run()

# 기업 정보 표시 섹션
def show_company_info():
    st.subheader("🏢 금융 공기업 정보")

    # CSV 데이터 로드
    data = load_data_from_csv(csv_file_path)

    if not data.empty:
        selected_company = None
        columns = st.columns(6)
        for index, company_name in enumerate(data["기업명"]):
            col = columns[index % 6]
            if col.button(company_name):
                selected_company = company_name

        # 선택된 기업 정보 표시
        if selected_company:
            company_info = data[data["기업명"] == selected_company].iloc[0]
            display_company_info(company_info)
        else:
            # 버튼이 선택되지 않았을 경우 기본 정보 표시
            default_company_info = data[data["기업명"] == "KDB 산업은행"].iloc[0]
            display_company_info(default_company_info)

    else:
        st.warning("데이터를 불러올 수 없습니다. CSV 파일을 확인해주세요.")

# Streamlit 실행
if __name__ == "__main__":
    show_company_info()