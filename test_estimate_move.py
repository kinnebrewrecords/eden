"""Regression checks for moving a saved estimate between projects."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from Brain import Brain
from ProjectManager import ProjectManager


class EstimateMoveTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        project_file = (
            Path(self.temporary_directory.name) / "projects.json"
        )

        with patch(
                "ProjectManager.workspace_file",
                return_value=project_file
        ):
            self.manager = ProjectManager()

        self.manager.data = {
            "active_project": "barn",
            "deleted_projects": [],
            "projects": {
                "barn": {
                    "name": "Barn",
                    "estimates": [
                        {"type": "Concrete Slab"},
                        {"type": "Framed Wall"}
                    ]
                },
                "fish": {
                    "name": "Fish",
                    "estimates": []
                }
            }
        }

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_move_only_newest_estimate_and_select_destination(self):
        result = self.manager.move_last_estimate_to_project("  FISH  ")

        self.assertTrue(result["ok"])
        self.assertEqual(result["source_project"], "Barn")
        self.assertEqual(result["destination_project"], "Fish")
        self.assertEqual(
            self.manager.data["projects"]["barn"]["estimates"],
            [{"type": "Concrete Slab"}]
        )
        self.assertEqual(
            self.manager.data["projects"]["fish"]["estimates"],
            [{"type": "Framed Wall"}]
        )
        self.assertEqual(self.manager.data["active_project"], "fish")

    def test_unknown_destination_does_not_change_estimates(self):
        result = self.manager.move_last_estimate_to_project("Missing")

        self.assertEqual(
            result,
            {"ok": False, "reason": "destination_not_found"}
        )
        self.assertEqual(
            len(self.manager.data["projects"]["barn"]["estimates"]),
            2
        )

    def test_brain_understands_wrong_project_phrase(self):
        memory = Mock()
        commands = Mock()
        commands.move_last_estimate_command.return_value = "moved"
        brain = Brain(memory, commands)

        response = brain.think("wrong project, save to Fish instead")

        self.assertEqual(response, "moved")
        commands.move_last_estimate_command.assert_called_once_with("fish")

    def test_brain_understands_save_last_estimate_phrase(self):
        memory = Mock()
        commands = Mock()
        commands.move_last_estimate_command.return_value = "moved"
        brain = Brain(memory, commands)

        response = brain.think("save last estimate to Fish")

        self.assertEqual(response, "moved")
        commands.move_last_estimate_command.assert_called_once_with("fish")

    def test_brain_ignores_chat_punctuation_around_project_name(self):
        memory = Mock()
        commands = Mock()
        commands.move_last_estimate_command.return_value = "moved"
        brain = Brain(memory, commands)

        response = brain.think('save last estimate to.... "Fish".')

        self.assertEqual(response, "moved")
        commands.move_last_estimate_command.assert_called_once_with("fish")


if __name__ == "__main__":
    unittest.main()
