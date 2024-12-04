import os
import streamlit as st
import pandas as pd
from datetime import datetime
from chatbot import show_chatbot
from economy_news import show_economic_trends
from fincorpinfo import show_company_info

###########################################################################

# 사이드바 네비게이션
def show_sidebar_navigation():
    """사이드바 네비게이션"""
    st.sidebar.title("📊 메뉴")
    # 섹션 이동 버튼
    if st.sidebar.button("📈 경제 현황"):
        st.session_state["section"] = "경제 현황"
    if st.sidebar.button("🏢 기업 동향"):
        st.session_state["section"] = "기업 동향"
    if st.sidebar.button("🤖 챗봇"):
        st.session_state["section"] = "챗봇"

# 메인 실행 함수
def main():
    # Streamlit 앱
    st.title("📊 금융기관 정보")
    
    # 사이드바 네비게이션 표시
    show_sidebar_navigation()

    # 현재 활성화된 섹션에 따라 해당 함수 호출
    if st.session_state.get("section", "경제 현황") == "경제 현황":
        show_economic_trends()
    elif st.session_state["section"] == "기업 동향":
        show_company_info()
    elif st.session_state["section"] == "챗봇":
        show_chatbot()

# 앱 실행
if __name__ == "__main__":
    main()

