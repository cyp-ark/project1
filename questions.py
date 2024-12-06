# interview_prep.py
import openai
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

# 질문 카테고리와 질문 리스트
question_categories = {
    "금융 및 경제": [
        "ESG 금융의 활성화 방안",
        "산업구조 고도화를 위한 투자전략",
        "포스트 코로나 시대의 기업구조조정 방안",
        "중소기업 금융지원 확대 전략",
        "반도체 산업 경쟁력 분석과 금융 지원 방안",
        "기업 신용평가 모델 개선 방안",
        "신재생에너지 산업 투자전략",
        "최근 글로벌 금융시장 이슈는?",
        "산업은행의 정책금융 역할은?",
        "디지털 금융의 발전 방향",
    ],
    "기업 및 정책": [
        "구조조정 대상 기업 실사 방안",
        "기업가치 평가 방법론 설명",
        "창업이라는 특이한 이력을 갖고 있는데, 본인이 담당했던 포지션은 무엇인지?",
        "벤처기업 지원에 관심이 있다고 했는데, 정책금융을 통해 투자 및 지원이 반드시 필요하다고 생각하는 분야는 어디인가?",
        "IT분야든 3차 서비스 분야든 일단 수익이 발생하는 분야부터 지원해야 한다는 의견에 대해 어떻게 생각하는지?",
        "산언은행 모바일 뱅킹과 다른 은행의 모바일 뱅킹 차이점은 무엇인가요?",
        "한국산업은행에 관련한 최근 이슈를 말해보세요",
        "산업은행담당자라면 어떤 기업의 M&A를 주선하겠는가?",
        "기업의 존재 이유는 뭐라고 생각합니까?",
    ],
    "개인 및 경험": [
        "30초 자기소개",
        "공모전 활동이 구체적으로 어떤 활동인지? 갈등 경험이 있었는지?",
        "기존 불편사항을 이렇게 바꿔봤다!하는 경험?",
        "조직에 들어왔을 때 어떤 분위기를 제일 힘들어하는가? 그 어려움을 어떻게 해결해 나갈 것인가?",
        "나의 강점 한가지 혹은 타인으로부터 들었던 말",
        "자신이 리더라고 생각합니까, 팔로워라고 생각합니까?",
        "작년에도 우리 회사에 지원했는데, 면접에서 왜 탈락한 것 같나요?",
        "산업은행과 기타 공기업의 차이점은?",
        "자신의 가장 큰 장점이 무엇인가?",
    ],
    "사회 및 기타": [
        "소득 불평등",
        "초등학교에서 인성교육을 시키는 것에 대해 찬반 토론을 하라",
        "미국 정치 캠페인이 한국과 어떤 점에서 다르다고 생각하는가?",
        "본인이 생각하는 성공이란 무엇인가?",
        "정의란 무엇이라 생각하는가?",
        "국민연금제도에 관해 어떻게 생각하는가?",
        "귀화한 선수가 올림픽 출전을 통해 금메달 획득하는 것에 대한 의견",
        "사관학교 규제에 관한 본인의 생각",
        "하우스푸어 지원에 대한 찬반",
    ],
}

class InterviewPrepAssistant:
    def __init__(self):
        # LangChain의 ChatOpenAI 모델을 설정
        self.chat_openai = ChatOpenAI(model="gpt-4", temperature=0.7)
        self.prompt_template = PromptTemplate(input_variables=["question"], template="{question}")
        self.llm_chain = LLMChain(llm=self.chat_openai, prompt=self.prompt_template)

    def generate_answer(self, question):
        """주어진 질문에 대한 답변을 생성합니다."""
        try:
            response = self.llm_chain.run(question=f"질문: {question}. 이에 대한 답변을 상세히 작성해주세요.")
            return response.strip()
        except Exception as e:
            return f"예기치 못한 오류가 발생했습니다: {str(e)}"

class StreamlitUI:
    def __init__(self, assistant):
        """Streamlit UI를 초기화하고 인터뷰 준비 도우미 객체를 설정합니다."""
        self.assistant = assistant

    def show(self):
        """Streamlit 인터페이스를 구성합니다."""
        import streamlit as st

        # 초기화: 세션 상태에 선택된 카테고리 저장
        if "selected_category" not in st.session_state:
            st.session_state.selected_category = None

        st.title("💼산업은행 면접 준비 도우미")
        st.write("면접 질문을 선택하거나 직접 입력하면 GPT-4가 답변을 생성해 드립니다.")
        st.write("---")

        # 버튼 형식의 카테고리 선택
        st.write("### 질문 카테고리를 선택하세요:")
        cols = st.columns(len(question_categories))
        for i, category in enumerate(question_categories.keys()):
            if cols[i].button(category):
                st.session_state.selected_category = category

        st.write("---")

        # 선택된 카테고리에 따른 질문 표시
        if st.session_state.selected_category:
            selected_category = st.session_state.selected_category
            st.write(f"**선택한 카테고리: {selected_category}**")
            selected_question = st.selectbox(
                "질문을 선택하세요:", question_categories[selected_category]
            )

            # 직접 질문 입력
            custom_question = st.text_input("직접 질문을 입력하세요 (선택 사항):")

            # 답변 생성 버튼
            if st.button("답변 생성하기"):
                question = custom_question.strip() if custom_question else selected_question
                if not question:
                    st.warning("질문을 선택하거나 입력해주세요.")
                    return

                st.info(f"질문: {question}")
                with st.spinner("답변을 생성 중입니다..."):
                    answer = self.assistant.generate_answer(question)
                st.success("답변 생성 완료!")
                st.write(answer)
