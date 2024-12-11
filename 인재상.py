import streamlit as st

def render_kdb_ideal_candidate():
    st.title("산업은행 인재상")
    st.image(
        "https://www.kdb.co.kr/resource/kdb_main_logo.png", 
        caption="KDB 산업은행",
        use_column_width=True
    )

    st.header("📌 핵심 가치")
    st.markdown(
        """
        - **고객 중심 (Customer Focus)**  
          고객의 필요와 기대를 최우선으로 생각하며 최고의 금융 서비스를 제공.
        
        - **창의와 혁신 (Creativity & Innovation)**  
          금융의 창의적 솔루션을 통해 새로운 가치를 창출.
        
        - **전문성 (Professionalism)**  
          전문 지식을 바탕으로 정밀한 금융 서비스를 제공.
        
        - **사회적 책임 (Social Responsibility)**  
          금융의 사회적 가치를 실현하며 국가 경제 발전에 기여.
        """
    )

    st.header("📌 산업은행이 추구하는 인재상")
    st.markdown(
        """
        - **도전 정신**: 어려운 상황에서도 새로운 길을 찾아 도전하는 태도.
        - **책임감**: 맡은 일에 대한 강한 책임감과 윤리적 자세.
        - **팀워크**: 협력과 소통을 통해 팀의 목표를 이루는 협업 능력.
        - **글로벌 마인드**: 국제적 감각과 경쟁력을 가진 인재.
        """
    )

    st.header("📌 추가 정보")
    st.markdown(
        """
        산업은행은 금융 전문성과 혁신적 사고를 바탕으로 대한민국 경제의 성장과 발전에 기여하고자 
        최고의 금융 전문가를 찾고 있습니다.
        """
    )
    st.write("🔗 [자세히 알아보기](https://www.kdb.co.kr)")

if __name__ == "__main__":
    render_kdb_ideal_candidate()
