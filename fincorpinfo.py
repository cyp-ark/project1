import os
import pandas as pd
import streamlit as st
from KDB import KDBAnalysisApp
from financial_visualization import main

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
    
    #st.header(f'{company_info["기업명"]}')
    st.markdown(
        f'''
        <div style="display: flex; align-items: center;">
            <div style="margin-right: 32px; font-size: 48px; font-weight: normal; color: #333;">
                <span>{company_info['기업명']}</span>
            </div>
            <div>
                <img src="{company_info['이미지 경로']}" alt="Example Image" style="border:None ; border-radius:10px; width:auto; height:50px;">
            </div>
        </div>
        '''
        , unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("기업 정보")
        st.markdown(
            f"""
            <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                <p><strong>산업:</strong> {company_info['산업']}</p>
                <p><strong>주소:</strong> {company_info['주소']}</p>
                <p><strong>설립일:</strong> {company_info['설립일']}</p>
                <p><strong>주력 사업:</strong> {company_info['주력 사업']}</p>
                <p><strong>자본금:</strong> {company_info['자본금']}</p>
                <p><strong>매출액:</strong> {company_info['매출액']}</p>
                <p><strong>대표자:</strong> {company_info['대표자']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with col2:
        st.subheader("인재상")
        
        
        st.markdown(
        """
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
        <ul>
            <p><strong>고객 중심</strong>: 고객의 니즈를 최우선으로 생각하며, 항상 고객의 요구에 부응합니다.</p>
            <p><strong>도전과 변화</strong>: 익숙함에 머무르지 않고 계산된 도전을 통해 새로운 변화를 수용합니다.</p>
            <p><strong>소통과 협력</strong>: 주도적으로 소통하며 협력을 통해 더 나은 길을 찾습니다.</p>
            <p><strong>현장 중심</strong>: 문제를 현장에서 해결하며, 실행력을 갖춘 인재를 선호합니다.</p>
            <p><strong>책임감과 신뢰</strong>: 책임을 완수하여 사회적 신뢰를 얻고자 합니다.</p>
            <p><strong>미래 지향</strong>: 미래를 생각하며 지속 가능한 성장을 추구합니다.</p>
            <p><strong>전문성</strong>: 각 분야에서 전문성을 갖추어 대안을 제시합니다.</p>
            <p><strong>디지털 마인드</strong>: 디지털 역량과 혁신적 사고를 겸비합니다.</p>
        </ul>
        </div>
        """,
        unsafe_allow_html=True
        )

        
    st.subheader(f"최신 이슈")

    st.markdown(f'''
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                        <p> 1. "AI 코리아 펀드 위탁운용사로 최종 4개 운용사 선정"</p>
                        <p> 2. "혁신성장펀드 4개 운용사 통과"</p>
                        <p> 3. "상생금융 지원방안에 2조원 부담 예상"</p>
                        <p> 4. "4대 금융지주 '역대급' 실적 경신에도 어두운 표정"</p>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
    
    
    st.subheader("🎯 합격자 통계")
    
    
    # 합격자, 급여 데이터 분석 앱 실행
    app = KDBAnalysisApp()
    app.run()
    main()

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