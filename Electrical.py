import math


class ElectricalEstimator:

    def __init__(self):
        self.name = "Electrical Estimator"

    def outlets(
            self,
            quantity,
            outlet_spec=None,
    ):
        if outlet_spec:
            material = outlet_spec
            total = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total
                }
            ]

            status = "specified"

        else:
            material = "Per approved electrical plan"
            total = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Electrical Outlets",
            "status": status,
            "source": "approved_electrical_plan",
            "material": material,
            "quantity": quantity,
            "total": total,
            "material_takeoff": material_takeoff
        }

    def switches(
            self,
            quantity,
            switch_spec=None,
    ):
        if switch_spec:
            material = switch_spec
            total = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total
                }
            ]

            status = "specified"

        else:
            material = "Per approved electrical plan"
            total = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Electrical Switches",
            "status": status,
            "source": "approved_electrical_plan",
            "material": material,
            "quantity": quantity,
            "total": total,
            "material_takeoff": material_takeoff
        }

    def lighting_fixtures(
            self,
            quantity,
            fixture_spec=None,
    ):
        if fixture_spec:
            material = fixture_spec
            total = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total
                }
            ]

            status = "specified"

        else:
            material = "Per approved electrical plan"
            total = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Lighting Fixtures",
            "status": status,
            "source": "approved_electrical_plan",
            "material": material,
            "quantity": quantity,
            "total": total,
            "material_takeoff": material_takeoff
        }

    def electrical_boxes(
            self,
            quantity,
            box_spec=None,
    ):
        if box_spec:
            material = box_spec
            total = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total
                }
            ]

            status = "specified"

        else:
            material = "Per approved electrical plan"
            total = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Electrical Boxes",
            "status": status,
            "source": "approved_electrical_plan",
            "material": material,
            "quantity": quantity,
            "total": total,
            "material_takeoff": material_takeoff
        }


    def breakers(
            self,
            quantity,
            breaker_spec=None,
    ):
        if breaker_spec:
            material = breaker_spec
            total = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total
                }
            ]

            status = "specified"

        else:
            material = "Per approved electrical plan"
            total = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Circuit Breakers",
            "status": status,
            "source": "approved_electrical_plan",
            "material": material,
            "quantity": quantity,
            "total": total,
            "material_takeoff": material_takeoff
        }

    def electrical_panel(self, panel_spec=None):
        if panel_spec:
            return {
                "type": "Electrical Panel",
                "status": "specified",
                "material": panel_spec,
                "quantity": 1,
                "material_takeoff": [
                    {
                        "item": panel_spec,
                        "unit": "EA",
                        "quantity": 1
                    }
                ]
            }

        return {
            "type": "Electrical Panel",
            "status": "plan_required",
            "source": "approved_electrical_plan",
            "material": "Per approved electrical plan",
            "quantity": None,
            "material_takeoff": []
        }