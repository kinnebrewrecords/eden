import streamlit as st

from CloudWorkspace import (
    backup_local_workspace,
    restore_local_workspace,
    restore_workspace_version
)
from EdenAuth import (
    current_user,
    get_authenticated_workspace_store,
    sign_in,
    sign_out,
    sign_up
)
from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_eden_login


st.set_page_config(
    page_title="Account & Cloud",
    layout="wide"
)

apply_eden_theme()
require_eden_login()
render_sidebar(
    show_command_center=False
)

st.title("Account & Cloud")
st.caption(
    "Sign in to back up your Eden workspace securely and restore it on another device."
)

user = current_user()

if not user:
    sign_in_tab, create_account_tab = st.tabs(
        ["Sign In", "Create Account"]
    )

    with sign_in_tab:
        with st.form("eden_sign_in_form"):
            email = st.text_input("Email", key="eden_sign_in_email")
            password = st.text_input(
                "Password",
                type="password",
                key="eden_sign_in_password"
            )
            submit = st.form_submit_button("Sign In")

        if submit:
            try:
                sign_in(email.strip(), password)
                st.success("Signed in successfully.")
                st.rerun()
            except Exception as error:
                st.error(f"Could not sign in: {error}")

    with create_account_tab:
        with st.form("eden_create_account_form"):
            email = st.text_input("Email", key="eden_create_email")
            password = st.text_input(
                "Create password",
                type="password",
                help="Use at least 8 characters.",
                key="eden_create_password"
            )
            submit = st.form_submit_button("Create Account")

        if submit:
            if len(password) < 8:
                st.error("Use a password with at least 8 characters.")
            else:
                try:
                    session, _ = sign_up(email.strip(), password)

                    if session:
                        st.success("Account created and signed in.")
                        st.rerun()
                    else:
                        st.success(
                            "Account created. Check your email to confirm it, "
                            "then return here and sign in."
                        )
                except Exception as error:
                    st.error(f"Could not create account: {error}")

    st.stop()

st.success(f"Signed in as {user.get('email', 'your Eden account')}.")

store, session = get_authenticated_workspace_store()

if store is None:
    st.error("Your account session has expired. Please sign in again.")
    sign_out()
    st.rerun()

backup_column, restore_column = st.columns(2)

with backup_column:
    st.subheader("Back up this device")
    st.write(
        "Upload this device's projects, pricing, settings, bids, schedule, and daily-log entries to your private cloud workspace."
    )
    st.caption(
        "Daily-log photo files remain on the device for now; Eden will show "
        "a dedicated photo-cloud backup option before treating them as cloud "
        "protected."
    )

    cloud_conflict = bool(
        st.session_state.get("eden_workspace_conflict")
    )
    confirm_cloud_replace = True

    if cloud_conflict:
        st.warning(
            "The cloud copy changed or you restored an older snapshot. "
            "Backing up now will make this device's data the current cloud copy."
        )
        confirm_cloud_replace = st.checkbox(
            "I understand this will replace the current cloud workspace.",
            key="eden_confirm_cloud_replace"
        )

    if st.button(
            "Back Up Eden to Cloud",
            type="primary",
            disabled=not confirm_cloud_replace
    ):
        try:
            workspace = backup_local_workspace(
                store,
                session["user_id"]
            )
            st.success(
                f"Cloud backup complete: {len(workspace['files'])} data files saved."
            )
        except Exception as error:
            st.error(f"Cloud backup failed: {error}")

with restore_column:
    st.subheader("Restore from cloud")
    st.warning(
        "Restoring replaces this device's local Eden data. A timestamped local backup is created first."
    )
    confirm_restore = st.checkbox(
        "I understand this will replace local Eden data on this device."
    )

    if st.button(
            "Restore Eden from Cloud",
            disabled=not confirm_restore
    ):
        try:
            restored, result = restore_local_workspace(
                store,
                session["user_id"]
            )

            if restored:
                st.success(
                    "Cloud workspace restored: " + ", ".join(result)
                )
            else:
                st.info(result)
        except Exception as error:
            st.error(f"Cloud restore failed: {error}")

with st.expander("Recovery snapshots"):
    st.caption(
        "Eden keeps recent cloud snapshots before saving changed workspace "
        "data. Restore one only when you need to recover a previous state."
    )

    try:
        recovery_versions = store.list_workspace_versions(
            session["user_id"]
        )
    except Exception:
        recovery_versions = []

    if recovery_versions:
        version_labels = {
            (
                f"{version.get('created_at', 'Unknown time')} — "
                f"{version.get('reason', 'workspace snapshot')}"
            ): version["id"]
            for version in recovery_versions
        }
        selected_version_label = st.selectbox(
            "Choose a recovery snapshot",
            list(version_labels),
            key="eden_recovery_snapshot"
        )
        confirm_version_restore = st.checkbox(
            "I understand this replaces my current local Eden data.",
            key="eden_confirm_recovery_snapshot"
        )

        if st.button(
                "Restore Selected Snapshot",
                disabled=not confirm_version_restore
        ):
            try:
                restored, result = restore_workspace_version(
                    store,
                    session["user_id"],
                    version_labels[selected_version_label]
                )

                if restored:
                    st.success(
                        "Recovery snapshot restored: " + ", ".join(result)
                    )
                    st.info(
                        "This snapshot is restored on this device only. "
                        "Use Back Up Eden to Cloud if you want it to become "
                        "the current cloud workspace."
                    )
                else:
                    st.info(result)
            except Exception as error:
                st.error(f"Recovery snapshot failed: {error}")
    else:
        st.info(
            "No recovery snapshots yet. Run the cloud-storage SQL update "
            "once, then Eden will begin preserving them."
        )

st.divider()

if st.button("Sign Out"):
    sign_out()
    st.session_state.pop("eden_splash_seen", None)
    st.session_state["eden_splash_active"] = True
    st.switch_page("Frontend.py")
