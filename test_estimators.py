"""Regression checks for Eden's core estimating calculations.

Run from the Eden folder:
    python -m unittest test_estimators.py
"""

import unittest

from Estimating import Estimator


class EstimatorRegressionTests(unittest.TestCase):
    def setUp(self):
        self.estimator = Estimator()

    def test_concrete_slab_volume_and_override(self):
        estimate = self.estimator.concrete_slab(
            20,
            20,
            4,
            waste_percent=0
        )

        self.assertEqual(estimate["order_quantity"], 5)
        self.assertEqual(estimate["waste_percent"], 0)

    def test_concrete_waste_override_for_all_legacy_shapes(self):
        estimates = [
            self.estimator.concrete_trench(20, 12, 12, waste_percent=0),
            self.estimator.concrete_retaining_wall(
                20, 4, 8, waste_percent=0
            ),
            self.estimator.concrete_spread_footing(
                20, 2, 12, waste_percent=0
            ),
            self.estimator.concrete_round_footing(
                24, 12, waste_percent=0
            ),
            self.estimator.concrete_pile_cap(
                4, 4, 12, waste_percent=0
            ),
            self.estimator.concrete_lintel(
                8, 8, 8, waste_percent=0
            )
        ]

        self.assertTrue(
            all(estimate["waste_percent"] == 0 for estimate in estimates)
        )

    def test_footing_system_accepts_explicit_inches(self):
        estimate = self.estimator.concrete_footing_system(
            [
                {
                    "length": 20,
                    "width_inches": 16,
                    "depth_inches": 16,
                    "quantity": 2
                }
            ],
            waste_percent=0
        )

        run = estimate["footing_runs"][0]
        self.assertEqual(run["width_inches"], 16.0)
        self.assertEqual(estimate["order_quantity"], 3)

    def test_roof_materials_share_one_geometry(self):
        arguments = {
            "roof_type": "gable",
            "pitch_rise": 6,
            "overhang_inches": 12,
            "waste_percent": 15
        }
        sheathing = self.estimator.roof_sheathing(20, 8, **arguments)
        shingles = self.estimator.shingles(20, 8, **arguments)
        underlayment = self.estimator.underlayment(20, 8, **arguments)

        self.assertEqual(sheathing["area"], shingles["area"])
        self.assertEqual(shingles["area"], underlayment["area"])
        self.assertEqual(sheathing["roof_plane_count"], 2)
        self.assertEqual(shingles["shingles"]["bundles"], 9)

    def test_wall_openings_never_add_unspecified_headers(self):
        estimate = self.estimator.frame_wall_with_openings(
            20,
            8,
            [{"type": "door", "width_feet": 3, "height_feet": 7}],
            header_spec=None,
            waste_percent=0
        )

        takeoff_names = [item["item"] for item in estimate["material_takeoff"]]
        self.assertFalse(
            any("Header Material" in name for name in takeoff_names)
        )

    def test_drywall_and_insulation_return_material_takeoff(self):
        drywall = self.estimator.wall_drywall(
            20,
            8,
            waste_percent=0
        )
        insulation = self.estimator.batt_insulation(
            20,
            8,
            waste_percent=0
        )

        self.assertEqual(drywall["material_takeoff"][0]["quantity"], 5)
        self.assertGreater(insulation["material_takeoff"][0]["quantity"], 0)

    def test_floor_system_counts_joists_across_selected_direction(self):
        estimate = self.estimator.floor_system_assembly(
            40,
            30,
            joist_spec={
                "size": "2x10",
                "member_length_feet": 30,
                "spacing_inches": 16
            },
            rim_spec={
                "size": "2x10",
                "stock_length_feet": 16
            },
            include_blocking=True,
            blocking_rows=1,
            joist_span_direction="width",
            waste_percent=0
        )

        takeoff = {
            item["item"]: item["quantity"]
            for item in estimate["material_takeoff"]
        }

        self.assertEqual(estimate["joist_span_direction"], "width")
        self.assertEqual(takeoff["2x10 x 30 ft Floor Joists"], 31)
        self.assertEqual(takeoff["2x10 x 14.5 in Blocking"], 30)

    def test_exterior_wall_openings_use_net_coverage(self):
        estimate = self.estimator.exterior_wall_assembly(
            20,
            8,
            quantity=2,
            include_housewrap=True,
            include_insulation=True,
            include_drywall=True,
            openings=[
                {"type": "door", "width_feet": 3, "height_feet": 7},
                {"type": "window", "width_feet": 4, "height_feet": 4}
            ],
            header_spec="2x10",
            header_plies=2,
            waste_percent=0
        )

        self.assertEqual(estimate["gross_wall_area_sqft"], 320)
        self.assertEqual(estimate["net_wall_area_sqft"], 246)

        takeoff = {
            item["item"]: item["quantity"]
            for item in estimate["material_takeoff"]
        }
        self.assertEqual(takeoff["4x8 7/16 OSB Wall Sheathing"], 8)
        self.assertEqual(takeoff["4x8 1/2 in Drywall Sheets"], 8)

    def test_foundation_combines_separate_pours_for_project_pricing(self):
        estimate = self.estimator.foundation_system_assembly(
            [{
                "length": 140,
                "width_inches": 16,
                "depth_inches": 8,
                "quantity": 1
            }],
            forms=True,
            gravel_base=True,
            include_foundation_wall=True,
            foundation_wall_length_feet=140,
            foundation_wall_height_feet=8,
            foundation_wall_thickness_inches=8,
            include_waterproofing=True,
            waste_percent=0
        )

        self.assertEqual(estimate["footing_order_quantity"], 5)
        self.assertEqual(estimate["foundation_wall_order_quantity"], 28)

        concrete_row = next(
            item for item in estimate["material_takeoff"]
            if item["item"] == "Ready Mix Concrete"
        )
        self.assertEqual(concrete_row["quantity"], 33)

    def test_whole_house_normalizes_matching_lumber_purchase_rows(self):
        standard_wall = self.estimator.exterior_wall_assembly(
            20,
            8,
            quantity=1,
            include_housewrap=False,
            include_insulation=False,
            include_drywall=False,
            stud_spacing_inches=16,
            waste_percent=0
        )
        opening_wall = self.estimator.exterior_wall_assembly(
            20,
            8,
            quantity=1,
            include_housewrap=False,
            include_insulation=False,
            include_drywall=False,
            openings=[
                {"type": "door", "width_feet": 3, "height_feet": 7}
            ],
            header_spec=None,
            stud_spacing_inches=16,
            waste_percent=0
        )
        estimate = self.estimator.residential_house_takeoff(
            "Regression House",
            {
                "Standard wall": standard_wall,
                "Opening wall": opening_wall
            },
            story_count=1
        )

        takeoff = {
            item["item"]: item["quantity"]
            for item in estimate["material_takeoff"]
        }

        self.assertIn("2x4 x 8 ft Studs", takeoff)
        self.assertNotIn("2x4 x 8 ft Wall, King, and Jack Studs", takeoff)
        self.assertEqual(takeoff["2x4 x 8 ft Studs"], 33)


if __name__ == "__main__":
    unittest.main()
