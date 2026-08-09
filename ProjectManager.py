import json
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4


class ProjectManager:
    PROJECT_RECOVERY_DAYS = 30

    PROJECT_STATUSES = [
        "Active",
        "Completed",
        "On Hold",
        "Lost",
        "Archived"
    ]

    SCHEDULE_ITEM_STATUSES = [
        "Upcoming",
        "In Progress",
        "Complete",
        "Blocked"
    ]

    PHASE_STATUSES = [
        "Not Started",
        "In Progress",
        "Complete",
        "On Hold"
    ]

    EQUIPMENT_STATUSES = [
        "Planned",
        "Reserved",
        "On Site",
        "In Use",
        "Returned",
        "Maintenance"
    ]

    DEFAULT_PROJECT_PHASES = [
        "Preconstruction",
        "Site Work",
        "Foundation",
        "Framing",
        "Dry-In",
        "Rough MEP",
        "Finishes",
        "Closeout"
    ]

    def __init__(self):
        self.file_path = Path(__file__).with_name("projects.json")
        self.data = {
            "projects": {},
            "active_project": None,
            "deleted_projects": [],
        }
        self.load()

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def load(self):
        if self.file_path.exists():
            with open(self.file_path, "r") as file:
                self.data.update(json.load(file))

        self.data.setdefault("projects", {})
        self.data.setdefault("active_project", None)
        self.data.setdefault("deleted_projects", [])
        self._purge_expired_deleted_projects()

    def _purge_expired_deleted_projects(self):
        cutoff = datetime.now(timezone.utc) - timedelta(
            days=self.PROJECT_RECOVERY_DAYS
        )
        kept_projects = []

        for deleted_project in self.data["deleted_projects"]:
            try:
                deleted_at = datetime.fromisoformat(
                    deleted_project["deleted_at"]
                )
            except (KeyError, TypeError, ValueError):
                continue

            if deleted_at >= cutoff:
                kept_projects.append(deleted_project)

        self.data["deleted_projects"] = kept_projects

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
            "status": "Active",
            "details": {
                "customer_name": "",
                "customer_email": "",
                "project_address": "",
                "pricing_region": "",
                "pricing_supplier": "",
                "material_suppliers": {},
                "proposal_title": "",
                "proposal_notes": "",
                "proposal_status": "Draft",
                "proposal_expiration_date": "",
                "proposal_scope": "",
                "proposal_exclusions": "",
            },
            "bid_settings": {
                "planned_labor_hours": 0.0,
                "crew_size": 0,
                "labor_hours_by_trade": {},
                "labor_trades": [],
                "overhead_percent": 0.0,
                "profit_markup_percent": 0.0
            },
            "estimates": [],
            "custom_items": [],
            "change_orders": [],
            "phases": [],
            "schedule_items": [],
            "equipment": [],
            "daily_logs": [],
        }

        self.save()
        return True

    def get_active_bid_settings(self):
        project = self.get_active_project()

        if project is None:
            return None

        defaults = {
            "planned_labor_hours": 0.0,
            "crew_size": 0,
            "labor_hours_by_trade": {},
            "labor_trades": [],
            "overhead_percent": 0.0,
            "profit_markup_percent": 0.0
        }

        return {
            **defaults,
            **project.get("bid_settings", {})
        }

    def update_active_bid_settings(self, settings):
        project = self.get_active_project()

        if project is None:
            return False

        project["bid_settings"] = {
            "planned_labor_hours": float(
                settings.get("planned_labor_hours", 0.0)
            ),
            "crew_size": int(settings.get("crew_size", 0)),
            "labor_hours_by_trade": settings.get(
                "labor_hours_by_trade",
                {}
            ),
            "labor_trades": settings.get("labor_trades", []),
            "overhead_percent": float(
                settings.get("overhead_percent", 0.0)
            ),
            "profit_markup_percent": float(
                settings.get("profit_markup_percent", 0.0)
            )
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

    def update_active_project_status(self, status):
        project = self.get_active_project()

        if project is None or status not in self.PROJECT_STATUSES:
            return False

        project["status"] = status
        self.save()
        return True

    def add_estimate(self, estimate):
        key=self.data["active_project"]

        if key is None:
            return False

        self.data["projects"][key]["estimates"].append(estimate)
        self.save()
        return True

    def add_custom_item(self, item):
        """Save one user-entered material or allowance to the active project."""
        project = self.get_active_project()

        if project is None:
            return False

        project.setdefault("custom_items", []).append(item)
        self.save()
        return True

    def delete_custom_item(self, item_index):
        project = self.get_active_project()

        if project is None:
            return False

        custom_items = project.get("custom_items", [])

        if item_index < 0 or item_index >= len(custom_items):
            return False

        del custom_items[item_index]
        self.save()
        return True

    def get_active_change_orders(self):
        project = self.get_active_project()

        if project is None:
            return []

        return project.get("change_orders", [])

    def add_change_order(self, change_order):
        project = self.get_active_project()

        if project is None:
            return False

        project.setdefault("change_orders", []).append(change_order)
        self.save()
        return True

    def update_change_order_status(self, change_order_index, status):
        valid_statuses = ["Draft", "Sent", "Approved", "Declined"]
        project = self.get_active_project()

        if project is None or status not in valid_statuses:
            return False

        change_orders = project.get("change_orders", [])

        if change_order_index < 0 or change_order_index >= len(change_orders):
            return False

        change_orders[change_order_index]["status"] = status
        self.save()
        return True

    def delete_change_order(self, change_order_index):
        project = self.get_active_project()

        if project is None:
            return False

        change_orders = project.get("change_orders", [])

        if change_order_index < 0 or change_order_index >= len(change_orders):
            return False

        del change_orders[change_order_index]
        self.save()
        return True

    def get_active_schedule_items(self):
        project = self.get_active_project()

        if project is None:
            return []

        return project.get("schedule_items", [])

    def get_active_equipment(self):
        project = self.get_active_project()

        if project is None:
            return []

        return project.setdefault("equipment", [])

    def add_equipment(self, equipment):
        project = self.get_active_project()

        if project is None:
            return False

        item = self._build_equipment(equipment)

        if not item["name"]:
            return False

        project.setdefault("equipment", []).append(item)
        self.save()
        return True

    def update_equipment(self, equipment_index, equipment):
        project = self.get_active_project()

        if project is None:
            return False

        equipment_items = project.setdefault("equipment", [])

        if equipment_index < 0 or equipment_index >= len(equipment_items):
            return False

        item = self._build_equipment(equipment)

        if not item["name"]:
            return False

        equipment_items[equipment_index] = item
        self.save()
        return True

    def delete_equipment(self, equipment_index):
        project = self.get_active_project()

        if project is None:
            return False

        equipment_items = project.get("equipment", [])

        if equipment_index < 0 or equipment_index >= len(equipment_items):
            return False

        del equipment_items[equipment_index]
        self.save()
        return True

    def get_active_phases(self):
        project = self.get_active_project()

        if project is None:
            return []

        return project.setdefault("phases", [])

    @staticmethod
    def normalize_labor_trade(trade_name):
        """Return a consistent name for common construction trades."""
        cleaned = " ".join(str(trade_name or "").split())
        aliases = {
            "carpenter": "Carpenter",
            "carpenters": "Carpenter",
            "finish carpenter": "Finish Carpenter",
            "finish carpenters": "Finish Carpenter",
            "laborer": "Laborer",
            "laborers": "Laborer",
            "concrete finisher": "Concrete Finisher",
            "concrete finishers": "Concrete Finisher",
            "electrician": "Electrician",
            "electricians": "Electrician",
            "plumber": "Plumber",
            "plumbers": "Plumber",
            "roofer": "Roofer",
            "roofers": "Roofer",
            "painter": "Painter",
            "painters": "Painter",
            "drywall installer": "Drywall Installer",
            "drywall installers": "Drywall Installer",
            "equipment operator": "Equipment Operator",
            "equipment operators": "Equipment Operator",
            "foreman": "Foreman",
            "foremen": "Foreman"
        }
        return aliases.get(cleaned.casefold(), cleaned)

    def get_active_scheduled_labor_plan(self):
        """Build a bid-ready labor plan from the active schedule.

        Task hours take priority within a phase. When task hours have not
        been entered yet, the phase total is used so hours are not doubled.
        """
        project = self.get_active_project()

        if project is None:
            return {
                "total_hours": 0.0,
                "trade_hours": {},
                "phase_rows": []
            }

        phases = project.get("phases", [])
        schedule_items = project.get("schedule_items", [])
        phase_rows = []
        trade_hours = {}
        assigned_task_indexes = set()

        for phase in phases:
            phase_name = phase.get("name", "Untitled phase")
            matching_tasks = [
                (index, item)
                for index, item in enumerate(schedule_items)
                if item.get("phase", "Unassigned") == phase_name
            ]
            assigned_task_indexes.update(
                index for index, _ in matching_tasks
            )
            task_hours = sum(
                float(item.get("planned_labor_hours", 0.0) or 0.0)
                for _, item in matching_tasks
            )
            phase_allocations = phase.get("labor_allocations", [])
            phase_hours = sum(
                float(allocation.get("labor_hours", 0.0) or 0.0)
                for allocation in phase_allocations
            ) or float(phase.get("planned_labor_hours", 0.0) or 0.0)
            hours = task_hours if task_hours > 0 else phase_hours
            source = (
                "Scheduled tasks"
                if task_hours > 0
                else (
                    "Phase crew plan"
                    if phase_allocations
                    else "Phase plan"
                )
            )
            phase_trade = self.normalize_labor_trade(
                phase.get("labor_trade", "")
            )

            if task_hours > 0:
                for _, item in matching_tasks:
                    item_hours = float(
                        item.get("planned_labor_hours", 0.0) or 0.0
                    )
                    item_trade = self.normalize_labor_trade(
                        item.get("labor_trade", "")
                    ) or phase_trade

                    if item_trade and item_hours > 0:
                        trade_hours[item_trade] = (
                            trade_hours.get(item_trade, 0.0) + item_hours
                        )
            elif phase_allocations:
                for allocation in phase_allocations:
                    allocation_trade = self.normalize_labor_trade(
                        allocation.get("trade", "")
                    )
                    allocation_hours = float(
                        allocation.get("labor_hours", 0.0) or 0.0
                    )

                    if allocation_trade and allocation_hours > 0:
                        trade_hours[allocation_trade] = (
                            trade_hours.get(allocation_trade, 0.0) +
                            allocation_hours
                        )
            elif phase_trade and hours > 0:
                trade_hours[phase_trade] = (
                    trade_hours.get(phase_trade, 0.0) + hours
                )

            phase_rows.append(
                {
                    "phase": phase_name,
                    "hours": round(hours, 2),
                    "source": source,
                    "trade": phase_trade or "Not assigned"
                }
            )

        unassigned_hours = 0.0

        for index, item in enumerate(schedule_items):
            if index in assigned_task_indexes:
                continue

            item_hours = float(
                item.get("planned_labor_hours", 0.0) or 0.0
            )
            unassigned_hours += item_hours
            item_trade = self.normalize_labor_trade(
                item.get("labor_trade", "")
            )

            if item_trade and item_hours > 0:
                trade_hours[item_trade] = (
                    trade_hours.get(item_trade, 0.0) + item_hours
                )

        if unassigned_hours > 0:
            phase_rows.append(
                {
                    "phase": "Unassigned tasks",
                    "hours": round(unassigned_hours, 2),
                    "source": "Scheduled tasks",
                    "trade": "Not assigned"
                }
            )

        return {
            "total_hours": round(
                sum(row["hours"] for row in phase_rows),
                2
            ),
            "trade_hours": {
                trade: round(hours, 2)
                for trade, hours in trade_hours.items()
            },
            "phase_rows": phase_rows
        }

    def add_default_project_phases(self):
        project = self.get_active_project()

        if project is None:
            return False

        phases = project.setdefault("phases", [])
        existing_names = {
            phase.get("name", "").strip().lower()
            for phase in phases
        }

        for name in self.DEFAULT_PROJECT_PHASES:
            if name.lower() not in existing_names:
                phases.append(self._build_phase({"name": name}))

        self.save()
        return True

    def clear_active_project_phases(self):
        """Remove the current phase plan and unassign linked work items."""
        project = self.get_active_project()

        if project is None:
            return False

        project["phases"] = []

        for item in project.get("schedule_items", []):
            item["phase"] = "Unassigned"

        for item in project.get("equipment", []):
            item["phase"] = "Unassigned"

        self.save()
        return True

    def add_project_phase(self, phase):
        project = self.get_active_project()

        if project is None:
            return False

        new_phase = self._build_phase(phase)

        if not new_phase["name"]:
            return False

        phases = project.setdefault("phases", [])

        if any(
                existing.get("name", "").lower()
                == new_phase["name"].lower()
                for existing in phases
        ):
            return False

        phases.append(new_phase)
        self.save()
        return True

    def update_project_phase(self, phase_index, phase):
        project = self.get_active_project()

        if project is None:
            return False

        phases = project.setdefault("phases", [])

        if phase_index < 0 or phase_index >= len(phases):
            return False

        updated_phase = self._build_phase(phase)

        if not updated_phase["name"]:
            return False

        if any(
                index != phase_index
                and existing.get("name", "").lower()
                == updated_phase["name"].lower()
                for index, existing in enumerate(phases)
        ):
            return False

        previous_name = phases[phase_index].get("name", "")
        phases[phase_index] = updated_phase

        for item in project.get("schedule_items", []):
            if item.get("phase", "") == previous_name:
                item["phase"] = updated_phase["name"]

        self.save()
        return True

    def delete_project_phase(self, phase_index):
        project = self.get_active_project()

        if project is None:
            return False

        phases = project.setdefault("phases", [])

        if phase_index < 0 or phase_index >= len(phases):
            return False

        deleted_name = phases[phase_index].get("name", "")
        del phases[phase_index]

        for item in project.get("schedule_items", []):
            if item.get("phase", "") == deleted_name:
                item["phase"] = "Unassigned"

        self.save()
        return True

    def _build_phase(self, phase):
        name = " ".join(
            str(phase.get("name", "")).strip().split()
        )
        status = phase.get("status", "Not Started")

        if status not in self.PHASE_STATUSES:
            status = "Not Started"

        labor_allocations = []

        for allocation in phase.get("labor_allocations", []):
            trade = self.normalize_labor_trade(allocation.get("trade", ""))
            member_count = int(allocation.get("member_count", 0) or 0)
            hours_per_person = float(
                allocation.get("hours_per_person", 0.0) or 0.0
            )

            if trade and member_count > 0 and hours_per_person > 0:
                labor_allocations.append(
                    {
                        "trade": trade,
                        "member_count": member_count,
                        "hours_per_person": hours_per_person,
                        "labor_hours": round(
                            member_count * hours_per_person,
                            2
                        )
                    }
                )

        planned_labor_hours = sum(
            allocation["labor_hours"]
            for allocation in labor_allocations
        ) or float(phase.get("planned_labor_hours", 0.0) or 0.0)

        return {
            "name": name,
            "start_date": str(phase.get("start_date", "")).strip(),
            "end_date": str(phase.get("end_date", "")).strip(),
            "status": status,
            "planned_labor_hours": planned_labor_hours,
            "labor_trade": self.normalize_labor_trade(
                phase.get("labor_trade", "")
            ),
            "labor_allocations": labor_allocations,
            "crew_notes": str(phase.get("crew_notes", "")).strip(),
            "equipment_notes": str(
                phase.get("equipment_notes", "")
            ).strip()
        }

    def _build_equipment(self, equipment):
        name = " ".join(
            str(equipment.get("name", "")).strip().split()
        )
        status = equipment.get("status", "Planned")

        if status not in self.EQUIPMENT_STATUSES:
            status = "Planned"

        return {
            "name": name,
            "source": str(
                equipment.get("source", "Company owned")
            ).strip() or "Company owned",
            "phase": str(
                equipment.get("phase", "Unassigned")
            ).strip() or "Unassigned",
            "start_date": str(equipment.get("start_date", "")).strip(),
            "end_date": str(equipment.get("end_date", "")).strip(),
            "status": status,
            "daily_cost": float(
                equipment.get("daily_cost", 0.0) or 0.0
            ),
            "notes": str(equipment.get("notes", "")).strip()
        }

    def add_schedule_item(self, item):
        project = self.get_active_project()

        if project is None:
            return False

        title = str(item.get("title", "")).strip()
        due_date = str(item.get("due_date", "")).strip()

        if not title or not due_date:
            return False

        status = item.get("status", "Upcoming")

        if status not in self.SCHEDULE_ITEM_STATUSES:
            status = "Upcoming"

        project.setdefault("schedule_items", []).append(
            {
                "title": title,
                "start_date": str(
                    item.get("start_date", due_date)
                ).strip() or due_date,
                "due_date": due_date,
                "phase": str(
                    item.get("phase", "Unassigned")
                ).strip() or "Unassigned",
                "item_type": str(
                    item.get("item_type", "Milestone")
                ).strip() or "Milestone",
                "status": status,
                "notes": str(item.get("notes", "")).strip(),
                "planned_labor_hours": float(
                    item.get("planned_labor_hours", 0.0) or 0.0
                ),
                "labor_trade": str(item.get("labor_trade", "")).strip(),
                "equipment_notes": str(
                    item.get("equipment_notes", "")
                ).strip()
            }
        )
        self.save()
        return True

    def update_schedule_item(self, item_index, item):
        project = self.get_active_project()

        if project is None:
            return False

        schedule_items = project.get("schedule_items", [])

        if item_index < 0 or item_index >= len(schedule_items):
            return False

        title = str(item.get("title", "")).strip()
        due_date = str(item.get("due_date", "")).strip()

        if not title or not due_date:
            return False

        status = item.get("status", "Upcoming")

        if status not in self.SCHEDULE_ITEM_STATUSES:
            return False

        schedule_items[item_index] = {
            "title": title,
            "start_date": str(
                item.get(
                    "start_date",
                    schedule_items[item_index].get("start_date", due_date)
                )
            ).strip() or due_date,
            "due_date": due_date,
            "phase": str(
                item.get("phase", "Unassigned")
            ).strip() or "Unassigned",
            "item_type": str(
                item.get("item_type", "Milestone")
            ).strip() or "Milestone",
            "status": status,
            "notes": str(item.get("notes", "")).strip(),
            "planned_labor_hours": float(
                item.get("planned_labor_hours", 0.0) or 0.0
            ),
            "labor_trade": str(item.get("labor_trade", "")).strip(),
            "equipment_notes": str(
                item.get("equipment_notes", "")
            ).strip()
        }
        self.save()
        return True

    def delete_schedule_item(self, item_index):
        project = self.get_active_project()

        if project is None:
            return False

        schedule_items = project.get("schedule_items", [])

        if item_index < 0 or item_index >= len(schedule_items):
            return False

        del schedule_items[item_index]
        self.save()
        return True

    def get_schedule_calendar_items(self, include_archived=False):
        """Return schedule entries across projects for the operations calendar."""
        calendar_items = []

        for project in self.data.get("projects", {}).values():
            project_status = project.get("status", "Active")

            if project_status == "Archived" and not include_archived:
                continue

            for item in project.get("schedule_items", []):
                calendar_items.append(
                    {
                        "project_name": project.get("name", "Untitled Project"),
                        "project_status": project_status,
                        "title": item.get("title", "Untitled task"),
                        "start_date": item.get("start_date", ""),
                        "due_date": item.get("due_date", ""),
                        "phase": item.get("phase", "Unassigned"),
                        "item_type": item.get("item_type", "Milestone"),
                        "status": item.get("status", "Upcoming"),
                        "notes": item.get("notes", "")
                    }
                )

        return sorted(
            calendar_items,
            key=lambda item: item.get("due_date", "")
        )

    def get_active_daily_logs(self):
        project = self.get_active_project()

        if project is None:
            return []

        return project.get("daily_logs", [])

    def add_daily_log(self, daily_log):
        project = self.get_active_project()

        if project is None:
            return False

        log_date = str(daily_log.get("date", "")).strip()
        work_completed = str(
            daily_log.get("work_completed", "")
        ).strip()

        if not log_date or not work_completed:
            return False

        project.setdefault("daily_logs", []).append(
            {
                "date": log_date,
                "crew_summary": str(
                    daily_log.get("crew_summary", "")
                ).strip(),
                "weather": str(daily_log.get("weather", "")
                ).strip(),
                "work_completed": work_completed,
                "materials_delivered": str(
                    daily_log.get("materials_delivered", "")
                ).strip(),
                "issues_delays": str(
                    daily_log.get("issues_delays", "")
                ).strip(),
                "safety_notes": str(
                    daily_log.get("safety_notes", "")
                ).strip(),
                "tomorrow_plan": str(
                    daily_log.get("tomorrow_plan", "")
                ).strip(),
                "photos": daily_log.get("photos", [])
            }
        )
        self.save()
        return True

    def update_daily_log(self, log_index, daily_log):
        project = self.get_active_project()

        if project is None:
            return False

        daily_logs = project.get("daily_logs", [])

        if log_index < 0 or log_index >= len(daily_logs):
            return False

        log_date = str(daily_log.get("date", "")).strip()
        work_completed = str(
            daily_log.get("work_completed", "")
        ).strip()

        if not log_date or not work_completed:
            return False

        daily_logs[log_index] = {
            "date": log_date,
            "crew_summary": str(
                daily_log.get("crew_summary", "")
            ).strip(),
            "weather": str(daily_log.get("weather", "")
            ).strip(),
            "work_completed": work_completed,
            "materials_delivered": str(
                daily_log.get("materials_delivered", "")
            ).strip(),
            "issues_delays": str(
                daily_log.get("issues_delays", "")
            ).strip(),
            "safety_notes": str(
                daily_log.get("safety_notes", "")
            ).strip(),
            "tomorrow_plan": str(
                daily_log.get("tomorrow_plan", "")
            ).strip(),
            "photos": daily_log.get(
                "photos",
                daily_logs[log_index].get("photos", [])
            )
        }
        self.save()
        return True

    def delete_daily_log(self, log_index):
        project = self.get_active_project()

        if project is None:
            return False

        daily_logs = project.get("daily_logs", [])

        if log_index < 0 or log_index >= len(daily_logs):
            return False

        del daily_logs[log_index]
        self.save()
        return True

    def get_active_material_takeoff(self):
        project = self.get_active_project()

        if project is None:
            return []

        totals = {}

        for estimate in project.get("estimates", []):
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

        # Keep custom items as individual lines. This lets a project-only
        # price stay separate from a catalog price for the same material.
        for item in project.get("custom_items", []):
            name = item.get("item")
            unit = item.get("unit")
            quantity = item.get("quantity")

            if not name or not unit or quantity is None:
                continue

            custom_takeoff = {
                "item": name,
                "unit": unit,
                "quantity": quantity,
                "manual_unit_cost": item.get("manual_unit_cost"),
                "category": item.get("category", "Custom"),
                "notes": item.get("notes", "")
            }

            takeoff.append(custom_takeoff)

        return takeoff

    def delete_project(self, name):
        key = " ".join(name.lower().split())

        if key not in self.data["projects"]:
            return False

        deleted_project = self.data["projects"].pop(key)
        self.data["deleted_projects"].append(
            {
                "id": str(uuid4()),
                "deleted_at": datetime.now(timezone.utc).isoformat(),
                "project": deepcopy(deleted_project)
            }
        )

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
                    "status": project.get("status", "Active"),
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
            "pricing_region": "",
            "pricing_supplier": "",
            "material_suppliers": {},
            "proposal_title": "",
            "proposal_notes": "",
            "proposal_status": "Draft",
            "proposal_expiration_date": "",
            "proposal_scope": "",
            "proposal_exclusions": ""
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
            "pricing_region": details.get(
                "pricing_region",
                ""
            ).strip(),
            "pricing_supplier": details.get(
                "pricing_supplier",
                ""
            ).strip(),
            "material_suppliers": details.get(
                "material_suppliers",
                {}
            ),
            "proposal_title": details.get(
                "proposal_title",
                ""
            ).strip(),
            "proposal_notes": details.get(
                "proposal_notes",
                ""
            ).strip(),
            "proposal_status": details.get(
                "proposal_status",
                "Draft"
            ).strip() or "Draft",
            "proposal_expiration_date": details.get(
                "proposal_expiration_date",
                ""
            ).strip(),
            "proposal_scope": details.get(
                "proposal_scope",
                ""
            ).strip(),
            "proposal_exclusions": details.get(
                "proposal_exclusions",
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

    def list_deleted_projects(self):
        self._purge_expired_deleted_projects()
        deleted_projects = []

        for deleted_project in self.data["deleted_projects"]:
            project = deleted_project.get("project", {})
            deleted_at = deleted_project.get("deleted_at", "")

            try:
                expires_at = datetime.fromisoformat(deleted_at) + timedelta(
                    days=self.PROJECT_RECOVERY_DAYS
                )
                expires_on = expires_at.strftime("%b %d, %Y")
            except (TypeError, ValueError):
                expires_on = "Unknown"

            deleted_projects.append(
                {
                    "id": deleted_project.get("id", ""),
                    "name": project.get("name", "Untitled project"),
                    "estimate_count": len(project.get("estimates", [])),
                    "expires_on": expires_on
                }
            )

        return deleted_projects

    def restore_deleted_project(self, deleted_id):
        for index, deleted_project in enumerate(
                self.data["deleted_projects"]
        ):
            if deleted_project.get("id") != deleted_id:
                continue

            project = deleted_project.get("project", {})
            project_name = project.get("name", "")
            key = " ".join(project_name.lower().split())

            if not project_name or key in self.data["projects"]:
                return False

            self.data["projects"][key] = project
            del self.data["deleted_projects"][index]
            self.save()
            return True

        return False

    def permanently_delete_project(self, deleted_id):
        original_count = len(self.data["deleted_projects"])
        self.data["deleted_projects"] = [
            deleted_project
            for deleted_project in self.data["deleted_projects"]
            if deleted_project.get("id") != deleted_id
        ]

        if len(self.data["deleted_projects"]) == original_count:
            return False

        self.save()
        return True

    def duplicate_estimate(self, estimate_index):
        project = self.get_active_project()

        if project is None:
            return False

        estimates = project.get("estimates", [])

        if estimate_index < 0 or estimate_index >= len(estimates):
            return False

        copied_estimate = deepcopy(estimates[estimate_index])
        original_name = copied_estimate.get(
            "display_name",
            copied_estimate.get("type", "Estimate")
        )

        copied_estimate["display_name"] = (
            f"Copy of {original_name}"
        )
        copied_estimate["revision_of"] = original_name

        estimates.append(copied_estimate)
        self.save()
        return True
