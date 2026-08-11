import math
from Settings import Settings
from EstimatingPreferences import EstimatingPreferences


class LumberEstimator:

    def _get_lumber_waste_percent(self, waste_percent):
        if waste_percent is not None:
            return waste_percent

        preferences = EstimatingPreferences()

        return preferences.get(
            "lumber_waste_percent"
        )

    def _get_lumber_stud_spacing_inches(
            self,
            stud_spacing_inches
    ):
        if stud_spacing_inches is not None:
            return stud_spacing_inches

        return EstimatingPreferences().get(
            "lumber_stud_spacing_inches"
        )

    def _get_lumber_stock_length_feet(
            self,
            stock_length_feet
    ):
        if stock_length_feet is not None:
            return stock_length_feet

        return EstimatingPreferences().get(
            "lumber_stock_length_feet"
        )

    # =========================
    # WALL FRAMING
    # =========================

    def frame_wall(
            self,
            length_feet,
            height_feet,
            stud_spacing_inches=None,
            quantity=1,
            waste_percent=None,
            plate_board_length=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        stud_spacing_inches = (
            self._get_lumber_stud_spacing_inches(
                stud_spacing_inches
            )
        )

        plate_board_length = (
            self._get_lumber_stock_length_feet(
                plate_board_length
            )
        )
        spacing_feet = stud_spacing_inches / 12

        # One stud at each end, plus studs between them.
        stud_count_per_wall = math.ceil(
            length_feet / spacing_feet
        ) + 1

        stud_count = stud_count_per_wall * quantity
        studs_to_order = math.ceil(
            stud_count * (1 + waste_percent / 100)
        )

        if height_feet <= 8:
            stud_length = 8
        elif height_feet <= 10:
            stud_length = 10
        else:
            stud_length = 12

        # One bottom plate and two top plates.
        plate_linear_feet = length_feet * 3 * quantity
        plate_linear_feet_to_order = math.ceil(
            plate_linear_feet * (1 + waste_percent / 100)
        )


        plate_boards = math.ceil(
            plate_linear_feet_to_order / plate_board_length
        )

        wall_area_sqft = length_feet * height_feet * quantity
        material_takeoff = [
            {
                "item": f"2x4 x {stud_length} ft Studs",
                "unit": "EA",
                "quantity": studs_to_order
            },
            {
                "item": f"2x4 x {plate_board_length} ft Plates",
                "unit": "EA",
                "quantity": plate_boards
            }
        ]

        return {
            "type": "Framed Wall",

            "dimensions": {
                "length": length_feet,
                "height": height_feet
            },

            "stud_spacing_inches": stud_spacing_inches,
            "stud_count": stud_count,

            "studs": {
                "size": "2x4",
                "length": f"{stud_length} ft",
                "quantity": studs_to_order
            },

            "plate_linear_feet": plate_linear_feet,

            "plates": {
                "size": "2x4",
                "length": f"{plate_board_length} ft",
                "quantity": plate_boards
            },

            "wall_area_sqft": round(wall_area_sqft, 2),
            "material_takeoff": material_takeoff,
            "quantity": quantity,
            "waste_percent": waste_percent
        }

    def frame_wall_with_openings(
            self,
            length_feet,
            height_feet,
            openings,
            stud_spacing_inches=None,
            quantity=1,
            waste_percent=None,
            plate_board_length=None,
            header_spec=None,
            header_plies=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        stud_spacing_inches = (
            self._get_lumber_stud_spacing_inches(
                stud_spacing_inches
            )
        )

        plate_board_length = (
            self._get_lumber_stock_length_feet(
                plate_board_length
            )
        )

        spacing_feet = stud_spacing_inches / 12

        if height_feet <= 8:
            stud_length = 8
        elif height_feet <= 10:
            stud_length = 10
        else:
            stud_length = 12

        base_stud_count_per_wall = (
                math.ceil(length_feet / spacing_feet) + 1
        )

        opening_stud_positions = 0
        opening_area_sqft_per_wall = 0
        header_linear_feet_per_wall = 0
        window_sill_linear_feet_per_wall = 0

        for opening in openings:
            opening_type = opening["type"].lower()
            opening_width = opening["width_feet"]
            opening_height = opening["height_feet"]

            opening_stud_positions += max(
                1,
                math.ceil(opening_width / spacing_feet)
            )

            opening_area_sqft_per_wall += (
                    opening_width * opening_height
            )

            # Header length includes 6 in bearing at each end.
            header_linear_feet_per_wall += (
                    opening_width + 1
            )

            if opening_type == "window":
                window_sill_linear_feet_per_wall += (
                    opening_width
                )

        field_studs_per_wall = max(
            2,
            base_stud_count_per_wall - opening_stud_positions
        )

        opening_count_per_wall = len(openings)
        king_studs_per_wall = opening_count_per_wall * 2
        jack_studs_per_wall = opening_count_per_wall * 2

        total_studs_before_waste = (
                                           field_studs_per_wall +
                                           king_studs_per_wall +
                                           jack_studs_per_wall
                                   ) * quantity

        studs_to_order = math.ceil(
            total_studs_before_waste *
            (1 + waste_percent / 100)
        )

        plate_linear_feet = length_feet * 3 * quantity

        plate_linear_feet_to_order = math.ceil(
            plate_linear_feet *
            (1 + waste_percent / 100)
        )

        plate_boards = math.ceil(
            plate_linear_feet_to_order /
            plate_board_length
        )

        header_material_specified = bool(
            header_spec
            and header_plies
            and header_plies > 0
        )

        header_linear_feet = (
                header_linear_feet_per_wall *
                quantity
        )

        if header_material_specified:
            header_linear_feet_to_order = round(
                header_linear_feet *
                header_plies *
                (1 + waste_percent / 100),
                2
            )

        else:
            header_linear_feet_to_order = None

        window_sill_linear_feet = (
                window_sill_linear_feet_per_wall *
                quantity
        )

        window_sill_boards = 0

        if window_sill_linear_feet > 0:
            window_sill_boards = math.ceil(
                window_sill_linear_feet *
                (1 + waste_percent / 100) /
                plate_board_length
            )

        gross_wall_area_sqft = (
                length_feet *
                height_feet *
                quantity
        )

        opening_area_sqft = (
                opening_area_sqft_per_wall *
                quantity
        )

        net_wall_area_sqft = (
                gross_wall_area_sqft -
                opening_area_sqft
        )

        material_takeoff = [
            {
                "item": (
                    f"2x4 x {stud_length} ft "
                    "Wall, King, and Jack Studs"
                ),
                "unit": "EA",
                "quantity": studs_to_order
            },
            {
                "item": (
                    f"2x4 x {plate_board_length} ft "
                    "Top and Bottom Plates"
                ),
                "unit": "EA",
                "quantity": plate_boards
            }
        ]

        if header_material_specified:
            material_takeoff.append(
                {
                    "item": (
                        f"Header Material "
                        f"({header_plies} ply {header_spec})"
                    ),
                    "unit": "LF",
                    "quantity": header_linear_feet_to_order
                }
            )

        if window_sill_boards > 0:
            material_takeoff.append(
                {
                    "item": (
                        f"2x4 x {plate_board_length} ft "
                        "Window Sills"
                    ),
                    "unit": "EA",
                    "quantity": window_sill_boards
                }
            )

        return {
            "type": "Framed Wall with Openings",
            "dimensions": {
                "length": length_feet,
                "height": height_feet
            },
            "quantity": quantity,
            "stud_spacing_inches": stud_spacing_inches,
            "stud_length": f"{stud_length} ft",
            "openings": openings,
            "opening_count_per_wall": opening_count_per_wall,
            "field_studs_per_wall": field_studs_per_wall,
            "king_studs_per_wall": king_studs_per_wall,
            "jack_studs_per_wall": jack_studs_per_wall,
            "studs_to_order": studs_to_order,
            "plate_linear_feet": plate_linear_feet,
            "plate_boards": plate_boards,
            "header_spec": (
                    header_spec
                    or "Per approved structural plan"
            ),
            "header_plies": header_plies,
            "header_material_specified": (
                header_material_specified
            ),
            "header_linear_feet": header_linear_feet_to_order,
            "gross_wall_area_sqft": round(
                gross_wall_area_sqft,
                2
            ),
            "opening_area_sqft": round(
                opening_area_sqft,
                2
            ),
            "net_wall_area_sqft": round(
                net_wall_area_sqft,
                2
            ),
            "material_takeoff": material_takeoff,
            "waste_percent": waste_percent,
            "structural_note": (
                "Header size, header plies, cripple studs, and "
                "opening layout must follow approved plans."
            )
        }
    def plates(
            self,
            length,
            plate_type="double top",
            waste_percent=None,
            stock_length_feet=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        stock_length_feet = (
            self._get_lumber_stock_length_feet(
                stock_length_feet
            )
        )

        if plate_type == "bottom":
            layers = 1

        elif plate_type == "top":
            layers = 2

        else:
            layers = 3  # two top plates + one bottom plate

        total_linear_feet = length * layers

        total_with_waste = math.ceil(
            total_linear_feet *
            (1 + waste_percent / 100)
        )

        board_length = stock_length_feet
        boards = math.ceil(
            total_with_waste / board_length
        )

        material_takeoff = [
            {
                "item": f"2x4 x {board_length} ft SPF Plates",
                "unit": "EA",
                "quantity": boards
            }
        ]

        return {
            "type": "Wall Plates",
            "material": "2x4 SPF",
            "plate_type": plate_type,
            "linear_feet": total_linear_feet,
            "boards": boards,
            "material_takeoff": material_takeoff,
            "waste_percent": waste_percent
        }

    def headers(
            self,
            opening_width_feet,
            header_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        if not header_spec:
            return {
                "type": "Header",
                "opening_width": opening_width_feet,
                "header_length": "Per approved structural plan",
                "material": "Per approved structural plan",
                "header": {
                    "size": "Per approved structural plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },
                "plies": "Per approved structural plan",
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = header_spec["size"]
        length_feet = header_spec["length_feet"]
        pieces = header_spec["pieces"]

        pieces_to_order = math.ceil(
            pieces * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} Header Members",
                "unit": "EA",
                "quantity": pieces_to_order
            }
        ]

        return {
            "type": "Header",
            "opening_width": opening_width_feet,
            "header_length": length_feet,
            "material": f"{pieces} Ply {size} — approved plan",
            "header": {
                "size": size,
                "length": f"{length_feet} ft",
                "quantity": pieces_to_order
            },
            "plies": pieces,
            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def blocking(
            self,
            wall_length,
            stud_spacing_inches=None,
            rows=1,
            waste_percent=None,
            material_size="2x4",
            block_length_inches=None
    ):

        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        stud_spacing_inches = (
            self._get_lumber_stud_spacing_inches(
                stud_spacing_inches
            )
        )

        spacing_feet = stud_spacing_inches / 12
        if block_length_inches is None:
            # Nominal 1.5-in member thickness is appropriate for typical
            # dimensional-lumber blocking at the entered spacing.
            block_length_inches = stud_spacing_inches - 1.5

        # Number of spaces between studs
        spaces = math.ceil(
            wall_length / spacing_feet
        )

        block_count = spaces * rows

        blocks_to_order = math.ceil(
            block_count * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": (
                    f"{material_size} x "
                    f"{round(block_length_inches, 1)} in Blocking"
                ),
                "unit": "EA",
                "quantity": blocks_to_order
            }
        ]

        return {

            "type": "Blocking",

            "wall_length": wall_length,

            "rows": rows,

            "blocking": {
                "size": material_size,
                "length": f"{round(block_length_inches, 1)} inches",
                "quantity": blocks_to_order
            },

            "spacing": stud_spacing_inches,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def wall_sheathing(
            self,
            length_feet,
            height_feet,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        area = length_feet * height_feet

        sheet_area = Settings.SHEATHING_SHEET_COVERAGE_SQFT

        sheets_needed = math.ceil(
            area / sheet_area
        )

        sheets_to_order = math.ceil(
            area *
            (1 + waste_percent / 100) /
            sheet_area
        )

        material_takeoff = [
            {
                "item": "4x8 7/16 OSB Wall Sheathing",
                "unit": "SHEETS",
                "quantity": sheets_to_order
            }
        ]

        return {
            "type": "Wall Sheathing",

            "dimensions": {
                "length": length_feet,
                "height": height_feet
            },

            "area": area,

            "material": {
                "size": "4x8",
                "type": "7/16 OSB",
                "quantity": sheets_to_order
            },

            "material_takeoff": material_takeoff,
            "waste_percent": waste_percent
        }

    def wall_sheathing_area(self, area_sqft, waste_percent=None):
        """Estimate wall sheathing from net measured wall area."""
        waste_percent = self._get_lumber_waste_percent(waste_percent)
        sheets_to_order = math.ceil(
            area_sqft * (1 + waste_percent / 100) /
            Settings.SHEATHING_SHEET_COVERAGE_SQFT
        )

        return {
            "type": "Wall Sheathing",
            "area": round(area_sqft, 2),
            "material_takeoff": [
                {
                    "item": "4x8 7/16 OSB Wall Sheathing",
                    "unit": "SHEETS",
                    "quantity": sheets_to_order
                }
            ],
            "waste_percent": waste_percent
        }


    # =========================
    # FLOOR SYSTEMS
    # =========================

    def floor_joists(
            self,
            length_feet,
            width_feet,
            joist_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        if not joist_spec:
            return {
                "type": "Floor Joists",

                "dimensions": {
                    "length": length_feet,
                    "width": width_feet
                },

                "spacing": "Per approved framing plan",

                "joists": {
                    "size": "Per approved framing plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },

                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        spacing_inches = joist_spec["spacing_inches"]
        size = joist_spec["size"]
        member_length_feet = joist_spec["member_length_feet"]

        spacing_feet = spacing_inches / 12

        joist_count = math.ceil(
            width_feet / spacing_feet
        ) + 1

        joists_to_order = math.ceil(
            joist_count * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} x {member_length_feet} ft Floor Joists",
                "unit": "EA",
                "quantity": joists_to_order
            }
        ]

        return {
            "type": "Floor Joists",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            "spacing": spacing_inches,

            "joists": {
                "size": size,
                "length": f"{member_length_feet} ft",
                "quantity": joists_to_order
            },

            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def subfloor_sheathing(
            self,
            length_feet,
            width_feet,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        area = length_feet * width_feet

        sheet_coverage = Settings.SHEATHING_SHEET_COVERAGE_SQFT

        sheets = math.ceil(
            area *
            (1 + waste_percent / 100) /
            sheet_coverage
        )

        material_takeoff = [
            {
                "item": "4x8 3/4 in T&G OSB Subfloor",
                "unit": "SHEETS",
                "quantity": sheets
            }
        ]

        return {
            "type": "Subfloor Sheathing",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            "area": area,

            "material": {
                "size": "4x8",
                "thickness": "3/4",
                "type": "T&G OSB",
                "quantity": sheets
            },

            "material_takeoff": material_takeoff,
            "waste_percent": waste_percent
        }

    def rim_joists(
            self,
            length_feet,
            width_feet,
            rim_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        perimeter = (length_feet * 2) + (width_feet * 2)

        if not rim_spec:
            return {
                "type": "Rim Joists",
                "dimensions": {
                    "length": length_feet,
                    "width": width_feet
                },
                "perimeter": perimeter,
                "rim_joists": {
                    "size": "Per approved framing plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = rim_spec["size"]
        stock_length_feet = rim_spec["stock_length_feet"]

        perimeter_to_order = perimeter * (
            1 + waste_percent / 100
        )

        boards = math.ceil(
            perimeter_to_order / stock_length_feet
        )

        material_takeoff = [
            {
                "item": f"{size} Rim Joists",
                "unit": "EA",
                "quantity": boards
            }
        ]

        return {
            "type": "Rim Joists",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            "perimeter": perimeter,

            "rim_joists": {
                "size": size,
                "length": f"{stock_length_feet} ft",
                "quantity": boards
            },

            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def sill_plate(
            self,
            length,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        total_length = math.ceil(
            length * (1 + waste_percent / 100)
        )

        board_length = Settings.LUMBER_STOCK_LENGTH_FEET

        boards = math.ceil(
            total_length / board_length
        )

        material_takeoff = [
            {
                "item": (
                    f"2x6 x {board_length} ft "
                    "Pressure-Treated Sill Plates"
                ),
                "unit": "EA",
                "quantity": boards
            }
        ]

        return {
            "type": "Sill Plate",

            "material": "2x6 Pressure Treated Lumber",

            "length": length,
            "total_length": total_length,
            "boards": boards,

            "material_takeoff": material_takeoff,
            "waste_percent": waste_percent
        }

    def posts(
            self,
            quantity,
            height,
            post_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )
        if not post_spec:
            return {
                "type": "Wood Posts",
                "material": "Per approved structural plan",
                "quantity": quantity,
                "total_quantity": "TBD",
                "height": height,
                "post_length": "Per approved structural plan",
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = post_spec["size"]
        member_length_feet = post_spec["member_length_feet"]

        total_quantity = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} x {member_length_feet} ft Posts",
                "unit": "EA",
                "quantity": total_quantity
            }
        ]

        return {
            "type": "Wood Posts",
            "material": f"{size} Posts — approved structural plan",
            "quantity": quantity,
            "total_quantity": total_quantity,
            "height": height,
            "post_length": f"{member_length_feet} ft",
            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    # =========================
    # ROOF FRAMING
    # =========================

    def ceiling_joists(
            self,
            length_feet,
            width_feet,
            joist_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )
        if not joist_spec:
            return {
                "type": "Ceiling Joists",
                "dimensions": {
                    "length": length_feet,
                    "width": width_feet
                },
                "spacing": "Per approved framing plan",
                "joists": {
                    "size": "Per approved framing plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        spacing_inches = joist_spec["spacing_inches"]
        size = joist_spec["size"]
        member_length_feet = joist_spec["member_length_feet"]

        spacing_feet = spacing_inches / 12

        joist_count = math.ceil(
            width_feet / spacing_feet
        ) + 1

        joists_to_order = math.ceil(
            joist_count * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} x {member_length_feet} ft Ceiling Joists",
                "unit": "EA",
                "quantity": joists_to_order
            }
        ]

        return {
            "type": "Ceiling Joists",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            "spacing": spacing_inches,

            "joists": {
                "size": size,
                "length": f"{member_length_feet} ft",
                "quantity": joists_to_order
            },

            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def rafters(
            self,
            span_feet,
            roof_length_feet,
            pitch,
            rafter_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )
        rise_per_foot = pitch / 12
        run = span_feet / 2
        rise = run * rise_per_foot

        rafter_line_length = math.sqrt(
            run ** 2 + rise ** 2
        )

        if not rafter_spec:
            return {
                "type": "Roof Rafters",
                "span": span_feet,
                "roof_length": roof_length_feet,
                "pitch": f"{pitch}/12",
                "rafter_length": round(rafter_line_length, 2),
                "rafters": {
                    "size": "Per approved framing plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },
                "spacing": "Per approved framing plan",
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = rafter_spec["size"]
        member_length_feet = rafter_spec["member_length_feet"]
        quantity = rafter_spec["quantity"]
        spacing_inches = rafter_spec["spacing_inches"]

        rafters_to_order = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} x {member_length_feet} ft Rafters",
                "unit": "EA",
                "quantity": rafters_to_order
            }
        ]

        return {
            "type": "Roof Rafters",
            "span": span_feet,
            "roof_length": roof_length_feet,
            "pitch": f"{pitch}/12",
            "rafter_length": round(rafter_line_length, 2),
            "rafters": {
                "size": size,
                "length": f"{member_length_feet} ft",
                "quantity": rafters_to_order
            },
            "spacing": spacing_inches,
            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def ridge_board(
            self,
            length_feet,
            ridge_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )
        if not ridge_spec:
            return {
                "type": "Ridge Board",
                "length": length_feet,
                "ridge_board": {
                    "size": "Per approved framing plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = ridge_spec["size"]
        stock_length_feet = ridge_spec["stock_length_feet"]

        boards_needed = math.ceil(
            length_feet / stock_length_feet
        )

        boards_to_order = math.ceil(
            boards_needed * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} Ridge Board",
                "unit": "EA",
                "quantity": boards_to_order
            }
        ]

        return {
            "type": "Ridge Board",
            "length": length_feet,
            "ridge_board": {
                "size": size,
                "length": f"{stock_length_feet} ft",
                "quantity": boards_to_order
            },
            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def collar_ties(
            self,
            roof_length,
            tie_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )
        if not tie_spec:
            return {
                "type": "Collar Ties",
                "roof_length": roof_length,
                "collar_ties": {
                    "size": "Per approved framing plan",
                    "length": "TBD",
                    "quantity": "TBD"
                },
                "spacing": "Per approved framing plan",
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = tie_spec["size"]
        member_length_feet = tie_spec["member_length_feet"]
        spacing_inches = tie_spec["spacing_inches"]

        spacing_feet = spacing_inches / 12

        tie_count = math.ceil(
            roof_length / spacing_feet
        ) + 1

        ties_to_order = math.ceil(
            tie_count * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} x {member_length_feet} ft Collar Ties",
                "unit": "EA",
                "quantity": ties_to_order
            }
        ]

        return {
            "type": "Collar Ties",
            "roof_length": roof_length,
            "collar_ties": {
                "size": size,
                "length": f"{member_length_feet} ft",
                "quantity": ties_to_order
            },
            "spacing": spacing_inches,
            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }

    def roof_sheathing(
            self,
            length_feet,
            width_feet,
            roof_type="gable",
            pitch_rise=6.0,
            overhang_inches=12.0,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        roof_type = str(roof_type).strip().lower()

        if roof_type not in ["gable", "shed"]:
            raise ValueError("Roof type must be gable or shed.")

        if pitch_rise <= 0:
            raise ValueError("Roof pitch must be greater than zero.")

        if overhang_inches < 0:
            raise ValueError("Overhang cannot be negative.")

        overhang_feet = overhang_inches / 12
        slope_factor = math.sqrt(1 + (pitch_rise / 12) ** 2)

        # Include eave and rake overhangs in the roof coverage calculation.
        roof_length = length_feet + (2 * overhang_feet)

        if roof_type == "gable":
            roof_plane_count = 2
            horizontal_run = (width_feet / 2) + overhang_feet
        else:
            roof_plane_count = 1
            horizontal_run = width_feet + (2 * overhang_feet)

        rafter_length = horizontal_run * slope_factor
        roof_plane_area = roof_length * rafter_length
        area = roof_plane_area * roof_plane_count

        sheet_area = Settings.SHEATHING_SHEET_COVERAGE_SQFT

        sheets_to_order = math.ceil(
            area *
            (1 + waste_percent / 100) /
            sheet_area
        )

        material_takeoff = [
            {
                "item": "4x8 7/16 OSB Roof Sheathing",
                "unit": "SHEETS",
                "quantity": sheets_to_order
            }
        ]

        return {
            "type": "Roof Sheathing",

            "dimensions": {
                "length": length_feet,
                "width": width_feet
            },

            "roof_type": roof_type,
            "pitch_rise": pitch_rise,
            "overhang_inches": overhang_inches,
            "roof_plane_count": roof_plane_count,
            "roof_length": round(roof_length, 2),
            "rafter_length": round(rafter_length, 2),
            "roof_plane_area": round(roof_plane_area, 2),
            "area": round(area, 2),

            "material": {
                "size": "4x8",
                "type": "7/16 OSB",
                "quantity": sheets_to_order
            },

            "material_takeoff": material_takeoff,
            "waste_percent": waste_percent
        }

    def studs(
            self,
            wall_length,
            wall_height,
            stud_spacing_inches=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        stud_spacing_inches = (
            self._get_lumber_stud_spacing_inches(
                stud_spacing_inches
            )
        )

        spacing_feet = stud_spacing_inches / 12

        # One stud at each end + studs between
        stud_count = math.ceil(
            wall_length / spacing_feet
        ) + 1

        # Determine stud length
        if wall_height <= 8:
            stud_length = "8 ft"
        elif wall_height <= 10:
            stud_length = "10 ft"
        else:
            stud_length = "12 ft"

        total_studs = math.ceil(
            stud_count * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"2x4 x {stud_length} SPF Studs",
                "unit": "EA",
                "quantity": total_studs
            }
        ]

        return {

            "type": "Wall Studs",

            "material": "2x4 SPF Studs",

            "wall_length": wall_length,

            "wall_height": wall_height,

            "spacing": f"{stud_spacing_inches} OC",

            "stud_length": stud_length,

            "quantity": stud_count,

            "total_quantity": total_studs,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def beams(
            self,
            length,
            beam_spec=None,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )
        if not beam_spec:
            return {
                "type": "Beam",
                "material": "Per approved structural plan",
                "length": length,
                "plies": "Per approved structural plan",
                "linear_feet": "TBD",
                "boards": "TBD",
                "status": "plan_required",
                "waste_percent": waste_percent,
                "material_takeoff": []
            }

        size = beam_spec["size"]
        member_length_feet = beam_spec["member_length_feet"]
        members = beam_spec["members"]

        boards_to_order = math.ceil(
            members * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": f"{size} x {member_length_feet} ft Beam Members",
                "unit": "EA",
                "quantity": boards_to_order
            }
        ]

        return {
            "type": "Beam",
            "material": f"{size} — approved structural plan",
            "length": length,
            "plies": members,
            "linear_feet": member_length_feet * members,
            "boards": boards_to_order,
            "status": "specified",
            "waste_percent": waste_percent,
            "material_takeoff": material_takeoff
        }


    # =========================
    # OPENINGS
    # =========================

    def king_studs(
            self,
            openings,
            wall_height,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        quantity = openings * 2

        total_quantity = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        if wall_height <= 8:
            stud_length = "8 ft"
        elif wall_height <= 10:
            stud_length = "10 ft"
        else:
            stud_length = "12 ft"

        material_takeoff = [
                {
                    "item": f"2x4 x {stud_length} SPF King Studs",
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

        return {

            "type": "King Studs",

            "material": "2x4 SPF Studs",

            "openings": openings,

            "wall_height": wall_height,

            "stud_length": stud_length,

            "quantity": quantity,

            "total_quantity": total_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def jack_studs(
            self,
            openings,
            opening_height,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        quantity = openings * 2

        total_quantity = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        if opening_height <= 6:
            stud_length = "6 ft"
        elif opening_height <= 8:
            stud_length = "8 ft"
        elif opening_height <= 10:
            stud_length = "10 ft"
        else:
            stud_length = "12 ft"

        material_takeoff = [
                {
                    "item": f"2x4 x {stud_length} SPF Jack Studs",
                    "unit": "EA",
                    "quantity": total_quantity
                }
            ]

        return {

            "type": "Jack Studs",

            "material": "2x4 SPF Studs",

            "openings": openings,

            "opening_height": opening_height,

            "stud_length": stud_length,

            "quantity": quantity,

            "total_quantity": total_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def cripple_studs(
            self,
            openings,
            opening_width,
            stud_spacing_inches=Settings.LUMBER_STUD_SPACING_INCHES,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        spacing_feet = stud_spacing_inches / 12

        cripples_per_opening = math.ceil(
            opening_width / spacing_feet
        ) + 1

        quantity = (
                openings * cripples_per_opening
        )

        total_quantity = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        material_takeoff = [
            {
                "item": "2x4 Cripple Studs (cut length per framing plan)",
                "unit": "EA",
                "quantity": total_quantity
            }
        ]

        return {

            "type": "Cripple Studs",

            "material": "2x4 SPF Studs",

            "openings": openings,

            "opening_width": opening_width,

            "spacing": f"{stud_spacing_inches} OC",

            "quantity": quantity,

            "total_quantity": total_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    def corner_posts(
            self,
            corners,
            wall_height,
            waste_percent=None
    ):
        waste_percent = self._get_lumber_waste_percent(
            waste_percent
        )

        studs_per_corner = 3

        quantity = (
                corners * studs_per_corner
        )

        total_quantity = math.ceil(
            quantity * (1 + waste_percent / 100)
        )

        if wall_height <= 8:
            stud_length = "8 ft"
        elif wall_height <= 10:
            stud_length = "10 ft"
        else:
            stud_length = "12 ft"

        material_takeoff = [
            {
                "item": f"2x4 x {stud_length} SPF Corner Studs",
                "unit": "EA",
                "quantity": total_quantity
            }
        ]

        return {

            "type": "Corner Posts",

            "material": "2x4 SPF Studs",

            "corners": corners,

            "wall_height": wall_height,

            "stud_length": stud_length,

            "quantity": quantity,

            "total_quantity": total_quantity,

            "material_takeoff": material_takeoff,

            "waste_percent": waste_percent
        }

    # =========================
    # WALL SYSTEM
    # =========================

    def framing_hardware(self, hardware_items):
        """Take off exact hardware quantities from an approved plan."""
        material_takeoff = []

        for item in hardware_items:
            name = str(item.get("item", "")).strip()
            quantity = int(item.get("quantity", 0) or 0)

            if name and quantity > 0:
                material_takeoff.append(
                    {
                        "item": name,
                        "unit": "EA",
                        "quantity": quantity
                    }
                )

        return {
            "type": "Framing Hardware Package",
            "material": "Plan-Specified Framing Hardware",
            "details": {
                "Hardware line items": len(material_takeoff)
            },
            "waste_percent": 0,
            "material_takeoff": material_takeoff,
            "note": (
                "Connection type, fastener count, and manufacturer "
                "requirements must follow the approved plans."
            )
        }

    def roof_trusses(
            self,
            building_length_feet,
            truss_spacing_inches=24,
            truss_spec="Roof Truss",
            connection_quantity=0
    ):
        spacing_feet = float(truss_spacing_inches) / 12
        truss_count = math.ceil(building_length_feet / spacing_feet) + 1
        material_takeoff = [
            {
                "item": truss_spec,
                "unit": "EA",
                "quantity": truss_count
            }
        ]

        if connection_quantity > 0:
            material_takeoff.append(
                {
                    "item": "Plan-Specified Truss Connections",
                    "unit": "EA",
                    "quantity": int(connection_quantity)
                }
            )

        return {
            "type": "Roof Truss Package",
            "material": truss_spec,
            "details": {
                "Building length": f"{building_length_feet} ft",
                "Truss spacing": f"{truss_spacing_inches} in OC",
                "Truss count": truss_count
            },
            "waste_percent": 0,
            "material_takeoff": material_takeoff,
            "note": (
                "Truss profile, span, bearing locations, bracing, and "
                "connections must match the sealed truss package."
            )
        }

    def wall_framing_package(
            self,
            length_feet,
            height_feet,
            quantity=1,
            stud_spacing_inches=None,
            include_sheathing=True,
            waste_percent=None
    ):
        wall = self.frame_wall(
            length_feet=length_feet,
            height_feet=height_feet,
            quantity=quantity,
            stud_spacing_inches=stud_spacing_inches,
            waste_percent=waste_percent
        )
        material_takeoff = list(wall["material_takeoff"])

        if include_sheathing:
            sheathing = self.wall_sheathing(
                length_feet,
                height_feet,
                waste_percent=wall["waste_percent"]
            )
            sheets = sheathing["material"]["quantity"] * quantity
            material_takeoff.append(
                {
                    "item": "4x8 7/16 OSB Wall Sheathing",
                    "unit": "SHEETS",
                    "quantity": sheets
                }
            )

        return {
            "type": "Wall Framing Package",
            "material": "2x4 SPF Wall Framing",
            "details": {
                "Wall size": f"{length_feet} ft x {height_feet} ft",
                "Identical walls": quantity,
                "Stud spacing": f"{wall['stud_spacing_inches']} in OC",
                "Wall sheathing": "Included" if include_sheathing else "Not included"
            },
            "waste_percent": wall["waste_percent"],
            "material_takeoff": material_takeoff,
            "note": (
                "This package covers field framing and optional wall "
                "sheathing. Add openings, headers, hold-downs, and hardware "
                "from approved plans as needed."
            )
        }

    def stair_framing(
            self,
            stair_width_feet,
            tread_count,
            stringer_count,
            stringer_spec="2x12 Stair Stringer",
            tread_spec="Stair Tread",
            riser_spec="Stair Riser"
    ):
        return {
            "type": "Stair Framing",
            "material": stringer_spec,
            "details": {
                "Stair width": f"{stair_width_feet} ft",
                "Treads": tread_count,
                "Stringers": stringer_count
            },
            "waste_percent": 0,
            "material_takeoff": [
                {
                    "item": stringer_spec,
                    "unit": "EA",
                    "quantity": int(stringer_count)
                },
                {
                    "item": tread_spec,
                    "unit": "EA",
                    "quantity": int(tread_count)
                },
                {
                    "item": riser_spec,
                    "unit": "EA",
                    "quantity": int(tread_count)
                }
            ],
            "note": (
                "Stringer layout, rise/run, landing framing, guard, and "
                "handrail requirements must follow approved plans and code."
            )
        }

    def deck_framing(
            self,
            length_feet,
            projection_feet,
            joist_spacing_inches=16,
            post_count=0,
            joist_spec="2x8 Deck Joists",
            beam_spec="Plan-Specified Deck Beam"
    ):
        joist_count = math.ceil(
            length_feet / (float(joist_spacing_inches) / 12)
        ) + 1
        stock_length = self._get_lumber_stock_length_feet(None)
        ledger_boards = math.ceil(length_feet / stock_length)

        material_takeoff = [
            {
                "item": f"{joist_spec} x {projection_feet} ft",
                "unit": "EA",
                "quantity": joist_count
            },
            {
                "item": f"2x Ledger Board ({stock_length} ft)",
                "unit": "EA",
                "quantity": ledger_boards
            },
            {
                "item": beam_spec,
                "unit": "LF",
                "quantity": round(float(length_feet), 2)
            }
        ]

        if post_count > 0:
            material_takeoff.extend([
                {
                    "item": "Plan-Specified Deck Posts",
                    "unit": "EA",
                    "quantity": int(post_count)
                },
                {
                    "item": "Plan-Specified Post Bases",
                    "unit": "EA",
                    "quantity": int(post_count)
                }
            ])

        return {
            "type": "Deck Framing",
            "material": joist_spec,
            "details": {
                "Deck size": f"{length_feet} ft x {projection_feet} ft",
                "Joist spacing": f"{joist_spacing_inches} in OC",
                "Joists": joist_count,
                "Posts": int(post_count)
            },
            "waste_percent": 0,
            "material_takeoff": material_takeoff,
            "note": (
                "Deck board coverage is estimated separately. Beam size, post "
                "locations, footings, ledger fastening, and hardware must "
                "follow approved plans and local requirements."
            )
        }

    def garage_door_framing(
            self,
            opening_width_feet,
            wall_height_feet,
            quantity=1,
            header_spec=None,
            header_plies=None
    ):
        stud_length = 8 if wall_height_feet <= 8 else 10
        stud_quantity = int(quantity) * 4
        material_takeoff = [
            {
                "item": f"2x4 x {stud_length} ft Garage Opening Studs",
                "unit": "EA",
                "quantity": stud_quantity
            }
        ]

        if header_spec and header_plies:
            material_takeoff.append(
                {
                    "item": (
                        f"Header Material ({header_plies} ply {header_spec})"
                    ),
                    "unit": "LF",
                    "quantity": round(
                        float(opening_width_feet) * int(header_plies) * quantity,
                        2
                    )
                }
            )

        return {
            "type": "Garage Door Framing",
            "material": "Garage Door Opening Framing",
            "details": {
                "Opening width": f"{opening_width_feet} ft",
                "Wall height": f"{wall_height_feet} ft",
                "Openings": quantity,
                "Header": header_spec or "Plan required"
            },
            "waste_percent": 0,
            "material_takeoff": material_takeoff,
            "note": (
                "Header size, plies, bearing, cripple framing, and connection "
                "details must follow approved structural plans."
            )
        }




