from pathlib import Path

import streamlit as st

from CloudWorkspace import auto_backup_if_needed
from EdenAuth import current_user, sign_out
from ProjectManager import ProjectManager


def render_sidebar(
        show_command_center=True,
        show_project_manager=True
):
    projects = ProjectManager()

    if st.session_state.get("eden_splash_active"):
        return projects

    signed_in_user = current_user()

    if not signed_in_user:
        return projects

    try:
        cloud_status = auto_backup_if_needed()
    except Exception:
        cloud_status = "unavailable"

    st.sidebar.markdown(
        """
        <p class="eden-sidebar-kicker">Construction intelligence</p>
        <p class="eden-sidebar-title">EDEN</p>
        """,
        unsafe_allow_html=True
    )

    if cloud_status == "synced":
        st.sidebar.caption("Cloud: synced")
    elif cloud_status == "current":
        st.sidebar.caption("Cloud: up to date")
    elif cloud_status == "unavailable":
        st.sidebar.caption("Cloud: reconnect in Account & Cloud")

    if show_command_center:
        st.sidebar.caption("ESTIMATING COMMAND CENTER")

    if show_project_manager:
        st.sidebar.header("Manage Projects")

        with st.sidebar.form("create_project_form"):
            new_project_name = st.text_input(
                "New project name"
            )
            create_project = st.form_submit_button(
                "Create Project"
            )

        if create_project:
            if projects.create_project(new_project_name):
                projects.select_project(new_project_name)
                st.rerun()
            else:
                st.sidebar.error(
                    "Enter a unique project name."
                )

        project_status_filter = st.sidebar.selectbox(
            "Show projects",
            ["Active", "Completed", "On Hold", "Lost", "Archived", "All"]
        )

        project_list = projects.list_projects()

        if project_status_filter != "All":
            project_list = [
                project
                for project in project_list
                if project["status"] == project_status_filter
            ]

        project_names = [
            project["name"]
            for project in project_list
        ]

        if project_names:
            active_project = projects.get_active_project()
            active_project_name = (
                active_project["name"]
                if active_project is not None
                else None
            )

            project_switcher_key = "eden_project_switcher"

            if st.session_state.get(project_switcher_key) not in project_names:
                st.session_state[project_switcher_key] = (
                    active_project_name
                    if active_project_name in project_names
                    else project_names[0]
                )

            def switch_active_project():
                projects.select_project(
                    st.session_state[project_switcher_key]
                )

            selected_project = st.sidebar.selectbox(
                "Active project",
                project_names,
                key=project_switcher_key,
                help=(
                    "Choose a project to make it active everywhere in Eden."
                ),
                on_change=switch_active_project
            )

            st.session_state["eden_active_project_name"] = (
                selected_project
            )
            st.sidebar.caption(f"Working in: {selected_project}")

            with st.sidebar.expander("Delete a Project"):
                st.warning(
                    f'"{selected_project}" will move to Recently Deleted. '
                    "You can restore it for 30 days."
                )

                confirm_project_delete = st.checkbox(
                    "I understand this removes the project from my active list."
                )

                if st.button(
                        "Move Selected Project to Recently Deleted",
                        disabled=not confirm_project_delete
                ):
                    projects.delete_project(selected_project)
                    st.rerun()

        deleted_projects = projects.list_deleted_projects()

        if deleted_projects:
            with st.sidebar.expander("Recently Deleted Projects"):
                st.caption(
                    "Projects remain recoverable for 30 days."
                )

                for deleted_project in deleted_projects:
                    project_id = deleted_project["id"]
                    st.write(f"**{deleted_project['name']}**")
                    st.caption(
                        f"{deleted_project['estimate_count']} estimates · "
                        f"Restore by {deleted_project['expires_on']}"
                    )

                    restore_column, remove_column = st.columns(2)

                    with restore_column:
                        if st.button(
                                "Restore",
                                key=f"restore_project_{project_id}"
                        ):
                            if projects.restore_deleted_project(project_id):
                                st.rerun()
                            else:
                                st.error(
                                "A project with that name already exists. "
                                "Rename or remove it before restoring."
                                )

                    with remove_column:
                        if st.button(
                                "Delete Forever",
                                key=f"permanent_delete_project_{project_id}"
                        ):
                            projects.permanently_delete_project(project_id)
                            st.rerun()

        else:
            st.sidebar.info(
                f"No {project_status_filter.lower()} projects found."
            )

        active_project = projects.get_active_project()

        if active_project is not None:
            current_status = active_project.get("status", "Active")

            with st.sidebar.expander("Project Status"):
                st.caption(f"Active project: {active_project['name']}")

                updated_status = st.selectbox(
                    "Status",
                    projects.PROJECT_STATUSES,
                    index=projects.PROJECT_STATUSES.index(current_status)
                )

                if st.button("Save Project Status"):
                    projects.update_active_project_status(updated_status)
                    st.rerun()

    st.sidebar.divider()
    st.sidebar.subheader("Workspace")

    st.sidebar.link_button(
        "Dashboard",
        url="/",
        icon=":material/dashboard:",
        use_container_width=True
    )

    st.sidebar.page_link(
        "pages/Chat.py",
        label="Chat with Eden",
        icon=":material/chat:"
    )

    st.sidebar.page_link(
        "pages/5_Schedule.py",
        label="Project Schedule",
        icon=":material/calendar_month:"
    )

    st.sidebar.page_link(
        "pages/6_Calendar.py",
        label="Operations Calendar",
        icon=":material/calendar_today:"
    )

    st.sidebar.page_link(
        "pages/7_Daily_Logs.py",
        label="Daily Logs",
        icon=":material/edit_note:"
    )

    st.sidebar.page_link(
        "pages/2_Account.py",
        label="Account & Cloud",
        icon=":material/cloud:"
    )

    st.sidebar.page_link(
        "pages/Help.py",
        label="Help",
        icon=":material/help:"
    )

    st.sidebar.page_link(
        "pages/3_Settings.py",
        label="Settings",
        icon=":material/settings:"
    )

    st.sidebar.page_link(
        "pages/4_Support.py",
        label="Support",
        icon=":material/support_agent:"
    )

    st.sidebar.divider()
    st.sidebar.caption(
        f"Signed in as {signed_in_user.get('email', 'Eden user')}"
    )

    logo_path = (
        Path(__file__).with_name("assets") /
        "eden_logo.png"
    )

    if logo_path.exists():
        st.sidebar.image(
            str(logo_path),
            use_container_width=True
        )

    st.sidebar.button(
        "Sign Out",
        icon=":material/logout:",
        use_container_width=True,
        key="eden_sign_out_button",
        on_click=sign_out
    )

    return projects
