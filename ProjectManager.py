import json
from pathlib import Path


class ProjectManager:
    def __init__(self):
        self.file_path = Path(__file__).with_name("projects.json")
        self.data = {
            "projects": {},
            "active_project": None,
        }
        self.load()

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def load(self):
        if self.file_path.exists():
            with open(self.file_path, "r") as file:
                self.data = json.load(file)

    def create_project(self, name):
        name = name.strip().strip('"').strip("'")
        name = " ".join(name.split())

        key = name.lower()

        if not name:
            return False

        if key in self.data["projects"]:
            return False

        self.data["projects"][key] = {
            "name": name,
            "details": {
                "customer_name": "",
                "customer_email": "",
                "project_address": "",
                "proposal_title": "",
                "proposal_notes": "",
            },
            "estimates": [],
        }

        self.save()
        return True

    def select_project(self, name):
        key = " ".join(name.lower().split())

        if key not in self.data["projects"]:
            return False

        self.data["active_project"] = key
        self.save()
        return True

    def get_active_project(self):
        key = self.data["active_project"]

        if key is None:
            return None

        return self.data["projects"][key]

    def add_estimate(self, estimate):
        key=self.data["active_project"]

        if key is None:
            return False

        self.data["projects"][key]["estimates"].append(estimate)
        self.save()
        return True

    def get_active_material_takeoff(self):
        project = self.get_active_project()

        if project is None:
            return []

        totals = {}

        for estimate in project["estimates"]:
            for item in estimate.get("material_takeoff", []):
                name = item.get("item")
                unit = item.get("unit")
                quantity = item.get("quantity")

                if not name or not unit or quantity is None:
                    continue

                key = (name, unit)
                totals[key] = totals.get(key, 0) + quantity

        takeoff = []

        for (name, unit), quantity in sorted(totals.items()):
            if isinstance(quantity, float):
                quantity = round(quantity, 2)

            takeoff.append(
                {
                    "item": name,
                    "unit": unit,
                    "quantity": quantity
                }
            )

        return takeoff

    def delete_project(self, name):
        key = " ".join(name.lower().split())

        if key not in self.data["projects"]:
            return False

        del self.data["projects"][key]

        if self.data["active_project"] == key:
            self.data["active_project"] = None

        self.save()
        return True

    def list_projects(self):
        projects = []

        for key, project in sorted(self.data["projects"].items()):
            projects.append(
                {
                    "name": project["name"],
                    "estimate_count": len(project["estimates"]),
                    "is_active": key == self.data["active_project"]
                }
            )

        return projects

    def get_active_project_details(self):
        project = self.get_active_project()

        if project is None:
            return None

        defaults = {
            "customer_name": "",
            "customer_email": "",
            "project_address": "",
            "proposal_title": "",
            "proposal_notes": ""
        }

        return {
            **defaults,
            **project.get("details", {})
        }

    def update_active_project_details(self, details):
        project = self.get_active_project()

        if project is None:
            return False

        project["details"] = {
            "customer_name": details.get(
                "customer_name",
                ""
            ).strip(),
            "customer_email": details.get(
                "customer_email",
                ""
            ).strip(),
            "project_address": details.get(
                "project_address",
                ""
            ).strip(),
            "proposal_title": details.get(
                "proposal_title",
                ""
            ).strip(),
            "proposal_notes": details.get(
                "proposal_notes",
                ""
            ).strip()

        }

        self.save()
        return True

    def delete_estimate(self, estimate_index):
        project = self.get_active_project()

        if project is None:
            return False

        estimates = project["estimates"]

        if estimate_index < 0 or estimate_index >= len(estimates):
            return False

        del estimates[estimate_index]
        self.save()
        return True