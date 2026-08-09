import json
from pathlib import Path

from Settings import Settings


class EstimatingPreferences:
    def __init__(self):
        self.file_path = Path(__file__).with_name(
            "estimating_preferences.json"
        )

        self.defaults = {
            "concrete_waste_percent": (
                Settings.CONCRETE_WASTE_PERCENT
            ),
            "gravel_base_depth_inches": (
                Settings.GRAVEL_BASE_DEPTH_INCHES
            ),
            "form_board_length_feet": (
                Settings.FORM_BOARD_LENGTH_FEET
            ),
            "concrete_form_tube_length_feet": (
                Settings.CONCRETE_FORM_TUBE_LENGTH_FEET
            ),
            "lumber_waste_percent": (
                Settings.LUMBER_WASTE_PERCENT
            ),
            "lumber_stud_spacing_inches": (
                Settings.LUMBER_STUD_SPACING_INCHES
            ),
            "lumber_stock_length_feet": (
                Settings.LUMBER_STOCK_LENGTH_FEET
            ),
            "roofing_waste_percent": (
                Settings.ROOFING_WASTE_PERCENT
            ),
            "drywall_waste_percent": (
                Settings.DRYWALL_WASTE_PERCENT
            ),
            "insulation_waste_percent": (
                Settings.INSULATION_WASTE_PERCENT
            )
        }

        self.data = self.defaults.copy()
        self.load()

    def load(self):
        if not self.file_path.exists():
            return

        with open(self.file_path, "r") as file:
            saved_data = json.load(file)

        self.data.update(saved_data)

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def get(self, setting_name):
        return self.data.get(
            setting_name,
            self.defaults.get(setting_name)
        )

    def update(self, values):
        for setting_name, value in values.items():
            if setting_name in self.defaults:
                self.data[setting_name] = value

        self.save()

    def reset(self):
        self.data = self.defaults.copy()
        self.save()