import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
import faiss
import pickle

# 키 호출
load_dotenv()

# FAISS 인덱스 로드
faiss_index = faiss.read_index("faiss_index/index.faiss")

# 메타데이터 로드
with open("faiss_index/index.pkl", "rb") as f:
    metadata = pickle.load(f)

# Streamlit 앱 설정
st.title("🔍 FAISS 기반 기업별 TOWS 분석")
st.write("FAISS 데이터베이스와 OpenAI의 GPT를 사용하여 질문에 답변합니다.")

# FAISS 데이터베이스 로드 함수
def create_or_load_faiss_index(folder_path, faiss_file_path, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embeddings = OpenAIEmbeddings()

    if os.path.exists(faiss_file_path):
        vector_store = FAISS(embedding=faiss_index, metadata=metadata)
    else:
        all_docs = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith(".pdf"):
                    file_path = os.path.join(root, file_name)
                    loader = PyPDFLoader(file_path)
                    documents = loader.load()
                    docs = text_splitter.split_documents(documents)
                    all_docs.extend(docs)

        vector_store = FAISS.from_documents(all_docs, embeddings)
        vector_store.save_local(faiss_file_path)
    return vector_store


# TOWS 분석 생성 함수
def generate_tows_analysis(query, vector_store):
    """FAISS 데이터베이스를 사용하여 TOWS 분석 생성"""
    try:
        # 유사 문서 검색
        docs = vector_store.similarity_search(query, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # OpenAI LLM 호출
        prompt = f"""
        문맥:
        {context}

        위 문맥을 기반으로 다음 질문에 대한 TOWS 분석을 작성해주세요:
        {query}

        형식:
        위협 (Threats):
        - 항목 1
        - 항목 2

        기회 (Opportunities):
        - 항목 1
        - 항목 2

        약점 (Weaknesses):
        - 항목 1
        - 항목 2

        강점 (Strengths):
        - 항목 1
        - 항목 2
        """

        llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
        response = llm.predict(prompt)
        return response.strip()
    except Exception as e:
        return f"에러 발생: {str(e)}"



# Streamlit 앱
st.title("🔍 기업별 TOWS 분석")
st.write("OpenAI의 GPT를 사용하여 TOWS 분석을 생성합니다.")

# 사용자 입력
company_name = st.text_input("분석 대상 회사명을 입력하세요:", "KDB산업은행")
if st.button("🔄TOWS 분석 생성"):
    # TOWS 분석 생성
    analysis = generate_tows_analysis(company_name)
    if "에러 발생" not in analysis:
        # 분석 결과 출력
        st.subheader("✔️TOWS 분석 결과")
        st.write(f"\n{analysis}\n")

    else:
        st.error(f"오류 발생: {analysis}")
