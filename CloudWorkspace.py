"""Manual cloud backup and restore for Eden's current local JSON workspace."""

import json
import hashlib
import os
import tempfile
from copy import deepcopy
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


def validate_workspace_archive(workspace):
    """Return a safe schema-v1 workspace or raise a user-facing error."""
    if not isinstance(workspace, dict):
        raise ValueError("The backup must contain one Eden workspace object.")

    schema_version = workspace.get("schema_version", 1)
    if schema_version != 1:
        raise ValueError(
            f"Eden cannot import workspace schema {schema_version}."
        )

    files = workspace.get("files")
    if not isinstance(files, dict):
        raise ValueError("The backup does not contain an Eden files section.")

    unknown_files = set(files) - set(WORKSPACE_FILES)
    if unknown_files:
        raise ValueError(
            "The backup contains unsupported files: "
            + ", ".join(sorted(unknown_files))
        )

    validated_files = {}
    for file_name, data in files.items():
        if not isinstance(data, dict):
            raise ValueError(f"{file_name} must contain a JSON object.")
        validated_files[file_name] = deepcopy(data)

    projects_file = validated_files.get("projects.json")
    if projects_file is not None:
        projects = projects_file.get("projects", {})
        deleted_projects = projects_file.get("deleted_projects", [])
        if not isinstance(projects, dict):
            raise ValueError("projects.json has an invalid projects section.")
        if not isinstance(deleted_projects, list):
            raise ValueError(
                "projects.json has an invalid recently-deleted section."
            )

    return {
        "schema_version": 1,
        "exported_at": str(
            workspace.get("exported_at")
            or datetime.now().isoformat(timespec="seconds")
        ),
        "files": validated_files
    }


def parse_workspace_archive(uploaded_data):
    """Decode and validate an uploaded Eden JSON backup."""
    if isinstance(uploaded_data, bytes):
        try:
            uploaded_data = uploaded_data.decode("utf-8-sig")
        except UnicodeDecodeError as error:
            raise ValueError("The backup is not valid UTF-8 JSON.") from error

    if isinstance(uploaded_data, str):
        try:
            uploaded_data = json.loads(uploaded_data)
        except json.JSONDecodeError as error:
            raise ValueError("The selected file is not valid JSON.") from error

    return validate_workspace_archive(uploaded_data)


def workspace_archive_bytes(workspace):
    """Serialize one validated workspace for a browser download."""
    validated = validate_workspace_archive(workspace)
    return json.dumps(validated, indent=4).encode("utf-8")


def workspace_project_names(workspace):
    """Return the display names present in a workspace archive."""
    validated = validate_workspace_archive(workspace)
    projects = (
        validated["files"]
        .get("projects.json", {})
        .get("projects", {})
    )
    return [
        project.get("name", key)
        for key, project in projects.items()
        if isinstance(project, dict)
    ]


def merge_workspace_archives(current_workspace, imported_workspace):
    """Merge projects without silently replacing current account data."""
    current = validate_workspace_archive(current_workspace)
    imported = validate_workspace_archive(imported_workspace)
    merged = deepcopy(current)
    merged["exported_at"] = datetime.now().isoformat(timespec="seconds")
    merged_files = merged["files"]

    # Non-project files fill gaps only. Existing profile, pricing, and
    # preferences always win during a merge; Replace is the explicit path
    # for changing them.
    for file_name, data in imported["files"].items():
        if file_name != "projects.json" and file_name not in merged_files:
            merged_files[file_name] = deepcopy(data)

    incoming_projects_file = imported["files"].get("projects.json")
    if incoming_projects_file is None:
        return merged, {"imported": [], "renamed": []}

    current_projects_file = merged_files.setdefault(
        "projects.json",
        {"projects": {}, "active_project": None, "deleted_projects": []}
    )
    current_projects = current_projects_file.setdefault("projects", {})
    imported_projects = incoming_projects_file.get("projects", {})
    key_map = {}
    imported_names = []
    renamed = []

    for incoming_key, incoming_project in imported_projects.items():
        if not isinstance(incoming_project, dict):
            continue

        original_name = str(
            incoming_project.get("name") or incoming_key
        ).strip() or "Imported Project"
        candidate_name = original_name
        candidate_key = " ".join(candidate_name.lower().split())
        suffix = 1

        while candidate_key in current_projects:
            suffix += 1
            candidate_name = f"{original_name} (Imported {suffix})"
            candidate_key = " ".join(candidate_name.lower().split())

        imported_project = deepcopy(incoming_project)
        imported_project["name"] = candidate_name
        current_projects[candidate_key] = imported_project
        key_map[incoming_key] = candidate_key
        imported_names.append(candidate_name)

        if candidate_name != original_name:
            renamed.append(
                {"from": original_name, "to": candidate_name}
            )

    if current_projects_file.get("active_project") is None:
        incoming_active = incoming_projects_file.get("active_project")
        current_projects_file["active_project"] = key_map.get(incoming_active)

    current_deleted = current_projects_file.setdefault(
        "deleted_projects", []
    )
    existing_deleted_ids = {
        item.get("id")
        for item in current_deleted
        if isinstance(item, dict)
    }
    for deleted_project in incoming_projects_file.get(
            "deleted_projects", []
    ):
        if (
                isinstance(deleted_project, dict)
                and deleted_project.get("id") not in existing_deleted_ids
        ):
            current_deleted.append(deepcopy(deleted_project))

    return merged, {"imported": imported_names, "renamed": renamed}


def _atomic_write_json(path, data):
    """Write JSON completely before replacing the destination file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent
    )

    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary_name, path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except OSError:
            pass
        raise


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


def export_cloud_workspace(store, user_id):
    """Load one authenticated account's workspace without changing it."""
    workspace = store.load_workspace(user_id)
    if not workspace:
        return None
    return validate_workspace_archive(workspace)


def import_workspace_archive(store, user_id, workspace, mode):
    """Merge or replace an entitled account's workspace safely."""
    imported = validate_workspace_archive(workspace)
    current = store.load_workspace(user_id)

    if current:
        current = validate_workspace_archive(current)
    else:
        current = {
            "schema_version": 1,
            "exported_at": datetime.now().isoformat(timespec="seconds"),
            "files": {}
        }

    normalized_mode = str(mode).strip().lower()
    if normalized_mode == "merge":
        result, report = merge_workspace_archives(current, imported)
    elif normalized_mode == "replace":
        result = deepcopy(imported)
        result["exported_at"] = datetime.now().isoformat(
            timespec="seconds"
        )
        report = {
            "imported": workspace_project_names(imported),
            "renamed": []
        }
    else:
        raise ValueError("Import mode must be Merge or Replace.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recovery_directory = _file_path("projects.json").parent
    local_backup_path = recovery_directory / (
        f"workspace_before_import_{timestamp}.json"
    )
    _atomic_write_json(local_backup_path, current)

    _save_workspace_safely(
        store,
        user_id,
        result,
        f"{normalized_mode}_import"
    )
    _restore_workspace_files(result["files"], create_backups=True)
    st.session_state["eden_cloud_workspace_hash"] = (
        _workspace_fingerprint(result)
    )
    st.session_state.pop("eden_workspace_conflict", None)

    return result, report, current


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
            _atomic_write_json(
                backup_path,
                json.loads(path.read_text(encoding="utf-8"))
            )

        _atomic_write_json(path, data)
        restored_files.append(file_name)

    return restored_files
