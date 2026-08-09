"""Manual cloud backup and restore for Eden's current local JSON workspace."""

import json
import hashlib
from datetime import datetime
from pathlib import Path

import streamlit as st

from EdenAuth import get_authenticated_workspace_store


WORKSPACE_FILES = [
    "projects.json",
    "user_profile.json",
    "estimating_preferences.json",
    "pricing.json",
    "memory.json"
]


def _file_path(file_name):
    return Path(__file__).with_name(file_name)


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

    restored_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for file_name, data in files.items():
        if file_name not in WORKSPACE_FILES:
            continue

        path = _file_path(file_name)

        if path.exists():
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

    if not restored_files:
        return False, "The cloud backup did not contain Eden workspace data."

    return True, restored_files
