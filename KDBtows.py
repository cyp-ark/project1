import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# FAISS 인덱스 초기화
def load_faiss_index(db_path):
    """주어진 경로에서 FAISS 인덱스를 불러옵니다."""
    embeddings = OpenAIEmbeddings()  # OpenAI API 키가 .env 파일에 설정되어 있어야 합니다.
    return FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)






# GPT-4o를 사용해 TOWS 분석 생성
def generate_tows_analysis_with_context(company_name, context):
    """faiss db를 사용하여 GPT-4o로 TOWS 분석을 생성합니다."""
    prompt = f"""
    당신은 분석 레포트를 작성하는 전문가입니다.
    TOWS 분석이란 기업 외부 환경의 기회와 위협을 찾아내고 기업 내부 환경의 강점과 약점을 발견해 기회를 활용하고 위협은 억제시키며, 강점을 활용하고 약점을 보완하는 전략 수립을 말합니다. 외부 환경에서 유리하게 작용하는 기회 요인, 외부환경에서 불리하게 작용하는 위협 요인, 경쟁사 대비 강점, 경쟁사 대비 약점이 각각 무엇인지 알아보기 위함입니다.
    A4용지 한페이지 정도의 분량으로 작성 해 주세요.
    회사의 사업, 현재 상황 등을 구체적으로 작성 해 주세요.
    제공된 faiss db를 바탕으로 다음 회사에 대해 형식에 맞게 TOWS 분석을 작성해주세요.

    아래 형식으로 작성해주세요.:

    회사명: {company_name} (큰 글씨로)

    산업 요약: {context}


    위협 (Threats): {company_name}의 위협 요인 (굵게, 중간크기 글씨)
    1. 제목 (굵게)

    내용
    2. 제목 (굵게)

    내용

    기회 (Opportunities): {company_name}의 기회 요인 (굵게, 중간크기 글씨)
    1. 제목 (굵게)

    내용
    2. 제목 (굵게)

    내용

    약점 (Weaknesses): {company_name}의 약점 (굵게, 중간크기 글씨)
    1. 제목 (굵게)

    내용
    2. 제목 (굵게)

    내용

    강점 (Strengths): {company_name}의 강점 (굵게, 중간크기 글씨)
    1. 제목 (굵게)

    내용
    2. 제목 (굵게)

    내용
    """
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        return llm.predict(prompt).strip()
    except Exception as e:
        return f"⚠️ GPT 모델 오류: {str(e)}"
    



# Streamlit 앱 설정
st.title("🔍 기업별 TOWS 분석")
st.write("OpenAI GPT를 활용해 기업의 TOWS 분석을 제공합니다.")

# FAISS 인덱스 불러오기
db_path = "faiss_index"  # FAISS 인덱스 폴더 경로
try:
    vector_db = load_faiss_index(db_path)
except Exception as e:
    st.error(f"❌ FAISS 데이터베이스를 불러오지 못했습니다: {str(e)}")
    st.stop()

# 사용자 입력 받기
company_name = st.text_input("분석할 회사명을 입력하세요:", "KDB산업은행")

if st.button("🔄 TOWS 분석 생성"):
    # FAISS 데이터베이스에서 맥락 검색
    with st.spinner("🔍 데이터베이스에서 관련 정보를 검색 중입니다..."):
        try:
            search_results = vector_db.similarity_search(company_name, k=10)
            context = "\n".join([result.page_content for result in search_results])
        except Exception as e:
            st.error(f"❌ 데이터베이스 검색 오류: {str(e)}")
            st.stop()

    # GPT-4를 사용해 TOWS 분석 생성
    with st.spinner("🤖 GPT 모델로 TOWS 분석을 생성 중입니다..."):
        analysis = generate_tows_analysis_with_context(company_name, context)

    # 결과 출력
    if "⚠️" not in analysis:
        st.subheader("✅ TOWS 분석 결과")
        st.write(analysis)
    else:
        st.error(analysis)
