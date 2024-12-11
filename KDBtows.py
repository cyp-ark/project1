import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
import os

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

# Predefined paths
pdf_folder_path = "C:/Users/Admin/Documents/GitHub/project1/kdb미래전략연구소"  # Path to the folder containing predefined PDFs
faiss_file_path = "C://Users//Admin//Documents//GitHub//project1//faiss_index"

# Load or Create FAISS Index
if os.path.exists(pdf_folder_path):
    st.info("FAISS 인덱스를 생성하거나 로드 중입니다...")
    vector_store = create_or_load_faiss_index(pdf_folder_path, faiss_file_path)
    st.success("FAISS 인덱스 로드 완료!")

    # Querying TOWS Analysis
    llm = ChatOpenAI(temperature=0.7)
    tows_prompt = """
    다음 텍스트를 기반으로 TOWS 분석을 수행하십시오. 
    분석 요소:
    - Strengths
    - Weaknesses
    - Opportunities
    - Threats
    텍스트:
    {text}
    """

    # Fixed Query Example
    query = "기업의 최신 동향 분석"
    st.write(f"**TOWS 분석을 위한 고정 질문:** {query}")
    
    results = vector_store.similarity_search(query, k=3)
    for result in results:
        response = llm.predict(tows_prompt.format(text=result.page_content))
        st.markdown(response)
    st.success("TOWS 분석 완료!")
else:
    st.error("사전 정의된 PDF 폴더를 찾을 수 없습니다. 경로를 확인하세요.")