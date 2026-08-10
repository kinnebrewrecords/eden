"""Shared page gate for Eden's authenticated workspace."""

import streamlit as st

from CloudWorkspace import activate_workspace_for_current_user
from EdenAccess import current_access
from EdenAuth import current_user, sign_in


def require_eden_login():
    """Stop protected pages until the visitor signs into an Eden account."""
    user = current_user()

    if user:
        verified_user_id = st.session_state.get(
            "eden_access_verified_user_id"
        )

        if verified_user_id == user["user_id"]:
            access = {"has_access": True}
        else:
            access = current_access()

        if not access.get("has_access"):
            st.markdown(
                """
                <section class="eden-hero">
                    <p class="eden-hero-kicker">Eden access required</p>
                    <h1>Your account is signed in, but does not have Eden access yet.</h1>
                    <p class="eden-hero-subtitle">
                        Start a subscription or redeem your private beta code
                        on the Eden website, then sign in again.
                    </p>
                </section>
                """,
                unsafe_allow_html=True
            )

            if access.get("error"):
                st.error(
                    "Eden could not verify account access. Make sure the "
                    "beta access SQL setup has been run in Supabase."
                )

            st.caption(
                "Open the Eden website Account & Billing page to redeem "
                "your code or start a subscription."
            )
            st.stop()

        st.session_state["eden_access_verified_user_id"] = user["user_id"]

        try:
            activate_workspace_for_current_user()
        except Exception:
            # A temporary cloud problem must not prevent a signed-in user
            # from reaching their already-loaded local workspace.
            pass
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
