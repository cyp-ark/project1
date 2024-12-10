import streamlit as st

def render_kdb_ideal_candidate():
    st.title("📌 산업은행 인재상")

    # 인재상 설명
    st.header("산업은행이 추구하는 인재상")
    st.markdown(
    """
    <p>산업은행은 다음과 같은 가치를 바탕으로 인재를 찾고 있습니다:</p>
    <ul>
        <li><strong>고객 중심</strong>: 고객의 니즈를 최우선으로 생각하며, 항상 고객의 요구에 부응합니다.</li>
        <li><strong>도전과 변화</strong>: 익숙함에 머무르지 않고 계산된 도전을 통해 새로운 변화를 수용합니다.</li>
        <li><strong>소통과 협력</strong>: 주도적으로 소통하며 협력을 통해 더 나은 길을 찾습니다.</li>
        <li><strong>현장 중심</strong>: 문제를 현장에서 해결하며, 실행력을 갖춘 인재를 선호합니다.</li>
        <li><strong>책임감과 신뢰</strong>: 책임을 완수하여 사회적 신뢰를 얻고자 합니다.</li>
        <li><strong>미래 지향</strong>: 미래를 생각하며 지속 가능한 성장을 추구합니다.</li>
        <li><strong>전문성</strong>: 각 분야에서 전문성을 갖추어 대안을 제시합니다.</li>
        <li><strong>디지털 마인드</strong>: 디지털 역량과 혁신적 사고를 겸비합니다.</li>
    </ul>
    """,
    unsafe_allow_html=True
    )

    st.header("산업은행 소개")
    st.markdown(
        """
        - **역할**: 대한민국 경제 발전을 지원하는 정책 금융기관.
        - **핵심 목표**: 창의적 금융 서비스를 통해 국가 경쟁력 강화.
        - **홈페이지**: [산업은행 공식 웹사이트](https://www.kdb.co.kr)
        """
    )

if __name__ == "__main__":
    render_kdb_ideal_candidate()
