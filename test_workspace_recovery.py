"""Regression checks for Eden workspace recovery archives."""

import json
import unittest

from CloudWorkspace import (
    determine_workspace_sync_action,
    merge_workspace_archives,
    parse_workspace_archive,
    validate_workspace_archive,
    workspace_archive_bytes,
    workspace_project_names
)


def workspace(projects=None, active_project=None, profile=None):
    files = {
        "projects.json": {
            "projects": projects or {},
            "active_project": active_project,
            "deleted_projects": []
        }
    }
    if profile is not None:
        files["user_profile.json"] = profile

    return {
        "schema_version": 1,
        "exported_at": "2026-08-24T12:00:00",
        "files": files
    }


class WorkspaceRecoveryTests(unittest.TestCase):
    def test_sync_action_uploads_local_when_cloud_base_is_unchanged(self):
        self.assertEqual(
            determine_workspace_sync_action(
                "local-new", "cloud-old", "cloud-old", True
            ),
            "upload_local"
        )

    def test_sync_action_restores_cloud_when_local_matches_old_base(self):
        self.assertEqual(
            determine_workspace_sync_action(
                "local-old", "cloud-new", "local-old", True
            ),
            "restore_cloud"
        )

    def test_sync_action_requires_choice_when_both_copies_changed(self):
        self.assertEqual(
            determine_workspace_sync_action(
                "local-new", "cloud-new", "old-base", True
            ),
            "conflict"
        )

    def test_sync_action_restores_cloud_to_an_empty_device(self):
        self.assertEqual(
            determine_workspace_sync_action(
                "empty", "cloud", None, False
            ),
            "restore_cloud"
        )

    def test_archive_round_trip_preserves_projects(self):
        original = workspace(
            {"barn": {"name": "Barn", "estimates": []}},
            "barn"
        )

        encoded = workspace_archive_bytes(original)
        decoded = parse_workspace_archive(encoded)

        self.assertEqual(workspace_project_names(decoded), ["Barn"])
        self.assertEqual(
            decoded["files"]["projects.json"]["active_project"],
            "barn"
        )

    def test_utf8_bom_upload_is_accepted(self):
        uploaded = b"\xef\xbb\xbf" + json.dumps(workspace()).encode("utf-8")
        self.assertEqual(parse_workspace_archive(uploaded)["schema_version"], 1)

    def test_unknown_files_are_rejected(self):
        archive = workspace()
        archive["files"]["secrets.toml"] = {}

        with self.assertRaisesRegex(ValueError, "unsupported files"):
            validate_workspace_archive(archive)

    def test_merge_never_overwrites_duplicate_project(self):
        current = workspace(
            {"barn": {"name": "Barn", "marker": "current"}},
            "barn",
            {"company": "Current Company"}
        )
        imported = workspace(
            {
                "barn": {"name": "Barn", "marker": "imported"},
                "fish": {"name": "Fish", "marker": "imported"}
            },
            "fish",
            {"company": "Imported Company"}
        )

        merged, report = merge_workspace_archives(current, imported)
        projects = merged["files"]["projects.json"]["projects"]

        self.assertEqual(projects["barn"]["marker"], "current")
        self.assertEqual(projects["barn (imported 2)"]["marker"], "imported")
        self.assertEqual(projects["fish"]["marker"], "imported")
        self.assertEqual(
            merged["files"]["user_profile.json"]["company"],
            "Current Company"
        )
        self.assertEqual(
            report["renamed"],
            [{"from": "Barn", "to": "Barn (Imported 2)"}]
        )

    def test_merge_uses_imported_active_project_only_when_current_has_none(self):
        current = workspace()
        imported = workspace(
            {"fish": {"name": "Fish", "estimates": []}},
            "fish"
        )

        merged, _ = merge_workspace_archives(current, imported)

        self.assertEqual(
            merged["files"]["projects.json"]["active_project"],
            "fish"
        )


if __name__ == "__main__":
    unittest.main()
