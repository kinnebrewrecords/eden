import math
from Settings import Settings
from EstimatingPreferences import EstimatingPreferences


class ConcreteEstimator:

    def _get_concrete_waste_percent(self, waste_percent):
        if waste_percent is not None:
            return waste_percent

        preferences = EstimatingPreferences()

        return preferences.get(
            "concrete_waste_percent"
        )

    def __init__(self):
        pass

    def _get_gravel_base_depth_inches(
            self,
            depth_inches=None
    ):
        if depth_inches is not None:
            return depth_inches

        return EstimatingPreferences().get(
            "gravel_base_depth_inches"
        )

    def _get_aggregate_base_material(self, material=None):
        if material:
            return str(material).strip()

        return EstimatingPreferences().get(
            "aggregate_base_material"
        )

    def _get_aggregate_base_tons_per_cubic_yard(
            self,
            tons_per_cubic_yard=None
    ):
        if tons_per_cubic_yard is not None:
            return float(tons_per_cubic_yard)

        return float(EstimatingPreferences().get(
            "aggregate_base_tons_per_cubic_yard"
        ))

    def _get_aggregate_base_purchase_unit(self, purchase_unit=None):
        if purchase_unit:
            return str(purchase_unit).strip().upper()

        return str(EstimatingPreferences().get(
            "aggregate_base_purchase_unit"
        )).upper()

    def _aggregate_base_takeoff(
            self,
            area_sqft,
            depth_inches=None,
            waste_percent=None,
            material=None,
            tons_per_cubic_yard=None,
            purchase_unit=None
    ):
        """Return one priced takeoff line plus both volume measurements."""
        depth_inches = self._get_gravel_base_depth_inches(depth_inches)
        material = self._get_aggregate_base_material(material)
        tons_per_cubic_yard = (
            self._get_aggregate_base_tons_per_cubic_yard(
                tons_per_cubic_yard
            )
        )
        purchase_unit = self._get_aggregate_base_purchase_unit(
            purchase_unit
        )
        waste_percent = self._get_concrete_waste_percent(waste_percent)

        cubic_yards = (
            float(area_sqft) * (float(depth_inches) / 12) / 27 *
            (1 + float(waste_percent) / 100)
        )
        estimated_tons = cubic_yards * tons_per_cubic_yard

        if purchase_unit not in ["CY", "TONS"]:
            purchase_unit = "CY"

        purchase_quantity = (
            estimated_tons
            if purchase_unit == "TONS"
            else cubic_yards
        )

        return {
            "item": material,
            "unit": purchase_unit,
            "quantity": round(purchase_quantity, 2),
            "base_depth_inches": round(float(depth_inches), 2),
            "cubic_yards": round(cubic_yards, 2),
            "estimated_tons": round(estimated_tons, 2)
        }

    def aggregate_base(
            self,
            area_sqft,
            depth_inches=None,
            material=None,
            tons_per_cubic_yard=None,
            purchase_unit=None,
            waste_percent=None
    ):
        takeoff = self._aggregate_base_takeoff(
            area_sqft=area_sqft,
            depth_inches=depth_inches,
            material=material,
            tons_per_cubic_yard=tons_per_cubic_yard,
            purchase_unit=purchase_unit,
            waste_percent=waste_percent
        )

        return {
            "type": "Aggregate Base",
            "area_sqft": round(float(area_sqft), 2),
            "material": takeoff["item"],
            "base_depth_inches": takeoff["base_depth_inches"],
            "cubic_yards": takeoff["cubic_yards"],
            "estimated_tons": takeoff["estimated_tons"],
            "purchase_unit": takeoff["unit"],
            "order_quantity": takeoff["quantity"],
            "waste_percent": self._get_concrete_waste_percent(
                waste_percent
            ),
            "material_takeoff": [takeoff]
        }

    def _get_form_board_length_feet(
            self,
            length_feet=None
    ):
        if length_feet is not None:
            return length_feet

        return EstimatingPreferences().get(
            "form_board_length_feet"
        )

    def _get_concrete_form_tube_length_feet(
            self,
            length_feet=None
    ):
        if length_feet is not None:
            return length_feet

        return EstimatingPreferences().get(
            "concrete_form_tube_length_feet"
        )

    def concrete_slab(
            self,
            length,
            width,
            thickness_inches,
            reinforced=False,
            rebar=None,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            control_joints=False,
            forms=False,
            build_type=None,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12

        cubic_feet = (
                length *
                width *
                thickness_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        flatwork_takeoff = self._flatwork_material_takeoff(
            length=length,
            width=width,
            cubic_yards=cubic_yards,
            waste_percent=waste_percent,
            wire_mesh=wire_mesh,
            vapor_barrier=vapor_barrier,
            gravel_base=gravel_base,
            forms=forms,
            form_item="Slab Forms"
        )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                flatwork_takeoff["material_takeoff"],
                rebar["takeoff"]
            )

        return {

            "type": "Concrete Slab",

            "material": "Ready Mix Concrete",

            "build_type": build_type,

            # Dimensions
            "length": length,
            "width": width,
            "thickness_inches": thickness_inches,
            "thickness_feet": round(thickness_feet, 2),

            # Concrete
            "area_sqft": flatwork_takeoff["area_sqft"],
            "perimeter_lf": flatwork_takeoff["perimeter_lf"],
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "waste_percent": waste_percent,

            # Assembly
            "reinforced": reinforced,
            "rebar": rebar,
            "wire_mesh": wire_mesh,
            "vapor_barrier": vapor_barrier,
            "gravel_base": gravel_base,
            "control_joints": control_joints,
            "forms": forms,
            "material_takeoff": flatwork_takeoff["material_takeoff"],

        }

    def concrete_footing(
            self,
            length,
            width,
            depth_inches,
            reinforced=False,
            rebar=None,
            forms=False,
            gravel_base=False,
            waste_percent=None,
            build_type=None,
    ):
        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        form_board_length_feet = (
            self._get_form_board_length_feet()
        )

        gravel_depth_inches = (
            self._get_gravel_base_depth_inches()
        )

        depth_feet = depth_inches / 12

        cubic_feet = (
                length *
                width *
                depth_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        footing_area_sqft = length * width

        form_contact_area_sqft = (
                2 * (length + width) * depth_feet
        )

        waste_multiplier = 1 + waste_percent / 100
        footing_perimeter_lf = 2 * (length + width)

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            form_boards = math.ceil(
                footing_perimeter_lf *
                waste_multiplier /
                form_board_length_feet
            )

            material_takeoff.append(
                {
                    "item": (
                        f"Footing Form Boards "
                        f"(2x4 x {form_board_length_feet} ft)"
                    ),
                    "unit": "EA",
                    "quantity": form_boards
                }
            )

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    footing_area_sqft,
                    depth_inches=gravel_depth_inches,
                    waste_percent=waste_percent
                )
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {
            "type": "Concrete Footing",
            "build_type": build_type,
            "material": "Ready Mix Concrete",
            "length": length,
            "width": width,
            "depth_inches": depth_inches,
            "depth_feet": round(depth_feet, 2),
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "reinforced": reinforced,
            "rebar": rebar,
            "forms": forms,
            "gravel_base": gravel_base,
            "waste_percent": waste_percent,
            "footing_area_sqft": round(footing_area_sqft, 2),
            "form_contact_area_sqft": round(
                form_contact_area_sqft,
                2
            ),
            "material_takeoff": material_takeoff,
        }

    def concrete_footing_system(
            self,
            footing_runs,
            reinforced=False,
            rebar=None,
            forms=False,
            gravel_base=False,
            waste_percent=None,
            build_type="Continuous Footing System"
    ):
        """Estimate multiple continuous footing runs as one foundation system.

        Each new run needs length, width_inches, depth_inches, and an optional
        quantity. Older saved runs with width in feet remain supported.
        Concrete is rounded once for the full system rather than once per run.
        """
        waste_percent = self._get_concrete_waste_percent(waste_percent)
        form_board_length_feet = self._get_form_board_length_feet()
        gravel_depth_inches = self._get_gravel_base_depth_inches()
        waste_multiplier = 1 + waste_percent / 100
        normalized_runs = []
        total_cubic_feet = 0.0
        total_footprint_sqft = 0.0
        total_form_perimeter_lf = 0.0

        for run in footing_runs:
            length = float(run["length"])
            if run.get("width_inches") is not None:
                width_inches = float(run["width_inches"])
                width = width_inches / 12
            elif run.get("width") is not None:
                # Backward compatibility for estimates saved before the
                # explicit width_inches field was introduced.
                width = float(run["width"])
                width_inches = width * 12
            else:
                raise ValueError(
                    "Each footing run needs a width in inches."
                )
            depth_inches = float(run["depth_inches"])
            quantity = int(run.get("quantity", 1) or 1)

            if length <= 0 or width <= 0 or depth_inches <= 0 or quantity <= 0:
                raise ValueError("Each footing run needs positive dimensions.")

            depth_feet = depth_inches / 12
            cubic_feet = length * width * depth_feet * quantity
            footprint_sqft = length * width * quantity
            form_perimeter_lf = 2 * (length + width) * quantity

            total_cubic_feet += cubic_feet
            total_footprint_sqft += footprint_sqft
            total_form_perimeter_lf += form_perimeter_lf
            normalized_runs.append(
                {
                    "length": length,
                    "width": width,
                    "width_inches": round(width_inches, 2),
                    "depth_inches": depth_inches,
                    "quantity": quantity,
                    "cubic_yards": round(cubic_feet / 27, 2)
                }
            )

        if not normalized_runs:
            raise ValueError("Add at least one footing run.")

        cubic_yards = total_cubic_feet / 27
        order_quantity = math.ceil(cubic_yards * waste_multiplier)
        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            material_takeoff.append(
                {
                    "item": (
                        "Footing System Form Boards "
                        f"(2x4 x {form_board_length_feet} ft)"
                    ),
                    "unit": "EA",
                    "quantity": math.ceil(
                        total_form_perimeter_lf * waste_multiplier /
                        form_board_length_feet
                    )
                }
            )

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    total_footprint_sqft,
                    depth_inches=gravel_depth_inches,
                    waste_percent=waste_percent
                )
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {
            "type": "Concrete Footing System",
            "build_type": build_type,
            "material": "Ready Mix Concrete",
            "footing_runs": normalized_runs,
            "run_count": sum(run["quantity"] for run in normalized_runs),
            "cubic_feet": round(total_cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "reinforced": reinforced,
            "rebar": rebar,
            "forms": forms,
            "gravel_base": gravel_base,
            "waste_percent": waste_percent,
            "footing_area_sqft": round(total_footprint_sqft, 2),
            "form_perimeter_lf": round(total_form_perimeter_lf, 2),
            "material_takeoff": material_takeoff,
            "structural_note": (
                "Footing size, reinforcing, stepped elevations, and bearing "
                "requirements must match approved structural plans."
            )
        }

    def concrete_foundation_wall(
            self,
            length,
            height,
            thickness_inches,
            reinforced=False,
            rebar=None,
            forms=False,
            waterproofing=False,
            build_type=None,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12

        cubic_feet = (
                length *
                height *
                thickness_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        wall_area_sqft = length * height
        form_contact_area_sqft = wall_area_sqft * 2

        waste_multiplier = 1 + waste_percent / 100

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            form_panels = math.ceil(
                form_contact_area_sqft *
                waste_multiplier /
                Settings.WALL_FORM_PANEL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "4x8 Foundation Wall Form Panels",
                    "unit": "EA",
                    "quantity": form_panels
                }
            )

        if waterproofing:
            waterproofing_pails = math.ceil(
                wall_area_sqft *
                waste_multiplier /
                Settings.FOUNDATION_WATERPROOFING_PAIL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "Foundation Waterproofing (5 gal pail)",
                    "unit": "PAILS",
                    "quantity": waterproofing_pails
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Foundation Wall",

            "build_type": build_type,

            "material": "Ready Mix Concrete",

            "length": length,

            "height": height,

            "thickness_inches": thickness_inches,

            "thickness_feet": round(
                thickness_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly

            "reinforced": reinforced,

            "rebar": rebar,

            "forms": forms,

            "waterproofing": waterproofing,

            "waste_percent": waste_percent,

            "wall_area_sqft": round(wall_area_sqft, 2),
            "form_contact_area_sqft": round(form_contact_area_sqft, 2),
            "material_takeoff": material_takeoff,
        }

    def concrete_pad(
            self,
            length,
            width,
            thickness_inches,
            reinforced=False,
            rebar=None,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            control_joints=False,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12
        cubic_feet = length * width * thickness_feet
        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards * (1 + waste_percent / 100)
        )

        flatwork_takeoff = self._flatwork_material_takeoff(
            length=length,
            width=width,
            cubic_yards=cubic_yards,
            waste_percent=waste_percent,
            wire_mesh=wire_mesh,
            vapor_barrier=vapor_barrier,
            gravel_base=gravel_base,
            forms=forms,
            form_item="Pad Forms"  # change per method
        )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                flatwork_takeoff["material_takeoff"],
                rebar["takeoff"]
            )

        return {
            "type": "Concrete Pad",
            "material": "Ready Mix Concrete",

            "length": length,
            "width": width,
            "thickness_inches": thickness_inches,
            "thickness_feet": round(thickness_feet, 2),

            "area_sqft": flatwork_takeoff["area_sqft"],
            "perimeter_lf": flatwork_takeoff["perimeter_lf"],
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "waste_percent": waste_percent,

            "reinforced": reinforced,
            "rebar": rebar,
            "wire_mesh": wire_mesh,
            "vapor_barrier": vapor_barrier,
            "gravel_base": gravel_base,
            "control_joints": control_joints,
            "forms": forms,

            "material_takeoff": flatwork_takeoff["material_takeoff"],
        }

    def concrete_pier(
            self,
            diameter_inches,
            height,
            quantity=1,
            reinforced=False,
            rebar=None,
            forms=False,
            gravel_base=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        radius_feet = (
                              diameter_inches / 12
                      ) / 2

        volume_per_pier = (
                math.pi *
                (radius_feet ** 2) *
                height
        )

        total_cubic_feet = (
                volume_per_pier *
                quantity
        )

        cubic_yards = (
                total_cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        footprint_sqft_each = math.pi * (radius_feet ** 2)
        total_footprint_sqft = footprint_sqft_each * quantity
        form_contact_area_sqft = (
            2 * math.pi * radius_feet * height * quantity
        )

        waste_multiplier = 1 + waste_percent / 100

        form_tube_length_feet = (
            self._get_concrete_form_tube_length_feet()
        )

        gravel_depth_inches = (
            self._get_gravel_base_depth_inches()
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            tubes_per_pier = math.ceil(
                height / form_tube_length_feet
            )

            total_tubes = tubes_per_pier * quantity

            material_takeoff.append(
                {
                    "item": (
                        f"{diameter_inches} in Concrete Form Tubes "
                        f"({form_tube_length_feet} ft)"
                    ),
                    "unit": "EA",
                    "quantity": total_tubes
                }
            )

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    total_footprint_sqft,
                    depth_inches=gravel_depth_inches,
                    waste_percent=waste_percent
                )
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Pier",

            "material": "Ready Mix Concrete",

            "diameter_inches": diameter_inches,

            "height": height,

            "quantity": quantity,

            "cubic_feet_each": round(
                volume_per_pier,
                2
            ),

            "total_cubic_feet": round(
                total_cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly

            "reinforced": reinforced,

            "rebar": rebar,

            "forms": forms,

            "gravel_base": gravel_base,

            "footprint_sqft_each": round(footprint_sqft_each, 2),
            "total_footprint_sqft": round(total_footprint_sqft, 2),
            "form_contact_area_sqft": round(form_contact_area_sqft, 2),
            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_column(
            self,
            diameter_inches,
            height,
            quantity=1,
            reinforced=False,
            rebar=None,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        radius_feet = (
                              diameter_inches / 12
                      ) / 2

        volume_each = (
                math.pi *
                (radius_feet ** 2) *
                height
        )

        total_cubic_feet = (
                volume_each *
                quantity
        )

        cubic_yards = (
                total_cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        footprint_sqft_each = math.pi * (radius_feet ** 2)
        total_footprint_sqft = footprint_sqft_each * quantity
        form_contact_area_sqft = (
            2 * math.pi * radius_feet * height * quantity
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            tubes_per_column = math.ceil(
                height / Settings.CONCRETE_FORM_TUBE_LENGTH_FEET
            )

            total_tubes = tubes_per_column * quantity

            material_takeoff.append(
                {
                    "item": (
                        f"{diameter_inches} in Concrete Form Tubes "
                        f"({Settings.CONCRETE_FORM_TUBE_LENGTH_FEET} ft)"
                    ),
                    "unit": "EA",
                    "quantity": total_tubes
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Column",

            "material": "Ready Mix Concrete",

            "diameter_inches": diameter_inches,

            "height": height,

            "quantity": quantity,

            "cubic_feet_each": round(
                volume_each,
                2
            ),

            "total_cubic_feet": round(
                total_cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly

            "reinforced": reinforced,

            "rebar": rebar,

            "forms": forms,

            "footprint_sqft_each": round(footprint_sqft_each, 2),
            "total_footprint_sqft": round(total_footprint_sqft, 2),
            "form_contact_area_sqft": round(form_contact_area_sqft, 2),
            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_curb(
            self,
            length,
            width_inches,
            height_inches,
            reinforced=False,
            rebar=None,
            forms=False,
            gravel_base=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        width_feet = width_inches / 12
        height_feet = height_inches / 12

        cubic_feet = (
                length *
                width_feet *
                height_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        waste_multiplier = 1 + waste_percent / 100
        curb_footprint_sqft = length * width_feet

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            form_boards = math.ceil(
                (length * 2) *
                waste_multiplier /
                Settings.FORM_BOARD_LENGTH_FEET
            )

            material_takeoff.append(
                {
                    "item": (
                        f"Curb Form Boards "
                        f"({Settings.FORM_BOARD_LENGTH_FEET} ft)"
                    ),
                    "unit": "EA",
                    "quantity": form_boards
                }
            )

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    curb_footprint_sqft,
                    waste_percent=waste_percent
                )
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Curb",

            "material": "Ready Mix Concrete",

            "length": length,

            "width_inches": width_inches,

            "height_inches": height_inches,

            "width_feet": round(
                width_feet,
                2
            ),

            "height_feet": round(
                height_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly Materials

            "reinforced": reinforced,

            "rebar": rebar,

            "forms": forms,

            "gravel_base": gravel_base,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_sidewalk(
            self,
            length,
            width,
            thickness_inches,
            reinforced=False,
            rebar=None,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            control_joints=False,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12
        cubic_feet = length * width * thickness_feet
        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards * (1 + waste_percent / 100)
        )

        flatwork_takeoff = self._flatwork_material_takeoff(
            length=length,
            width=width,
            cubic_yards=cubic_yards,
            waste_percent=waste_percent,
            wire_mesh=wire_mesh,
            vapor_barrier=vapor_barrier,
            gravel_base=gravel_base,
            forms=forms,
            form_item="Sidewalk Forms"  # change per method
        )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                flatwork_takeoff["material_takeoff"],
                rebar["takeoff"]
            )

        return {
            "type": "Concrete Sidewalk",
            "material": "Ready Mix Concrete",

            "length": length,
            "width": width,
            "thickness_inches": thickness_inches,
            "thickness_feet": round(thickness_feet, 2),
            "area_sqft": flatwork_takeoff["area_sqft"],
            "perimeter_lf": flatwork_takeoff["perimeter_lf"],
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "waste_percent": waste_percent,

            "reinforced": reinforced,
            "rebar": rebar,
            "wire_mesh": wire_mesh,
            "vapor_barrier": vapor_barrier,
            "gravel_base": gravel_base,
            "control_joints": control_joints,
            "forms": forms,

            "material_takeoff": flatwork_takeoff["material_takeoff"],
        }

    def concrete_driveway(
            self,
            length,
            width,
            thickness_inches,
            reinforced=False,
            rebar=None,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            control_joints=False,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12
        cubic_feet = length * width * thickness_feet
        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards * (1 + waste_percent / 100)
        )

        flatwork_takeoff = self._flatwork_material_takeoff(
            length=length,
            width=width,
            cubic_yards=cubic_yards,
            waste_percent=waste_percent,
            wire_mesh=wire_mesh,
            vapor_barrier=vapor_barrier,
            gravel_base=gravel_base,
            forms=forms,
            form_item="Driveway Forms"  # change per method
        )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                flatwork_takeoff["material_takeoff"],
                rebar["takeoff"]
            )

        return {
            "type": "Concrete Driveway",
            "material": "Ready Mix Concrete",

            "length": length,
            "width": width,
            "thickness_inches": thickness_inches,
            "thickness_feet": round(thickness_feet, 2),
            "area_sqft": flatwork_takeoff["area_sqft"],
            "perimeter_lf": flatwork_takeoff["perimeter_lf"],
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "waste_percent": waste_percent,

            "reinforced": reinforced,
            "rebar": rebar,
            "wire_mesh": wire_mesh,
            "vapor_barrier": vapor_barrier,
            "gravel_base": gravel_base,
            "control_joints": control_joints,
            "forms": forms,

            "material_takeoff": flatwork_takeoff["material_takeoff"],
        }

    def concrete_patio(
            self,
            length,
            width,
            thickness_inches,
            reinforced=False,
            rebar=None,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            control_joints=False,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12

        cubic_feet = (
                length *
                width *
                thickness_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        flatwork_takeoff = self._flatwork_material_takeoff(
            length=length,
            width=width,
            cubic_yards=cubic_yards,
            waste_percent=waste_percent,
            wire_mesh=wire_mesh,
            vapor_barrier=vapor_barrier,
            gravel_base=gravel_base,
            forms=forms,
            form_item="Patio Forms"  # change per method
        )

        if rebar and rebar.get("status") == "specified":
            for rebar_item in rebar.get("takeoff", []):
                flatwork_takeoff["material_takeoff"].append(
                    {
                        "item": (
                            f"{rebar_item['size']} Rebar "
                            f"({rebar_item['stock_length_feet']} ft sticks)"
                        ),
                        "unit": "EA",
                        "quantity": rebar_item["sticks"]
                    }
                )

        return {

            "type": "Concrete Patio",

            "material": "Ready Mix Concrete",

            "length": length,

            "width": width,

            "thickness_inches": thickness_inches,

            "thickness_feet": round(
                thickness_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly Materials

            "reinforced": reinforced,

            "rebar": rebar,

            "wire_mesh": wire_mesh,

            "vapor_barrier": vapor_barrier,

            "gravel_base": gravel_base,

            "control_joints": control_joints,

            "forms": forms,

            "area_sqft": flatwork_takeoff["area_sqft"],
            "perimeter_lf": flatwork_takeoff["perimeter_lf"],
            "material_takeoff": flatwork_takeoff["material_takeoff"],

            "waste_percent": waste_percent

        }

    def concrete_steps(
            self,
            width,
            tread_depth,
            riser_height_inches,
            steps,
            reinforced=False,
            rebar=None,
            gravel_base=False,
            vapor_barrier=False,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        riser_height = riser_height_inches / 12
        tread_depth_feet = tread_depth / 12

        total_cubic_feet = 0

        for step in range(1, steps + 1):
            step_height = (
                    riser_height * step
            )

            step_volume = (
                    width *
                    tread_depth_feet *
                    step_height
            )

            total_cubic_feet += step_volume

        cubic_yards = (
                total_cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        total_run_feet = tread_depth_feet * steps
        footprint_sqft = width * total_run_feet
        waste_multiplier = 1 + waste_percent / 100

        riser_form_area_sqft = width * riser_height * steps
        side_form_area_sqft = 2 * (total_cubic_feet / width)
        form_contact_area_sqft = (
            riser_form_area_sqft +
            side_form_area_sqft
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    footprint_sqft,
                    waste_percent=waste_percent
                )
            )

        if vapor_barrier:
            vapor_barrier_rolls = math.ceil(
                footprint_sqft *
                waste_multiplier /
                Settings.VAPOR_BARRIER_ROLL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "6 mil Vapor Barrier",
                    "unit": "ROLLS",
                    "quantity": vapor_barrier_rolls
                }
            )

        if forms:
            form_panels = math.ceil(
                form_contact_area_sqft *
                waste_multiplier /
                Settings.FORM_PANEL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "4x8 Concrete Step Form Panels",
                    "unit": "EA",
                    "quantity": form_panels
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Steps",

            "material": "Ready Mix Concrete",

            "width": width,

            "tread_depth_inches": tread_depth ,

            "riser_height_inches": riser_height_inches,

            "steps": steps,

            "cubic_feet": round(
                total_cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly Materials

            "reinforced": reinforced,

            "rebar": rebar,

            "gravel_base": gravel_base,

            "vapor_barrier": vapor_barrier,

            "forms": forms,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_beam(
            self,
            length,
            width_inches,
            height_inches,
            reinforced=False,
            rebar=None,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        width_feet = width_inches / 12
        height_feet = height_inches / 12

        cubic_feet = (
                length *
                width_feet *
                height_feet
        )

        cubic_yards = (
                cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        waste_multiplier = 1 + waste_percent / 100
        form_contact_area_sqft = (
            length *
            (width_feet + (2 * height_feet))
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            form_panels = math.ceil(
                form_contact_area_sqft *
                waste_multiplier /
                Settings.FORM_PANEL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "4x8 Concrete Beam Form Panels",
                    "unit": "EA",
                    "quantity": form_panels
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Beam",

            "material": "Ready Mix Concrete",

            "length": length,

            "width_inches": width_inches,

            "height_inches": height_inches,

            "width_feet": round(
                width_feet,
                2
            ),

            "height_feet": round(
                height_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly

            "reinforced": reinforced,

            "rebar": rebar,

            "forms": forms,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_ramp(
            self,
            length,
            width,
            height_inches,
            reinforced=False,
            rebar=None,
            gravel_base=False,
            forms=False,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        height_feet = height_inches / 12

        average_height = height_feet / 2

        cubic_feet = (
                length *
                width *
                average_height
        )

        cubic_yards = (
                cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        waste_multiplier = 1 + waste_percent / 100
        ramp_footprint_sqft = length * width

        side_form_area_sqft = length * height_feet
        end_form_area_sqft = width * height_feet
        form_contact_area_sqft = (
            side_form_area_sqft +
            end_form_area_sqft
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    ramp_footprint_sqft,
                    waste_percent=waste_percent
                )
            )

        if forms:
            form_panels = math.ceil(
                form_contact_area_sqft *
                waste_multiplier /
                Settings.FORM_PANEL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "4x8 Concrete Ramp Form Panels",
                    "unit": "EA",
                    "quantity": form_panels
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Ramp",

            "material": "Ready Mix Concrete",

            "length": length,

            "width": width,

            "height_inches": height_inches,

            "height_feet": round(
                height_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            # Assembly

            "reinforced": reinforced,

            "rebar": rebar,

            "gravel_base": gravel_base,

            "forms": forms,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_trench(
            self,
            length,
            width_inches,
            depth_inches,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        width_feet = width_inches / 12
        depth_feet = depth_inches / 12

        cubic_feet = (
                length *
                width_feet *
                depth_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {

            "type": "Concrete Trench",

            "material": "Ready Mix Concrete",

            "length": length,

            "width_inches": width_inches,

            "depth_inches": depth_inches,

            "width_feet": round(
                width_feet,
                2
            ),

            "depth_feet": round(
                depth_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_retaining_wall(
            self,
            length,
            height,
            thickness_inches,
            waste_percent=None    ):
        
        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        thickness_feet = thickness_inches / 12

        cubic_feet = (
                length *
                thickness_feet *
                height
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {

            "type": "Concrete Retaining Wall",

            "material": "Ready Mix Concrete",

            "length": length,

            "height": height,

            "thickness_inches": thickness_inches,

            "thickness_feet": round(
                thickness_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_grade_beam(
            self,
            length,
            width_inches,
            height_inches,
            reinforced=False,
            rebar=None,
            forms=False,
            build_type=None,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        width_feet = width_inches / 12
        height_feet = height_inches / 12

        cubic_feet = (
                length *
                width_feet *
                height_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        waste_multiplier = 1 + waste_percent / 100
        form_contact_area_sqft = (
            length *
            (width_feet + (2 * height_feet))
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if forms:
            form_panels = math.ceil(
                form_contact_area_sqft *
                waste_multiplier /
                Settings.FORM_PANEL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "4x8 Grade Beam Form Panels",
                    "unit": "EA",
                    "quantity": form_panels
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {

            "type": "Concrete Grade Beam",

            "material": "Ready Mix Concrete",

            "build_type": build_type,
            "reinforced": reinforced,
            "rebar": rebar,
            "forms": forms,

            "length": length,

            "width_inches": width_inches,

            "height_inches": height_inches,

            "width_feet": round(
                width_feet,
                2
            ),

            "height_feet": round(
                height_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_spread_footing(
            self,
            length,
            width,
            depth_inches,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        depth_feet = depth_inches / 12

        cubic_feet = (
                length *
                width *
                depth_feet
        )

        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        footing_area_sqft = length * width

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {

            "type": "Concrete Spread Footing",

            "material": "Ready Mix Concrete",

            "length": length,

            "width": width,

            "depth_inches": depth_inches,

            "depth_feet": round(
                depth_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "footing_area_sqft": round(footing_area_sqft, 2),
            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_round_footing(
            self,
            diameter_inches,
            depth,
            quantity=1,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        radius_feet = (
                              diameter_inches / 12
                      ) / 2

        volume_each = (
                math.pi *
                (radius_feet ** 2) *
                depth
        )

        total_cubic_feet = (
                volume_each *
                quantity
        )

        cubic_yards = (
                total_cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        footprint_sqft_each = math.pi * (radius_feet ** 2)
        total_footprint_sqft = footprint_sqft_each * quantity

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {

            "type": "Concrete Round Footing",

            "material": "Ready Mix Concrete",

            "diameter_inches": diameter_inches,

            "depth": depth,

            "quantity": quantity,

            "cubic_feet_each": round(
                volume_each,
                2
            ),

            "total_cubic_feet": round(
                total_cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "footprint_sqft_each": round(footprint_sqft_each, 2),
            "total_footprint_sqft": round(total_footprint_sqft, 2),
            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_pile_cap(
            self,
            length,
            width,
            depth_inches,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        depth_feet = depth_inches / 12

        cubic_feet = (
                length *
                width *
                depth_feet
        )

        cubic_yards = (
                cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {

            "type": "Concrete Pile Cap",

            "material": "Ready Mix Concrete",

            "length": length,

            "width": width,

            "depth_inches": depth_inches,

            "depth_feet": round(
                depth_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_lintel(
            self,
            length,
            width_inches,
            height_inches,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        width_feet = width_inches / 12
        height_feet = height_inches / 12

        cubic_feet = (
                length *
                width_feet *
                height_feet
        )

        cubic_yards = (
                cubic_feet / 27
        )

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {

            "type": "Concrete Lintel",

            "material": "Ready Mix Concrete",

            "length": length,

            "width_inches": width_inches,

            "height_inches": height_inches,

            "width_feet": round(
                width_feet,
                2
            ),

            "height_feet": round(
                height_feet,
                2
            ),

            "cubic_feet": round(
                cubic_feet,
                2
            ),

            "cubic_yards": round(
                cubic_yards,
                2
            ),

            "order_quantity": order_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def concrete_slab_edge(
            self,
            length,
            width,
            edge_width_inches,
            edge_depth_inches,
            waste_percent=None    ):

        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        edge_width_feet = edge_width_inches / 12
        edge_depth_feet = edge_depth_inches / 12

        perimeter_lf = 2 * (length + width)

        inner_length = max(length - (2 * edge_width_feet), 0)
        inner_width = max(width - (2 * edge_width_feet), 0)

        edge_area_sqft = (
            (length * width) -
            (inner_length * inner_width)
        )

        cubic_feet = edge_area_sqft * edge_depth_feet
        cubic_yards = cubic_feet / 27

        order_quantity = math.ceil(
            cubic_yards *
            (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        return {
            "type": "Thickened Concrete Slab Edge",
            "material": "Ready Mix Concrete",

            "length": length,
            "width": width,
            "edge_width_inches": edge_width_inches,
            "edge_depth_inches": edge_depth_inches,

            "perimeter_lf": round(perimeter_lf, 2),
            "edge_area_sqft": round(edge_area_sqft, 2),
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    #### HELPERS ####

    def rectangular_concrete(self,length,width,depth,waste_percent):
        volume = length * width * depth
        yards = volume / 27
        return self.add_waste(yards,waste_percent)

    def cylinder_concrete(self,diameter_inches,height,quantity,waste_percent):
        radius = (diameter_inches / 12) / 2
        area = math.pi * radius ** 2
        volume = area * height
        total_volume = volume * quantity
        yards = total_volume / 27
        return self.add_waste(yards, waste_percent)

    def add_waste(self, yards, waste_percent):
        waste = yards * (waste_percent / 100)
        total = yards + waste
        return {
            "yards": round(total, 2),
            "order": math.ceil(total)
        }

    def _flatwork_material_takeoff(
            self,
            length,
            width,
            cubic_yards,
            waste_percent,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            forms=False,
            form_item="Concrete Forms"
    ):
        area_sqft = length * width
        perimeter_lf = 2 * (length + width)
        waste_multiplier = 1 + waste_percent / 100

        gravel_depth_inches = (
            self._get_gravel_base_depth_inches()
        )

        form_board_length_feet = (
            self._get_form_board_length_feet()
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": math.ceil(
                    cubic_yards * waste_multiplier
                )
            }
        ]

        if wire_mesh:
            mesh_sheets = math.ceil(
                area_sqft *
                waste_multiplier /
                Settings.WIRE_MESH_SHEET_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "5x10 Wire Mesh Sheets",
                    "unit": "SHEETS",
                    "quantity": mesh_sheets
                }
            )

        if vapor_barrier:
            vapor_barrier_rolls = math.ceil(
                area_sqft *
                waste_multiplier /
                Settings.VAPOR_BARRIER_ROLL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "6 mil Vapor Barrier",
                    "unit": "ROLLS",
                    "quantity": vapor_barrier_rolls
                }
            )

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    area_sqft,
                    depth_inches=gravel_depth_inches,
                    waste_percent=waste_percent
                )
            )

        if forms:
            form_boards = math.ceil(
                perimeter_lf *
                waste_multiplier /
                form_board_length_feet
            )

            material_takeoff.append(
                {
                    "item": (
                        f"{form_item} "
                        f"(2x4 x {form_board_length_feet} ft)"
                    ),
                    "unit": "EA",
                    "quantity": form_boards
                }
            )

        return {
            "area_sqft": round(area_sqft, 2),
            "perimeter_lf": round(perimeter_lf, 2),
            "material_takeoff": material_takeoff
        }

    def _append_rebar_material_takeoff(
            self,
            material_takeoff,
            rebar_takeoffs
    ):
        for rebar_item in rebar_takeoffs:
            if not rebar_item:
                continue

            material_takeoff.append(
                {
                    "item": (
                        f"{rebar_item['size']} Rebar "
                        f"({rebar_item['stock_length_feet']} ft sticks)"
                    ),
                    "unit": "EA",
                    "quantity": rebar_item["sticks"]
                }
            )
                                                                                                                                                                                                                                 

    def concrete_custom_flatwork(
            self,
            area_sqft,
            perimeter_lf,
            thickness_inches,
            reinforced=False,
            rebar=None,
            wire_mesh=False,
            vapor_barrier=False,
            gravel_base=False,
            control_joints=False,
            forms=False,
            build_type="Custom Concrete Flatwork",
            waste_percent=None
    ):
        waste_percent = self._get_concrete_waste_percent(
            waste_percent
        )

        gravel_depth_inches = (
            self._get_gravel_base_depth_inches()
        )

        form_board_length_feet = (
            self._get_form_board_length_feet()
        )

        thickness_feet = thickness_inches / 12
        cubic_feet = area_sqft * thickness_feet
        cubic_yards = cubic_feet / 27
        waste_multiplier = 1 + waste_percent / 100

        order_quantity = math.ceil(
            cubic_yards * waste_multiplier
        )

        material_takeoff = [
            {
                "item": "Ready Mix Concrete",
                "unit": "CY",
                "quantity": order_quantity
            }
        ]

        if wire_mesh:
            mesh_sheets = math.ceil(
                area_sqft *
                waste_multiplier /
                Settings.WIRE_MESH_SHEET_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "5x10 Wire Mesh Sheets",
                    "unit": "SHEETS",
                    "quantity": mesh_sheets
                }
            )

        if vapor_barrier:
            vapor_barrier_rolls = math.ceil(
                area_sqft *
                waste_multiplier /
                Settings.VAPOR_BARRIER_ROLL_COVERAGE_SQFT
            )

            material_takeoff.append(
                {
                    "item": "6 mil Vapor Barrier",
                    "unit": "ROLLS",
                    "quantity": vapor_barrier_rolls
                }
            )

        if gravel_base:
            material_takeoff.append(
                self._aggregate_base_takeoff(
                    area_sqft,
                    depth_inches=gravel_depth_inches,
                    waste_percent=waste_percent
                )
            )

        if forms:
            form_boards = math.ceil(
                perimeter_lf *
                waste_multiplier /
                form_board_length_feet
            )

            material_takeoff.append(
                {
                    "item": (
                        f"Custom Flatwork Forms "
                        f"(2x4 x {form_board_length_feet} ft)"
                    ),
                    "unit": "EA",
                    "quantity": form_boards
                }
            )

        if rebar and rebar.get("status") == "specified":
            self._append_rebar_material_takeoff(
                material_takeoff,
                rebar.get("takeoff", [])
            )

        return {
            "type": "Custom Concrete Flatwork",
            "build_type": build_type,
            "material": "Ready Mix Concrete",
            "area_sqft": round(area_sqft, 2),
            "perimeter_lf": round(perimeter_lf, 2),
            "thickness_inches": thickness_inches,
            "thickness_feet": round(thickness_feet, 2),
            "cubic_feet": round(cubic_feet, 2),
            "cubic_yards": round(cubic_yards, 2),
            "order_quantity": order_quantity,
            "reinforced": reinforced,
            "rebar": rebar,
            "wire_mesh": wire_mesh,
            "vapor_barrier": vapor_barrier,
            "gravel_base": gravel_base,
            "control_joints": control_joints,
            "forms": forms,
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }
