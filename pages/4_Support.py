from datetime import datetime
from urllib.parse import quote

import streamlit as st
from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_eden_login
from EdenAuth import current_user


SUPPORT_EMAIL = "kinnebrewrecords@gmail.com"


st.set_page_config(
    page_title="Eden Support",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
render_sidebar(
    show_command_center=False,
    show_project_manager=False
)

st.title("Support")
st.caption(
    "Get help with Eden or create a report for a problem you found."
)
st.caption(f"Support email: {SUPPORT_EMAIL}")

st.subheader("Before you report an issue")

st.markdown("""
- Check the Help page for example commands.
- Include the estimate type and the exact message you entered.
- Include any error message shown by Eden.
""")

st.subheader("Create a support report")

with st.form("support_form"):
    name = st.text_input("Your name (optional)")

    email = st.text_input(
        "Your reply email",
        value=current_user().get("email", "")
    )

    issue_type = st.selectbox(
        "What do you need help with?",
        [
            "Estimate question",
            "Project question",
            "Incorrect calculation",
            "Error message",
            "Suggestion"
        ]
    )

    description = st.text_area(
        "Describe what happened",
        placeholder=(
            "Example: I estimated a 20 x 20 slab, "
            "but the material takeoff did not appear."
        )
    )

    submitted = st.form_submit_button(
        "Create Support Report"
    )

if submitted:
    if not description.strip():
        st.error("Please describe the issue first.")

    else:
        report = f"""
EDEN SUPPORT REPORT

Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}
Name: {name or "Not provided"}
Reply Email: {email or "Not provided"}
Issue Type: {issue_type}

Description:
{description}
"""

        subject = quote(f"Eden Support: {issue_type}")
        body = quote(report.strip())
        email_url = (
            f"mailto:{SUPPORT_EMAIL}?subject={subject}&body={body}"
        )

        st.success("Your support report is ready to send.")

        st.link_button(
            "Email Report to Eden Support",
            email_url,
            icon=":material/send:",
            type="primary"
        )

        st.caption(
            "This opens your email app with the report addressed to Eden "
            "Support. Review it, then press Send."
        )

        st.download_button(
            "Download a Copy",
            data=report,
            file_name="eden_support_report.txt",
            mime="text/plain"
        )
