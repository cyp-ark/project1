import streamlit as st
import pandas as pd
from datetime import datetime

###########################################################################

# 샘플 채용 일정 데이터 생성
def get_recruitment_schedule():
    data = {
        "날짜": [
            "2024-12-01", "2024-12-05", "2024-12-10",
            "2024-12-15", "2024-12-20", "2024-12-25"
        ],
        "이벤트": [
            "KDB 산업은행 채용 공고",
            "서류 제출 시작",
            "서류 심사 마감",
            "1차 면접 일정 발표",
            "최종 면접 진행",
            "최종 결과 발표"
        ],
    }
    df = pd.DataFrame(data)
    df["날짜"] = pd.to_datetime(df["날짜"])  # 날짜 형식 변환
    return df

# 채용 달력 섹션
def show_recruitment_calendar():
    """채용 달력을 사이드바 하단에 표시"""
    st.sidebar.markdown("---")  # 상단과 구분선 추가
    st.sidebar.markdown("### 📅 채용 달력")

    # 데이터 가져오기
    recruitment_schedule = get_recruitment_schedule()

    # 날짜 선택 위젯
    selected_date = st.sidebar.date_input("날짜를 선택하세요:", datetime.now())

    # 선택한 날짜에 해당하는 이벤트 필터링
    selected_events = recruitment_schedule[recruitment_schedule["날짜"] == pd.Timestamp(selected_date)]

    # 선택된 날짜의 이벤트 표시
    if not selected_events.empty:
        for _, row in selected_events.iterrows():
            st.sidebar.success(f"📌 {row['날짜'].strftime('%Y-%m-%d')}: {row['이벤트']}")
    else:
        st.sidebar.info("선택한 날짜에 채용 일정이 없습니다.")

###########################################################################

# 사이드바 네비게이션
def show_sidebar_navigation():
    """사이드바 네비게이션"""
    st.sidebar.title("📊 메뉴")
    # 섹션 이동 버튼
    if st.sidebar.button("📈 경제 현황"):
        st.session_state["section"] = "경제 현황"
    if st.sidebar.button("🏢 기업 동향"):
        st.session_state["section"] = "기업 동향"
    if st.sidebar.button("🤖 챗봇"):
        st.session_state["section"] = "챗봇"

###########################################################################

# 샘플 키워드 및 최근 이슈 데이터 생성 - 자동 업데이트되게 수정해야함
def get_economic_issues():
    data = {
        "키워드": ["금리", "환율", "주식 시장", "부동산", "물가"],
        "최근 이슈": [
            "금리 인상이 계속될 가능성이 높아지고 있습니다.",
            "환율 변동성이 확대되며 원달러 환율이 1300원을 돌파했습니다.",
            "주식 시장은 대형 기술주의 강세로 반등을 보이고 있습니다.",
            "부동산 시장의 침체가 지속되며 거래량이 감소하고 있습니다.",
            "소비자 물가가 전년 대비 5% 상승하며 인플레이션 우려가 커지고 있습니다.",
        ],
    }
    return pd.DataFrame(data)

# 경제 현황 섹션
def show_economic_trends():
    """키워드별 최근 이슈를 표시하는 섹션"""
    st.header("한국 경제 현황")
    st.write("아래 키워드를 클릭하여 관련 이슈를 확인하세요.")
    
    # 데이터 가져오기
    economic_issues = get_economic_issues()

    # 키워드 선택
    selected_keyword = st.selectbox("키워드를 선택하세요:", economic_issues["키워드"])

    # 선택한 키워드에 대한 이슈 표시
    selected_issue = economic_issues[economic_issues["키워드"] == selected_keyword]["최근 이슈"].values[0]
    st.subheader(f"📰 {selected_keyword} 관련 최근 이슈")
    st.write(selected_issue)
    
    # 전체 데이터 표시 버튼
    if st.checkbox("모든 키워드 보기"):
        st.write(economic_issues)

###########

# 샘플 금융 공기업 데이터 생성
def get_financial_institutions():
    data = {
        "기업명": ["KDB 산업은행", "한국수출입은행", "한국투자공사", "예금보험공사", "신용보증기금"],
        "주력 사업": [
            "기업 금융 지원 및 구조 조정",
            "수출입 거래 금융 지원",
            "해외 투자 및 자산 관리",
            "예금자 보호 및 금융 안정",
            "중소기업 및 창업 지원"
        ],
        "최근 동향": [
            "2024년 구조조정 계획 발표 및 주요 산업 지원 확대",
            "중소기업 수출 금융 지원 패키지 출시",
            "글로벌 투자 포트폴리오 다각화 진행",
            "2024년 예금 보험료율 조정 검토",
            "스타트업 금융 지원 프로그램 확장"
        ],
    }
    return pd.DataFrame(data)

# 기업 동향 섹션
def show_company_trends():
    """기업 동향 섹션"""
    st.header("금융 공기업 동향")
    st.write("아래에서 관심 있는 기업을 선택하여 상세 정보를 확인하세요.")

    # 금융 공기업 데이터
    institutions = get_financial_institutions()

    # 기업 선택
    selected_company = st.selectbox("기업명을 선택하세요:", institutions["기업명"])

    # 선택한 기업 정보 표시
    company_info = institutions[institutions["기업명"] == selected_company].iloc[0]
    st.subheader(f"🏢 {selected_company}")
    st.write(f"**주력 사업:** {company_info['주력 사업']}")
    st.write(f"**최근 동향:** {company_info['최근 동향']}")

    # 모든 데이터 보기 옵션
    if st.checkbox("모든 기업 정보 보기"):
        st.write(institutions)


###########

def show_chatbot():
    """LLM 챗봇 섹션"""
    st.header("요약 분석 LLM 챗봇")

    # 사용자 입력
    user_input = st.text_input("질문을 입력하세요:", "")

    if st.button("분석 요청"):
        if user_input.strip():
            st.session_state["messages"].append({"role": "user", "content": user_input})
            with st.spinner("GPT가 분석 중입니다..."):
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=st.session_state["messages"]
                    )
                    answer = response["choices"][0]["message"]["content"]
                    st.session_state["messages"].append({"role": "assistant", "content": answer})
                    st.success("GPT의 응답:")
                    st.write(answer)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("질문을 입력해주세요!")

    # 대화 기록 표시
    st.markdown("### 대화 기록")
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**GPT:** {message['content']}")

# 메인 실행 함수
def main():
    """메인 실행 함수"""
    # 사이드바 네비게이션 표시
    show_sidebar_navigation()

    # 사이드바 하단에 채용 달력 표시
    show_recruitment_calendar()

    # 현재 활성화된 섹션에 따라 해당 함수 호출
    if st.session_state.get("section", "경제 현황") == "경제 현황":
        show_economic_trends()
    elif st.session_state["section"] == "기업 동향":
        show_company_trends()
    elif st.session_state["section"] == "챗봇":
        show_chatbot()

# 앱 실행
if __name__ == "__main__":
    main()
