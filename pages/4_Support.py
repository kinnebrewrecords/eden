from datetime import datetime
from email.message import EmailMessage
import smtplib

import streamlit as st
from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_eden_login
from EdenAuth import current_user


SUPPORT_EMAIL = "eden.intelligence.support@gmail.com"


def send_support_report(report, issue_type, reply_email):
    """Send a submitted support report to Eden's private support inbox."""
    app_password = st.secrets["support"]["gmail_app_password"]

    message = EmailMessage()
    message["Subject"] = f"Eden Support: {issue_type}"
    message["From"] = SUPPORT_EMAIL
    message["To"] = SUPPORT_EMAIL

    if reply_email.strip():
        message["Reply-To"] = reply_email.strip()

    message.set_content(report.strip())

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SUPPORT_EMAIL, app_password)
        server.send_message(message)


st.set_page_config(
    page_title="Eden Support",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
render_sidebar(
    show_command_center=False
)

st.title("Support")
st.caption(
    "Get help with Eden or create a report for a problem you found."
)

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

        try:
            send_support_report(report, issue_type, email)
            st.success("Your support report was sent to Eden Support.")
        except KeyError:
            st.error(
                "Support delivery is not configured yet. Please try again "
                "later."
            )
        except Exception:
            st.error(
                "Eden could not send your report right now. Please try "
                "again later."
            )

        st.download_button(
            "Download a Copy",
            data=report,
            file_name="eden_support_report.txt",
            mime="text/plain"
        )
