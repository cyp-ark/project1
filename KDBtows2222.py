import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import openai
import os

# OpenAI API 키 설정
openai.api_key = "OPENAI_API_KEY"

# Streamlit App
st.title("KDB 미래전략연구소 PDF 분석 및 TOWS 요약")

# FAISS 인덱스 생성 및 로드 함수
def create_or_load_faiss_index(folder_path, faiss_file_path, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    embeddings = OpenAIEmbeddings()

    if os.path.exists(faiss_file_path):
        vector_store = FAISS.load_local(faiss_file_path, embeddings, allow_dangerous_deserialization=True)
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
def generate_tows_analysis(company_name):
    """OpenAI API를 사용하여 TOWS 분석 생성"""
    prompt = f"""
    다음 회사에 대한 TOWS 분석을 작성해주세요.
    회사명: {company_name}

    아래 형식으로 작성해주세요:
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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 한국어로 TOWS 분석을 제공하는 유용한 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"에러 발생: {str(e)}"

# Predefined paths
pdf_folder_path = "C:/Users/Admin/Documents/GitHub/project1/kdb미래전략연구소"  # Path to the folder containing predefined PDFs
faiss_file_path = "C://Users//Admin//Documents//GitHub//project1//faiss_index"

# Load or Create FAISS Index
if os.path.exists(pdf_folder_path):
    st.info("FAISS 인덱스를 생성하거나 로드 중입니다...")
    vector_store = create_or_load_faiss_index(pdf_folder_path, faiss_file_path)
    st.success("FAISS 인덱스 로드 완료!")

    # Querying TOWS Analysis
    company_name = st.text_input("TOWS 분석을 수행할 회사명을 입력하세요:", "산업은행")
    if company_name:
        analysis_result = generate_tows_analysis(company_name)
        st.write("**TOWS 분석 결과**")
        st.markdown(analysis_result)
else:
    st.error("사전 정의된 PDF 폴더를 찾을 수 없습니다. 경로를 확인하세요.")
