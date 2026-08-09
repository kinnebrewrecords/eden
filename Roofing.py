import math
from Settings import Settings
from EstimatingPreferences import EstimatingPreferences


class RoofingEstimator:

    def _get_roofing_waste_percent(self, waste_percent):
        if waste_percent is not None:
            return waste_percent

        preferences = EstimatingPreferences()

        return preferences.get(
            "roofing_waste_percent"
        )

    def _calculate_roof_geometry(
            self,
            length_feet,
            width_feet,
            roof_type,
            pitch_rise,
            overhang_inches
    ):
        """Return the actual sloped roof coverage from a building footprint."""
        roof_type = str(roof_type).strip().lower()
        pitch_rise = float(pitch_rise)
        overhang_inches = float(overhang_inches)

        if roof_type not in ["gable", "shed"]:
            raise ValueError("Roof type must be gable or shed.")
        if pitch_rise <= 0:
            raise ValueError("Roof pitch must be greater than zero.")
        if overhang_inches < 0:
            raise ValueError("Overhang cannot be negative.")

        overhang_feet = overhang_inches / 12
        slope_factor = math.sqrt(1 + (pitch_rise / 12) ** 2)
        roof_length = length_feet + (2 * overhang_feet)

        if roof_type == "gable":
            roof_plane_count = 2
            horizontal_run = (width_feet / 2) + overhang_feet
        else:
            roof_plane_count = 1
            horizontal_run = width_feet + (2 * overhang_feet)

        rafter_length = horizontal_run * slope_factor
        roof_plane_area = roof_length * rafter_length

        return {
            "roof_type": roof_type,
            "pitch_rise": pitch_rise,
            "overhang_inches": overhang_inches,
            "roof_plane_count": roof_plane_count,
            "roof_length": round(roof_length, 2),
            "rafter_length": round(rafter_length, 2),
            "roof_plane_area": round(roof_plane_area, 2),
            "area": round(roof_plane_area * roof_plane_count, 2)
        }

    def shingles(
            self,
            length_feet,
            width_feet,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            waste_percent=None
    ):

        waste_percent = self._get_roofing_waste_percent(
            waste_percent
        )

        geometry = self._calculate_roof_geometry(
            length_feet,
            width_feet,
            roof_type,
            pitch_rise,
            overhang_inches
        )
        area = geometry["area"]

        area_with_waste = area * (
            1 + waste_percent / 100
        )

        # 1 roofing square = 100 sq ft
        squares = math.ceil(
            area_with_waste /
            Settings.ROOFING_SQUARE_COVERAGE_SQFT
        )

        bundles = (
                squares *
                Settings.SHINGLE_BUNDLES_PER_SQUARE
        )

        material_takeoff = [
            {
                "item": (
                    f"Asphalt Shingles "
                    f"({Settings.SHINGLE_BUNDLES_PER_SQUARE} bundles per square)"
                ),
                "unit": "BUNDLES",
                "quantity": bundles
            }
        ]

        return {

            "type": "Asphalt Shingles",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            **geometry,
            "area": area,

            "squares": squares,

            "shingles": {
                "bundles": bundles
            },

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def underlayment(
            self,
            length_feet,
            width_feet,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            waste_percent=None
    ):
        waste_percent = self._get_roofing_waste_percent(
            waste_percent
        )

        geometry = self._calculate_roof_geometry(
            length_feet,
            width_feet,
            roof_type,
            pitch_rise,
            overhang_inches
        )
        area = geometry["area"]

        # Add waste
        area_with_waste = area * (
                1 + waste_percent / 100
        )

        # Synthetic underlayment coverage
        # Typical roll coverage varies, using 1000 sq ft/roll estimate
        roll_coverage = Settings.UNDERLAYMENT_ROLL_COVERAGE_SQFT

        rolls = math.ceil(
            area_with_waste / roll_coverage
        )

        material_takeoff = [
            {
                "item": "Synthetic Roof Underlayment",
                "unit": "ROLLS",
                "quantity": rolls
            }
        ]

        return {

            "type": "Roof Underlayment",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            **geometry,
            "area": area,

            "material": {
                "type": "Synthetic Underlayment",
                "rolls": rolls
            },

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def drip_edge(
            self,
            required_length_feet,
            stock_length_feet=Settings.DRIP_EDGE_PIECE_LENGTH_FEET,
            waste_percent=None
    ):
        waste_percent = self._get_roofing_waste_percent(
            waste_percent
        )
        total_length = math.ceil(
            required_length_feet *
            (1 + waste_percent / 100)
        )

        pieces = math.ceil(
            total_length / stock_length_feet
        )

        material_takeoff = [
            {
                "item": f"{stock_length_feet} ft Roof Drip Edge",
                "unit": "EA",
                "quantity": pieces
            }
        ]

        return {
            "type": "Roof Drip Edge",

            "required_length": required_length_feet,

            "total_length": total_length,

            "material": {
                "size": f"{stock_length_feet} ft",
                "quantity": pieces
            },

            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def ice_water_shield(
            self,
            required_coverage_sqft,
            waste_percent=None
    ):
        waste_percent = self._get_roofing_waste_percent(
            waste_percent
        )
        roll_coverage = (
            Settings.ICE_WATER_SHIELD_ROLL_COVERAGE_SQFT
        )

        area_with_waste = required_coverage_sqft * (
            1 + waste_percent / 100
        )

        rolls = math.ceil(
            area_with_waste / roll_coverage
        )

        material_takeoff = [
            {
                "item": "Self-Adhered Ice & Water Shield",
                "unit": "ROLLS",
                "quantity": rolls
            }
        ]

        return {
            "type": "Ice & Water Shield",

            "required_coverage_sqft": required_coverage_sqft,

            "area_with_waste": round(area_with_waste, 2),

            "material": {
                "rolls": rolls,
                "type": "Self-Adhered Ice Barrier"
            },

            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def ridge_vent(
            self,
            length_feet,
            waste_percent=None
    ):
        waste_percent = self._get_roofing_waste_percent(
            waste_percent
        )

        total_length = math.ceil(
            length_feet * (1 + waste_percent / 100)
        )

        section_length = Settings.RIDGE_VENT_SECTION_LENGTH_FEET

        pieces = math.ceil(
            total_length / section_length
        )

        material_takeoff = [
            {
                "item": "10 ft Ridge Vent",
                "unit": "EA",
                "quantity": pieces
            }
        ]

        return {

            "type": "Ridge Vent",

            "length": length_feet,

            "material": {
                "size": f"{section_length} ft",
                "quantity": pieces
            },

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def flashing(
            self,
            quantity,
            waste_percent=None
    ):
        waste_percent = self._get_roofing_waste_percent(
            waste_percent
        )
        import math

        total_quantity = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "Roof Flashing Pieces",
                "unit": "EA",
                "quantity": total_quantity
            }
        ]

        return {

            "type": "Roof Flashing",

            "locations": quantity,

            "material": {
                "quantity": total_quantity,
                "type": "Flashing Pieces"
            },

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }
