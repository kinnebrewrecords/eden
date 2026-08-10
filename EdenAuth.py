"""Minimal Supabase email/password authentication for Eden beta."""

import json
from datetime import datetime, timezone

import streamlit as st

from SupabaseStorage import create_workspace_store


SESSION_KEY = "eden_supabase_session"
COOKIE_KEY = "eden-auth-session"
COOKIE_MANAGER_KEY = "eden_cookie_manager"
COOKIE_LAST_VALUE_KEY = "eden_cookie_last_value"
SIGNED_OUT_KEY = "eden_signed_out"
WORKSPACE_STORE_KEY = "eden_workspace_store"
WORKSPACE_STORE_USER_KEY = "eden_workspace_store_user_id"


def _get_cookie_manager():
    """Return Eden's encrypted browser-cookie manager when available."""
    existing_manager = st.session_state.get(COOKIE_MANAGER_KEY)

    if existing_manager is not None:
        return existing_manager

    try:
        from streamlit_cookies_manager import EncryptedCookieManager
    except ImportError:
        return None

    try:
        password = st.secrets["supabase"]["cookie_password"]
    except Exception:
        return None

    cookies = EncryptedCookieManager(
        prefix="eden/",
        password=password
    )

    if not cookies.ready():
        st.stop()

    st.session_state[COOKIE_MANAGER_KEY] = cookies
    return cookies


def _save_session_cookie(data):
    cookies = _get_cookie_manager()

    if cookies is None:
        return

    value = json.dumps(data)

    # The cookie component may only be saved once for a given change during
    # a Streamlit render.  Re-saving identical data creates a duplicate
    # component key and prevents sign-in from completing.
    if st.session_state.get(COOKIE_LAST_VALUE_KEY) == value:
        return

    cookies[COOKIE_KEY] = value
    cookies.save()
    st.session_state[COOKIE_LAST_VALUE_KEY] = value


def _clear_session_cookie():
    cookies = _get_cookie_manager()

    if cookies is None:
        return

    if st.session_state.get(COOKIE_LAST_VALUE_KEY) is None:
        return

    if COOKIE_KEY in cookies:
        del cookies[COOKIE_KEY]
        cookies.save()

    st.session_state[COOKIE_LAST_VALUE_KEY] = None


def _store_session(session, verified_access=None):
    if not session or not session.user:
        return None

    previous_session = st.session_state.get(SESSION_KEY, {})

    if verified_access is None:
        verified_access = (
            previous_session.get("access_verified_user_id")
            == session.user.id
        )

    data = {
        "user_id": session.user.id,
        "email": session.user.email,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token
    }

    if verified_access:
        data["access_verified_user_id"] = session.user.id

    st.session_state.pop(SIGNED_OUT_KEY, None)
    st.session_state[SESSION_KEY] = data
    _save_session_cookie(data)
    return data


def current_user():
    if st.session_state.get(SIGNED_OUT_KEY):
        return None

    session = st.session_state.get(SESSION_KEY)

    if session:
        return session

    cookies = _get_cookie_manager()

    if cookies is None:
        return None

    raw_session = cookies.get(COOKIE_KEY)

    if not raw_session:
        st.session_state[COOKIE_LAST_VALUE_KEY] = None
        return None

    st.session_state[COOKIE_LAST_VALUE_KEY] = raw_session

    try:
        session = json.loads(raw_session)
    except (TypeError, json.JSONDecodeError):
        _clear_session_cookie()
        return None

    required_keys = {
        "user_id",
        "email",
        "access_token",
        "refresh_token"
    }

    if not required_keys.issubset(session):
        _clear_session_cookie()
        return None

    st.session_state[SESSION_KEY] = session
    return session


def mark_current_session_access_verified():
    """Persist a successful Eden-access check in the existing login cookie."""
    session = current_user()

    if not session:
        return

    user_id = session["user_id"]
    if session.get("access_verified_user_id") == user_id:
        return

    verified_session = dict(session)
    verified_session["access_verified_user_id"] = user_id
    st.session_state[SESSION_KEY] = verified_session
    _save_session_cookie(verified_session)


def sign_up(email, password):
    store = create_workspace_store()
    response = store.client.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )

    return _store_session(response.session, False), response


def _has_eden_access(store, user_id):
    """Check entitlement while the client holds a newly signed-in session."""
    try:
        response = store.client.rpc("get_eden_access").execute()
        data = getattr(response, "data", None)

        if isinstance(data, dict):
            return bool(data.get("has_access"))

        if isinstance(data, list) and data and isinstance(data[0], dict):
            return bool(data[0].get("has_access"))

        if isinstance(data, str):
            parsed = json.loads(data)
            if isinstance(parsed, dict):
                return bool(parsed.get("has_access"))
    except Exception:
        pass

    try:
        response = (
            store.client.table("eden_access_entitlements")
            .select("access_expires_at")
            .eq("user_id", user_id)
            .eq("status", "active")
            .limit(1)
            .execute()
        )
        rows = getattr(response, "data", None) or []

        if not rows:
            return False

        expires_at = rows[0].get("access_expires_at")
        if not expires_at:
            return True

        expires = datetime.fromisoformat(
            str(expires_at).replace("Z", "+00:00")
        )
        return expires > datetime.now(timezone.utc)
    except Exception:
        pass

    return False


def sign_in(email, password):
    store = create_workspace_store()
    response = store.client.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )

    return _store_session(
        response.session,
        _has_eden_access(store, response.session.user.id)
    )


def sign_out():
    # Mark the current Streamlit session as signed out before contacting any
    # external service. This makes logout immediate even if Supabase is slow
    # or the browser-cookie update needs an extra render to complete.
    session = st.session_state.get(SESSION_KEY)
    st.session_state[SIGNED_OUT_KEY] = True

    # Account-specific UI, chat, cloud, and project context must never be
    # carried into the next sign-in in the same browser session.
    for key in [
            SESSION_KEY,
            WORKSPACE_STORE_KEY,
            WORKSPACE_STORE_USER_KEY,
            "eden_workspace_loaded_for_user",
            "eden_access_verified_user_id",
            "eden_cloud_workspace_hash",
            "eden_project_workspace_path",
            "eden_active_project_name",
            "eden_project_switcher",
            "eden_web_engine",
            "eden_web_engine_user_id",
            "eden_browser_messages",
            "eden_pending_command",
            "eden_pending_answers",
            "eden_ai"
    ]:
        st.session_state.pop(key, None)

    _clear_session_cookie()

    if session:
        try:
            store = create_workspace_store()
            store.set_session(
                session["access_token"],
                session["refresh_token"]
            )
            store.client.auth.sign_out()
        except Exception:
            # Local sign-out still succeeds if the network request fails.
            pass


def get_authenticated_workspace_store():
    session = current_user()

    if not session:
        return None, None

    cached_store = st.session_state.get(WORKSPACE_STORE_KEY)
    cached_user_id = st.session_state.get(WORKSPACE_STORE_USER_KEY)

    if cached_store is not None and cached_user_id == session["user_id"]:
        return cached_store, session

    store = create_workspace_store()

    try:
        refreshed_session = store.set_session(
            session["access_token"],
            session["refresh_token"]
        )
    except Exception:
        # Cloud syncing must never sign the user out. A token can briefly be
        # stale after a browser reload because Supabase rotates refresh tokens.
        # Keep the authenticated Eden session and try cloud sync again later.
        return None, None

    updated_session = _store_session(refreshed_session)

    if not updated_session:
        st.session_state.pop(SESSION_KEY, None)
        _clear_session_cookie()
        return None, None

    st.session_state[WORKSPACE_STORE_KEY] = store
    st.session_state[WORKSPACE_STORE_USER_KEY] = (
        updated_session["user_id"]
    )

    return store, updated_session


def refresh_authenticated_workspace_store():
    """Force a fresh Supabase token refresh for the current browser session."""
    st.session_state.pop(WORKSPACE_STORE_KEY, None)
    st.session_state.pop(WORKSPACE_STORE_USER_KEY, None)
    return get_authenticated_workspace_store()
