from datetime import date, timedelta

import streamlit as st

from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_eden_login


st.set_page_config(
    page_title="Operations Calendar",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
projects = render_sidebar(
    show_command_center=False,
    show_project_manager=False
)

st.title("Operations Calendar")
st.caption(
    "See upcoming milestones, deliveries, inspections, and meetings across your projects."
)

calendar_items = projects.get_schedule_calendar_items()
today = date.today()

filter_columns = st.columns([2, 2, 2])

with filter_columns[0]:
    date_range = st.date_input(
        "Calendar range",
        value=(today, today + timedelta(days=30))
    )

with filter_columns[1]:
    project_options = sorted(
        {
            item["project_name"]
            for item in calendar_items
        }
    )
    selected_projects = st.multiselect(
        "Projects",
        project_options,
        default=project_options
    )

with filter_columns[2]:
    selected_statuses = st.multiselect(
        "Schedule status",
        projects.SCHEDULE_ITEM_STATUSES,
        default=["Upcoming", "In Progress", "Blocked"]
    )

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = date_range
    end_date = date_range

filtered_items = []

for item in calendar_items:
    try:
        item_date = date.fromisoformat(item["due_date"])
    except (TypeError, ValueError):
        continue

    if (
            start_date <= item_date <= end_date
            and item["project_name"] in selected_projects
            and item["status"] in selected_statuses
    ):
        filtered_items.append(item)

today_items = sum(
    item["due_date"] == today.isoformat()
    for item in filtered_items
)
next_seven_days = sum(
    today <= date.fromisoformat(item["due_date"])
    <= today + timedelta(days=7)
    for item in filtered_items
)
blocked_items = sum(
    item["status"] == "Blocked"
    for item in filtered_items
)

metric_columns = st.columns(3)
metric_columns[0].metric("Today", today_items)
metric_columns[1].metric("Next 7 Days", next_seven_days)
metric_columns[2].metric("Blocked", blocked_items)

st.subheader("Upcoming Work")

if not filtered_items:
    st.info(
        "No schedule items match the selected range and filters."
    )
    st.stop()

rows = []

for item in filtered_items:
    rows.append(
        {
            "Date": item["due_date"],
            "Project": item["project_name"],
            "Task": item["title"],
            "Type": item["item_type"],
            "Status": item["status"],
            "Notes": item["notes"]
        }
    )

st.dataframe(
    rows,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Manage individual tasks from the Project Schedule page."
)
