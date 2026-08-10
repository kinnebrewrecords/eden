"""Verified Eden access checks for beta codes and subscriptions."""

import json
from datetime import datetime, timezone

from EdenAuth import get_authenticated_workspace_store


def _access_from_response(data):
    """Normalize the JSON shape returned by different Supabase clients."""
    if isinstance(data, dict):
        return data

    if isinstance(data, list) and data and isinstance(data[0], dict):
        return data[0]

    if isinstance(data, str):
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            return None

        if isinstance(parsed, dict):
            return parsed

    return None


def _direct_entitlement_access(store, user_id):
    """Fallback for an RPC response that is unavailable or malformed."""
    response = (
        store.client.table("eden_access_entitlements")
        .select("access_type, status, access_expires_at")
        .eq("user_id", user_id)
        .eq("status", "active")
        .limit(1)
        .execute()
    )

    rows = getattr(response, "data", None) or []
    if not rows:
        return {"has_access": False}

    entitlement = rows[0]
    expires_at = entitlement.get("access_expires_at")

    if expires_at:
        expires = datetime.fromisoformat(
            str(expires_at).replace("Z", "+00:00")
        )

        if expires <= datetime.now(timezone.utc):
            return {"has_access": False}

    return {
        "has_access": True,
        "access_type": entitlement.get("access_type"),
        "access_expires_at": expires_at
    }


def current_access():
    """Return the current user's verified Eden entitlement."""
    store, session = get_authenticated_workspace_store()

    if store is None or session is None:
        return {"has_access": False}

    rpc_error = None

    try:
        response = store.client.rpc("get_eden_access").execute()
        access = _access_from_response(getattr(response, "data", None))

        if access is not None:
            return access
    except Exception as error:
        rpc_error = str(error)

    try:
        return _direct_entitlement_access(store, session["user_id"])
    except Exception as error:
        return {
            "has_access": False,
            "error": str(error) if not rpc_error else rpc_error
        }
