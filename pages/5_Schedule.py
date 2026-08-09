from datetime import date

import streamlit as st

from AuthGate import require_eden_login
from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar


def parse_date(value):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return date.today()


st.set_page_config(
    page_title="Project Schedule",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
projects = render_sidebar(
    show_command_center=False,
    show_project_manager=False
)

st.title("Project Schedule")
st.caption(
    "Organize the job by phase, then connect each phase to its tasks, "
    "planned labor, and equipment needs."
)

active_project = projects.get_active_project()

if active_project is None:
    st.info("Open a project from the Dashboard before creating its schedule.")
    st.page_link("Frontend.py", label="Open Dashboard", icon=":material/dashboard:")
    st.stop()

st.markdown(
    f"""
    <div class="eden-project-bar">
        <div>
            <div class="eden-project-label">Scheduling project</div>
            <div class="eden-project-name">{active_project['name']}</div>
        </div>
        <div class="eden-status-pill">
            {active_project.get('status', 'Active')}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader("Project Phases")
st.caption(
    "A phase is a piece of the job such as Foundation or Framing. Add only "
    "the phases you want this project to use."
)


def clear_project_phase_plan():
    """Clear phases while preserving tasks and equipment records."""
    if hasattr(projects, "clear_active_project_phases"):
        projects.clear_active_project_phases()
        return

    # Supports a running Streamlit process that still has the old
    # ProjectManager class in memory until the next full restart.
    reset_project = projects.get_active_project()
    reset_project["phases"] = []

    for task in reset_project.get("schedule_items", []):
        task["phase"] = "Unassigned"

    for equipment in reset_project.get("equipment", []):
        equipment["phase"] = "Unassigned"

    projects.save()


saved_phase_names = {
    phase.get("name", "").strip().casefold()
    for phase in projects.get_active_phases()
    if phase.get("name", "").strip()
}
starter_phase_names = {
    phase_name.casefold()
    for phase_name in projects.DEFAULT_PROJECT_PHASES
}

if saved_phase_names == starter_phase_names:
    st.warning(
        "This project still has Eden's old starter phase template. "
        "Remove it to start this project's schedule blank."
    )

    if st.button("Remove Starter Phases and Start Blank"):
        clear_project_phase_plan()
        st.rerun()

with st.expander("Reset Phase Plan"):
    st.warning(
        "This removes every project phase and unassigns existing schedule "
        "tasks and equipment. It does not delete the tasks or equipment."
    )
    confirm_clear_phases = st.checkbox(
        "I understand the project will have no phases afterward.",
        key="confirm_clear_project_phases"
    )

    if st.button(
            "Clear All Project Phases",
            disabled=not confirm_clear_phases
    ):
        clear_project_phase_plan()
        st.rerun()

existing_phase_names = {
    phase.get("name", "").strip().lower()
    for phase in projects.get_active_phases()
}
available_phase_choices = [
    phase_name
    for phase_name in projects.DEFAULT_PROJECT_PHASES
    if phase_name.lower() not in existing_phase_names
]
available_phase_choices.append("Custom Phase")

with st.expander("Add Project Phase", expanded=True):
    phase_choice = st.selectbox(
        "Choose a phase to add",
        available_phase_choices,
        help=(
            "Already-added standard phases are removed from this list. "
            "Choose Custom Phase to name your own."
        )
    )

    if "new_phase_trade_count" not in st.session_state:
        st.session_state.new_phase_trade_count = 1

    phase_role_count = st.session_state.new_phase_trade_count

    trade_controls = st.columns([1, 1, 4])

    with trade_controls[0]:
        if st.button("Add a Trade", key="add_phase_trade"):
            st.session_state.new_phase_trade_count = min(
                phase_role_count + 1,
                5
            )
            st.rerun()

    with trade_controls[1]:
        if phase_role_count > 1 and st.button(
                "Remove Trade",
                key="remove_phase_trade"
        ):
            st.session_state.new_phase_trade_count -= 1
            st.rerun()

    with trade_controls[2]:
        st.caption(
            "Add each trade working in this phase. Example: 3 concrete "
            "finishers and 1 laborer."
        )

    with st.form("add_phase_form", clear_on_submit=True):
        if phase_choice == "Custom Phase":
            phase_name = st.text_input(
                "Custom phase name",
                placeholder="Example: Permit Review"
            )
        else:
            phase_name = phase_choice
            st.caption(f"Adding phase: **{phase_name}**")
        phase_dates = st.columns(2)

        with phase_dates[0]:
            phase_start = st.date_input("Planned start", value=date.today())

        with phase_dates[1]:
            phase_end = st.date_input("Planned finish", value=date.today())

        st.markdown("**Phase crew plan**")
        st.caption(
            "Enter each role, crew size, and hours per person. Eden totals "
            "the labor hours for you."
        )
        phase_labor_allocations = []

        for number in range(1, phase_role_count + 1):
            role_columns = st.columns([2, 1, 1])

            with role_columns[0]:
                role_trade = st.text_input(
                    f"Trade {number}",
                    placeholder="Example: Concrete Finisher",
                    key=f"new_phase_trade_{number}"
                )

            with role_columns[1]:
                role_crew_size = st.number_input(
                    "Crew size",
                    min_value=1,
                    value=1,
                    step=1,
                    key=f"new_phase_crew_size_{number}"
                )

            with role_columns[2]:
                role_hours_per_person = st.number_input(
                    "Hours per person",
                    min_value=0.0,
                    step=1.0,
                    key=f"new_phase_hours_{number}"
                )

            if role_trade.strip() and role_hours_per_person > 0:
                phase_labor_allocations.append(
                    {
                        "trade": role_trade,
                        "member_count": role_crew_size,
                        "hours_per_person": role_hours_per_person
                    }
                )

        phase_equipment = st.text_input(
            "Planned equipment (optional)",
            placeholder="Example: Skid steer rental, plate compactor"
        )
        add_phase = st.form_submit_button("Add Phase")

    if add_phase:
        if projects.add_project_phase(
                {
                    "name": phase_name,
                    "start_date": phase_start.isoformat(),
                    "end_date": phase_end.isoformat(),
                    "labor_allocations": phase_labor_allocations,
                    "equipment_notes": phase_equipment
                }
        ):
            st.session_state.new_phase_trade_count = 1
            st.rerun()
        else:
            st.error(
                "That phase already exists. Select it below to manage it, "
                "or enter a different phase name."
            )

phases = projects.get_active_phases()
schedule_items = projects.get_active_schedule_items()
today = date.today().isoformat()

if not phases:
    st.info(
        "No phases have been added yet. Add a project phase before "
        "scheduling tasks."
    )

st.divider()
st.subheader("Schedule Tasks")
st.caption(
    "Add project phases first, then assign every new task to the phase "
    "where the work belongs."
)

phase_names = [phase.get("name", "") for phase in phases]
task_phase_options = ["Unassigned", *phase_names]
new_task_phase_options = phase_names or ["Add a project phase first"]

if not phase_names:
    st.info(
        "Add a custom phase before scheduling tasks."
    )

with st.expander("Add Schedule Task", expanded=True):
    with st.form("add_schedule_item_form", clear_on_submit=True):
        title = st.text_input(
            "Task, milestone, delivery, or inspection",
            placeholder="Example: Foundation inspection"
        )
        task_phase = st.selectbox(
            "Assign this task to a project phase",
            new_task_phase_options,
            disabled=not phase_names
        )
        task_dates = st.columns(2)

        with task_dates[0]:
            start_date = st.date_input("Planned start", value=date.today())

        with task_dates[1]:
            due_date = st.date_input("Planned finish", value=date.today())

        task_details = st.columns(3)

        with task_details[0]:
            item_type = st.selectbox(
                "Type",
                [
                    "Task",
                    "Milestone",
                    "Site Work",
                    "Material Delivery",
                    "Inspection",
                    "Client Meeting",
                    "Other"
                ]
            )

        with task_details[1]:
            item_status = st.selectbox(
                "Status",
                projects.SCHEDULE_ITEM_STATUSES
            )

        with task_details[2]:
            task_labor = st.number_input(
                "Planned labor hours",
                min_value=0.0,
                step=1.0
            )

        task_trade = st.text_input(
            "Primary labor trade (optional)",
            placeholder="Example: Carpenter"
        )
        task_equipment = st.text_input(
            "Equipment needed (optional)",
            placeholder="Example: Excavator and trench compactor"
        )
        notes = st.text_area(
            "Notes (optional)",
            placeholder="Example: Confirm inspection time with the city."
        )
        add_schedule_item = st.form_submit_button(
            "Add to Project Schedule",
            disabled=not phase_names
        )

    if add_schedule_item:
        if projects.add_schedule_item(
                {
                    "title": title,
                    "phase": task_phase,
                    "start_date": start_date.isoformat(),
                    "due_date": due_date.isoformat(),
                    "item_type": item_type,
                    "status": item_status,
                    "planned_labor_hours": task_labor,
                    "labor_trade": task_trade,
                    "equipment_notes": task_equipment,
                    "notes": notes
                }
        ):
            st.rerun()
        else:
            st.error("Enter a task name and planned finish date.")

st.divider()
st.subheader("Project Labor Costs")
st.caption(
    "Labor hours and trades come from your phases and tasks. Set each "
    "trade's loaded hourly cost here so Eden can price the bid."
)

scheduled_labor_plan = projects.get_active_scheduled_labor_plan()
scheduled_trade_hours = scheduled_labor_plan["trade_hours"]
bid_settings = projects.get_active_bid_settings()
saved_rates = {}

for saved_trade in bid_settings.get("labor_trades", []):
    normalized_trade = projects.normalize_labor_trade(
        saved_trade.get("trade", "")
    )
    saved_rate = float(saved_trade.get("hourly_rate", 0.0) or 0.0)

    if normalized_trade and (
            normalized_trade.casefold() not in saved_rates
            or saved_rate > 0
    ):
        saved_rates[normalized_trade.casefold()] = saved_rate

if scheduled_trade_hours:
    with st.form("project_labor_cost_rates_form"):
        updated_labor_trades = []

        for trade_name, labor_hours in scheduled_trade_hours.items():
            rate_column, hours_column = st.columns(2)

            with rate_column:
                hourly_rate = st.number_input(
                    f"{trade_name} loaded hourly cost ($)",
                    min_value=0.0,
                    value=saved_rates.get(trade_name.casefold(), 0.0),
                    step=1.0
                )

            with hours_column:
                st.metric("Scheduled hours", f"{labor_hours:,.1f}")

            updated_labor_trades.append(
                {
                    "trade": trade_name,
                    "labor_hours": labor_hours,
                    "hourly_rate": hourly_rate
                }
            )

        save_labor_costs = st.form_submit_button("Save Labor Costs")

    if save_labor_costs:
        projects.update_active_bid_settings(
            {
                "planned_labor_hours": scheduled_labor_plan["total_hours"],
                "crew_size": bid_settings.get("crew_size", 0),
                "labor_hours_by_trade": {},
                "labor_trades": updated_labor_trades,
                "overhead_percent": bid_settings["overhead_percent"],
                "profit_markup_percent": bid_settings[
                    "profit_markup_percent"
                ]
            }
        )
        st.success("Scheduled labor costs saved.")
        st.rerun()
else:
    st.info(
        "Add planned labor hours and a primary trade to a phase or task "
        "to set labor costs."
    )

st.divider()
st.subheader("Project Equipment")
st.caption(
    "Track the equipment needed for this job. Rental cost is a planning "
    "reference until Eden adds equipment cost into the bid automatically."
)

equipment_items = projects.get_active_equipment()

with st.expander("Add Equipment", expanded=False):
    with st.form("add_equipment_form", clear_on_submit=True):
        equipment_name = st.text_input(
            "Equipment name",
            placeholder="Example: Plate compactor"
        )
        equipment_source = st.text_input(
            "Source / rental supplier",
            value="Company owned",
            placeholder="Example: United Rentals"
        )
        equipment_phase = st.selectbox(
            "Project phase for equipment",
            task_phase_options,
            key="new_equipment_phase"
        )
        equipment_dates = st.columns(2)

        with equipment_dates[0]:
            equipment_start = st.date_input(
                "Equipment start",
                value=date.today(),
                key="new_equipment_start"
            )

        with equipment_dates[1]:
            equipment_end = st.date_input(
                "Equipment finish",
                value=date.today(),
                key="new_equipment_end"
            )

        equipment_details = st.columns(2)

        with equipment_details[0]:
            equipment_status = st.selectbox(
                "Equipment status",
                projects.EQUIPMENT_STATUSES
            )

        with equipment_details[1]:
            equipment_daily_cost = st.number_input(
                "Daily rental cost ($)",
                min_value=0.0,
                step=1.0
            )

        equipment_notes = st.text_area(
            "Equipment notes (optional)",
            placeholder="Example: Confirm delivery before base preparation."
        )
        add_equipment = st.form_submit_button("Add Equipment")

    if add_equipment:
        if projects.add_equipment(
                {
                    "name": equipment_name,
                    "source": equipment_source,
                    "phase": equipment_phase,
                    "start_date": equipment_start.isoformat(),
                    "end_date": equipment_end.isoformat(),
                    "status": equipment_status,
                    "daily_cost": equipment_daily_cost,
                    "notes": equipment_notes
                }
        ):
            st.rerun()
        else:
            st.error("Enter an equipment name.")

if equipment_items:
    st.dataframe(
        [
            {
                "Equipment": item.get("name", ""),
                "Phase": item.get("phase", "Unassigned"),
                "Source": item.get("source", "Company owned"),
                "Start": item.get("start_date", "") or "Not set",
                "Finish": item.get("end_date", "") or "Not set",
                "Status": item.get("status", "Planned"),
                "Daily Cost": f"${item.get('daily_cost', 0):,.2f}",
                "Notes": item.get("notes", "") or "—"
            }
            for item in equipment_items
        ],
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Manage Equipment"):
        equipment_choices = {
            (
                f"{item.get('phase', 'Unassigned')} · "
                f"{item.get('name', 'Untitled equipment')}"
            ): index
            for index, item in enumerate(equipment_items)
        }
        selected_equipment_label = st.selectbox(
            "Select equipment",
            list(equipment_choices.keys())
        )
        selected_equipment_index = equipment_choices[
            selected_equipment_label
        ]
        selected_equipment = equipment_items[selected_equipment_index]

        with st.form("manage_equipment_form"):
            updated_equipment_name = st.text_input(
                "Equipment name",
                value=selected_equipment.get("name", "")
            )
            updated_equipment_source = st.text_input(
                "Source / rental supplier",
                value=selected_equipment.get(
                    "source",
                    "Company owned"
                )
            )
            updated_equipment_phase = st.selectbox(
                "Project phase",
                task_phase_options,
                index=(
                    task_phase_options.index(
                        selected_equipment.get("phase", "Unassigned")
                    )
                    if selected_equipment.get("phase", "Unassigned")
                    in task_phase_options
                    else 0
                ),
                key="manage_equipment_phase"
            )
            updated_equipment_dates = st.columns(2)

            with updated_equipment_dates[0]:
                updated_equipment_start = st.date_input(
                    "Equipment start",
                    value=parse_date(selected_equipment.get("start_date")),
                    key="manage_equipment_start"
                )

            with updated_equipment_dates[1]:
                updated_equipment_end = st.date_input(
                    "Equipment finish",
                    value=parse_date(selected_equipment.get("end_date")),
                    key="manage_equipment_end"
                )

            updated_equipment_status = st.selectbox(
                "Equipment status",
                projects.EQUIPMENT_STATUSES,
                index=(
                    projects.EQUIPMENT_STATUSES.index(
                        selected_equipment.get("status", "Planned")
                    )
                    if selected_equipment.get("status", "Planned")
                    in projects.EQUIPMENT_STATUSES
                    else 0
                )
            )
            updated_equipment_daily_cost = st.number_input(
                "Daily rental cost ($)",
                min_value=0.0,
                value=float(selected_equipment.get("daily_cost", 0.0)),
                step=1.0
            )
            updated_equipment_notes = st.text_area(
                "Equipment notes",
                value=selected_equipment.get("notes", "")
            )
            save_equipment, delete_equipment = st.columns(2)

            with save_equipment:
                save_updated_equipment = st.form_submit_button(
                    "Save Equipment"
                )

            with delete_equipment:
                delete_selected_equipment = st.form_submit_button(
                    "Delete Equipment"
                )

        if save_updated_equipment:
            projects.update_equipment(
                selected_equipment_index,
                {
                    "name": updated_equipment_name,
                    "source": updated_equipment_source,
                    "phase": updated_equipment_phase,
                    "start_date": updated_equipment_start.isoformat(),
                    "end_date": updated_equipment_end.isoformat(),
                    "status": updated_equipment_status,
                    "daily_cost": updated_equipment_daily_cost,
                    "notes": updated_equipment_notes
                }
            )
            st.rerun()

        if delete_selected_equipment:
            projects.delete_equipment(selected_equipment_index)
            st.rerun()
else:
    st.info("No equipment has been added to this project yet.")

upcoming_count = sum(
    item.get("status") == "Upcoming"
    for item in schedule_items
)
in_progress_count = sum(
    item.get("status") == "In Progress"
    for item in schedule_items
)
complete_count = sum(
    item.get("status") == "Complete"
    for item in schedule_items
)
overdue_count = sum(
    item.get("due_date", "") < today
    and item.get("status") not in ["Complete"]
    for item in schedule_items
)

metric_columns = st.columns(4)
metric_columns[0].metric("Upcoming", upcoming_count)
metric_columns[1].metric("In Progress", in_progress_count)
metric_columns[2].metric("Completed", complete_count)
metric_columns[3].metric("Overdue", overdue_count)

display_phase_names = [*phase_names]

if any(
        item.get("phase", "Unassigned") == "Unassigned"
        for item in schedule_items
):
    display_phase_names.append("Unassigned")

if not schedule_items:
    st.info("No schedule tasks yet. Add a task above to start the job plan.")

for phase_name in display_phase_names:
    phase_tasks = [
        (index, item)
        for index, item in enumerate(schedule_items)
        if item.get("phase", "Unassigned") == phase_name
    ]

    phase = next(
        (
            item for item in phases
            if item.get("name") == phase_name
        ),
        None
    )
    phase_status = (
        phase.get("status", "Not Started")
        if phase is not None
        else "Needs assignment"
    )

    with st.expander(
            f"{phase_name} — {phase_status} ({len(phase_tasks)} task(s))",
            expanded=phase_status == "In Progress"
    ):
        if phase is not None:
            st.caption(
                f"{phase.get('start_date') or 'Start not set'} to "
                f"{phase.get('end_date') or 'Finish not set'} · "
                f"{phase.get('planned_labor_hours', 0)} planned labor hours"
            )
            if phase.get("labor_trade"):
                st.write(f"**Primary trade:** {phase['labor_trade']}")
            if phase.get("crew_notes"):
                st.write(f"**Crew / trades:** {phase['crew_notes']}")
            if phase.get("equipment_notes"):
                st.write(f"**Equipment plan:** {phase['equipment_notes']}")

        if phase_tasks:
            st.dataframe(
                [
                    {
                        "Start": item.get("start_date", item.get("due_date", "")),
                        "Finish": item.get("due_date", ""),
                        "Task": item.get("title", ""),
                        "Type": item.get("item_type", "Task"),
                        "Status": item.get("status", "Upcoming"),
                        "Labor Hours": item.get("planned_labor_hours", 0),
                        "Primary Trade": item.get("labor_trade", "") or "—",
                        "Equipment": item.get("equipment_notes", "") or "—",
                        "Notes": item.get("notes", "") or "—"
                    }
                    for _, item in sorted(
                        phase_tasks,
                        key=lambda indexed_item: indexed_item[1].get("start_date", "")
                    )
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No tasks assigned to this phase yet.")

if phases:
    with st.expander("Manage Project Phase"):
        phase_choices = {
            phase.get("name", "Untitled phase"): index
            for index, phase in enumerate(phases)
        }
        selected_phase_label = st.selectbox(
            "Select phase",
            list(phase_choices.keys())
        )
        selected_phase_index = phase_choices[selected_phase_label]
        selected_phase = phases[selected_phase_index]
        existing_allocations = selected_phase.get(
            "labor_allocations",
            []
        )

        if not existing_allocations and selected_phase.get("labor_trade"):
            existing_allocations = [
                {
                    "trade": selected_phase.get("labor_trade", ""),
                    "member_count": 1,
                    "hours_per_person": float(
                        selected_phase.get("planned_labor_hours", 0.0)
                    )
                }
            ]

        edit_role_count = st.selectbox(
            "Number of trade roles",
            [1, 2, 3, 4, 5],
            index=min(max(len(existing_allocations), 1), 5) - 1,
            key=f"edit_phase_role_count_{selected_phase_index}"
        )

        with st.form("manage_phase_form"):
            updated_phase_name = st.text_input(
                "Phase name",
                value=selected_phase.get("name", "")
            )
            updated_phase_dates = st.columns(2)

            with updated_phase_dates[0]:
                updated_phase_start = st.date_input(
                    "Planned start",
                    value=parse_date(selected_phase.get("start_date"))
                )

            with updated_phase_dates[1]:
                updated_phase_end = st.date_input(
                    "Planned finish",
                    value=parse_date(selected_phase.get("end_date"))
                )

            current_phase_status = selected_phase.get("status", "Not Started")
            updated_phase_status = st.selectbox(
                "Phase status",
                projects.PHASE_STATUSES,
                index=(
                    projects.PHASE_STATUSES.index(current_phase_status)
                    if current_phase_status in projects.PHASE_STATUSES
                    else 0
                )
            )
            st.markdown("**Phase crew plan**")
            updated_phase_allocations = []

            for number in range(1, edit_role_count + 1):
                current_role = (
                    existing_allocations[number - 1]
                    if number <= len(existing_allocations)
                    else {}
                )
                role_columns = st.columns([2, 1, 1])

                with role_columns[0]:
                    updated_role_trade = st.text_input(
                        f"Trade role {number}",
                        value=current_role.get("trade", ""),
                        key=(
                            f"edit_phase_trade_{selected_phase_index}_"
                            f"{number}"
                        )
                    )

                with role_columns[1]:
                    updated_role_crew_size = st.number_input(
                        "Crew size",
                        min_value=1,
                        value=int(current_role.get("member_count", 1) or 1),
                        step=1,
                        key=(
                            f"edit_phase_crew_size_{selected_phase_index}_"
                            f"{number}"
                        )
                    )

                with role_columns[2]:
                    updated_role_hours = st.number_input(
                        "Hours per person",
                        min_value=0.0,
                        value=float(
                            current_role.get("hours_per_person", 0.0) or 0.0
                        ),
                        step=1.0,
                        key=(
                            f"edit_phase_hours_{selected_phase_index}_"
                            f"{number}"
                        )
                    )

                if updated_role_trade.strip() and updated_role_hours > 0:
                    updated_phase_allocations.append(
                        {
                            "trade": updated_role_trade,
                            "member_count": updated_role_crew_size,
                            "hours_per_person": updated_role_hours
                        }
                    )

            updated_phase_crew = st.text_input(
                "Crew notes (optional)",
                value=selected_phase.get("crew_notes", "")
            )
            updated_phase_equipment = st.text_input(
                "Equipment plan",
                value=selected_phase.get("equipment_notes", "")
            )
            save_phase, delete_phase = st.columns(2)

            with save_phase:
                save_updated_phase = st.form_submit_button("Save Phase")

            with delete_phase:
                delete_selected_phase = st.form_submit_button("Delete Phase")

        if save_updated_phase:
            if projects.update_project_phase(
                    selected_phase_index,
                    {
                        "name": updated_phase_name,
                        "start_date": updated_phase_start.isoformat(),
                        "end_date": updated_phase_end.isoformat(),
                        "status": updated_phase_status,
                        "labor_allocations": updated_phase_allocations,
                        "crew_notes": updated_phase_crew,
                        "equipment_notes": updated_phase_equipment
                    }
            ):
                st.rerun()
            else:
                st.error("Enter a unique phase name.")

        if delete_selected_phase:
            projects.delete_project_phase(selected_phase_index)
            st.rerun()

if schedule_items:
    with st.expander("Manage Schedule Task"):
        task_choices = {
            (
                f"{item.get('phase', 'Unassigned')} · "
                f"{item.get('start_date', item.get('due_date', ''))} · "
                f"{item.get('title', 'Untitled task')}"
            ): index
            for index, item in enumerate(schedule_items)
        }
        selected_task_label = st.selectbox(
            "Select task",
            list(task_choices.keys())
        )
        selected_task_index = task_choices[selected_task_label]
        selected_task = schedule_items[selected_task_index]

        with st.form("manage_schedule_item_form"):
            updated_title = st.text_input(
                "Task, milestone, delivery, or inspection",
                value=selected_task.get("title", "")
            )
            updated_phase = st.selectbox(
                "Project phase",
                task_phase_options,
                index=(
                    task_phase_options.index(
                        selected_task.get("phase", "Unassigned")
                    )
                    if selected_task.get("phase", "Unassigned")
                    in task_phase_options
                    else 0
                )
            )
            updated_dates = st.columns(2)

            with updated_dates[0]:
                updated_start_date = st.date_input(
                    "Planned start",
                    value=parse_date(
                        selected_task.get(
                            "start_date",
                            selected_task.get("due_date")
                        )
                    )
                )

            with updated_dates[1]:
                updated_due_date = st.date_input(
                    "Planned finish",
                    value=parse_date(selected_task.get("due_date"))
                )

            updated_details = st.columns(3)
            type_options = [
                "Task",
                "Milestone",
                "Site Work",
                "Material Delivery",
                "Inspection",
                "Client Meeting",
                "Other"
            ]

            with updated_details[0]:
                current_type = selected_task.get("item_type", "Task")
                updated_type = st.selectbox(
                    "Type",
                    type_options,
                    index=(
                        type_options.index(current_type)
                        if current_type in type_options
                        else 0
                    )
                )

            with updated_details[1]:
                current_status = selected_task.get("status", "Upcoming")
                updated_status = st.selectbox(
                    "Status",
                    projects.SCHEDULE_ITEM_STATUSES,
                    index=(
                        projects.SCHEDULE_ITEM_STATUSES.index(current_status)
                        if current_status in projects.SCHEDULE_ITEM_STATUSES
                        else 0
                    )
                )

            with updated_details[2]:
                updated_labor = st.number_input(
                    "Planned labor hours",
                    min_value=0.0,
                    value=float(selected_task.get("planned_labor_hours", 0.0)),
                    step=1.0
                )

            updated_task_trade = st.text_input(
                "Primary labor trade",
                value=selected_task.get("labor_trade", "")
            )
            updated_equipment = st.text_input(
                "Equipment needed",
                value=selected_task.get("equipment_notes", "")
            )
            updated_notes = st.text_area(
                "Notes",
                value=selected_task.get("notes", "")
            )
            save_task, delete_task = st.columns(2)

            with save_task:
                save_updated_task = st.form_submit_button("Save Task")

            with delete_task:
                delete_selected_task = st.form_submit_button("Delete Task")

        if save_updated_task:
            projects.update_schedule_item(
                selected_task_index,
                {
                    "title": updated_title,
                    "phase": updated_phase,
                    "start_date": updated_start_date.isoformat(),
                    "due_date": updated_due_date.isoformat(),
                    "item_type": updated_type,
                    "status": updated_status,
                    "planned_labor_hours": updated_labor,
                    "labor_trade": updated_task_trade,
                    "equipment_notes": updated_equipment,
                    "notes": updated_notes
                }
            )
            st.rerun()

        if delete_selected_task:
            projects.delete_schedule_item(selected_task_index)
            st.rerun()
