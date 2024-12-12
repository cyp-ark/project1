import streamlit as st
from streamlit_calendar import calendar

class CalendarApp:
    def __init__(self):
        self.calendar_options = {
            "editable": True,
            "selectable": True,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth,listMonth",
            },
            "initialView": "dayGridMonth",
        }

        self.calendar_events = []

        # 색상 설정
        self.color_map = {
            "발표": "#FF6F61",         # 부드러운 주황색
            "서류 시작": "#4FC3F7",    # 밝은 하늘색
            "서류 마감": "#81C784",    # 연한 초록색
            "시험일": "#BA68C8",        # 연한 보라색
            "발표일": "#9575CD",       # 은은한 보라색
            "면접": "#FFA726",         # 오렌지색
            "시험 접수": "#B0BEC5"     # 차분한 회색
        }

        # 캘린더 데이터
        calendar_data:{df_loaded = pd.read_csv("C:/data/december_schedule.csv", encoding="utf-8") }
        

        # 이벤트로 변환
        for day, events in calendar_data["12월"].items():
            if events:  # 이벤트가 있는 경우에만 추가
                date = f"2024-12-{int(day[:-1]):02d}"  # "1일" -> "2024-12-01"
                for event in events:
                    category = self.get_event_category(event)
                    self.calendar_events.append(
                        {
                            "title": event,
                            "start": date,
                            "color": self.color_map[category],
                            "category": category
                        }
                    )

    def get_event_category(self, event):
        """이벤트 제목에 따라 카테고리를 반환"""
        if "발표" in event and "면접" not in event and "서류" not in event:
            return "발표일"
        elif "면접" in event:
            return "면접"
        elif "발표" in event:
            return "발표"
        elif "서류 시작" in event:
            return "서류 시작"
        elif "서류 마감" in event:
            return "서류 마감"
        elif "시험" in event:
            return "시험일"
        else:
            return "시험 접수"

    def render(self):
        st.subheader("📅 금융권 채용 & 자격증 캘린더")

        # 셀렉트 박스 카테고리 선택
        categories = [
            "전체 보기", "발표", "면접", "서류 시작", "서류 마감",
            "시험일", "발표일", "시험 접수"
        ]
        selected_category = st.selectbox("카테고리 선택", categories)

        # 필터링된 이벤트
        if selected_category == "전체 보기":
            filtered_events = self.calendar_events  # 모든 이벤트 표시
        else:
            filtered_events = [
                event for event in self.calendar_events
                if event["category"] == selected_category
            ]

        # 캘린더 출력
        calendar(events=filtered_events, options=self.calendar_options)


if __name__ == "__main__":
    app = CalendarApp()
    app.render()
