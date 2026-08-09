import math
from Settings import Settings


class HVACEstimator:

    def ductwork(
            self,
            length,
            duct_spec=None,
            length_allowance_percent=Settings.HVAC_LENGTH_ALLOWANCE_PERCENT
    ):
        if duct_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": duct_spec,
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
            "type": "Ductwork",
            "status": status,
            "source": "approved_hvac_plan",
            "material": duct_spec or "Per approved HVAC plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def supply_register(self, quantity, register_spec=None):
        if register_spec:
            material = register_spec
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
            material = "Per approved HVAC plan"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Supply Registers",
            "status": status,
            "source": "approved_hvac_plan",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def return_grilles(self, quantity, grille_spec=None):
        if grille_spec:
            material = grille_spec
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
            material = "Per approved HVAC plan"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Return Grilles",
            "status": status,
            "source": "approved_hvac_plan",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def flex_duct(
            self,
            length,
            duct_spec=None,
            length_allowance_percent=Settings.HVAC_LENGTH_ALLOWANCE_PERCENT
    ):
        if duct_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": duct_spec,
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
            "type": "Flex Duct",
            "status": status,
            "source": "approved_hvac_plan",
            "material": duct_spec or "Per approved HVAC plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def thermostat(self, quantity, thermostat_spec=None):
        if thermostat_spec:
            material = thermostat_spec
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
            material = "Per approved HVAC controls schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Thermostat",
            "status": status,
            "source": "approved_hvac_controls_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def air_filters(self, quantity, filter_spec=None):
        if filter_spec:
            material = filter_spec
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
            material = "Per approved HVAC equipment schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Air Filters",
            "status": status,
            "source": "approved_hvac_equipment_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def refrigerant_line_set(
            self,
            length,
            line_set_spec=None,
            length_allowance_percent=Settings.HVAC_LENGTH_ALLOWANCE_PERCENT
    ):
        if line_set_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": line_set_spec,
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
            "type": "Refrigerant Line Set",
            "status": status,
            "source": "approved_hvac_plan",
            "material": line_set_spec or "Per approved HVAC plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def condensate_drain(
            self,
            length,
            drain_spec=None,
            length_allowance_percent=Settings.HVAC_LENGTH_ALLOWANCE_PERCENT
    ):
        if drain_spec:
            total_length = math.ceil(
                length * (100 + length_allowance_percent) / 100
            )

            material_takeoff = [
                {
                    "item": drain_spec,
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
            "type": "Condensate Drain",
            "status": status,
            "source": "approved_hvac_plan",
            "material": drain_spec or "Per approved HVAC plan",
            "length": length,
            "total_length": total_length,
            "length_allowance_percent": length_allowance_percent,
            "material_takeoff": material_takeoff
        }

    def furnace(self, quantity, furnace_spec=None):
        if furnace_spec:
            material = furnace_spec
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
            material = "Per approved HVAC equipment schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Furnace",
            "status": status,
            "source": "approved_hvac_equipment_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }

    def air_conditioner(self, quantity, ac_spec=None):
        if ac_spec:
            material = ac_spec
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
            material = "Per approved HVAC equipment schedule"
            total_quantity = None
            material_takeoff = []
            status = "plan_required"

        return {
            "type": "Air Conditioner Unit",
            "status": status,
            "source": "approved_hvac_equipment_schedule",
            "material": material,
            "quantity": quantity,
            "total_quantity": total_quantity,
            "material_takeoff": material_takeoff
        }