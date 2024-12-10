import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import os

# Streamlit UI 설정
st.set_page_config(page_title="Streamlit Chatbot", layout="centered")

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory)

    # 채팅 히스토리 저장소
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # UI 레이아웃 구성
    st.title("LangChain 기반 채팅")

    # 채팅 히스토리 표시
    chat_container = st.container()
    with chat_container:
        st.subheader("채팅 히스토리")
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.chat_message("👤 사용자: " + message["content"])
            else:
                st.chat_message("🤖 챗봇: " + message["content"])

    # 채팅 입력 영역
    user_input = st.text_input("메시지를 입력하세요:", key="user_input", placeholder="질문을 입력하세요...")

    # 사용자 입력 처리
    if user_input:
        # LangChain에서 응답 생성
        response = conversation.run(input=user_input)

        # 히스토리에 추가
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": response})

        # 입력창 비우기
        st.experimental_rerun()

else:
    st.warning("OpenAI API Key를 입력하세요.")