import streamlit as st
<<<<<<< Updated upstream
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
import openai
import os
=======
from langchain_openai import ChatOpenAI
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import platform
from matplotlib import rc
from dotenv import load_dotenv
>>>>>>> Stashed changes

load_dotenv()

# 한글 폰트 설정
if platform.system() == "Windows":
    rc('font', family='Malgun Gothic')  # Windows
elif platform.system() == "Darwin":
    rc('font', family='AppleGothic')  # macOS
else:
    rc('font', family='NanumGothic')  # Linux (NanumGothic 필요)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


def generate_tows_analysis(company_name):
    """LangChain OpenAI를 사용하여 TOWS 분석 생성"""
    prompt = f"""
    당신은 분석 레포트를 쓰는 전문가 입니다. A4용지 한페이지 정도의 분량으로 각 항목마다 1-2가지 요인씩 자세하지만 깔끔하게 요약 정리 해주세요.
    다음 회사에 대한 TOWS 분석을 작성해주세요.
    회사명: {company_name}

    아래 형식으로 작성해주세요:
    위협 (Threats): KDB 산업은행의 위협 요인

    기회 (Opportunities): KDB 산업은행의 기회 요인

    약점 (Weaknesses): KDB 산업은행의 약점

    강점 (Strengths): KDB 산업은행의 강점
    """
    try:
        llm = ChatOpenAI(model="gpt-4", temperature=0.7)
        response = llm.predict(prompt)
        return response.strip()
    except Exception as e:
        return f"에러 발생: {str(e)}"


def parse_tows_analysis(analysis_text):
    """TOWS 분석 텍스트를 딕셔너리로 변환"""
    categories = {
        "위협": "Threat (위협)",
        "기회": "Opportunity (기회)",
        "약점": "Weakness (약점)",
        "강점": "Strength (강점)",
    }
    tows_dict = {v: [] for v in categories.values()}
    current_category = None

    for line in analysis_text.split("\n"):
        line = line.strip()
        for keyword, category in categories.items():
            if line.startswith(keyword):
                current_category = category
                break
        if current_category and line.startswith("-"):
            tows_dict[current_category].append(line.lstrip("- ").strip())

    return tows_dict



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
