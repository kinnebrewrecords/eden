"""Secure cloud workspace persistence for Eden.

This module uses only the Supabase publishable key. Database access is
protected by Supabase Auth and Row Level Security; never put a service-role
key in this application.
"""

import os

from supabase import create_client


class SupabaseWorkspaceStore:
    TABLE_NAME = "eden_workspaces"

    def __init__(self, project_url, publishable_key):
        if not project_url or not publishable_key:
            raise ValueError("Supabase URL and publishable key are required.")

        self.client = create_client(project_url, publishable_key)

    def set_session(self, access_token, refresh_token):
        """Attach a session and return its current token pair.

        Supabase may rotate the refresh token here, so callers must save the
        returned session instead of continuing to reuse the previous token.
        """
        response = self.client.auth.set_session(
            access_token,
            refresh_token
        )

        return getattr(response, "session", response)

    def load_workspace(self, user_id):
        response = (
            self.client.table(self.TABLE_NAME)
            .select("state")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        rows = getattr(response, "data", None) or []

        if not rows:
            return None

        return rows[0].get("state") or {}

    def save_workspace(self, user_id, state):
        """Create or replace the signed-in user's complete Eden workspace."""
        response = (
            self.client.table(self.TABLE_NAME)
            .upsert(
                {
                    "user_id": user_id,
                    "state": state
                },
                on_conflict="user_id"
            )
            .execute()
        )

        return response.data


def create_workspace_store():
    """Create a store from Streamlit secrets, with env-vars as a fallback."""
    project_url = os.getenv("SUPABASE_URL")
    publishable_key = os.getenv("SUPABASE_PUBLISHABLE_KEY")

    try:
        import streamlit as st

        project_url = project_url or st.secrets["supabase"]["url"]
        publishable_key = (
            publishable_key
            or st.secrets["supabase"]["publishable_key"]
        )
    except Exception:
        pass

    return SupabaseWorkspaceStore(project_url, publishable_key)
