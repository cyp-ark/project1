import os
import streamlit as st
import pandas as pd
from datetime import datetime
#import chatbot
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

###########################################################################

def show_chatbot():
    """LLM 챗봇 섹션"""
    st.header("요약 분석 LLM 챗봇")

    # 사용자 입력
    user_input = st.text_input("질문을 입력하세요:", "")

    if st.button("분석 요청"):
        if user_input.strip():
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.spinner("GPT가 분석 중입니다..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4o",
                        messages=st.session_state["messages"]
                    )
                    answer = response["choices"][0]["message"]["content"]
                    st.session_state["messages"].append({"role": "assistant", "content": answer})
                    st.success("GPT의 응답:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("질문을 입력해주세요!")

    # 대화 기록 표시
    st.markdown("### 대화 기록")
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**GPT:** {message['content']}")

# 메인 실행 함수
def main():
    # Streamlit 앱
    st.title("📊 금융기관 정보")
    
    """메인 실행 함수"""
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
