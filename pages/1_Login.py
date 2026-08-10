import streamlit as st

from EdenAuth import (
    current_user,
    refresh_authenticated_workspace_store,
    sign_in,
    sign_out
)
from EdenTheme import apply_eden_theme


st.set_page_config(page_title="Sign in to Eden", layout="wide")
apply_eden_theme()

st.title("Sign in to Eden")
st.caption("Use the Eden account that has your subscription or beta access.")

login_notice = st.session_state.pop("eden_login_notice", None)
if login_notice:
    st.info(login_notice)

user = current_user()

if user:
    st.info(f"This browser is currently signed in as {user['email']}.")
    st.caption("To protect project privacy, sign out before using a different Eden account.")

    if st.button("Sign Out and Use a Different Account", type="primary"):
        sign_out()
        st.rerun()

    if st.button("Continue to My Eden Workspace"):
        # Refresh the saved Supabase session before the protected page checks
        # beta/subscription access. This prevents a stale browser token from
        # being mistaken for an account with no Eden access.
        _, refreshed_user = refresh_authenticated_workspace_store()

        if refreshed_user:
            st.switch_page("Frontend.py")
            st.stop()
        else:
            sign_out()
            st.session_state["eden_login_notice"] = (
                "Your saved Eden session expired. Sign in again below with "
                "the same Eden account to continue to your Dashboard."
            )
            st.rerun()

    st.stop()

with st.form("website_eden_sign_in_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Sign In to Eden")

if submit:
    try:
        sign_in(email.strip(), password)
        st.switch_page("Frontend.py")
    except Exception as error:
        st.error(f"Could not sign in: {error}")

st.caption("Create your account on the Eden website after receiving access.")
