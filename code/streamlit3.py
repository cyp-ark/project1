import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc
from PIL import Image
import os

# 한글 폰트 설정
rc('font', family='Malgun Gothic')  # Windows 사용 시

# 페이지 설정
st.set_page_config(page_title="재무제표 시각화", layout="wide")

# 제목
st.title("재무제표 시각화")

# 데이터 선택 옵션
option = st.sidebar.selectbox(
    "시각화할 항목을 선택하세요",
    ("재무상태표", "포괄손익계산서", "연결재무상태표", "연결포괄손익계산서")
)


# 데이터 입력
if option == "재무상태표":
    data = {
        "항목": ["현금 및 현금성 자산", "공정가치 측정 금융자산(FVTPL)", "기타포괄손익-공정가치 금융자산(FVOCI)", 
                "상각후원가 측정 대출채권", "기타 자산"],
        "금액 (백만원)": [8659808, 16085556, 33888064, 19998120, 10177583]
    }
    df = pd.DataFrame(data)

elif option == "포괄손익계산서":
    data = {
        "항목": ["이자수익", "수수료수익", "배당수익", 
                "공정가치 측정 금융자산(FVTPL) 순손익", "기타 영업수익"],
        "금액 (백만원)": [1561519, 409836, 76370, 518808, 1386462]
    }
    df = pd.DataFrame(data)

elif option == "연결재무상태표":
    data = {
        "항목": ["현금 및 현금성 자산", "기타포괄손익-공정가치 금융자산(FVOCI)", 
                "상각후원가 측정 대출채권", "관계기업 투자", "기타 자산"],
        "금액 (백만원)": [8306382, 23770064, 21838747, 21086136, 11077694]
    }
    df = pd.DataFrame(data)

elif option == "연결포괄손익계산서":
    data = {
        "항목": ["이자수익", "배당수익", "공정가치 측정 금융상품(FVTPL) 순손익", 
                "파생상품 순손익", "기타 영업수익"],
        "금액 (백만원)": [2435618, 316017, 743632, 49455, 2964399]
    }
    df = pd.DataFrame(data)

# 2단 레이아웃
col1, col2 = st.columns(2)

# col1: 업로드된 이미지 표시
with col1:
    st.subheader(f"{option} 이미지")
    img1 = Image.open('./image/재무상태표.jpg')
    img2 = Image.open('./image/포괄손익계산서.jpg')
    img3 = Image.open('./image/연결재무상태표.jpg')
    img4 = Image.open('./image/연결포괄손익계산서.jpg')

    if option == '재무상태표': st.image(img1, caption='재무상태표')
    elif option == '포괄손익계산서': st.image(img2, caption='포괄손익계산서')
    elif option == '연결재무상태표': st.image(img3, caption='연결재무상태표')
    elif option == '연결포괄손익계산서': st.image(img4, caption='연결포괄손익계산서')

# col2: 데이터와 그래프 표시
with col2:
    st.subheader(f"{option} 데이터")
    st.table(df)

    # 시각화
    st.subheader(f"{option} 그래프")
    fig, ax = plt.subplots()

    if option in ["재무상태표", "연결재무상태표"]:
        # 막대 그래프
        ax.bar(df["항목"], df["금액 (백만원)"], color="skyblue")
        ax.set_xlabel("항목")
        ax.set_ylabel("금액 (백만원)")
        ax.set_title("자산 분포")
        plt.xticks(rotation=45)  # X축 항목 회전
    elif option in ["포괄손익계산서", "연결포괄손익계산서"]:
        # 원형 그래프
        ax.pie(df["금액 (백만원)"], labels=df["항목"], autopct='%1.1f%%', startangle=90)
        ax.set_title("손익 분포")

    st.pyplot(fig)
