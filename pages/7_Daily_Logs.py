from datetime import date

import streamlit as st

from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_eden_login
from DailyLogPhotos import (
    get_daily_log_photo_path,
    save_daily_log_photos
)


st.set_page_config(
    page_title="Daily Logs",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
projects = render_sidebar(
    show_command_center=False
)

st.title("Daily Logs")
st.caption(
    "Create a reliable job record for work completed, site conditions, and tomorrow's plan."
)

active_project = projects.get_active_project()

if active_project is None:
    st.info("Open a project from the Dashboard before creating a daily log.")
    st.page_link(
        "Frontend.py",
        label="Open Dashboard",
        icon=":material/dashboard:"
    )
    st.stop()

st.markdown(
    f"""
    <div class="eden-project-bar">
        <div>
            <div class="eden-project-label">Daily log project</div>
            <div class="eden-project-name">{active_project['name']}</div>
        </div>
        <div class="eden-status-pill">
            {active_project.get('status', 'Active')}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.expander("Create Daily Log", expanded=True):
    with st.form("create_daily_log_form", clear_on_submit=True):
        log_date = st.date_input(
            "Log date",
            value=date.today()
        )

        crew_summary = st.text_input(
            "Crew and trades on site (optional)",
            placeholder="Example: 2 carpenters, 1 concrete finisher"
        )

        weather = st.text_input(
            "Site conditions or weather (optional)",
            placeholder="Example: Clear, 78°F, dry site"
        )

        work_completed = st.text_area(
            "Work completed",
            placeholder="Example: Framed east wall and installed window headers."
        )

        first_column, second_column = st.columns(2)

        with first_column:
            materials_delivered = st.text_area(
                "Materials delivered (optional)",
                placeholder="Example: 40 sheets 7/16 OSB delivered."
            )

            safety_notes = st.text_area(
                "Safety notes (optional)",
                placeholder="Example: Toolbox talk completed."
            )

        with second_column:
            issues_delays = st.text_area(
                "Issues or delays (optional)",
                placeholder="Example: Inspection moved to tomorrow."
            )

        tomorrow_plan = st.text_area(
            "Tomorrow's plan (optional)",
            placeholder="Example: Complete exterior wall sheathing."
        )

        uploaded_photos = st.file_uploader(
            "Field photos (optional)",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
            help=(
                "Photos are stored on this Eden machine for now. Cloud "
                "photo sync will be added with Supabase Storage."
            )
        )

        save_daily_log = st.form_submit_button("Save Daily Log")

    if save_daily_log:
        saved_photos = save_daily_log_photos(
            active_project["name"],
            uploaded_photos
        )

        if projects.add_daily_log(
                {
                    "date": log_date.isoformat(),
                    "crew_summary": crew_summary,
                    "weather": weather,
                    "work_completed": work_completed,
                    "materials_delivered": materials_delivered,
                    "issues_delays": issues_delays,
                    "safety_notes": safety_notes,
                    "tomorrow_plan": tomorrow_plan,
                    "photos": saved_photos
                }
        ):
            st.success("Daily log saved.")
            st.rerun()

        else:
            st.error("Add the work completed before saving the daily log.")

daily_logs = projects.get_active_daily_logs()

st.subheader("Project Log History")

if not daily_logs:
    st.info("No daily logs have been saved for this project yet.")
    st.stop()

for log_index, daily_log in reversed(list(enumerate(daily_logs))):
    title = (
        f"{daily_log.get('date', 'Undated')} — "
        f"{daily_log.get('work_completed', 'Daily log')[:72]}"
    )

    with st.expander(title):
        summary_columns = st.columns(2)

        with summary_columns[0]:
            st.caption("Crew and trades")
            st.write(daily_log.get("crew_summary") or "Not recorded")

        with summary_columns[1]:
            st.caption("Site conditions")
            st.write(daily_log.get("weather") or "Not recorded")

        st.caption("Work completed")
        st.write(daily_log.get("work_completed", ""))

        detail_columns = st.columns(2)

        with detail_columns[0]:
            st.caption("Materials delivered")
            st.write(daily_log.get("materials_delivered") or "None recorded")
            st.caption("Safety notes")
            st.write(daily_log.get("safety_notes") or "None recorded")

        with detail_columns[1]:
            st.caption("Issues or delays")
            st.write(daily_log.get("issues_delays") or "None recorded")
            st.caption("Tomorrow's plan")
            st.write(daily_log.get("tomorrow_plan") or "None recorded")

        photo_paths = [
            path
            for path in (
                get_daily_log_photo_path(photo)
                for photo in daily_log.get("photos", [])
            )
            if path is not None
        ]

        if photo_paths:
            st.caption("Field photos")
            st.image(
                [str(path) for path in photo_paths],
                caption=[path.name for path in photo_paths],
                use_container_width=True
            )

        if st.button(
                "Delete This Daily Log",
                key=f"delete_daily_log_{log_index}"
        ):
            projects.delete_daily_log(log_index)
            st.rerun()

log_choices = {
    (
        f"{daily_log.get('date', '')} — "
        f"{daily_log.get('work_completed', 'Daily log')[:55]}"
    ): index
    for index, daily_log in enumerate(daily_logs)
}

with st.expander("Edit Daily Log"):
    selected_label = st.selectbox(
        "Select daily log",
        list(log_choices.keys())
    )
    selected_index = log_choices[selected_label]
    selected_log = daily_logs[selected_index]

    try:
        selected_date = date.fromisoformat(
            selected_log.get("date", date.today().isoformat())
        )
    except ValueError:
        selected_date = date.today()

    with st.form("edit_daily_log_form"):
        edited_date = st.date_input(
            "Log date",
            value=selected_date
        )
        edited_crew = st.text_input(
            "Crew and trades on site",
            value=selected_log.get("crew_summary", "")
        )
        edited_weather = st.text_input(
            "Site conditions or weather",
            value=selected_log.get("weather", "")
        )
        edited_work = st.text_area(
            "Work completed",
            value=selected_log.get("work_completed", "")
        )
        edited_materials = st.text_area(
            "Materials delivered",
            value=selected_log.get("materials_delivered", "")
        )
        edited_issues = st.text_area(
            "Issues or delays",
            value=selected_log.get("issues_delays", "")
        )
        edited_safety = st.text_area(
            "Safety notes",
            value=selected_log.get("safety_notes", "")
        )
        edited_tomorrow = st.text_area(
            "Tomorrow's plan",
            value=selected_log.get("tomorrow_plan", "")
        )
        save_edited_log = st.form_submit_button("Save Changes")

    if save_edited_log:
        if projects.update_daily_log(
                selected_index,
                {
                    "date": edited_date.isoformat(),
                    "crew_summary": edited_crew,
                    "weather": edited_weather,
                    "work_completed": edited_work,
                    "materials_delivered": edited_materials,
                    "issues_delays": edited_issues,
                    "safety_notes": edited_safety,
                    "tomorrow_plan": edited_tomorrow
                }
        ):
            st.rerun()

        else:
            st.error("Work completed is required for a daily log.")
