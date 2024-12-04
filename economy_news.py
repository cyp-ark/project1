import pandas as pd
import streamlit as st

# 샘플 키워드 및 최근 이슈 데이터 생성 - 자동 업데이트되게 수정해야함
def get_economic_issues():
    data = {
        "키워드": ["금리", "환율", "주식 시장", "부동산", "물가"],
        "최근 이슈": [
            "금리 인상이 계속될 가능성이 높아지고 있습니다. 싫은데요",
            "환율 변동성이 확대되며 원달러 환율이 1300원을 돌파했습니다.",
            "주식 시장은 대형 기술주의 강세로 반등을 보이고 있습니다.",
            "부동산 시장의 침체가 지속되며 거래량이 감소하고 있습니다.",
            "소비자 물가가 전년 대비 5% 상승하며 인플레이션 우려가 커지고 있습니다. 안녕",
        ],
    }
    return pd.DataFrame(data)

# 경제 현황 섹션
def show_economic_trends():
    """키워드별 최근 이슈를 표시하는 섹션"""
    st.header("한국 경제 현황")
    st.write("아래 키워드를 클릭하여 관련 이슈를 확인하세요.")
    
    # 데이터 가져오기
    economic_issues = get_economic_issues()

    # 키워드 선택
    selected_keyword = st.selectbox("키워드를 선택하세요:", economic_issues["키워드"])

    # 선택한 키워드에 대한 이슈 표시
    selected_issue = economic_issues[economic_issues["키워드"] == selected_keyword]["최근 이슈"].values[0]
    st.subheader(f"📰 {selected_keyword} 관련 최근 이슈")
    st.write(selected_issue)
    
    # 전체 데이터 표시 버튼
    if st.checkbox("모든 키워드 보기"):
        st.write(economic_issues)