import streamlit as st

from CloudWorkspace import (
    activate_workspace_for_current_user,
    backup_local_workspace,
    export_cloud_workspace,
    import_workspace_archive,
    parse_workspace_archive,
    restore_local_workspace,
    restore_workspace_version,
    workspace_archive_bytes,
    workspace_project_names
)
from EdenAuth import (
    current_user,
    get_authenticated_workspace_store,
    sign_out
)
from EdenAccess import current_access
from EdenTheme import apply_eden_theme
from Sidebar import render_sidebar
from AuthGate import require_authenticated_login


st.set_page_config(
    page_title="Account & Cloud",
    layout="wide"
)

apply_eden_theme()
user = require_authenticated_login()

store, session = get_authenticated_workspace_store()

if store is None or session is None:
    st.error("Your account session has expired. Please sign in again.")
    sign_out()
    st.rerun()

access = current_access()
has_eden_access = bool(access.get("has_access"))

if has_eden_access:
    try:
        activate_workspace_for_current_user()
    except Exception:
        st.error(
            "Eden could not safely load your workspace. Your data was not "
            "changed. Please refresh and try again."
        )
        st.stop()

    render_sidebar(show_command_center=False)

st.title("Account & Cloud")
st.caption(
    "Sign in to back up your Eden workspace securely and restore it on another device."
)

st.success(f"Signed in as {user.get('email', 'your Eden account')}.")

try:
    cloud_workspace = export_cloud_workspace(store, session["user_id"])
except Exception:
    cloud_workspace = None
    st.error(
        "Eden could not read this account's cloud workspace right now. "
        "Nothing was changed."
    )

st.subheader("Recovery Center")

if cloud_workspace:
    cloud_project_names = workspace_project_names(cloud_workspace)
    project_summary = (
        ", ".join(cloud_project_names)
        if cloud_project_names
        else "No named projects"
    )
    st.write(
        f"Current cloud workspace: {len(cloud_project_names)} projects"
    )
    st.caption(project_summary)
    st.download_button(
        "Download Current Cloud Workspace",
        data=workspace_archive_bytes(cloud_workspace),
        file_name=(
            "eden_workspace_"
            + session["user_id"][:8]
            + ".json"
        ),
        mime="application/json",
        type="primary" if not has_eden_access else "secondary"
    )
else:
    st.info("No current cloud workspace exists for this account yet.")

if not has_eden_access:
    st.warning(
        "This account does not currently have Eden access. Recovery remains "
        "available, but estimating, cloud backup, restore, and import stay "
        "locked."
    )

    with st.expander("Download a recovery snapshot"):
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
            selected_label = st.selectbox(
                "Recovery snapshot",
                list(version_labels),
                key="eden_restricted_recovery_snapshot"
            )
            selected_workspace = store.load_workspace_version(
                session["user_id"],
                version_labels[selected_label]
            )

            if selected_workspace:
                st.download_button(
                    "Download Selected Snapshot",
                    data=workspace_archive_bytes(selected_workspace),
                    file_name="eden_recovery_snapshot.json",
                    mime="application/json"
                )
        else:
            st.info("No recovery snapshots are available for this account.")

    if st.button("Sign Out"):
        sign_out()
        st.switch_page("pages/1_Login.py")

    st.stop()

st.divider()

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

with st.expander("Import or merge an Eden workspace"):
    st.caption(
        "Merge adds projects without replacing current projects. Replace "
        "makes the uploaded backup the complete current workspace. Eden "
        "creates a pre-import backup first."
    )
    uploaded_workspace = st.file_uploader(
        "Eden workspace backup",
        type=["json"],
        key="eden_workspace_import"
    )

    imported_workspace = None
    if uploaded_workspace is not None:
        if uploaded_workspace.size > 10 * 1024 * 1024:
            st.error("Workspace backups must be 10 MB or smaller.")
        else:
            try:
                imported_workspace = parse_workspace_archive(
                    uploaded_workspace.getvalue()
                )
                imported_project_names = workspace_project_names(
                    imported_workspace
                )
                st.success(
                    f"Valid Eden backup: {len(imported_project_names)} "
                    "projects found."
                )
                if imported_project_names:
                    st.caption(", ".join(imported_project_names))
            except ValueError as error:
                st.error(str(error))

    import_mode = st.radio(
        "Import mode",
        ["Merge", "Replace"],
        horizontal=True,
        help=(
            "Merge keeps current profile, settings, and pricing and adds "
            "projects. Replace imports every file in the backup."
        )
    )

    if import_mode == "Replace":
        st.warning(
            "Replace will make the uploaded backup the current cloud and "
            "local workspace."
        )
        import_confirmation = st.checkbox(
            "I understand Replace changes the complete current workspace.",
            key="eden_confirm_workspace_replace"
        )
    else:
        import_confirmation = st.checkbox(
            "I reviewed this backup and want to merge its projects.",
            key="eden_confirm_workspace_merge"
        )

    if st.button(
            f"{import_mode} Workspace",
            disabled=(
                imported_workspace is None
                or not import_confirmation
            )
    ):
        try:
            _, import_report, previous_workspace = import_workspace_archive(
                store,
                session["user_id"],
                imported_workspace,
                import_mode
            )
            st.session_state["eden_pre_import_download"] = (
                workspace_archive_bytes(previous_workspace)
            )
            st.success(
                f"{import_mode} complete: "
                f"{len(import_report['imported'])} projects imported."
            )

            if import_report["renamed"]:
                st.info(
                    "Duplicate project names were preserved as: "
                    + ", ".join(
                        item["to"]
                        for item in import_report["renamed"]
                    )
                )
        except Exception:
            st.error(
                "Eden could not import that workspace. Nothing else should "
                "be changed; download the current cloud workspace and try "
                "again."
            )

    previous_download = st.session_state.get("eden_pre_import_download")
    if previous_download:
        st.download_button(
            "Download Pre-Import Backup",
            data=previous_download,
            file_name="eden_workspace_before_import.json",
            mime="application/json"
        )

st.divider()

if st.button("Sign Out"):
    sign_out()
    st.session_state.pop("eden_splash_seen", None)
    st.session_state["eden_splash_active"] = True
    st.switch_page("Frontend.py")
