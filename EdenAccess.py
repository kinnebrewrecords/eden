"""Verified Eden access checks for beta codes and subscriptions."""

from EdenAuth import get_authenticated_workspace_store


def current_access():
    """Return the current user's verified Eden entitlement."""
    store, _ = get_authenticated_workspace_store()

    if store is None:
        return {"has_access": False}

    try:
        response = store.client.rpc("get_eden_access").execute()
    except Exception as error:
        return {
            "has_access": False,
            "error": str(error)
        }

    if isinstance(response.data, dict):
        return response.data

    return {"has_access": False}
