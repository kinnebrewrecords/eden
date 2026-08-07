import math
from Settings import Settings


class LumberEstimator:

    # =========================
    # WALL FRAMING
    # =========================

    def frame_wall(
            self,
            length_feet,
            height_feet,
            stud_spacing_inches=Settings.LUMBER_STUD_SPACING_INCHES,
            quantity=1,
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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

        plate_board_length = Settings.LUMBER_STOCK_LENGTH_FEET

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

    def plates(
            self,
            length,
            plate_type="double top",
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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

        board_length = Settings.LUMBER_STOCK_LENGTH_FEET

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            stud_spacing_inches=Settings.LUMBER_BLOCKING_SPACING_INCHES,
            rows=1,
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

        spacing_feet = stud_spacing_inches / 12

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
                "item": "2x4 x 14.5 in Blocking",
                "unit": "EA",
                "quantity": blocks_to_order
            }
        ]

        return {

            "type": "Blocking",

            "wall_length": wall_length,

            "rows": rows,

            "blocking": {
                "size": "2x4",
                "length": "14.5 inches",
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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


    # =========================
    # FLOOR SYSTEMS
    # =========================

    def floor_joists(
            self,
            length_feet,
            width_feet,
            joist_spec=None,
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

        area = length_feet * width_feet

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

            "area": area,

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
            stud_spacing_inches=Settings.LUMBER_STUD_SPACING_INCHES,
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):
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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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
            waste_percent=Settings.LUMBER_WASTE_PERCENT
    ):

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




