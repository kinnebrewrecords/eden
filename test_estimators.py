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


if __name__ == "__main__":
    unittest.main()
