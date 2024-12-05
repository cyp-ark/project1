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
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialView": "dayGridMonth",
        }

        self.calendar_events = []

        # 캘린더 데이터 추가
        calendar_data = {
            "12월": {
                "1일": ["하나손해보험 서류"],
                "2일": ["기업은행 면접"],
                "3일": ["국민은행 최종 합격", "신한은행 2차 면접"],
                "4일": ["예금보험공사 인턴 서류", "우리자산운용 서류"],
                "5일": ["우체국금융개발원 서류", "우리자산운용 1차 면접"],
                "6일": ["농협은행 5급 공채", "신용보증재단중앙회 서류"],
                "7일": ["우리금융캐피탈 필기", "전산세무회계"],
                "8일": [],
                "9일": ["농협은행 2차 필기", "신용보증재단중앙회 2차 면접"],
                "10일": ["예금보험공사 인턴 면접", "신용보증재단중앙회 최종"],
                "11일": ["기업은행 통계 인턴 서류"],
                "12일": [],
                "13일": ["AFPK 시험"],
                "14일": ["경기신용보증재단 필기"],
                "15일": ["교보증권 인턴 서류"],
                "16일": ["예금보험공사 인턴", "신용보증재단중앙회 합격"],
                "17일": ["유통관리사 2급 시험"],
                "18일": ["우리은행 체험형 인턴 서류", "교보증권 인턴 실무 면접"],
                "19일": ["지역농협 통계 인턴 최종", "펀드투자자문사 인력"],
                "20일": ["수협중앙회 서류"],
                "21일": ["재경관리사", "AT자격 시험"],
                "22일": [],
                "23일": ["우리은행 체험형 인턴 면접"],
                "24일": ["우리자산운용 최종"],
                "25일": [],
                "26일": ["신협중앙회 서류"],
                "27일": ["재경관리사"],
                "28일": ["테셋"]
            }
        }

        # 데이터를 이벤트로 변환
        for day, events in calendar_data["12월"].items():
            if events:  # 이벤트가 있는 경우에만 추가
                date = f"2024-12-{int(day[:-1]):02d}"  # "1일" -> "2024-12-01"
                for event in events:
                    self.calendar_events.append(
                        {
                            "title": event,
                            "start": date,  # 시간 제외
                        }
                    )

    def render(self):
        st.title("캘린더 일정")
        calendar(events=self.calendar_events, options=self.calendar_options)


if __name__ == "__main__":
    app = CalendarApp()
    app.render()
