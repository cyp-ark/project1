import os
import pandas as pd
import streamlit as st

base_dir = os.getcwd()
csv_file_path = os.path.join(base_dir, "corpinfo.csv")

print(f"CSV 파일 경로: {csv_file_path}")

# CSV 데이터 읽기
def load_data_from_csv(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8-sig')
        return data[["기업명", "산업", "설립일","자본금","매출액","대표자","주력 사업","최근 동향","주소","이미지 경로"]]  # 필요한 열만 선택
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 기업 정보 표시 섹션
def show_company_info():
    """기업 정보 표시 섹션"""
    st.header("📊 기업 정보")

    # CSV 데이터 로드
    data = load_data_from_csv(csv_file_path)

    if not data.empty:
        # 기업 선택
        selected_company = st.selectbox("기업명을 선택하세요:", data["기업명"])

         # 선택한 기업 정보 표시
        if selected_company:
            company_info = data[data["기업명"] == selected_company].iloc[0]
            
            # 기업 정보 상세 표시
            st.subheader(f"🏢 {company_info['기업명']}")
            st.markdown(f"**산업:** {company_info['산업']}")
            st.markdown(f"**설립일:** {company_info['설립일']}")
            st.markdown(f"**자본금:** {company_info['자본금']}")
            st.markdown(f"**매출액:** {company_info['매출액']}")
            st.markdown(f"**대표자:** {company_info['대표자']}")
            st.markdown(f"**주력 사업:** {company_info['주력 사업']}")
            st.markdown(f"**최근 동향:** {company_info['최근 동향']}")
            st.markdown(f"**주소:** {company_info['주소']}")

            # 이미지 표시 (이미지 경로가 포함된 경우)
            if pd.notna(company_info['이미지 경로']):
                st.image(company_info['이미지 경로'], caption=f"{company_info['기업명']} 로고")

        # 모든 기업 정보 보기 옵션
        if st.checkbox("모든 기업 정보 보기"):
            st.dataframe(data, use_container_width=True)

    else:
        st.warning("데이터를 불러올 수 없습니다. CSV 파일을 확인해주세요.")

