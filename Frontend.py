import streamlit as st

from Concrete import ConcreteEstimator
from Lumber import LumberEstimator
from ProjectManager import ProjectManager
from UserProfile import (
    load_profile,
    save_profile,
    complete_onboarding
)
from pathlib import Path
from PDFReport import create_project_pdf


st.set_page_config(
    page_title="Eden",
    layout="wide"
)

projects = ProjectManager()
concrete = ConcreteEstimator()
lumber = LumberEstimator()


def save_estimate(estimate):
    projects.add_estimate(estimate)

    st.success(
        f"{estimate['type']} estimate saved to the active project."
    )

    st.dataframe(
        estimate["material_takeoff"],
        use_container_width=True,
        hide_index=True
    )


profile = load_profile()

if (
        not profile.get("name")
        and not st.session_state.get("eden_started")
):
    st.markdown(
        "<h1 style='text-align: center;'>EDEN</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h3 style='text-align: center;'>"
        "Construction made easier."
        "</h3>",
        unsafe_allow_html=True
    )

    st.write("")
    st.write("")

    left_space, start_column, right_space = st.columns([2, 2, 2])

    with start_column:
        if st.button(
                "Press to Start",
                use_container_width=True
        ):
            st.session_state["eden_started"] = True
            st.rerun()

    st.stop()

if not profile.get("name") or not profile.get("company"):
    st.title("Welcome to Eden")
    st.caption(
        "Set up your local profile to begin estimating."
    )

    with st.form("profile_setup_form"):
        name = st.text_input("Your first name")
        company = st.text_input("Company name")

        save_setup = st.form_submit_button(
            "Start Using Eden"
        )

    if save_setup:
        if name.strip() and company.strip():
            save_profile(
                name,
                company
            )

            st.rerun()

        else:
            st.error(
                "Please enter your name and company name."
            )

    st.stop()

avatar_relative_path = profile.get(
    "avatar_path",
    ""
)

avatar_path = (
    Path(__file__).parent /
    avatar_relative_path
)

avatar_column, welcome_column = st.columns(
    [1, 6]
)

with avatar_column:
    if avatar_relative_path and avatar_path.exists():
        st.image(
            str(avatar_path),
            width=90
        )

with welcome_column:
    st.title(
        f"Welcome back, {profile['name']}"
    )

    st.caption(
        f"{profile['company']} • Construction Material Estimating"
    )

if not profile.get("onboarding_complete"):
    st.info(
        "Welcome to Eden. Here is how to get started."
    )

    st.markdown("""
1. Create a project in the Projects sidebar.
2. Open the Chat page.
3. Ask Eden to estimate an item, such as `estimate a slab`.
4. Use `show project` to review your material takeoff.
""")

    if st.button("Got It — Start Estimating"):
        complete_onboarding()
        st.rerun()

    st.divider()

st.sidebar.header("Manage Projects")

with st.sidebar.form("create_project_form"):
    new_project_name = st.text_input("New project name")
    create_project = st.form_submit_button("Create Project")

if create_project:
    if projects.create_project(new_project_name):
        projects.select_project(new_project_name)
        st.rerun()
    else:
        st.sidebar.error("Enter a unique project name.")

project_list = projects.list_projects()
project_names = [project["name"] for project in project_list]

if project_names:
    selected_project = st.sidebar.selectbox(
        "Open project",
        project_names
    )

    if st.sidebar.button("Open Selected Project"):
        projects.select_project(selected_project)
        st.rerun()

    with st.sidebar.expander("Delete a Project"):
        st.warning(
            f'Deleting "{selected_project}" permanently removes its '
            "saved estimates and material takeoff."
        )

        confirm_project_delete = st.checkbox(
            "I understand this cannot be undone."
        )

        if st.button(
                "Delete Selected Project",
                disabled=not confirm_project_delete
        ):
            projects.delete_project(selected_project)
            st.rerun()

active_project = projects.get_active_project()

if active_project is None:
    st.info("Create or open a project to begin estimating.")
    st.stop()

st.success(f"Working on: {active_project['name']}")

project_details = projects.get_active_project_details()

with st.expander(
    "Customer and Project Details",
    expanded=not project_details["customer_name"]
):
    with st.form("project_details_form"):
        customer_name = st.text_input(
            "Customer name",
            value=project_details["customer_name"]
        )

        customer_email = st.text_input(
            "Customer email",
            value=project_details["customer_email"]
        )

        project_address = st.text_area(
            "Project address",
            value=project_details["project_address"]
        )

        proposal_title = st.text_input(
            "Proposal title",
            value=project_details["proposal_title"]
        )

        proposal_notes = st.text_area(
            "Customer report notes",
            value=project_details.get("proposal_notes", ""),
            placeholder=(
                "Example: Material quantities are based on approved plans. "
                "Pricing and labor are not included in this material report."
            )
        )

        save_details = st.form_submit_button(
            "Save Customer and Project Details"
        )

    if save_details:
        projects.update_active_project_details(
            {
                "customer_name": customer_name,
                "customer_email": customer_email,
                "project_address": project_address,
                "proposal_title": proposal_title,
                "proposal_notes": proposal_notes
            }
        )

        st.success("Customer and project details saved.")
        st.rerun()

estimate_type = st.selectbox(
    "Estimate type",
    [
        "Concrete Patio",
        "Concrete Slab",
        "Lumber Framed Wall"
    ]
)

if estimate_type in ["Concrete Patio", "Concrete Slab"]:
    st.subheader(f"{estimate_type} Estimate")

    st.caption(
        "Rebar is not included in this visual form. "
        "Structural reinforcement must come from approved plans."
    )

    with st.form("concrete_estimate_form"):
        left_column, right_column = st.columns(2)

        with left_column:
            length = st.number_input(
                "Length (ft)",
                min_value=0.1,
                value=20.0
            )

            width = st.number_input(
                "Width (ft)",
                min_value=0.1,
                value=20.0
            )

            thickness = st.number_input(
                "Thickness (in)",
                min_value=1.0,
                value=4.0
            )

        with right_column:
            wire_mesh = st.checkbox("Include wire mesh")
            vapor_barrier = st.checkbox("Include vapor barrier")
            gravel_base = st.checkbox("Include gravel base")
            control_joints = st.checkbox(
                "Include control joints"
            )
            forms = st.checkbox("Include forms")

        create_estimate = st.form_submit_button(
            f"Create {estimate_type} Estimate"
        )

    if create_estimate:
        estimate_options = {
            "length": length,
            "width": width,
            "thickness_inches": thickness,
            "wire_mesh": wire_mesh,
            "vapor_barrier": vapor_barrier,
            "gravel_base": gravel_base,
            "control_joints": control_joints,
            "forms": forms
        }

        if estimate_type == "Concrete Patio":
            estimate = concrete.concrete_patio(
                **estimate_options
            )
        else:
            estimate = concrete.concrete_slab(
                **estimate_options
            )

        save_estimate(estimate)

elif estimate_type == "Lumber Framed Wall":
    st.subheader("Lumber Framed Wall Estimate")

    st.caption(
        "Stud spacing must match the approved framing plan."
    )

    with st.form("framed_wall_form"):
        left_column, right_column = st.columns(2)

        with left_column:
            wall_length = st.number_input(
                "Wall length (ft)",
                min_value=0.1,
                value=20.0
            )

            wall_height = st.number_input(
                "Wall height (ft)",
                min_value=0.1,
                value=8.0
            )

        with right_column:
            stud_spacing = st.selectbox(
                "Stud spacing (inches OC)",
                [16, 24]
            )

        create_wall_estimate = st.form_submit_button(
            "Create Framed Wall Estimate"
        )

    if create_wall_estimate:
        estimate = lumber.frame_wall(
            length_feet=wall_length,
            height_feet=wall_height,
            stud_spacing_inches=stud_spacing
        )

        save_estimate(estimate)

st.divider()
st.subheader("Saved Estimates")

if active_project["estimates"]:
    estimate_rows = []

    for number, estimate in enumerate(
            active_project["estimates"],
            start=1
    ):
        estimate_rows.append(
            {
                "#": number,
                "Type": estimate.get("type", "Unknown"),
                "Primary Material": estimate.get(
                    "material",
                    "Not specified"
                ),
                "Takeoff Items": len(
                    estimate.get("material_takeoff", [])
                )
            }
        )

    st.dataframe(
        estimate_rows,
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Manage Saved Estimates"):
        estimate_choices = {}

        for number, estimate in enumerate(
                active_project["estimates"],
                start=1
        ):
            label = (
                f"#{number} - "
                f"{estimate.get('type', 'Unknown estimate')}"
            )
            estimate_choices[label] = number - 1

        selected_estimate = st.selectbox(
            "Estimate to remove",
            list(estimate_choices.keys())
        )

        confirm_delete = st.checkbox(
            "I understand this will remove the estimate and update "
            "the project material takeoff."
        )

        if st.button(
                "Delete Selected Estimate",
                disabled=not confirm_delete
        ):
            projects.delete_estimate(
                estimate_choices[selected_estimate]
            )
            st.rerun()

else:
    st.info("No estimates have been saved to this project yet.")

st.divider()
st.subheader("Project Material Takeoff")

material_takeoff = projects.get_active_material_takeoff()

if material_takeoff:
    st.dataframe(
        material_takeoff,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No material takeoff items have been saved yet.")

st.divider()
st.subheader("Customer PDF Report")

st.caption(
    "Create a customer-ready material estimate using the company "
    "and project details saved in Eden."
)

if st.button("Create Customer PDF"):
    pdf_path = create_project_pdf(
        active_project,
        profile,
        material_takeoff
    )

    st.session_state["customer_pdf_path"] = str(pdf_path)

if "customer_pdf_path" in st.session_state:
    saved_pdf_path = st.session_state["customer_pdf_path"]

    with open(saved_pdf_path, "rb") as pdf_file:
        st.download_button(
            "Download Customer PDF",
            data=pdf_file.read(),
            file_name=active_project["name"].replace(
                " ",
                "_"
            ) + "_material_report.pdf",
            mime="application/pdf"
        )