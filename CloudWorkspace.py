"""Manual cloud backup and restore for Eden's current local JSON workspace."""

import json
import hashlib
from datetime import datetime
from pathlib import Path

import streamlit as st

from EdenAuth import get_authenticated_workspace_store
from WorkspaceFiles import workspace_file


WORKSPACE_FILES = [
    "projects.json",
    "user_profile.json",
    "estimating_preferences.json",
    "pricing.json",
    "memory.json"
]


def _workspace_fingerprint(workspace):
    """Return a stable fingerprint without relying on export timestamps."""
    files = workspace.get("files", {}) if workspace else {}
    encoded_files = json.dumps(
        files,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded_files).hexdigest()


def _workspace_has_user_data(workspace):
    """Do not treat an empty first-run folder as a backup candidate."""
    files = workspace.get("files", {}) if workspace else {}
    profile = files.get("user_profile.json", {})
    projects = files.get("projects.json", {}).get("projects", {})
    pricing = files.get("pricing.json", {}).get("regions", {})

    if not isinstance(profile, dict):
        profile = {}

    if not isinstance(projects, dict):
        projects = {}

    if not isinstance(pricing, dict):
        pricing = {}

    return bool(
        projects or
        (profile.get("name") and profile.get("company")) or
        any(
            isinstance(region, dict) and region.get("material_prices")
            for region in pricing.values()
        )
    )


def _save_workspace_safely(store, user_id, workspace, reason):
    """Preserve snapshots without letting optional versioning block a save."""
    previous_workspace = store.load_workspace(user_id)

    try:
        if (
                previous_workspace and
                _workspace_fingerprint(previous_workspace)
                != _workspace_fingerprint(workspace)
        ):
            store.save_workspace_version(
                user_id,
                previous_workspace,
                f"before_{reason}"
            )

        store.save_workspace_version(user_id, workspace, reason)
    except Exception:
        # Version snapshots become active after the companion SQL migration.
        # The current workspace save remains available until then.
        pass

    store.save_workspace(user_id, workspace)


def _file_path(file_name):
    return workspace_file(__file__, file_name)


def export_local_workspace():
    files = {}

    for file_name in WORKSPACE_FILES:
        path = _file_path(file_name)

        if not path.exists():
            continue

        with open(path, "r", encoding="utf-8") as file:
            files[file_name] = json.load(file)

    return {
        "schema_version": 1,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "files": files
    }


def backup_local_workspace(store, user_id):
    workspace = export_local_workspace()
    _save_workspace_safely(store, user_id, workspace, "manual_backup")
    st.session_state["eden_cloud_workspace_hash"] = (
        _workspace_fingerprint(workspace)
    )
    st.session_state.pop("eden_workspace_conflict", None)
    return workspace


def activate_workspace_for_current_user():
    """Load the signed-in account's cloud workspace before rendering Eden."""
    store, session = get_authenticated_workspace_store()

    if store is None or session is None:
        return False

    user_id = session["user_id"]

    if st.session_state.get("eden_workspace_loaded_for_user") == user_id:
        return True

    workspace = store.load_workspace(user_id)
    local_workspace = export_local_workspace()

    if workspace and isinstance(workspace.get("files"), dict):
        cloud_fingerprint = _workspace_fingerprint(workspace)
        local_has_data = _workspace_has_user_data(local_workspace)
        local_fingerprint = _workspace_fingerprint(local_workspace)

        if local_has_data and local_fingerprint != cloud_fingerprint:
            # Never overwrite meaningful local work simply because a cloud
            # copy exists. The user can decide between restore and manual
            # backup in Account & Cloud.
            st.session_state["eden_workspace_conflict"] = True
            st.session_state["eden_cloud_workspace_hash"] = cloud_fingerprint
        else:
            _restore_workspace_files(workspace["files"], create_backups=False)
            st.session_state.pop("eden_workspace_conflict", None)
            st.session_state["eden_cloud_workspace_hash"] = cloud_fingerprint
    else:
        st.session_state.pop("eden_workspace_conflict", None)
        st.session_state.pop("eden_cloud_workspace_hash", None)

    st.session_state["eden_workspace_loaded_for_user"] = user_id
    return True


def auto_backup_if_needed():
    """Sync changed local JSON data once per Streamlit rerun.

    No action is taken until the user has signed in. The fingerprint excludes
    the export timestamp so an unchanged workspace is never uploaded twice.
    """
    store, session = get_authenticated_workspace_store()

    if store is None:
        return "offline"

    # A backup is allowed only after this account's workspace has been
    # loaded successfully. This prevents an empty local folder from
    # overwriting a returning user's cloud workspace after a load failure.
    if (
            st.session_state.get("eden_workspace_loaded_for_user")
            != session["user_id"]
    ):
        return "not_loaded"

    if st.session_state.get("eden_workspace_conflict"):
        return "cloud_changed"

    workspace = export_local_workspace()
    if not _workspace_has_user_data(workspace):
        return "waiting_for_setup"

    fingerprint = _workspace_fingerprint(workspace)
    known_cloud_fingerprint = st.session_state.get(
        "eden_cloud_workspace_hash"
    )
    current_cloud_workspace = store.load_workspace(session["user_id"])

    if current_cloud_workspace:
        current_cloud_fingerprint = _workspace_fingerprint(
            current_cloud_workspace
        )

        if (
                known_cloud_fingerprint and
                current_cloud_fingerprint != known_cloud_fingerprint
        ):
            return "cloud_changed"

        if not known_cloud_fingerprint:
            # Do not decide that local data should replace an existing cloud
            # workspace unless this session loaded that exact workspace first.
            return "cloud_changed"

    if known_cloud_fingerprint == fingerprint:
        return "current"

    _save_workspace_safely(
        store,
        session["user_id"],
        workspace,
        "automatic_backup"
    )
    st.session_state["eden_cloud_workspace_hash"] = fingerprint
    return "synced"


def restore_local_workspace(store, user_id):
    workspace = store.load_workspace(user_id)

    if not workspace:
        return False, "No cloud backup exists for this account yet."

    files = workspace.get("files")

    if not isinstance(files, dict):
        return False, "The cloud backup format is not valid."

    restored_files = _restore_workspace_files(files, create_backups=True)

    if not restored_files:
        return False, "The cloud backup did not contain Eden workspace data."

    st.session_state["eden_cloud_workspace_hash"] = (
        _workspace_fingerprint(workspace)
    )
    st.session_state.pop("eden_workspace_conflict", None)

    return True, restored_files


def restore_workspace_version(store, user_id, version_id):
    """Restore one prior cloud snapshot for this exact account only."""
    workspace = store.load_workspace_version(user_id, version_id)

    if not workspace:
        return False, "That recovery snapshot could not be found."

    files = workspace.get("files")

    if not isinstance(files, dict):
        return False, "The recovery snapshot format is not valid."

    restored_files = _restore_workspace_files(files, create_backups=True)

    if not restored_files:
        return False, "The recovery snapshot did not contain Eden data."

    st.session_state["eden_cloud_workspace_hash"] = (
        _workspace_fingerprint(workspace)
    )
    # The cloud's current workspace is intentionally left unchanged. Keep
    # automatic sync paused until the user explicitly chooses to back up this
    # restored version as the new cloud current workspace.
    st.session_state["eden_workspace_conflict"] = True

    return True, restored_files


def _restore_workspace_files(files, create_backups):
    restored_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for file_name, data in files.items():
        if file_name not in WORKSPACE_FILES:
            continue

        path = _file_path(file_name)

        if create_backups and path.exists():
            backup_path = path.with_name(
                f"{path.stem}_cloud_restore_backup_{timestamp}.json"
            )
            backup_path.write_text(
                path.read_text(encoding="utf-8"),
                encoding="utf-8"
            )

        path.write_text(
            json.dumps(data, indent=4),
            encoding="utf-8"
        )
        restored_files.append(file_name)

    return restored_files
