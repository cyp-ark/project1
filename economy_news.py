import pandas as pd
import streamlit as st

# 샘플 키워드 및 최근 이슈 데이터 생성 - 자동 업데이트되게 수정해야함


# 경제 현황 섹션
def show_economic_trends():
    df = pd.read_csv('trend_df.csv',encoding='cp949')
    df.drop('Unnamed: 0',axis=1,inplace=True)
    top_keyword = df['keyword'].value_counts().head(10).index.tolist()
    top_df = df[df['keyword'].isin(top_keyword)]
    pivot_df = top_df.pivot_table(index='month',columns='keyword',values='keyword',aggfunc='size', fill_value=0)
    
    """키워드별 최근 이슈를 표시하는 섹션"""
    st.subheader("📈 11월 경제 이슈")

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
    st.image("./image/wordcloud.png",use_column_width=False)
    
    st.subheader('📉 경제 트렌드 분석')
    st.line_chart(pivot_df,height=600, use_container_width=True)
    
    