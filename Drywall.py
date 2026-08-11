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

    def wall_drywall_area(self, area_sqft, waste_percent=None):
        """Estimate wall drywall from net measured wall area."""
        waste_percent = self._get_drywall_waste_percent(waste_percent)
        sheets = math.ceil(
            area_sqft * (1 + waste_percent / 100) /
            Settings.DRYWALL_SHEET_COVERAGE_SQFT
        )

        return {
            "type": "Wall Drywall",
            "material": "1/2 in Drywall",
            "area": round(area_sqft, 2),
            "sheets": sheets,
            "waste_percent": waste_percent,
            "material_takeoff": [
                {
                    "item": "4x8 1/2 in Drywall Sheets",
                    "unit": "SHEETS",
                    "quantity": sheets
                }
            ]
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

    def ceiling_drywall_area(self, area_sqft, waste_percent=None):
        """Estimate ceiling drywall from measured ceiling area."""
        waste_percent = self._get_drywall_waste_percent(waste_percent)
        sheets = math.ceil(
            area_sqft * (1 + waste_percent / 100) /
            Settings.DRYWALL_SHEET_COVERAGE_SQFT
        )

        return {
            "type": "Ceiling Drywall",
            "material": "1/2 in Drywall",
            "area": round(area_sqft, 2),
            "sheets": sheets,
            "waste_percent": waste_percent,
            "material_takeoff": [
                {
                    "item": "4x8 1/2 in Ceiling Drywall Sheets",
                    "unit": "SHEETS",
                    "quantity": sheets
                }
            ]
        }
