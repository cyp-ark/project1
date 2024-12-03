import os
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

# Streamlit 앱
st.title("📊 금융기관 정보")

# 현재 사용자 경로를 기반으로 CSV 파일 경로 생성
base_dir = os.path.expanduser("~/Desktop/VE/fincorp")
csv_file_path = os.path.join(base_dir, "corpinfo.csv")

print(f"CSV 파일 경로: {csv_file_path}")

# CSV 데이터 읽기
def load_data_from_csv(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8-sig')
        return data[["기업명", "산업", "설립일","자본금","매출액","대표자","주력 사업","최근 동향","주소","이미지 경로"]]  # 필요한 열만 선택
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 기업 정보 표시 섹션
def show_company_info():
    """기업 정보 표시 섹션"""
    st.header("📊 기업 정보")

    # CSV 데이터 로드
    data = load_data_from_csv(csv_file_path)

    if not data.empty:
        # 기업 선택
        selected_company = st.selectbox("기업명을 선택하세요:", data["기업명"])

         # 선택한 기업 정보 표시
        if selected_company:
            company_info = data[data["기업명"] == selected_company].iloc[0]
            
            # 기업 정보 상세 표시
            st.subheader(f"🏢 {company_info['기업명']}")
            st.markdown(f"**산업:** {company_info['산업']}")
            st.markdown(f"**설립일:** {company_info['설립일']}")
            st.markdown(f"**자본금:** {company_info['자본금']}")
            st.markdown(f"**매출액:** {company_info['매출액']}")
            st.markdown(f"**대표자:** {company_info['대표자']}")
            st.markdown(f"**주력 사업:** {company_info['주력 사업']}")
            st.markdown(f"**최근 동향:** {company_info['최근 동향']}")
            st.markdown(f"**주소:** {company_info['주소']}")

            # 이미지 표시 (이미지 경로가 포함된 경우)
            if pd.notna(company_info['이미지 경로']):
                st.image(company_info['이미지 경로'], caption=f"{company_info['기업명']} 로고")

        # 모든 기업 정보 보기 옵션
        if st.checkbox("모든 기업 정보 보기"):
            st.dataframe(data, use_container_width=True)

    else:
        st.warning("데이터를 불러올 수 없습니다. CSV 파일을 확인해주세요.")



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
        show_company_info()
    elif st.session_state["section"] == "챗봇":
        show_chatbot()

# 앱 실행
if __name__ == "__main__":
    main()
