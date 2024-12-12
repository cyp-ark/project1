import os
import streamlit as st
import pandas as pd
from chatbot import show_chatbot
from economy_news import show_economic_trends
#from fincorpinfo import show_company_info
from calendar_app import CalendarApp
from questions import InterviewPrepAssistant, StreamlitUI
import corpinfo

# 사이드바 네비게이션
def show_sidebar_navigation():
    """사이드바 네비게이션"""
    st.sidebar.title("📊 메뉴")
    # 섹션 이동 버튼
    if st.sidebar.button("📈 경제 현황"):
        st.session_state["section"] = "경제 현황"
    if st.sidebar.button("🏢 금융 공기업 정보"):
        st.session_state["section"] = "기업 동향"
    if st.sidebar.button("💬 면접 예상 질문"):
        st.session_state["section"] = "면접 질문"
    if st.sidebar.button("🤖 챗봇"):
        st.session_state["section"] = "챗봇"
    if st.sidebar.button("📅 채용 달력"):
        st.session_state["section"] = "채용 달력"

# 메인 실행 함수
def main():
    # Streamlit 앱
    st.set_page_config(page_title="경제금융기업 AI 활용 취업 지원 서비스", layout="wide")
    st.title("📊 경제금융기업 AI 활용 취업 지원 서비스")
    
    # 사이드바 네비게이션 표시
    show_sidebar_navigation()

    # 현재 활성화된 섹션에 따라 해당 함수 호출
    if st.session_state.get("section", "경제 현황") == "경제 현황":
        show_economic_trends()    
    elif st.session_state["section"] == "기업 동향":
        corpinfo.run()
    elif st.session_state["section"] == "면접 질문":
        # InterviewPrepAssistant 객체 생성
        assistant = InterviewPrepAssistant()
        # StreamlitUI 객체 생성 및 실행
        ui = StreamlitUI(assistant)
        ui.show()
    elif st.session_state["section"] == "챗봇":
        show_chatbot()
    elif st.session_state["section"] == "채용 달력":
        # CalendarApp 객체 생성
        app = CalendarApp()

        # 캘린더 렌더링
        app.render()
        

# 앱 실행
if __name__ == "__main__":
    main()