"""Minimal Supabase email/password authentication for Eden beta."""

import json

import streamlit as st

from SupabaseStorage import create_workspace_store


SESSION_KEY = "eden_supabase_session"
COOKIE_KEY = "eden-auth-session"
COOKIE_MANAGER_KEY = "eden_cookie_manager"
COOKIE_LAST_VALUE_KEY = "eden_cookie_last_value"
SIGNED_OUT_KEY = "eden_signed_out"
LOGOUT_QUERY_KEY = "eden_logout"


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


def _store_session(session):
    if not session or not session.user:
        return None

    data = {
        "user_id": session.user.id,
        "email": session.user.email,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token
    }
    st.session_state.pop(SIGNED_OUT_KEY, None)
    st.query_params.pop(LOGOUT_QUERY_KEY, None)
    st.session_state[SESSION_KEY] = data
    _save_session_cookie(data)
    return data


def current_user():
    if st.query_params.get(LOGOUT_QUERY_KEY) == "1":
        # A logout rerun can occur before the browser receives the cookie
        # deletion. Run the cleanup again from the login screen, where no
        # cloud refresh can compete with it.
        st.query_params.pop(LOGOUT_QUERY_KEY, None)
        _clear_session_cookie()
        return None

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


def sign_up(email, password):
    store = create_workspace_store()
    response = store.client.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )

    return _store_session(response.session), response


def sign_in(email, password):
    store = create_workspace_store()
    response = store.client.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )

    return _store_session(response.session)


def sign_out():
    # Mark the current Streamlit session as signed out before contacting any
    # external service. This makes logout immediate even if Supabase is slow
    # or the browser-cookie update needs an extra render to complete.
    session = st.session_state.get(SESSION_KEY)
    st.session_state[SIGNED_OUT_KEY] = True
    st.session_state.pop(SESSION_KEY, None)
    st.query_params[LOGOUT_QUERY_KEY] = "1"

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

    store = create_workspace_store()

    try:
        refreshed_session = store.set_session(
            session["access_token"],
            session["refresh_token"]
        )
    except Exception:
        # An old refresh token cannot be used again. Clear only Eden's local
        # browser session and let the user sign in again.
        st.session_state.pop(SESSION_KEY, None)
        _clear_session_cookie()
        return None, None

    updated_session = _store_session(refreshed_session)

    if not updated_session:
        st.session_state.pop(SESSION_KEY, None)
        _clear_session_cookie()
        return None, None

    return store, updated_session
