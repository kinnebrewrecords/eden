"""Shared page gate for Eden's authenticated workspace."""

import streamlit as st

from EdenAuth import current_user, sign_in


def require_eden_login():
    """Stop protected pages until the visitor signs into an Eden account."""
    if current_user():
        return

    st.markdown(
        """
        <section class="eden-hero">
            <p class="eden-hero-kicker">Eden account required</p>
            <h1>Sign in to open your workspace.</h1>
            <p class="eden-hero-subtitle">
                Your projects, pricing, bids, schedule, and daily logs are
                available after you sign into your Eden account.
            </p>
        </section>
        """,
        unsafe_allow_html=True
    )

    with st.form("eden_splash_sign_in_form"):
        email = st.text_input("Email", key="eden_splash_sign_in_email")
        password = st.text_input(
            "Password",
            type="password",
            key="eden_splash_sign_in_password"
        )
        submit = st.form_submit_button("Open Eden Workspace")

    if submit:
        try:
            sign_in(email.strip(), password)
            st.rerun()
        except Exception as error:
            st.error(f"Could not sign in: {error}")

    st.caption(
        "New to Eden? Create your account through the Eden website after "
        "starting your trial or subscription."
    )

    st.stop()
