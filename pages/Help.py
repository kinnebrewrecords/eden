import streamlit as st

from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_eden_login


st.set_page_config(
    page_title="Eden Help",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
render_sidebar(
    show_command_center=False
)

st.markdown(
    """
    <section class="eden-hero">
        <p class="eden-hero-kicker">Eden field guide</p>
        <h1>How can Eden help?</h1>
        <p class="eden-hero-subtitle">
            Start with a plain-language request. Eden asks only for the
            measurements and plan details it needs for a material takeoff.
        </p>
    </section>
    """,
    unsafe_allow_html=True
)

st.markdown("#### Featured estimating tools")
flatwork_feature, openings_feature = st.columns(2)

with flatwork_feature:
    st.markdown(
        """
        <div class="eden-feature-card">
            <p class="eden-feature-label">Advanced concrete</p>
            <p class="eden-feature-title">Custom Flatwork</p>
            <p class="eden-feature-copy">
                Estimate irregular driveways, sidewalks, ramps, and other
                layouts from measured area, form perimeter, and thickness.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code("estimate custom flatwork", language=None)

with openings_feature:
    st.markdown(
        """
        <div class="eden-feature-card">
            <p class="eden-feature-label">Advanced framing</p>
            <p class="eden-feature-title">Walls With Openings</p>
            <p class="eden-feature-copy">
                Add doors and windows to a wall takeoff, including framing,
                plates, window sills, and plan-based header material.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code("estimate a framed wall with an opening", language=None)

st.markdown("#### Project assemblies")
st.info(
    "Assemblies combine related work into one traceable material takeoff. "
    "Each one lists its assumptions and plan-required exclusions so you can "
    "review the scope before ordering."
)
st.code(
    "estimate a whole house takeoff\n"
    "estimate a two story house takeoff\n"
    "estimate a foundation system assembly\n"
    "estimate an exterior wall assembly\n"
    "estimate a roof covering assembly\n"
    "estimate a floor system assembly\n"
    "estimate an interior finish assembly\n"
    "estimate a backyard studio shell",
    language=None
)
st.caption(
    "Whole-House Takeoff guides you through the systems actually included "
    "in the plan. It preserves each system as a separate component while "
    "also producing one combined project material takeoff."
)

getting_started_tab, commands_tab, estimating_tab, bids_tab, guidance_tab = (
    st.tabs(
        [
            "Getting Started",
            "Chat Commands",
            "What Eden Estimates",
            "Pricing, Bids & Reports",
            "Guidance"
        ]
    )
)

with getting_started_tab:
    st.subheader("Your first project")
    st.markdown(
        """
        1. Go to **Dashboard** and create a project in the sidebar.
        2. Open **Chat with Eden** and describe the work in normal language.
        3. Answer Eden's follow-up questions one at a time.
        4. Eden saves the completed estimate to the active project.
        5. Return to the Dashboard to review the combined material takeoff,
           pricing, bid, and reports.
        """
    )

    st.info(
        "Tip: Keep one active project open while estimating. Everything you "
        "save is added to that project's material takeoff."
    )

    st.subheader("A good first request")
    st.code(
        "estimate a 20 by 20 concrete slab, 6 inches thick",
        language=None
    )

with commands_tab:
    st.subheader("Project commands")
    st.code(
        "create project Demo House\n"
        "select project Demo House\n"
        "show project\n"
        "delete project Demo House",
        language=None
    )

    st.subheader("During an estimate")
    st.markdown(
        """
        - Type `cancel` to stop the current estimate.
        - Type `change to <estimate type>` to begin a different estimate.
        - Update future default waste directly in Chat, for example:
          `set concrete waste to 10%`.
        - Answer each question directly. For example, type `20`, then `8`
          when Eden asks for wall length and height.
        - Eden asks for missing dimensions rather than assuming them.
        """
    )

    st.subheader("Useful examples")
    st.code(
        "estimate a whole house takeoff\n"
        "estimate a patio\n"
            "estimate a framed wall with an opening\n"
            "estimate an exterior wall assembly\n"
            "estimate batt insulation\n"
        "estimate roof sheathing",
        language=None
    )

with estimating_tab:
    concrete_tab, framing_tab, exterior_tab, finishes_tab, mep_tab = st.tabs(
        ["Concrete", "Lumber & Roofing", "Exterior", "Interior", "MEP"]
    )

    with concrete_tab:
        st.subheader("Concrete and flatwork")
        st.code(
            "estimate a 20 x 20 slab, 6 inches thick\n"
            "estimate a concrete patio\n"
            "estimate a concrete footing\n"
            "estimate a footing system\n"
            "estimate a foundation system assembly\n"
            "estimate a whole house takeoff\n"
            "estimate a roof covering assembly\n"
            "estimate a floor system assembly\n"
            "estimate an interior finish assembly\n"
            "estimate a concrete pier\n"
            "estimate custom flatwork",
            language=None
        )
        st.caption(
            "For custom or irregular flatwork, Eden asks for measured area, "
            "form perimeter, and thickness from plans or field layout."
        )
        st.info(
            "Use **footing system** for a foundation made of multiple "
            "continuous footing runs. Eden combines them into one material "
            "takeoff and rounds concrete once for the complete system."
        )

    with framing_tab:
        st.subheader("Lumber, framing, and roofing")
        st.code(
            "estimate a framed wall\n"
            "estimate a framed wall with an opening\n"
            "estimate a wall framing package\n"
            "estimate an exterior wall assembly\n"
            "estimate roof trusses\n"
            "estimate framing hardware\n"
            "estimate stair framing\n"
            "estimate deck framing\n"
            "estimate garage door framing\n"
            "estimate roof sheathing\n"
            "estimate shingles\n"
            "estimate ceiling joists",
            language=None
        )
        st.info(
            "For a wall with doors or windows, Eden can estimate framing, "
            "plates, and window sills. Header size and plies must come from "
            "the approved structural plan before header material is added."
        )

        st.caption(
            "Need a repeatable system instead of a single item? Try "
            "`estimate an exterior wall assembly` for straight exterior "
            "wall segments, or `estimate a backyard studio shell` for a "
            "starter project package."
        )

    with exterior_tab:
        st.subheader("Exterior, decks, and fencing")
        st.code(
            "estimate exterior siding\n"
            "estimate housewrap\n"
            "estimate exterior trim\n"
            "estimate windows\n"
            "estimate exterior doors\n"
            "estimate decking\n"
            "estimate a fence",
            language=None
        )
        st.caption(
            "Eden calculates buying quantities. Confirm product selections, "
            "site conditions, approved plans, and local requirements before "
            "ordering."
        )

    with finishes_tab:
        st.subheader("Interior finishes")
        st.code(
            "estimate wall drywall\n"
            "estimate ceiling drywall\n"
            "estimate batt insulation\n"
            "estimate interior paint\n"
            "estimate flooring\n"
            "estimate baseboard\n"
            "estimate interior doors",
            language=None
        )

    with mep_tab:
        st.subheader("Mechanical, electrical, and plumbing")
        st.code(
            "estimate outlets\n"
            "estimate pex pipe\n"
            "estimate ductwork",
            language=None
        )

with bids_tab:
    st.subheader("Price a completed material takeoff")
    st.markdown(
        """
        1. On the Dashboard, open **Customer and Project Details**.
        2. Select the project's pricing region and supplier.
        3. Add prices for anything marked **Price needed**. Eden multiplies
           each saved unit price by the estimated quantity automatically.
        4. Add labor, overhead, and profit in the Bid Summary area.
        """
    )

    st.subheader("Customer-ready documents")
    st.markdown(
        """
        - **Internal Cost Sheet PDF**: company-only; includes supplier costs,
          labor, overhead, and profit.
        - **Customer Proposal PDF**: safe to email; includes scope, final
          price, exclusions, and acceptance lines only.
        - **Change Order PDF**: documents added work or a customer credit
          separately from the original proposal.
        - **Material Takeoff CSV**: download a supplier-ready item list that
          opens directly in Excel.
        """
    )

    st.warning(
        "Customer PDFs are intentionally blocked until the customer name, "
        "project address, and all supplier material prices are complete."
    )

with guidance_tab:
    st.subheader("Use Eden responsibly")
    st.markdown(
        """
        - Eden creates estimating quantities and material takeoffs; verify
          measurements, local requirements, and supplier pricing before
          ordering.
        - Rebar, header sizing, engineered lumber, structural connections,
          and similar items must follow approved plans and applicable code.
        - Use **Settings** to manage company information, estimating defaults,
          preferred suppliers, pricing regions, and supplier prices.
        - Use **Support** if you need help with the application or want to
          report an issue.
        """
    )

    st.page_link(
        "pages/4_Support.py",
        label="Open Eden Support",
        icon=":material/support_agent:"
    )
