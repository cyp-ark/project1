import pandas as pd
import streamlit as st

# 샘플 키워드 및 최근 이슈 데이터 생성 - 자동 업데이트되게 수정해야함


# 경제 현황 섹션
def show_economic_trends():
    
    """키워드별 최근 이슈를 표시하는 섹션"""
    st.subheader("📈 11월 마지막주 경제뉴스 헤드라인")

    st.markdown(
                    f'''
                    <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                        <p> 1. "글로벌 주요 증시, 미국 소비자물가 30년 만에 최고치 상승"</p>
                        <p> 2. "미국 신규 실업수당 신청, 예상치 상회"</p>
                        <p> 3. "중국 경제성장률, 전 분기 대비 하락세"</p>
                        <p> 4. "유럽 연합, 코로나19로 인한 경제 위기 극복을 위한 경제 지원안 추진"</p>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
    
    st.subheader('🔑 경제 키워드 분석')
    st.latex('E = mc^2')
    
    st.subheader('📉 경제 트렌드 분석')