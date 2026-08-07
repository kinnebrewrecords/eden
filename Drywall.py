import math
from Settings import Settings


class DrywallEstimator:

    def __init__(self):
        self.name = "Drywall Estimator"

    def wall_drywall(
            self,
            length,
            height,
            quantity=1,
            waste_percent=Settings.DRYWALL_WASTE_PERCENT
    ):
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
            waste_percent=Settings.DRYWALL_WASTE_PERCENT
    ):
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