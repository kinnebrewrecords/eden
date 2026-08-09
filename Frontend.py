from datetime import date
from base64 import b64encode
import csv
import time
from io import StringIO
from html import escape

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
from PDFReport import (
    create_project_pdf,
    create_customer_proposal_pdf,
    create_change_order_pdf
)
from Sidebar import render_sidebar
from EdenTheme import apply_eden_theme
from PricingCatalog import PricingCatalog
from AuthGate import require_eden_login
from EdenAuth import current_user


st.set_page_config(
    page_title="Eden",
    layout="wide"
)

if (
        not current_user()
        and not st.session_state.get("eden_splash_seen")
):
    st.session_state["eden_splash_active"] = True

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


def create_material_takeoff_csv(project_name, material_takeoff):
    """Create a supplier-ready CSV that can be opened directly in Excel."""
    output = StringIO()
    fieldnames = [
        "Project",
        "Item",
        "Unit",
        "Quantity",
        "Category",
        "Notes"
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for item in material_takeoff:
        writer.writerow(
            {
                "Project": project_name,
                "Item": item.get("item", ""),
                "Unit": item.get("unit", ""),
                "Quantity": item.get("quantity", ""),
                "Category": item.get("category", "Material"),
                "Notes": item.get("notes", "")
            }
        )

    return output.getvalue().encode("utf-8-sig")


st.set_page_config(
    page_title="Eden",
    layout="wide"
)

apply_eden_theme()

if st.session_state.get("eden_splash_active"):
    splash_logo_path = (
        Path(__file__).with_name("assets") /
        "eden_logo.png"
    )

    if splash_logo_path.exists():
        splash_logo_data = b64encode(
            splash_logo_path.read_bytes()
        ).decode("ascii")
        splash_logo_markup = (
            '<img class="eden-splash-logo" '
            f'src="data:image/png;base64,{splash_logo_data}" '
            'alt="Eden">'
        )
    else:
        splash_logo_markup = "<h1>EDEN</h1>"

    st.markdown(
        f"""
        <section class="eden-splash">
            {splash_logo_markup}
            <p class="eden-splash-tagline">CONSTRUCTION MADE EASIER</p>
        </section>
        """,
        unsafe_allow_html=True
    )
    time.sleep(1.2)
    st.session_state["eden_splash_seen"] = True
    st.session_state["eden_splash_active"] = False
    st.rerun()

require_eden_login()

concrete = ConcreteEstimator()
lumber = LumberEstimator()
pricing = PricingCatalog()
pricing.add_starter_regions()

projects = render_sidebar()

profile = load_profile()


if (
        not profile.get("name")
        and not st.session_state.get("eden_started")
):
            st.session_state["eden_started"] = True
            st.rerun()

            st.stop()

if not profile.get("name") or not profile.get("company"):
    st.title("Welcome to Eden")
    st.caption(
        "Set up your company defaults to begin estimating."
    )

    with st.form("profile_setup_form"):
        name = st.text_input("Your first name")
        company = st.text_input("Company name")
        setup_regions = pricing.list_regions()
        default_region = st.selectbox(
            "Your primary estimating region",
            setup_regions,
            help="Required. You can change this later in Settings."
        )
        preferred_supplier = st.text_input(
            "Primary supplier (optional)",
            placeholder="Example: ABC Ready Mix or Home Depot"
        )
        price_setup_choice = st.radio(
            "Would you like to enter supplier prices now?",
            ["Later", "Now"],
            horizontal=True
        )

        save_setup = st.form_submit_button(
            "Start Using Eden"
        )

    if save_setup:
        if name.strip() and company.strip() and default_region:
            save_profile(
                name,
                company,
                default_region=default_region,
                preferred_supplier=preferred_supplier
            )

            if preferred_supplier.strip():
                pricing.add_supplier(preferred_supplier)

            if price_setup_choice == "Now":
                st.session_state["eden_open_pricing_setup"] = True
                st.switch_page("pages/3_Settings.py")

            st.rerun()

        else:
            st.error(
                "Please enter your name, company name, and region."
            )

    st.stop()

st.markdown(
    f"""
    <section class="eden-welcome-bubble">
        <p class="eden-welcome-kicker">{
            "Let's build your workspace" if not profile.get("onboarding_complete")
            else "Your Eden workspace"
        }</p>
        <h1 class="eden-welcome-title">{
            "Welcome to Eden" if not profile.get("onboarding_complete")
            else "Welcome back"
        }, {escape(profile['name'])}</h1>
        <p class="eden-welcome-company">
            {escape(profile['company'])} &bull; Construction Material Estimating
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

_ = (
        f"{profile['company']} • Construction Material Estimating"
    )

if not profile.get("onboarding_complete"):
    st.markdown(
        """
        <section class="eden-tour">
            <p class="eden-tour-kicker">FIRST PROJECT GUIDE</p>
            <h2>Start with a project. Eden will guide the rest.</h2>
            <p>Follow these steps once, then estimate, schedule, price, and
            prepare a customer-ready proposal from one workspace.</p>
        </section>
        """,
        unsafe_allow_html=True
    )

    tour_project, tour_chat, tour_schedule, tour_review = st.columns(4)

    with tour_project:
        st.markdown(
            """
            <div class="eden-tour-card eden-tour-card-start">
                <span class="eden-tour-number">1</span>
                <h3>Create a project</h3>
                <p>Use <strong>Manage Projects</strong> in the sidebar.
                <span class="eden-tour-arrow">&larr;</span></p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tour_chat:
        st.markdown(
            """
            <div class="eden-tour-card">
                <span class="eden-tour-number">2</span>
                <h3>Create an estimate</h3>
                <p>Describe the work in plain language and Eden asks for
                the missing details.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.page_link(
            "pages/Chat.py",
            label="Open Chat with Eden",
            icon=":material/chat:"
        )

    with tour_schedule:
        st.markdown(
            """
            <div class="eden-tour-card">
                <span class="eden-tour-number">3</span>
                <h3>Plan the work</h3>
                <p>Add phases, tasks, crew assignments, equipment, and
                planned labor hours.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.page_link(
            "pages/5_Schedule.py",
            label="Open Project Schedule",
            icon=":material/calendar_month:"
        )

    with tour_review:
        st.markdown(
            """
            <div class="eden-tour-card">
                <span class="eden-tour-number">4</span>
                <h3>Review your bid</h3>
                <p>Return here for material costs, labor, markup, and
                customer PDFs.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("Got It — Start Estimating"):
        complete_onboarding()
        st.rerun()

    st.divider()

active_project = projects.get_active_project()

if active_project is None:
    st.info("Create or open a project to begin estimating.")
    st.stop()

st.markdown(
    f"""
    <div class="eden-project-bar">
        <div>
            <div class="eden-project-label">Active project</div>
            <div class="eden-project-name">{escape(active_project['name'])}</div>
        </div>
        <div class="eden-status-pill">
            {escape(active_project.get('status', 'Active'))}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

project_details = projects.get_active_project_details()
pricing_regions = pricing.list_regions()

selected_project_region = project_details.get("pricing_region", "")

if not selected_project_region:
    selected_project_region = (
        profile.get("default_region", "") or
        pricing.get_default_region() or
        ""
    )

if selected_project_region not in pricing_regions and pricing_regions:
    selected_project_region = pricing_regions[0]

project_suppliers = pricing.list_suppliers(selected_project_region)
selected_project_supplier = project_details.get(
    "pricing_supplier",
    ""
)

if not selected_project_supplier:
    selected_project_supplier = profile.get(
        "preferred_supplier",
        ""
    )

if (
        selected_project_supplier
        and selected_project_supplier not in project_suppliers
):
    project_suppliers = [
        selected_project_supplier,
        *project_suppliers
    ]

if not selected_project_supplier and project_suppliers:
    selected_project_supplier = project_suppliers[0]

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

        if pricing_regions:
            project_region = st.selectbox(
                "Pricing region",
                pricing_regions,
                index=pricing_regions.index(selected_project_region),
                help=(
                    "Eden will use this region's supplier prices when "
                    "pricing this project's material takeoff."
                )
            )
        else:
            project_region = ""
            st.info(
                "Create a pricing region in Settings before pricing "
                "this project."
            )

        if project_suppliers:
            project_supplier = st.selectbox(
                "Preferred material supplier",
                project_suppliers,
                index=project_suppliers.index(
                    selected_project_supplier
                ),
                help=(
                    "Eden uses this supplier's saved prices for the "
                    "project cost preview."
                )
            )
        else:
            project_supplier = ""
            st.info(
                "Add a material price with a supplier in Settings "
                "before pricing this project."
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
                **project_details,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "project_address": project_address,
                "pricing_region": project_region,
                "pricing_supplier": project_supplier,
                "material_suppliers": project_details.get(
                    "material_suppliers",
                    {}
                ),
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
        "Concrete Footing System",
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

elif estimate_type == "Concrete Footing System":
    st.subheader("Concrete Footing System Estimate")
    st.caption(
        "Combine continuous footing runs into one order. Footing size and "
        "reinforcing must match approved structural plans."
    )

    footing_run_type_count = st.selectbox(
        "Number of different footing run types",
        [1, 2, 3, 4],
        help=(
            "Example: use two types for two 40 ft runs and two 30 ft runs."
        )
    )

    with st.form("footing_system_form"):
        footing_runs = []

        for number in range(1, footing_run_type_count + 1):
            st.markdown(f"**Footing run type {number}**")
            run_columns = st.columns(4)

            with run_columns[0]:
                run_length = st.number_input(
                    "Continuous length (ft)",
                    min_value=0.1,
                    value=20.0,
                    key=f"footing_system_length_{number}"
                )

            with run_columns[1]:
                run_width_inches = st.number_input(
                    "Footing width (in)",
                    min_value=1.0,
                    value=16.0,
                    help="Typical residential continuous footings are often 16–24 inches wide. Eden converts this to feet automatically.",
                    key=f"footing_system_width_{number}"
                )

            with run_columns[2]:
                run_depth = st.number_input(
                    "Depth (in)",
                    min_value=1.0,
                    value=12.0,
                    key=f"footing_system_depth_{number}"
                )

            with run_columns[3]:
                run_quantity = st.number_input(
                    "Identical runs",
                    min_value=1,
                    value=1,
                    step=1,
                    key=f"footing_system_quantity_{number}"
                )

            footing_runs.append(
                {
                    "length": run_length,
                    "width_inches": run_width_inches,
                    "depth_inches": run_depth,
                    "quantity": run_quantity
                }
            )

        footing_options = st.columns(3)

        with footing_options[0]:
            footing_reinforced = st.checkbox(
                "Reinforcing required by plan"
            )

        with footing_options[1]:
            footing_forms = st.checkbox("Include forms", value=True)

        with footing_options[2]:
            footing_gravel = st.checkbox("Include gravel base")

        create_footing_system = st.form_submit_button(
            "Create Footing System Estimate"
        )

    if create_footing_system:
        footing_rebar = (
            {
                "status": "plan_required",
                "source": "approved_structural_plan",
                "schedule": None
            }
            if footing_reinforced
            else None
        )
        estimate = concrete.concrete_footing_system(
            footing_runs,
            reinforced=footing_reinforced,
            rebar=footing_rebar,
            forms=footing_forms,
            gravel_base=footing_gravel
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
                    "Estimate": estimate.get(
                        "display_name",
                        estimate.get("type", "Unknown")
                    ),
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
                f"{estimate.get(
                    'display_name',
                    estimate.get('type', 'Unknown estimate')
                )}"
            )
            estimate_choices[label] = number - 1

        selected_estimate = st.selectbox(
            "Select an estimate",
            list(estimate_choices.keys())
        )

        if st.button("Duplicate Selected Estimate"):
            projects.duplicate_estimate(
                estimate_choices[selected_estimate]
            )
            st.rerun()

        st.caption(
            "A duplicate is saved as a separate estimate and will add its "
            "materials to the project takeoff."
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
st.subheader("Custom Project Items")
st.caption(
    "Add one-off materials, permits, equipment, subcontractor allowances, "
    "or anything Eden does not estimate yet. These costs stay with this project."
)

with st.expander("Add Custom Item"):
    with st.form("custom_project_item_form"):
        custom_left, custom_right = st.columns(2)

        with custom_left:
            custom_item_name = st.text_input(
                "Item name",
                placeholder="Example: Dumpster rental"
            )

            custom_category = st.selectbox(
                "Category",
                [
                    "Material",
                    "Equipment",
                    "Permit",
                    "Subcontractor",
                    "Allowance",
                    "Other"
                ]
            )

            custom_unit = st.text_input(
                "Unit",
                value="EA",
                help="Examples: EA, LS, HR, DAY, CY, LF"
            )

        with custom_right:
            custom_quantity = st.number_input(
                "Quantity",
                min_value=0.01,
                value=1.0,
                step=1.0
            )

            custom_unit_cost = st.number_input(
                "Unit cost ($)",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

            custom_notes = st.text_input(
                "Notes (optional)",
                placeholder="Example: Includes delivery"
            )

        save_custom_item = st.form_submit_button("Add Custom Item")

    if save_custom_item:
        if not custom_item_name.strip() or not custom_unit.strip():
            st.error("Enter an item name and unit.")
        else:
            projects.add_custom_item(
                {
                    "item": custom_item_name.strip(),
                    "unit": custom_unit.strip().upper(),
                    "quantity": custom_quantity,
                    "manual_unit_cost": custom_unit_cost,
                    "category": custom_category,
                    "notes": custom_notes.strip()
                }
            )
            st.success("Custom project item added.")
            st.rerun()

custom_items = active_project.get("custom_items", [])

if custom_items:
    custom_item_rows = []

    for number, item in enumerate(custom_items, start=1):
        custom_item_rows.append(
            {
                "#": number,
                "Item": item.get("item", ""),
                "Category": item.get("category", "Custom"),
                "Quantity": item.get("quantity", 0),
                "Unit": item.get("unit", ""),
                "Unit Cost": (
                    f"${float(item.get('manual_unit_cost') or 0):,.2f}"
                ),
                "Notes": item.get("notes", "")
            }
        )

    st.dataframe(
        custom_item_rows,
        use_container_width=True,
        hide_index=True
    )

    with st.expander("Remove Custom Item"):
        custom_item_choices = {
            f"#{number} - {item.get('item', 'Custom item')}": number - 1
            for number, item in enumerate(custom_items, start=1)
        }

        selected_custom_item = st.selectbox(
            "Custom item to remove",
            list(custom_item_choices.keys())
        )

        confirm_custom_item_delete = st.checkbox(
            "I understand this removes the item from this project."
        )

        if st.button(
                "Remove Custom Item",
                disabled=not confirm_custom_item_delete
        ):
            projects.delete_custom_item(
                custom_item_choices[selected_custom_item]
            )
            st.rerun()

st.divider()
st.subheader("Project Material Takeoff")

material_takeoff = projects.get_active_material_takeoff()

if material_takeoff:
    st.dataframe(
        material_takeoff,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Material Takeoff CSV",
        data=create_material_takeoff_csv(
            active_project["name"],
            material_takeoff
        ),
        file_name=(
            active_project["name"].replace(" ", "_") +
            "_material_takeoff.csv"
        ),
        mime="text/csv",
        help="Opens directly in Microsoft Excel or can be sent to a supplier."
    )

    project_pricing_region = (
        project_details.get("pricing_region", "") or
        profile.get("default_region", "")
    )
    project_pricing_supplier = (
        project_details.get("pricing_supplier", "") or
        profile.get("preferred_supplier", "")
    )
    material_supplier_overrides = project_details.get(
        "material_suppliers",
        {}
    )

    if project_pricing_region:
        priced_takeoff = pricing.price_material_takeoff(
            material_takeoff,
            project_pricing_region,
            project_pricing_supplier or None,
            material_supplier_overrides
        )

        st.subheader("Project Material Cost Preview")
        if material_supplier_overrides:
            st.caption(
                "Using material-specific supplier selections where saved, "
                f"with {project_pricing_supplier or 'available'} prices "
                f"as the default in {priced_takeoff['pricing_region']}."
            )
        elif project_pricing_supplier:
            st.caption(
                f"Using {priced_takeoff['pricing_supplier']} prices in "
                f"{priced_takeoff['pricing_region']}."
            )
        else:
            st.caption(
                "Using saved prices where only one supplier price is "
                f"available in {priced_takeoff['pricing_region']}."
            )

        cost_column, missing_price_column = st.columns(2)

        with cost_column:
            st.metric(
                "Priced Material Cost",
                f"${priced_takeoff['total_material_cost']:,.2f}"
            )

        with missing_price_column:
            st.metric(
                "Items Needing a Price",
                len(priced_takeoff["unpriced_items"])
            )

        priced_takeoff_rows = []

        for item in priced_takeoff["priced_items"]:
            priced_takeoff_rows.append(
                {
                    "Item": item["item"],
                    "Unit": item["unit"],
                    "Quantity": item["quantity"],
                    "Unit Cost": (
                        f"${item['unit_cost']:,.2f}"
                        if item["unit_cost"] is not None
                        else "—"
                    ),
                    "Extended Cost": (
                        f"${item['extended_cost']:,.2f}"
                        if item["extended_cost"] is not None
                        else "—"
                    ),
                    "Supplier / Store": item.get(
                        "supplier",
                        "Not recorded"
                    ),
                    "Price Date": item.get(
                        "price_date",
                        "Not recorded"
                    ),
                    "Status": item["status"]
                }
            )

        st.dataframe(
            priced_takeoff_rows,
            use_container_width=True,
            hide_index=True
        )

        with st.expander("Choose Suppliers by Material"):
            st.caption(
                "Choose a supplier only when that material should come "
                "from somewhere other than the project default. Eden only "
                "shows suppliers with an exact saved price for each item."
            )

            with st.form("material_supplier_overrides_form"):
                updated_overrides = {}

                for number, item in enumerate(material_takeoff):
                    material_key = pricing._make_material_key(
                        item["item"],
                        item["unit"]
                    )
                    item_suppliers = pricing.list_material_suppliers(
                        item["item"],
                        item["unit"],
                        project_pricing_region
                    )
                    choices = ["Use project default", *item_suppliers]
                    saved_supplier = material_supplier_overrides.get(
                        material_key,
                        "Use project default"
                    )

                    if saved_supplier not in choices:
                        saved_supplier = "Use project default"

                    choice = st.selectbox(
                        f"{item['item']} ({item['unit']})",
                        choices,
                        index=choices.index(saved_supplier),
                        key=f"material_supplier_{number}"
                    )

                    if choice != "Use project default":
                        updated_overrides[material_key] = choice

                save_supplier_overrides = st.form_submit_button(
                    "Save Material Supplier Choices"
                )

            if save_supplier_overrides:
                projects.update_active_project_details(
                    {
                        **project_details,
                        "material_suppliers": updated_overrides
                    }
                )
                st.success("Material supplier choices saved.")
                st.rerun()

        if priced_takeoff["unpriced_items"]:
            st.warning(
                "This total excludes items without a saved supplier price."
            )

            with st.expander(
                    "Price Missing Takeoff Items",
                    expanded=True
            ):
                st.caption(
                    "Enter the price for one unit. Eden multiplies it by the "
                    "takeoff quantity and shows the extended cost."
                )

                with st.form("missing_project_prices_form"):
                    missing_price_supplier = st.text_input(
                        "Supplier or store",
                        value=project_pricing_supplier,
                        placeholder="Example: Home Depot or ABC Ready Mix"
                    )

                    missing_price_date = st.date_input(
                        "Price date",
                        value=date.today()
                    )

                    missing_price_values = {}

                    for number, item in enumerate(
                            priced_takeoff["unpriced_items"]
                    ):
                        missing_price_values[number] = st.number_input(
                            f"{item['item']} ({item['unit']}) — unit cost ($)",
                            min_value=0.0,
                            step=0.01,
                            key=f"missing_price_{number}"
                        )

                        extended_cost_preview = (
                            float(item["quantity"]) *
                            missing_price_values[number]
                        )

                        st.caption(
                            f"{item['quantity']} {item['unit']} x "
                            f"${missing_price_values[number]:,.2f} = "
                            f"${extended_cost_preview:,.2f}"
                        )

                    save_missing_prices = st.form_submit_button(
                        "Save Unit Prices"
                    )

                if save_missing_prices:
                    if not missing_price_supplier.strip():
                        st.error("Enter the supplier or store name.")
                    else:
                        for number, item in enumerate(
                                priced_takeoff["unpriced_items"]
                        ):
                            pricing.set_material_price(
                                item["item"],
                                item["unit"],
                                missing_price_values[number],
                                project_pricing_region,
                                supplier=missing_price_supplier,
                                price_date=missing_price_date
                            )

                        st.success("Missing material prices saved.")
                        st.rerun()

        with st.expander("Add Any Supplier Material Price"):
            st.caption(
                "Save a price for any material now. Eden will use it when "
                "a future takeoff has the same material name and unit."
            )

            with st.form("any_supplier_material_price_form"):
                any_price_supplier = st.text_input(
                    "Supplier or store",
                    value=project_pricing_supplier,
                    placeholder="Example: Home Depot or ABC Ready Mix",
                    key="any_price_supplier"
                )

                any_price_date = st.date_input(
                    "Price date",
                    value=date.today(),
                    key="any_price_date"
                )

                any_material_item = st.text_input(
                    "Material item",
                    placeholder="Example: 2x4 x 8 ft Studs",
                    key="any_price_item"
                )

                any_material_unit = st.text_input(
                    "Unit",
                    placeholder="Example: EA",
                    key="any_price_unit"
                )

                any_material_cost = st.number_input(
                    "Unit cost ($)",
                    min_value=0.0,
                    step=0.01,
                    key="any_price_cost"
                )

                save_any_material_price = st.form_submit_button(
                    "Save Material Price"
                )

            if save_any_material_price:
                if (
                        any_price_supplier.strip()
                        and any_material_item.strip()
                        and any_material_unit.strip()
                ):
                    pricing.set_material_price(
                        any_material_item,
                        any_material_unit,
                        any_material_cost,
                        project_pricing_region,
                        supplier=any_price_supplier,
                        price_date=any_price_date
                    )
                    st.success("Supplier material price saved.")
                    st.rerun()
                else:
                    st.error(
                        "Supplier, material item, and unit are required."
                    )

        st.subheader("Bid Summary Preview")
        st.caption(
            "Labor is planned in Project Schedule. Review the scheduled "
            "cost here, then set project markup."
        )

        bid_settings = projects.get_active_bid_settings()
        scheduled_labor_plan = projects.get_active_scheduled_labor_plan()
        saved_project_trades = bid_settings.get("labor_trades", [])

        with st.expander("Bid assumptions", expanded=True):
            st.caption(
                "Scheduled labor is managed in Project Schedule. These "
                "settings apply markup to the project bid."
            )

            scheduled_hours = scheduled_labor_plan["total_hours"]
            scheduled_trade_hours = scheduled_labor_plan["trade_hours"]

            if scheduled_hours > 0:
                st.info(
                    f"The project schedule contains {scheduled_hours:,.1f} "
                    "planned labor hours. Task hours take priority over a "
                    "phase total so Eden does not double-count work."
                )

                if scheduled_trade_hours:
                    st.caption(
                        "Scheduled trade plan: " + ", ".join(
                            f"{hours:,.1f}h {trade}"
                            for trade, hours in scheduled_trade_hours.items()
                        )
                    )

                    if st.button(
                            "Use Scheduled Labor Plan",
                            key="use_scheduled_labor_plan"
                    ):
                        saved_rates = {}

                        for saved_trade in saved_project_trades:
                            normalized_trade = (
                                projects.normalize_labor_trade(
                                    saved_trade.get("trade", "")
                                )
                            )
                            saved_rate = float(
                                saved_trade.get("hourly_rate", 0.0) or 0.0
                            )

                            if normalized_trade and (
                                    normalized_trade.casefold()
                                    not in saved_rates
                                    or saved_rate > 0
                            ):
                                saved_rates[normalized_trade.casefold()] = (
                                    saved_rate
                                )
                        scheduled_trades = [
                            {
                                "trade": trade,
                                "labor_hours": hours,
                                "hourly_rate": saved_rates.get(
                                    trade.casefold(),
                                    0.0
                                )
                            }
                            for trade, hours in scheduled_trade_hours.items()
                        ]
                        projects.update_active_bid_settings(
                            {
                                "planned_labor_hours": scheduled_hours,
                                "crew_size": bid_settings.get("crew_size", 0),
                                "labor_hours_by_trade": {},
                                "labor_trades": scheduled_trades,
                                "overhead_percent": bid_settings[
                                    "overhead_percent"
                                ],
                                "profit_markup_percent": bid_settings[
                                    "profit_markup_percent"
                                ]
                            }
                        )
                        st.rerun()
                else:
                    st.caption(
                        "Assign a primary labor trade to each planned phase "
                        "or task before importing the schedule into the bid."
                    )
            else:
                st.caption(
                    "Add planned labor hours to phases or schedule tasks to "
                    "build a labor plan from the schedule."
                )

            with st.form("bid_assumptions_form"):
                save_bid_assumptions = st.form_submit_button(
                    "Save Bid Assumptions"
                )

                overhead_percent = st.number_input(
                    "Overhead allowance (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        bid_settings["overhead_percent"]
                    ),
                    step=0.5
                )

                profit_markup_percent = st.number_input(
                    "Profit markup (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        bid_settings["profit_markup_percent"]
                    ),
                    step=0.5
                )

            if save_bid_assumptions:
                projects.update_active_bid_settings(
                    {
                        "planned_labor_hours": bid_settings[
                            "planned_labor_hours"
                        ],
                        "crew_size": bid_settings["crew_size"],
                        "labor_hours_by_trade": bid_settings[
                            "labor_hours_by_trade"
                        ],
                        "labor_trades": saved_project_trades,
                        "overhead_percent": overhead_percent,
                        "profit_markup_percent": (
                            profit_markup_percent
                        )
                    }
                )

                st.success("Bid assumptions saved.")
                st.rerun()

        material_cost = priced_takeoff["total_material_cost"]

        project_labor_trades = bid_settings.get("labor_trades", [])

        if project_labor_trades:
            labor_cost = sum(
                trade.get(
                    "labor_hours",
                    trade.get("member_count", 1) *
                    trade.get("hours_per_person", 0.0)
                ) *
                trade["hourly_rate"]
                for trade in project_labor_trades
            )
            labor_summary = ", ".join(
                f"{trade.get('labor_hours', trade.get('member_count', 1) * trade.get('hours_per_person', 0.0)):,.1f}h "
                f"{trade['trade']} @ "
                f"${trade['hourly_rate']:,.2f}/hr"
                for trade in project_labor_trades
            ) or "No trade hours entered"
        else:
            labor_cost = 0.0
            labor_summary = (
                "No project trade labor has been added."
            )
        direct_cost = material_cost + labor_cost
        overhead_cost = direct_cost * (
            bid_settings["overhead_percent"] / 100
        )
        cost_before_profit = direct_cost + overhead_cost
        profit_amount = cost_before_profit * (
            bid_settings["profit_markup_percent"] / 100
        )
        customer_price = cost_before_profit + profit_amount

        material_column, labor_column, price_column = st.columns(3)

        with material_column:
            st.metric(
                "Priced Materials",
                f"${material_cost:,.2f}"
            )

        with labor_column:
            st.metric(
                "Labor Cost",
                f"${labor_cost:,.2f}"
            )

        with price_column:
            st.metric(
                "Customer Price Preview",
                f"${customer_price:,.2f}"
            )

        st.caption(
            f"Labor: {labor_summary} · "
            f"Overhead: ${overhead_cost:,.2f} · "
            f"Profit: ${profit_amount:,.2f}"
        )

        if priced_takeoff["unpriced_items"]:
            st.warning(
                "Customer Price Preview is incomplete until all material "
                "items have supplier prices."
            )
    else:
        st.info(
            "Choose a pricing region in Customer and Project Details "
            "to see material costs."
        )

else:
    st.info("No material takeoff items have been saved yet.")

st.divider()
st.subheader("Bid Review")
st.caption(
    "Review the customer-facing bid before creating a PDF. Eden will not "
    "mark a proposal ready while material prices are missing."
)

if "priced_takeoff" in locals():
    proposal_statuses = [
        "Draft",
        "Ready for Review",
        "Sent to Customer",
        "Approved",
        "Lost"
    ]
    current_proposal_status = project_details.get(
        "proposal_status",
        "Draft"
    )

    if current_proposal_status not in proposal_statuses:
        current_proposal_status = "Draft"

    saved_expiration = project_details.get(
        "proposal_expiration_date",
        ""
    )

    try:
        proposal_expiration = (
            date.fromisoformat(saved_expiration)
            if saved_expiration
            else date.today()
        )
    except ValueError:
        proposal_expiration = date.today()

    with st.form("bid_review_form"):
        review_left, review_right = st.columns(2)

        with review_left:
            reviewed_proposal_status = st.selectbox(
                "Proposal status",
                proposal_statuses,
                index=proposal_statuses.index(
                    current_proposal_status
                )
            )

            reviewed_expiration = st.date_input(
                "Quote valid through",
                value=proposal_expiration
            )

            reviewed_scope = st.text_area(
                "Scope of work",
                value=project_details.get("proposal_scope", ""),
                placeholder=(
                    "Example: Furnish and install the concrete patio "
                    "materials described in this estimate."
                )
            )

        with review_right:
            reviewed_exclusions = st.text_area(
                "Exclusions and assumptions",
                value=project_details.get(
                    "proposal_exclusions",
                    ""
                ),
                placeholder=(
                    "Example: Permits, engineering, and unforeseen site "
                    "conditions are excluded unless listed above."
                )
            )

            reviewed_notes = st.text_area(
                "Additional customer notes",
                value=project_details.get("proposal_notes", "")
            )

        save_bid_review = st.form_submit_button("Save Bid Review")

    if save_bid_review:
        ready_statuses = [
            "Ready for Review",
            "Sent to Customer",
            "Approved"
        ]
        readiness_problems = []

        if priced_takeoff["unpriced_items"]:
            readiness_problems.append("all material prices")

        if not project_details.get("customer_name"):
            readiness_problems.append("a customer name")

        if not project_details.get("project_address"):
            readiness_problems.append("a project address")

        if (
                reviewed_proposal_status in ready_statuses
                and readiness_problems
        ):
            st.error(
                "Keep this proposal as Draft until it has "
                + ", ".join(readiness_problems) + "."
            )
        else:
            projects.update_active_project_details(
                {
                    **project_details,
                    "proposal_status": reviewed_proposal_status,
                    "proposal_expiration_date": str(reviewed_expiration),
                    "proposal_scope": reviewed_scope,
                    "proposal_exclusions": reviewed_exclusions,
                    "proposal_notes": reviewed_notes
                }
            )
            st.success("Bid review saved.")
            st.rerun()

    review_issues = []

    if priced_takeoff["unpriced_items"]:
        review_issues.append(
            f"{len(priced_takeoff['unpriced_items'])} item(s) need a price"
        )

    if not project_details.get("customer_name"):
        review_issues.append("customer name is missing")

    if not project_details.get("project_address"):
        review_issues.append("project address is missing")

    review_material, review_labor, review_price = st.columns(3)

    with review_material:
        st.metric("Materials", f"${material_cost:,.2f}")

    with review_labor:
        st.metric("Labor", f"${labor_cost:,.2f}")

    with review_price:
        st.metric("Customer Price", f"${customer_price:,.2f}")

    if review_issues:
        st.warning(
            "Not ready to send: " + "; ".join(review_issues) + "."
        )
    else:
        st.success(
            "Bid pricing is complete and customer/project details are ready "
            "for a customer PDF."
        )
else:
    st.info(
        "Add a takeoff and select a pricing region to begin bid review."
    )

st.divider()
st.subheader("Change Orders")
st.caption(
    "Document added work or credits separately from the original bid. "
    "Change orders do not alter the original material takeoff."
)

with st.form("add_change_order_form"):
    change_title = st.text_input(
        "Change order title",
        placeholder="Example: Add rear patio steps"
    )
    change_date = st.date_input("Change order date", value=date.today())
    change_amount = st.number_input(
        "Customer price change ($)",
        value=0.0,
        step=100.0,
        help="Use a negative amount for a credit to the customer."
    )
    change_description = st.text_area(
        "Added or revised scope",
        placeholder="Describe exactly what is changing."
    )
    change_notes = st.text_area(
        "Notes and assumptions (optional)"
    )
    save_change_order = st.form_submit_button("Save Change Order")

if save_change_order:
    if not change_title.strip() or not change_description.strip():
        st.error("Enter a title and description for the change order.")
    elif change_amount == 0:
        st.error("Enter a price increase or credit amount.")
    else:
        projects.add_change_order(
            {
                "title": change_title.strip(),
                "date": str(change_date),
                "amount": float(change_amount),
                "description": change_description.strip(),
                "notes": change_notes.strip(),
                "status": "Draft"
            }
        )
        st.success("Change order saved as Draft.")
        st.rerun()

change_orders = projects.get_active_change_orders()

if change_orders:
    approved_change_total = round(
        sum(
            float(change_order.get("amount", 0.0))
            for change_order in change_orders
            if change_order.get("status") == "Approved"
        ),
        2
    )
    original_contract_price = (
        float(customer_price)
        if "customer_price" in locals()
        else 0.0
    )

    change_base, change_approved, change_revised = st.columns(3)
    with change_base:
        st.metric("Original Bid", f"${original_contract_price:,.2f}")
    with change_approved:
        st.metric("Approved Changes", f"${approved_change_total:,.2f}")
    with change_revised:
        st.metric(
            "Revised Contract Price",
            f"${original_contract_price + approved_change_total:,.2f}"
        )

    change_rows = []
    change_choices = {}

    for number, change_order in enumerate(change_orders, start=1):
        label = f"#{number} - {change_order.get('title', 'Change Order')}"
        change_choices[label] = number - 1
        change_rows.append(
            {
                "#": number,
                "Title": change_order.get("title", ""),
                "Date": change_order.get("date", ""),
                "Status": change_order.get("status", "Draft"),
                "Customer Price Change": (
                    f"${float(change_order.get('amount', 0.0)):,.2f}"
                )
            }
        )

    st.dataframe(change_rows, use_container_width=True, hide_index=True)

    with st.expander("Manage Change Orders"):
        selected_change_label = st.selectbox(
            "Change order",
            list(change_choices.keys())
        )
        selected_change_index = change_choices[selected_change_label]
        selected_change_order = change_orders[selected_change_index]
        change_statuses = ["Draft", "Sent", "Approved", "Declined"]
        selected_change_status = selected_change_order.get("status", "Draft")

        if selected_change_status not in change_statuses:
            selected_change_status = "Draft"

        updated_change_status = st.selectbox(
            "Status",
            change_statuses,
            index=change_statuses.index(selected_change_status)
        )

        manage_left, manage_right = st.columns(2)
        with manage_left:
            if st.button("Save Change Order Status"):
                projects.update_change_order_status(
                    selected_change_index,
                    updated_change_status
                )
                st.rerun()

        with manage_right:
            if st.button("Create Change Order PDF"):
                change_pdf_problems = []

                if (
                        "priced_takeoff" not in locals() or
                        priced_takeoff["unpriced_items"]
                ):
                    change_pdf_problems.append(
                        "a fully priced material takeoff"
                    )

                if not project_details.get("customer_name"):
                    change_pdf_problems.append("a customer name")

                if not project_details.get("project_address"):
                    change_pdf_problems.append("a project address")

                if change_pdf_problems:
                    st.error(
                        "Complete " + ", ".join(change_pdf_problems) +
                        " before creating a change order PDF."
                    )
                else:
                    prior_approved_changes = sum(
                        float(change_order.get("amount", 0.0))
                        for index, change_order in enumerate(change_orders)
                        if (
                            index != selected_change_index and
                            change_order.get("status") == "Approved"
                        )
                    )
                    change_pdf_path = create_change_order_pdf(
                        active_project,
                        profile,
                        selected_change_order,
                        selected_change_index + 1,
                        original_contract_price,
                        prior_approved_changes
                    )
                    st.session_state["change_order_pdf_path"] = str(
                        change_pdf_path
                    )

        confirm_change_delete = st.checkbox(
            "I understand this permanently removes the selected change order."
        )

        if st.button(
                "Delete Selected Change Order",
                disabled=not confirm_change_delete
        ):
            projects.delete_change_order(selected_change_index)
            st.rerun()

    if "change_order_pdf_path" in st.session_state:
        change_pdf_path = st.session_state["change_order_pdf_path"]

        with open(change_pdf_path, "rb") as pdf_file:
            st.download_button(
                "Download Change Order PDF",
                data=pdf_file.read(),
                file_name=(
                    active_project["name"].replace(" ", "_") +
                    "_change_order.pdf"
                ),
                mime="application/pdf"
            )
else:
    st.info("No change orders have been saved to this project yet.")

st.divider()
st.subheader("Reports")
st.caption(
    "Create an internal cost sheet for your company or a customer-safe "
    "proposal that does not reveal supplier costs, labor costs, or markup."
)

pdf_priced_takeoff = (
    priced_takeoff
    if "priced_takeoff" in locals()
    else None
)
pdf_bid_summary = None

if pdf_priced_takeoff is not None:
    pdf_bid_summary = {
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "overhead_cost": overhead_cost,
        "profit_amount": profit_amount,
        "customer_price": customer_price,
        "materials_complete": not bool(
            pdf_priced_takeoff["unpriced_items"]
        ),
        "labor_trades": project_labor_trades
    }

internal_report_column, customer_proposal_column = st.columns(2)

with internal_report_column:
    st.markdown("#### Internal Cost Sheet")
    st.caption(
        "For your company only. Includes takeoff, supplier costs, labor, "
        "overhead, and profit."
    )

    if st.button("Create Internal Cost Sheet PDF"):
        internal_pdf_path = create_project_pdf(
            active_project,
            profile,
            material_takeoff,
            priced_takeoff=pdf_priced_takeoff,
            bid_summary=pdf_bid_summary
        )
        st.session_state["internal_cost_sheet_pdf_path"] = str(
            internal_pdf_path
        )

with customer_proposal_column:
    st.markdown("#### Customer Proposal")
    st.caption(
        "Safe to email. Shows the scope, final price, exclusions, and "
        "acceptance lines only."
    )

    if st.button("Create Customer Proposal PDF"):
        proposal_problems = []

        if pdf_bid_summary is None:
            proposal_problems.append("a priced material takeoff")
        elif not pdf_bid_summary["materials_complete"]:
            proposal_problems.append("all supplier material prices")

        if not project_details.get("customer_name"):
            proposal_problems.append("a customer name")

        if not project_details.get("project_address"):
            proposal_problems.append("a project address")

        if proposal_problems:
            st.error(
                "Complete " + ", ".join(proposal_problems) +
                " before creating a customer proposal."
            )
        else:
            proposal_pdf_path = create_customer_proposal_pdf(
                active_project,
                profile,
                pdf_bid_summary
            )
            st.session_state["customer_proposal_pdf_path"] = str(
                proposal_pdf_path
            )

if "internal_cost_sheet_pdf_path" in st.session_state:
    internal_pdf_path = st.session_state["internal_cost_sheet_pdf_path"]

    with open(internal_pdf_path, "rb") as pdf_file:
        st.download_button(
            "Download Internal Cost Sheet PDF",
            data=pdf_file.read(),
            file_name=active_project["name"].replace(" ", "_") +
            "_internal_cost_sheet.pdf",
            mime="application/pdf"
        )

if "customer_proposal_pdf_path" in st.session_state:
    proposal_pdf_path = st.session_state["customer_proposal_pdf_path"]

    with open(proposal_pdf_path, "rb") as pdf_file:
        st.download_button(
            "Download Customer Proposal PDF",
            data=pdf_file.read(),
            file_name=active_project["name"].replace(" ", "_") +
            "_customer_proposal.pdf",
            mime="application/pdf"
        )
