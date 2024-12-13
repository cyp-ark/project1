import os
import json
import platform
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# 운영체제에 따라 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows에서 맑은고딕
elif platform.system() == 'Darwin':  # MacOS는 'Darwin'으로 인식됨
    plt.rcParams['font.family'] = 'AppleGothic'  # MacOS에서 AppleGothic

# 환경변수 로드
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

class CompanyInfo:
    def __init__(self, csv_file_path):
        self.csv_file_path = csv_file_path
        self.data = self._load_data()
    
    def _load_data(self):
        try:
            data = pd.read_csv(self.csv_file_path, encoding='utf-8-sig')
            return data
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return pd.DataFrame()

    def display_company_info(self, company_info):
        st.markdown(
            f'''
            <div style="display: flex; align-items: center;">
                <div style="margin-right: 32px; font-size: 48px; font-weight: normal; color: #333;">
                    <span>{company_info['기업명']}</span>
                </div>
                <div>
                    <img src="{company_info['이미지 경로']}" alt="Image" style="border-radius:10px; width:auto; height:50px;">
                </div>
            </div>
            ''', unsafe_allow_html=True
        )
        self._display_details(company_info)

    def _display_details(self, company_info):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("기업 정보")
            st.markdown(self._get_html(company_info), unsafe_allow_html=True)

        with col2:
            st.subheader("인재상")
            st.markdown(self._get_values_html(), unsafe_allow_html=True)
        
        st.subheader("최근 이슈")
        st.markdown(self._get_issue_html(), unsafe_allow_html=True)

    def _get_html(self, company_info):
        return f"""
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
            <p><strong>산업:</strong> {company_info['산업']}</p>
            <p><strong>주소:</strong> {company_info['주소']}</p>
            <p><strong>설립일:</strong> {company_info['설립일']}</p>
            <p><strong>주력 사업:</strong> {company_info['주력 사업']}</p>
            <p><strong>자본금:</strong> {company_info['자본금']}</p>
            <p><strong>매출액:</strong> {company_info['매출액']}</p>
            <p><strong>대표자:</strong> {company_info['대표자']}</p>
        </div>
        """

    def _get_values_html(self):
        return """
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
        <ul>
            <p><strong>고객 중심</strong>: 고객의 니즈를 최우선으로 생각하며, 항상 고객의 요구에 부응합니다.</p>
            <p><strong>도전과 변화</strong>: 익숙함에 머무르지 않고 계산된 도전을 통해 새로운 변화를 수용합니다.</p>
            <p><strong>소통과 협력</strong>: 주도적으로 소통하며 협력을 통해 더 나은 길을 찾습니다.</p>
            <p><strong>현장 중심</strong>: 문제를 현장에서 해결하며, 실행력을 갖춘 인재를 선호합니다.</p>
            <p><strong>책임감과 신뢰</strong>: 책임을 완수하여 사회적 신뢰를 얻고자 합니다.</p>
            <p><strong>미래 지향</strong>: 미래를 생각하며 지속 가능한 성장을 추구합니다.</p>
            <p><strong>전문성</strong>: 각 분야에서 전문성을 갖추어 대안을 제시합니다.</p>
            <p><strong>디지털 마인드</strong>: 디지털 역량과 혁신적 사고를 겸비합니다.</p>
        </ul>
        </div>
        """
    
    def _get_issue_html(self):
        return """
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                        <p> 1. "AI 코리아 펀드 위탁운용사로 최종 4개 운용사 선정"</p>
                        <p> 2. "혁신성장펀드 4개 운용사 통과"</p>
                        <p> 3. "상생금융 지원방안에 2조원 부담 예상"</p>
                        <p> 4. "4대 금융지주 '역대급' 실적 경신에도 어두운 표정"</p>
        </div>
        """

    def show(self):
        if self.data.empty:
            st.warning("데이터를 불러올 수 없습니다. JSON 파일을 확인해주세요.")
            return

        st.subheader("🏢 금융 공기업 정보")
        selected_company = None
        columns = st.columns(6)
        for index, company_name in enumerate(self.data["기업명"]):
            col = columns[index % 6]
            if col.button(company_name, key=company_name):
                selected_company = company_name

        if selected_company:
            company_info = self.data[self.data["기업명"] == selected_company].iloc[0]
            self.display_company_info(company_info)
        else:
            default_company_info = self.data.iloc[0]
            self.display_company_info(default_company_info)


class FinancialVisualization:
    def __init__(self, json_path, image_path):
        self.json_path = json_path
        self.image_path = image_path
        self.financial_data = self._load_financial_data()

    def _load_financial_data(self):
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return json_data.get('financial', {})
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return {}

    def display_graph(self, data, financial_option):
        fig, ax = plt.subplots()
        if financial_option in ["재무상태표", "연결재무상태표"]:
            ax.bar(data["항목"], data["금액 (백만원)"], color="skyblue")
            ax.set_xlabel("항목")
            ax.set_ylabel("금액 (백만원)")
            ax.set_title("자산 분포")
            plt.xticks(rotation=45)
        else:
            ax.pie(data["금액 (백만원)"], labels=data["항목"], autopct='%1.1f%%', startangle=90)
            ax.set_title("손익 분포")
        st.pyplot(fig)
    
    def display_image(self,financial_option):
        img_path = os.path.join(self.image_path, f'{financial_option}.jpg')
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, caption=financial_option)

    def show(self):
        st.divider()
        st.subheader("재무제표 시각화")
        financial_option = st.selectbox(
            "시각화할 항목을 선택하세요",
            list(self.financial_data.keys())
        )
        if financial_option:
            data = self.financial_data[financial_option]
            df = pd.DataFrame(data)

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(f"{financial_option} 이미지")
                self.display_image(financial_option)


            with col2:
                st.subheader(f"{financial_option} 데이터")
                st.table(df)
                st.subheader(f"{financial_option} 그래프")
                self.display_graph(data, financial_option)

class RecruitInfo:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = self._load_data()
        self.llm = ChatOpenAI(model="gpt-4o")
    def _load_data(self):
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return json_data.get('recruit', {})
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return {}
    def _analysis(self, info, column, title, bar=True):
        st.write(title)
        df = pd.DataFrame(self.data).set_index("년도")[column]
        if bar:
            st.bar_chart(df)
        else:
            st.line_chart(df)
        with st.popover(f"💡 {info} AI 분석"):
            if st.button(f"AI 답변 생성", key=info):
                with st.spinner(f"AI가 데이터를 분석 중입니다..."):
                    prompt = f"취업 준비생에게 도움이 될 수 있도록 {column} 데이터를 분석하고 주요 패턴과 인사이트를을 두 문장으로 요약하세요:\n" + df.to_string(index=False)
                    st.session_state[f"{column}_analysis"] = self.llm.predict(prompt)
                if f'{column}_analysis' in st.session_state:
                    st.write(st.session_state[f"{column}_analysis"])
        
    def show(self):
        st.divider()
        st.subheader("합격자 통계")
        col1, col2, col3 = st.columns(3)
        with col1:
            self._analysis("서류전형",["서류전형 응시인원", "서류전형 합격인원"], "서류전형 응시인원 및 합격인원",bar=True)
        with col2:
            self._analysis("필기전형",["필기전형 응시율", "필기전형 합격률"], "필기전형 응시율 및 합격률", bar=False)
        with col3:
            self._analysis("경쟁률",["서류전형 경쟁률", "서류/최종 경쟁률"], "경쟁률 비교", bar=False)
            
class SalaryInfo:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = self._load_data()
        self.llm = ChatOpenAI(model="gpt-4o")
    def _load_data(self):
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return json_data.get('salary', {})
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
            return {}
    def _analysis(self, column,bar=True):
        st.write(f"{column} 변화")
        df = pd.DataFrame(self.data).set_index("년도")[column]
        if bar:
            st.bar_chart(df)
        else:
            st.line_chart(df)
        with st.popover(f"💡 {column} AI 분석"):
            if st.button("AI 답변 생성", key=column):
                with st.spinner(f"AI가 {column} 데이터를 분석 중입니다..."):
                    prompt = f"취업 준비생에게 도움이 될 수 있도록 {column} 데이터를 분석하고 주요 패턴과 인사이트를을 두 문장으로 요약하세요:\n" + df.to_string(index=False)
                    st.session_state[f"{column}_analysis"] = self.llm.predict(prompt)
                if f'{column}_analysis' in st.session_state:
                    st.write(st.session_state[f"{column}_analysis"])
    
    def show(self):
        col1, col2, col3 = st.columns(3)
        # 기본급
        with col1:
            self._analysis("기본급")

        # 성과상여금
        with col2:
            self._analysis("성과상여금",bar=False)

        # 평균 근속연수
        with col3:
            self._analysis("평균근속연수",bar=False)

def show():
    base_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(base_dir, "./data/corpinfo.csv")
    json_file_path = os.path.join(base_dir, "./data/data.json")
    image_file_path = os.path.join(base_dir, "./image")

    app = CompanyInfo(csv_file_path)
    app.show()
    recruit_app = RecruitInfo(json_file_path)
    recruit_app.show()
    salary_app = SalaryInfo(json_file_path)
    salary_app.show()
    financial_app = FinancialVisualization(json_file_path,image_file_path)
    financial_app.show()

# Streamlit 실행
if __name__ == "__main__":
    show()
