import streamlit as st
import openai
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import platform
from matplotlib import rc

# 한글 폰트 설정
if platform.system() == "Windows":
    rc('font', family='Malgun Gothic')  # Windows
elif platform.system() == "Darwin":
    rc('font', family='AppleGothic')  # macOS
else:
    rc('font', family='NanumGothic')  # Linux (NanumGothic 필요)
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# OpenAI API 키 설정
openai.api_key = "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"

def generate_tows_analysis(company_name):
    """OpenAI API를 사용하여 TOWS 분석 생성"""
    prompt = f"""
    다음 회사에 대한 TOWS 분석을 작성해주세요.
    회사명: {company_name}

    아래 형식으로 작성해주세요:
    위협 (Threats):
    - 항목 1
    - 항목 2

    기회 (Opportunities):
    - 항목 1
    - 항목 2

    약점 (Weaknesses):
    - 항목 1
    - 항목 2

    강점 (Strengths):
    - 항목 1
    - 항목 2
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 한국어로 TOWS 분석을 제공하는 유용한 어시스턴트입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"에러 발생: {str(e)}"

def parse_tows_analysis(analysis_text):
    """TOWS 분석 텍스트를 딕셔너리로 변환"""
    lines = analysis_text.split("\n")
    tows_dict = {"Threat (위협)": [], "Opportunity (기회)": [], "Weakness (약점)": [], "Strength (강점)": []}
    current_category = None

    for line in lines:
        if line.startswith("위협"):
            current_category = "Threat (위협)"
        elif line.startswith("기회"):
            current_category = "Opportunity (기회)"
        elif line.startswith("약점"):
            current_category = "Weakness (약점)"
        elif line.startswith("강점"):
            current_category = "Strength (강점)"
        elif line.startswith("-") and current_category:
            tows_dict[current_category].append(line.strip("- ").strip())
    return tows_dict

def plot_tows_with_labels(data):
    """TOWS 분석 결과를 원형으로 시각화"""
    fig, ax = plt.subplots(figsize=(10, 8))

    # Wedge로 원형 구역 생성
    colors = ['#A1D0FF', '#FFE699', '#A0EACF', '#FFB6C1']
    categories = list(data.keys())
    wedges = [
        Wedge((0, 0), 1, 0, 90, facecolor=colors[0], label=categories[0]),
        Wedge((0, 0), 1, 90, 180, facecolor=colors[1], label=categories[1]),
        Wedge((0, 0), 1, 180, 270, facecolor=colors[2], label=categories[2]),
        Wedge((0, 0), 1, 270, 360, facecolor=colors[3], label=categories[3]),
    ]

    for wedge in wedges:
        ax.add_patch(wedge)

    # 텍스트 추가
    ax.text(-0.7, 0.7, "Threat\n(위협)\n" + "\n".join(data[categories[0]]), ha='center', fontsize=10, color='blue')
    ax.text(0.7, 0.7, "Opportunity\n(기회)\n" + "\n".join(data[categories[1]]), ha='center', fontsize=10, color='orange')
    ax.text(0.7, -0.7, "Weakness\n(약점)\n" + "\n".join(data[categories[2]]), ha='center', fontsize=10, color='green')
    ax.text(-0.7, -0.7, "Strength\n(강점)\n" + "\n".join(data[categories[3]]), ha='center', fontsize=10, color='red')
    ax.text(0, 0, "TOWS", ha='center', va='center', fontsize=16, fontweight='bold')

    # 시각화 조정
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    st.pyplot(fig)

# Streamlit 앱
st.title("KDB산업은행 TOWS 분석 시각화")
st.write("OpenAI의 GPT를 사용하여 TOWS 분석을 생성하고 시각화합니다.")

# 사용자 입력
company_name = "KDB산업은행"
st.write(f"분석 대상: {company_name}")

# TOWS 분석 생성
analysis = generate_tows_analysis(company_name)
if "에러 발생" not in analysis:
    # 분석 결과 출력
    st.subheader("TOWS 분석 결과")
    st.text(analysis)

    # 분석 결과 시각화
    tows_dict = parse_tows_analysis(analysis)
    st.subheader("TOWS 분석 시각화")
    plot_tows_with_labels(tows_dict)
else:
    st.error(analysis)