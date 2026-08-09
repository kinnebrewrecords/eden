"""Resolve Eden data files to the signed-in user's local workspace."""

import json
import re
import shutil
from pathlib import Path

import streamlit as st


SESSION_KEY = "eden_supabase_session"
WORKSPACE_FOLDER = ".eden_workspaces"
LEGACY_OWNER_FILE = ".eden_legacy_workspace_owner.json"


def _base_path(anchor_file):
    return Path(anchor_file).resolve().parent


def _user_id():
    session = st.session_state.get(SESSION_KEY, {})
    return session.get("user_id") if isinstance(session, dict) else None


def _safe_user_id(user_id):
    return re.sub(r"[^a-zA-Z0-9_-]", "", str(user_id))


def _legacy_owner_path(base_path):
    return base_path / LEGACY_OWNER_FILE


def _legacy_owner(base_path):
    path = _legacy_owner_path(base_path)

    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8")).get("user_id")
    except (OSError, json.JSONDecodeError):
        return None


def _claim_legacy_workspace(base_path, user_id):
    path = _legacy_owner_path(base_path)
    path.write_text(
        json.dumps({"user_id": user_id}, indent=4),
        encoding="utf-8"
    )


def workspace_file(anchor_file, filename):
    """Return a file path private to the active Eden account.

    The first signed-in account claims existing legacy JSON files once, so
    existing beta data is preserved. Other accounts begin with empty files
    instead of inheriting that account's projects or pricing.
    """
    base_path = _base_path(anchor_file)
    user_id = _user_id()

    if not user_id:
        return base_path / filename

    workspace_path = base_path / WORKSPACE_FOLDER / _safe_user_id(user_id)
    workspace_path.mkdir(parents=True, exist_ok=True)
    destination = workspace_path / filename

    if destination.exists():
        return destination

    legacy_path = base_path / filename
    legacy_owner = _legacy_owner(base_path)

    if legacy_owner is None and legacy_path.exists():
        _claim_legacy_workspace(base_path, user_id)
        legacy_owner = user_id

    if legacy_owner == user_id and legacy_path.exists():
        shutil.copy2(legacy_path, destination)

    return destination
