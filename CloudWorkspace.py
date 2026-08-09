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
    store.save_workspace(user_id, workspace)
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

    if workspace and isinstance(workspace.get("files"), dict):
        _restore_workspace_files(workspace["files"], create_backups=False)

    st.session_state["eden_workspace_loaded_for_user"] = user_id
    st.session_state.pop("eden_cloud_workspace_hash", None)
    return True


def auto_backup_if_needed():
    """Sync changed local JSON data once per Streamlit rerun.

    No action is taken until the user has signed in. The fingerprint excludes
    the export timestamp so an unchanged workspace is never uploaded twice.
    """
    store, session = get_authenticated_workspace_store()

    if store is None:
        return "offline"

    workspace = export_local_workspace()
    encoded_files = json.dumps(
        workspace["files"],
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")
    fingerprint = hashlib.sha256(encoded_files).hexdigest()

    if st.session_state.get("eden_cloud_workspace_hash") == fingerprint:
        return "current"

    store.save_workspace(session["user_id"], workspace)
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
