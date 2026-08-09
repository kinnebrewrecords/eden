import math
from Settings import Settings


class DrywallFinishEstimator:

    def __init__(self):
        self.name = "Drywall Finish Estimator"

    def joint_compound(self, area, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_bucket = (
            Settings.JOINT_COMPOUND_COVERAGE_PER_BUCKET_SQFT
        )

        buckets = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_bucket
        )

        material_takeoff = [
            {
                "item": "Drywall Joint Compound (5 gal bucket)",
                "unit": "BUCKETS",
                "quantity": buckets
            }
        ]

        return {
            "type": "Joint Compound",
            "material": "Drywall Joint Compound",
            "area": round(area, 2),
            "coverage_per_bucket": coverage_per_bucket,
            "buckets": buckets,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def drywall_tape(self, area, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_roll = (
            Settings.DRYWALL_TAPE_COVERAGE_PER_ROLL_SQFT
        )

        rolls = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_roll
        )

        material_takeoff = [
            {
                "item": "Paper Drywall Tape",
                "unit": "ROLLS",
                "quantity": rolls
            }
        ]

        return {
            "type": "Drywall Tape",
            "material": "Paper Drywall Tape",
            "area": round(area, 2),
            "coverage_per_roll": coverage_per_roll,
            "rolls": rolls,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def corner_bead(self, length, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        piece_length = Settings.CORNER_BEAD_PIECE_LENGTH_FEET

        pieces = math.ceil(
            length * (1 + waste_percent / 100) / piece_length
        )

        material_takeoff = [
            {
                "item": f"{piece_length} ft Vinyl Corner Bead",
                "unit": "EA",
                "quantity": pieces
            }
        ]

        return {
            "type": "Corner Bead",
            "material": "Vinyl Corner Bead",
            "length": length,
            "piece_length": piece_length,
            "pieces": pieces,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def drywall_screws(
            self,
            area,
            screws_per_sheet=Settings.DRYWALL_SCREWS_PER_SHEET,
            screws_per_box=Settings.DRYWALL_SCREWS_PER_BOX,
            waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT
    ):
        sheet_area = Settings.DRYWALL_SHEET_COVERAGE_SQFT

        sheets = math.ceil(area / sheet_area)

        screws = math.ceil(
            sheets * screws_per_sheet * (1 + waste_percent / 100)
        )

        boxes = math.ceil(screws / screws_per_box)

        material_takeoff = [
            {
                "item": f"1-5/8 in Drywall Screws ({screws_per_box}-count box)",
                "unit": "BOXES",
                "quantity": boxes
            }
        ]

        return {
            "type": "Drywall Screws",
            "material": "1-5/8 inch Drywall Screws",
            "area": round(area, 2),
            "sheets": sheets,
            "screws_per_sheet": screws_per_sheet,
            "screws": screws,
            "screws_per_box": screws_per_box,
            "boxes": boxes,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def drywall_sanding(self, area, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_pack = (
            Settings.DRYWALL_SANDING_COVERAGE_PER_PACK_SQFT
        )

        packs = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_pack
        )

        material_takeoff = [
            {
                "item": "Drywall Sanding Sheets",
                "unit": "PACKS",
                "quantity": packs
            }
        ]

        return {
            "type": "Drywall Sanding",
            "material": "Drywall Sanding Sheets",
            "area": round(area, 2),
            "coverage_per_pack": coverage_per_pack,
            "packs": packs,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def primer(self, area, coats=1, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_gallon = (
            Settings.PRIMER_COVERAGE_PER_GALLON_SQFT
        )

        gallons = math.ceil(
            area * coats * (1 + waste_percent / 100)
            / coverage_per_gallon
        )

        material_takeoff = [
            {
                "item": "PVA Drywall Primer",
                "unit": "GALLONS",
                "quantity": gallons
            }
        ]

        return {
            "type": "Drywall Primer",
            "material": "PVA Drywall Primer",
            "area": round(area, 2),
            "coats": coats,
            "coverage_per_gallon": coverage_per_gallon,
            "gallons": gallons,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def texture(self, area,waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_bucket = (
            Settings.TEXTURE_COVERAGE_PER_BUCKET_SQFT
        )

        buckets = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_bucket
        )

        material_takeoff = [
            {
                "item": "Spray Applied Wall Texture",
                "unit": "BUCKETS",
                "quantity": buckets
            }
        ]

        return {
            "type": "Drywall Texture",
            "material": "Spray Applied Wall Texture",
            "area": round(area, 2),
            "coverage_per_bucket": coverage_per_bucket,
            "buckets": buckets,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def interior_paint(self, area, coats=2, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_gallon = (
            Settings.INTERIOR_PAINT_COVERAGE_PER_GALLON_SQFT
        )

        gallons = math.ceil(
            area * coats * (1 + waste_percent / 100)
            / coverage_per_gallon
        )

        material_takeoff = [
            {
                "item": "Latex Interior Wall Paint",
                "unit": "GALLONS",
                "quantity": gallons
            }
        ]

        return {
            "type": "Interior Paint",
            "material": "Latex Interior Wall Paint",
            "area": round(area, 2),
            "coats": coats,
            "coverage_per_gallon": coverage_per_gallon,
            "gallons": gallons,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def ceiling_paint(self, area, coats=2, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_gallon = (
            Settings.CEILING_PAINT_COVERAGE_PER_GALLON_SQFT
        )

        gallons = math.ceil(
            area * coats * (1 + waste_percent / 100)
            / coverage_per_gallon
        )

        material_takeoff = [
            {
                "item": "Flat White Ceiling Paint",
                "unit": "GALLONS",
                "quantity": gallons
            }
        ]

        return {
            "type": "Ceiling Paint",
            "material": "Flat White Ceiling Paint",
            "area": round(area, 2),
            "coats": coats,
            "coverage_per_gallon": coverage_per_gallon,
            "gallons": gallons,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def trim_paint(
            self,
            length,
            face_width_inches,
            coats=2,
            waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT
    ):
        face_width_feet = face_width_inches / 12
        area = length * face_width_feet
        coverage_per_gallon = (
            Settings.TRIM_PAINT_COVERAGE_PER_GALLON_SQFT
        )

        gallons = math.ceil(
            area * coats * (1 + waste_percent / 100)
            / coverage_per_gallon
        )

        material_takeoff = [
            {
                "item": "Semi-Gloss Trim Paint",
                "unit": "GALLONS",
                "quantity": gallons
            }
        ]

        return {
            "type": "Trim Paint",
            "material": "Semi-Gloss Trim Paint",
            "length": length,
            "face_width_inches": face_width_inches,
            "area": round(area, 2),
            "coats": coats,
            "coverage_per_gallon": coverage_per_gallon,
            "gallons": gallons,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def door_paint(self, quantity, coats=2, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        doors_per_gallon = Settings.DOORS_PER_GALLON

        gallons = math.ceil(
            quantity * coats * (1 + waste_percent / 100)
            / doors_per_gallon
        )

        material_takeoff = [
            {
                "item": "Semi-Gloss Door Paint",
                "unit": "GALLONS",
                "quantity": gallons
            }
        ]

        return {
            "type": "Door Paint",
            "material": "Semi-Gloss Door Paint",
            "doors": quantity,
            "coats": coats,
            "doors_per_gallon": doors_per_gallon,
            "gallons": gallons,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def exterior_paint(self, area, coats=2, waste_percent=Settings.DRYWALL_FINISH_WASTE_PERCENT):
        coverage_per_gallon = (
            Settings.EXTERIOR_PAINT_COVERAGE_PER_GALLON_SQFT
        )

        gallons = math.ceil(
            area * coats * (1 + waste_percent / 100)
            / coverage_per_gallon
        )

        material_takeoff = [
            {
                "item": "Exterior Latex Paint",
                "unit": "GALLONS",
                "quantity": gallons
            }
        ]

        return {
            "type": "Exterior Paint",
            "material": "Exterior Latex Paint",
            "area": round(area, 2),
            "coats": coats,
            "coverage_per_gallon": coverage_per_gallon,
            "gallons": gallons,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

