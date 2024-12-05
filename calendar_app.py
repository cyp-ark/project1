from streamlit_calendar import calendar

class CalendarApp:
    def __init__(self):
        self.calendar_options = {
            "editable": "true",
            "selectable": "true",
            "headerToolbar": {
                "left": "today prev,next",
                "center": "title",
                "right": "dayGridMonth,listMonth",
            },
            "slotMinTime": "06:00:00",
            "slotMaxTime": "18:00:00",
            "initialView": "dayGridMonth",
            "resourceGroupField": "building",
            "resources": [
                {"id": "a", "building": "Building A", "title": "Building A"},
                {"id": "b", "building": "Building A", "title": "Building B"},
                {"id": "c", "building": "Building B", "title": "Building C"},
                {"id": "d", "building": "Building B", "title": "Building D"},
                {"id": "e", "building": "Building C", "title": "Building E"},
                {"id": "f", "building": "Building C", "title": "Building F"},
            ],
        }

        self.calendar_events = [
            {
                "title": "Event 1",
                "start": "2024-12-01T08:30:00",
                "resourceId": "a",
            },
            {
                "title": "Event 2",
                "start": "2024-12-05T07:30:00",
                "resourceId": "b",
            },
            {
                "title": "Event 3",
                "start": "2023-07-31T10:40:00",
                "end": "2023-07-31T12:30:00",
                "resourceId": "a",
            }
        ]

        self.custom_css = """
            .fc-event-past {
                opacity: 0.8;
            }
            .fc-event-time {
                font-style: italic;
            }
            .fc-event-title {
                font-weight: 700;
            }
            .fc-toolbar-title {
                font-size: 2rem;
            }
        """

    def render(self):
        return calendar(
            events=self.calendar_events,
            options=self.calendar_options,
            custom_css=self.custom_css
        )
