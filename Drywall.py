import math
from Settings import Settings
from EstimatingPreferences import EstimatingPreferences


class DrywallEstimator:

    def __init__(self):
        self.name = "Drywall Estimator"


    def _get_drywall_waste_percent(self, waste_percent):
        if waste_percent is not None:
            return waste_percent

        preferences = EstimatingPreferences()

        return preferences.get(
            "drywall_waste_percent"
        )

    def wall_drywall(
            self,
            length,
            height,
            quantity=1,
            waste_percent=None    ):

        waste_percent = self._get_drywall_waste_percent(
            waste_percent
        )

        area = length * height * quantity

        sheets = math.ceil(
            area *
            (1 + waste_percent / 100) /
            Settings.DRYWALL_SHEET_COVERAGE_SQFT
        )

        material_takeoff = [
            {
                "item": "4x8 1/2 in Drywall Sheets",
                "unit": "SHEETS",
                "quantity": sheets
            }
        ]

        return {
            "type": "Wall Drywall",
            "material": "1/2 in Drywall",
            "length": length,
            "height": height,
            "area": area,
            "sheets": sheets,
            "quantity": quantity,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def ceiling_drywall(
            self,
            length,
            width,
            quantity=1,
            waste_percent=None
    ):
        waste_percent = self._get_drywall_waste_percent(
            waste_percent
        )

        area = length * width

        sheets = math.ceil(
            area *
            (1 + waste_percent / 100) /
            Settings.DRYWALL_SHEET_COVERAGE_SQFT
        )

        material_takeoff = [
            {
                "item": "4x8 1/2 in Ceiling Drywall Sheets",
                "unit": "SHEETS",
                "quantity": sheets
            }
        ]

        return {
            "type": "Ceiling Drywall",
            "material": "1/2 in Drywall",
            "length": length,
            "width": width,
            "area": area,
            "sheets": sheets,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }