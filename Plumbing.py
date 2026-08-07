import math
from Settings import Settings


class PlumbingEstimator:

    def pex_pipe(
            self,
            length,
            pipe_spec=None,
            length_allowance_percent=Settings.PLUMBING_LENGTH_ALLOWANCE_PERCENT
    ):
        if pipe_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": pipe_spec,
                    "unit": "LF",
                    "quantity": total_length
                }
            ]

            status = "specified"

        else:
            total_length = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "PEX Water Pipe",
            "status": status,
            "source": "approved_plumbing_plan",
            "material": pipe_spec or "Per approved plumbing plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def pvc_drain_pipe(
            self,
            length,
            pipe_spec=None,
            length_allowance_percent=Settings.PLUMBING_LENGTH_ALLOWANCE_PERCENT
    ):
        if pipe_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": pipe_spec,
                    "unit": "LF",
                    "quantity": total_length
                }
            ]

            status = "specified"

        else:
            total_length = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "PVC Drain Pipe",
            "status": status,
            "source": "approved_plumbing_plan",
            "material": pipe_spec or "Per approved plumbing plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def copper_pipe(
            self,
            length,
            pipe_spec=None,
            length_allowance_percent=Settings.PLUMBING_LENGTH_ALLOWANCE_PERCENT
    ):
        if pipe_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": pipe_spec,
                    "unit": "LF",
                    "quantity": total_length
                }
            ]

            status = "specified"

        else:
            total_length = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Copper Pipe",
            "status": status,
            "source": "approved_plumbing_plan",
            "material": pipe_spec or "Per approved plumbing plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def fittings(self, quantity, fitting_spec=None):
        if fitting_spec:
            material = fitting_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing plan"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Plumbing Fittings",
            "status": status,
            "source": "approved_plumbing_plan",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def plumbing_valve(self, quantity, valve_spec=None):
        if valve_spec:
            material = valve_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing plan"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Plumbing Valves",
            "status": status,
            "source": "approved_plumbing_plan",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def toilets(self, quantity, fixture_spec=None):
        if fixture_spec:
            material = fixture_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing fixture schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Toilets",
            "status": status,
            "source": "approved_plumbing_fixture_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def faucet(self, quantity, fixture_spec=None):
        if fixture_spec:
            material = fixture_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing fixture schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Faucets",
            "status": status,
            "source": "approved_plumbing_fixture_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def showers_tubs(self, quantity, fixture_spec=None):
        if fixture_spec:
            material = fixture_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing fixture schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Showers/Tubs",
            "status": status,
            "source": "approved_plumbing_fixture_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def water_heater(self, quantity, heater_spec=None):
        if heater_spec:
            material = heater_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing/MEP schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Water Heater",
            "status": status,
            "source": "approved_plumbing_mep_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def sink(self, quantity, fixture_spec=None):
        if fixture_spec:
            material = fixture_spec
            total_quantity = quantity

            material_takeoff = [
                {
                    "item": material,
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

            status = "specified"

        else:
            material = "Per approved plumbing fixture schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Sinks",
            "status": status,
            "source": "approved_plumbing_fixture_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }