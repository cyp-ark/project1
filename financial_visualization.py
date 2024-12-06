# financial_visualization.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

plt.rcParams['font.family'] = 'AppleGothic'  # 또는 'NanumGothic' 사용 가능

def get_financial_data(financial_option):
    if financial_option == "재무상태표":
        return {
            "항목": ["현금 및 현금성 자산", "공정가치 측정 금융자산(FVTPL)", "기타포괄손익-공정가치 금융자산(FVOCI)", 
                     "상각후원가 측정 대출채권", "기타 자산"],
            "금액 (백만원)": [8659808, 16085556, 33888064, 19998120, 10177583]
        }
    elif financial_option == "포괄손익계산서":
        return {
            "항목": ["이자수익", "수수료수익", "배당수익", 
                     "공정가치 측정 금융자산(FVTPL) 순손익", "기타 영업수익"],
            "금액 (백만원)": [1561519, 409836, 76370, 518808, 1386462]
        }
    elif financial_option == "연결재무상태표":
        return {
            "항목": ["현금 및 현금성 자산", "기타포괄손익-공정가치 금융자산(FVOCI)", 
                     "상각후원가 측정 대출채권", "관계기업 투자", "기타 자산"],
            "금액 (백만원)": [8306382, 23770064, 21838747, 21086136, 11077694]
        }
    else:
        return {
            "항목": ["이자수익", "배당수익", "공정가치 측정 금융상품(FVTPL) 순손익", 
                     "파생상품 순손익", "기타 영업수익"],
            "금액 (백만원)": [2435618, 316017, 743632, 49455, 2964399]
        }

def display_image(financial_option):
    img_path = f'./image/{financial_option}.jpg'
    if os.path.exists(img_path):
        img = Image.open(img_path)
        st.image(img, caption=financial_option)

def display_table(df):
    st.table(df)

def display_graph(df, financial_option):
    fig, ax = plt.subplots()
    
    if financial_option in ["재무상태표", "연결재무상태표"]:
        ax.bar(df["항목"], df["금액 (백만원)"], color="skyblue")
        ax.set_xlabel("항목")
        ax.set_ylabel("금액 (백만원)")
        ax.set_title("자산 분포")
        plt.xticks(rotation=45)
    else:
        ax.pie(df["금액 (백만원)"], labels=df["항목"], autopct='%1.1f%%', startangle=90)
        ax.set_title("손익 분포")
    st.pyplot(fig)

def main():
    st.subheader("재무제표 시각화")
    financial_option = st.selectbox(
        "시각화할 항목을 선택하세요",
        ("재무상태표", "포괄손익계산서", "연결재무상태표", "연결포괄손익계산서")
    )

    data = get_financial_data(financial_option)
    df = pd.DataFrame(data)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"{financial_option} 이미지")
        display_image(financial_option)

    with col2:
        st.subheader(f"{financial_option} 데이터")
        display_table(df)

        st.subheader(f"{financial_option} 그래프")
        display_graph(df, financial_option)

if __name__ == "__main__":
    main()
