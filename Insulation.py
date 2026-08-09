import math
from Settings import Settings
from EstimatingPreferences import EstimatingPreferences


class InsulationEstimator:

    def __init__(self):
        self.name = "Insulation Estimator"

    def _get_insulation_waste_percent(self, waste_percent):
        if waste_percent is not None:
            return waste_percent

        preferences = EstimatingPreferences()

        return preferences.get(
            "insulation_waste_percent"
        )

    def batt_insulation(
            self,
            length,
            height,
            r_value="R-13",
            stud_spacing=Settings.BATT_INSULATION_STUD_SPACING_INCHES,
            quantity=1,
            waste_percent=None    ):

        waste_percent = self._get_insulation_waste_percent(
            waste_percent
        )

        area = length * height * quantity

        coverage_per_batt = (
            Settings.BATT_INSULATION_COVERAGE_PER_BATT_SQFT
        )

        batts_per_bundle = Settings.BATTS_PER_BUNDLE

        batts = math.ceil(
            area *
            (1 + waste_percent / 100) /
            coverage_per_batt
        )

        bundles = math.ceil(
            batts / batts_per_bundle
        )

        material = f"{r_value} Batt Insulation"

        material_takeoff = [
            {
                "item": material,
                "unit": "BUNDLES",
                "quantity": bundles
            }
        ]

        return {
            "type": "Batt Insulation",
            "material": material,
            "r_value": r_value,
            "stud_spacing": stud_spacing,
            "length": length,
            "height": height,
            "area": round(area, 2),
            "coverage_per_batt": coverage_per_batt,
            "batts": batts,
            "bundles": bundles,
            "quantity": quantity,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def blown_insulation(
            self,
            length,
            width,
            r_value="R-38",
            coverage_per_bag=(
                    Settings.BLOWN_INSULATION_COVERAGE_PER_BAG_SQFT
            ),
            waste_percent=None):
        waste_percent = self._get_insulation_waste_percent(
            waste_percent
        )
        area = length * width

        bags = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_bag
        )

        material = f"Blown Fiberglass Insulation ({r_value})"

        material_takeoff = [
            {
                "item": material,
                "unit": "BAGS",
                "quantity": bags
            }
        ]

        return {
            "type": "Blown-In Attic Insulation",
            "material": material,
            "r_value": r_value,
            "length": length,
            "width": width,
            "area": round(area, 2),
            "coverage_per_bag": coverage_per_bag,
            "bags": bags,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def spray_foam(
            self,
            length,
            height,
            thickness_inches,
            coverage_per_kit_sqft,
            waste_percent=None):
        waste_percent = self._get_insulation_waste_percent(
            waste_percent
        )
        area = length * height

        kits = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_kit_sqft
        )

        material = "Closed-Cell Spray Foam"

        material_takeoff = [
            {
                "item": material,
                "unit": "KITS",
                "quantity": kits
            }
        ]

        return {
            "type": "Spray Foam Insulation",
            "material": material,
            "r_value": "R-7 per inch nominal",
            "length": length,
            "height": height,
            "area": round(area, 2),
            "thickness_inches": thickness_inches,
            "coverage_per_kit_sqft": coverage_per_kit_sqft,
            "kits": kits,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }