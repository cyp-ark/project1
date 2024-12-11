import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

class KDBAnalysisApp:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o")

    def load_data(self) -> pd.DataFrame:
        """Load and return the KDB analysis dataset."""
        data = {
            "년도": ["2023(상)", "2022(상)", "2021(상)", "2020(하)", "2020(상)", "2019(상)"],
            "서류전형 응시인원": [3416, 3357, 2611, 3576, 1802, 2841],
            "서류전형 합격인원": [2317, 1823, 1501, 1006, 627, 1294],
            "서류전형 경쟁률": [1.47, 1.84, 1.74, 3.55, 2.87, 2.20],
            "필기전형 응시율": [58.90, 70.80, 68.00, 82.10, 57.10, 49.60],
            "필기전형 합격률": [26.60, 23.30, 18.00, 19.40, 29.10, 34.30],
            "서류/최종 경쟁률": [29.7, 36.1, 43.52, 71.52, 60.07, 43.71]
        }
        return pd.DataFrame(data)
    
    def display_salary_analysis(self):
        """Display salary-related data analysis."""
        st.subheader("급여 데이터 분석")

        # 급여 데이터
        data = {
            "구분": [
                "기본급", "고정수당", "실적수당", "급여성 복리후생비",
                "성과상여금", "경영평가 성과금", "기타",
                "1인당 평균 보수액", "평균근속연수"
            ],
            "2020년 결산": [54954, 11996, 5110, 1227, 38656, "-", 56, 111999, 16.3],
            "2021년 결산": [54481, 12119, 6255, 1312, 39458, "-", 78, 113703, 16.6],
            "2022년 결산": [54761, 12238, 5966, 1374, 38475, "-", 76, 112890, 16.8],
            "2023년 결산": [54924, 12268, 5423, 1415, 38875, "-", 94, 112999, 16.4],
            "2024년 예산": [56297, 12575, 5558, 1451, 29510, "-", 97, 105488, 17.4]
        }
        df = pd.DataFrame(data)

        # 각 데이터셋 생성
        basic_salary_data = pd.DataFrame({
            "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
            "기본급": df.set_index("구분").loc["기본급"].values
        })

        performance_data = pd.DataFrame({
            "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
            "성과상여금": df.set_index("구분").loc["성과상여금"].replace("-", 0).astype(float).values
        })

        tenure_data = pd.DataFrame({
            "년도": ["2020년 결산", "2021년 결산", "2022년 결산", "2023년 결산", "2024년 예산"],
            "평균근속연수": df.set_index("구분").loc["평균근속연수"].values
        })

        col1, col2, col3 = st.columns(3)

        # 기본급
        with col1:
            st.write("기본급 변화")
            st.bar_chart(basic_salary_data.set_index("년도"))

            if st.button("💡 기본급 AI 분석"):
                with st.spinner("AI가 기본급 데이터를 분석 중입니다..."):
                    prompt = "다음 기본급 데이터를 분석하고 주요 패턴을 두 문장으로 요약하세요:\n" + basic_salary_data.to_string(index=False)
                    result = self.llm.predict(prompt)
                    st.write(result)

        # 성과상여금
        with col2:
            st.write("성과상여금 변화")
            st.line_chart(performance_data.set_index("년도"))

            if st.button("💡 성과상여금 AI 분석"):
                with st.spinner("AI가 성과상여금 데이터를 분석 중입니다..."):
                    prompt = "다음 성과상여금 데이터를 분석하고 주요 패턴을 두 문장으로 요약하세요:\n" + performance_data.to_string(index=False)
                    result = self.llm.predict(prompt)
                    st.write(result)

        # 평균 근속연수
        with col3:
            st.write("평균근속연수 변화")
            st.line_chart(tenure_data.set_index("년도"))

            if st.button("💡 평균근속연수 AI 분석"):
                with st.spinner("AI가 평균근속연수 데이터를 분석 중입니다..."):
                    prompt = "다음 평균근속연수 데이터를 분석하고 주요 패턴을 두 문장으로 요약하세요:\n" + tenure_data.to_string(index=False)
                    result = self.llm.predict(prompt)
                    st.write(result)


    def plot_charts(self, df: pd.DataFrame):
        """Render charts for KDB analysis."""
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("서류전형 응시인원 및 합격인원")
            st.bar_chart(df.set_index("년도")[["서류전형 응시인원", "서류전형 합격인원"]])
        with col2:
            st.write("필기전형 응시율 및 합격률")
            st.line_chart(df.set_index("년도")[["필기전형 응시율", "필기전형 합격률"]])
        with col3:
            st.write("경쟁률 비교")
            st.line_chart(df.set_index("년도")[["서류전형 경쟁률", "서류/최종 경쟁률"]])

    def analyze_data_with_ai(self, df: pd.DataFrame):
        """Generate AI analysis result and store it in session state."""
        prompt = f"다음 데이터를 분석하여 주요 패턴과 인사이트를 도출하세요:\n{df.to_string(index=False)}"
        result = self.llm.predict(prompt)
        st.session_state["analysis_result"] = result

    def display_analysis_result(self):
        """Display the AI analysis result for each category based on button clicks."""
        col1, col2, col3 = st.columns(3)

        # 서류전형 분석 버튼
        with col1:
            if st.button("💡 서류전형 분석"):
                with st.spinner("AI가 서류전형 데이터를 분석 중입니다..."):
                    prompt = f"취업 준비생에게 도움이 될 수 있도록 서류전형 관련 데이터를 분석하여 주요 패턴과 인사이트를 2문장 이내로 짧게 도출하세요:\n{self.load_data().to_string(index=False)}"
                    st.session_state["document_analysis"] = self.llm.predict(prompt)
            if "document_analysis" in st.session_state:
                st.write(st.session_state["document_analysis"])

        # 필기전형 분석 버튼
        with col2:
            if st.button("💡 필기전형 분석"):
                with st.spinner("AI가 필기전형 데이터를 분석 중입니다..."):
                    prompt = f"취업 준비생에게 도움이 될 수 있도록 필기전형 관련 데이터를 분석하여 주요 패턴과 인사이트를 2문장 이내로 짧게 도출하세요:\n{self.load_data().to_string(index=False)}"
                    st.session_state["written_analysis"] = self.llm.predict(prompt)
            if "written_analysis" in st.session_state:
                st.write(st.session_state["written_analysis"])

        # 최종 결과 분석 버튼
        with col3:
            if st.button("💡 최종 결과 분석"):
                with st.spinner("AI가 최종 데이터를 분석 중입니다..."):
                    prompt = f"취업 준비생에게 도움이 될 수 있도록 최종 경쟁률 관련 데이터를 분석하여 주요 패턴과 인사이트를 2문장 이내로 짧게 도출하세요:\n{self.load_data().to_string(index=False)}"
                    st.session_state["final_analysis"] = self.llm.predict(prompt)
            if "final_analysis" in st.session_state:
                st.write(st.session_state["final_analysis"])

    def run(self):
        load_dotenv()
        """Run the Streamlit app."""
        df = self.load_data()
        self.plot_charts(df)

        # 합격자 분석 결과
        self.analyze_data_with_ai(df)
        self.display_analysis_result()

        # 급여 데이터 분석 결과
        self.display_salary_analysis()



if __name__ == "__main__":
    load_dotenv()
    app = KDBAnalysisApp()
    app.run()
