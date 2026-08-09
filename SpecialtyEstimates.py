import math

from EstimatingPreferences import EstimatingPreferences


class SpecialtyEstimator:
    """Measured takeoffs for common exterior and finish materials.

    These calculations create buying quantities. Product selections, local
    code, fastening schedules, and installation details remain the
    contractor's responsibility.
    """

    def _lumber_waste_percent(self, waste_percent):
        if waste_percent is not None:
            return waste_percent

        return EstimatingPreferences().get("lumber_waste_percent")

    def siding(self, wall_area_sqft, siding_type="Siding", waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        squares = math.ceil(
            wall_area_sqft * (1 + waste_percent / 100) / 100
        )

        return {
            "type": "Exterior Siding",
            "material": siding_type,
            "details": {"Wall area": f"{wall_area_sqft} sq ft", "Coverage": "100 sq ft per square"},
            "waste_percent": waste_percent,
            "material_takeoff": [{"item": siding_type, "unit": "SQUARES", "quantity": squares}],
            "note": "Verify siding profile, accessory pieces, and manufacturer coverage before ordering."
        }

    def housewrap(self, wall_area_sqft, roll_coverage_sqft=900, waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        rolls = math.ceil(
            wall_area_sqft * (1 + waste_percent / 100) / roll_coverage_sqft
        )

        return {
            "type": "Housewrap",
            "material": "Weather-Resistive Barrier",
            "details": {"Wall area": f"{wall_area_sqft} sq ft", "Roll coverage": f"{roll_coverage_sqft} sq ft"},
            "waste_percent": waste_percent,
            "material_takeoff": [{"item": "Housewrap / Weather-Resistive Barrier", "unit": "ROLLS", "quantity": rolls}],
            "note": "Flashing tape, cap fasteners, and installation details must follow the selected manufacturer's instructions."
        }

    def exterior_trim(self, linear_feet, trim_spec="1x4 Exterior Trim", board_length_feet=16, waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        boards = math.ceil(
            linear_feet * (1 + waste_percent / 100) / board_length_feet
        )

        return {
            "type": "Exterior Trim",
            "material": trim_spec,
            "details": {"Trim length": f"{linear_feet} LF", "Stock length": f"{board_length_feet} ft"},
            "waste_percent": waste_percent,
            "material_takeoff": [{"item": f"{trim_spec} ({board_length_feet} ft)", "unit": "EA", "quantity": boards}],
            "note": "Measure all corners, returns, and openings. Verify trim dimensions and finish before ordering."
        }

    def windows(self, quantity, window_spec="Window Unit"):
        return {
            "type": "Windows",
            "material": window_spec,
            "details": {"Quantity": quantity, "Specification": window_spec},
            "waste_percent": 0,
            "material_takeoff": [{"item": window_spec, "unit": "EA", "quantity": quantity}],
            "note": "Verify rough-opening dimensions, glazing, egress, flashing, and energy requirements from approved plans."
        }

    def exterior_doors(self, quantity, door_spec="Exterior Door Unit"):
        return {
            "type": "Exterior Doors",
            "material": door_spec,
            "details": {"Quantity": quantity, "Specification": door_spec},
            "waste_percent": 0,
            "material_takeoff": [{"item": door_spec, "unit": "EA", "quantity": quantity}],
            "note": "Verify handing, swing, rough opening, hardware, threshold, and weatherproofing from the door schedule."
        }

    def decking(self, length, width, board_width_inches=5.5, board_length_feet=12, gap_inches=0.125, waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        area = length * width
        coverage_per_board = board_length_feet * ((board_width_inches + gap_inches) / 12)
        boards = math.ceil(
            area * (1 + waste_percent / 100) / coverage_per_board
        )

        return {
            "type": "Decking",
            "material": "Deck Boards",
            "details": {"Deck area": f"{area} sq ft", "Board size": f"{board_width_inches} in x {board_length_feet} ft", "Board gap": f"{gap_inches} in"},
            "waste_percent": waste_percent,
            "material_takeoff": [{"item": f"Deck Boards ({board_width_inches} in x {board_length_feet} ft)", "unit": "EA", "quantity": boards}],
            "note": "This is deck-board coverage only. Estimate framing, posts, footings, railings, and fasteners separately."
        }

    def fence(self, length, height, panel_width_feet=8, post_spacing_feet=8, waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        panels = math.ceil(
            length * (1 + waste_percent / 100) / panel_width_feet
        )
        posts = math.ceil(length / post_spacing_feet) + 1

        return {
            "type": "Fence",
            "material": "Fence Panels and Posts",
            "details": {"Fence length": f"{length} LF", "Fence height": f"{height} ft", "Panel width": f"{panel_width_feet} ft", "Post spacing": f"{post_spacing_feet} ft"},
            "waste_percent": waste_percent,
            "material_takeoff": [
                {"item": f"{panel_width_feet} ft Fence Panels", "unit": "EA", "quantity": panels},
                {"item": "Fence Posts", "unit": "EA", "quantity": posts}
            ],
            "note": "Post type, length, embedment, concrete, gates, hardware, and local fence requirements must be verified for the site."
        }

    def flooring(self, area_sqft, flooring_type="Flooring", carton_coverage_sqft=20, waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        cartons = math.ceil(
            area_sqft * (1 + waste_percent / 100) / carton_coverage_sqft
        )

        return {
            "type": "Flooring",
            "material": flooring_type,
            "details": {"Floor area": f"{area_sqft} sq ft", "Carton coverage": f"{carton_coverage_sqft} sq ft"},
            "waste_percent": waste_percent,
            "material_takeoff": [{"item": flooring_type, "unit": "CARTONS", "quantity": cartons}],
            "note": "Verify carton coverage, underlayment, transitions, moisture requirements, and manufacturer installation instructions."
        }

    def baseboard(self, linear_feet, board_length_feet=16, baseboard_spec="Baseboard Trim", waste_percent=None):
        waste_percent = self._lumber_waste_percent(waste_percent)
        boards = math.ceil(
            linear_feet * (1 + waste_percent / 100) / board_length_feet
        )

        return {
            "type": "Baseboard Trim",
            "material": baseboard_spec,
            "details": {"Baseboard length": f"{linear_feet} LF", "Stock length": f"{board_length_feet} ft"},
            "waste_percent": waste_percent,
            "material_takeoff": [{"item": f"{baseboard_spec} ({board_length_feet} ft)", "unit": "EA", "quantity": boards}],
            "note": "Measure returns, closets, and transitions. Nails, caulk, and paint are not included."
        }

    def interior_doors(self, quantity, door_spec="Interior Door Unit"):
        return {
            "type": "Interior Doors",
            "material": door_spec,
            "details": {"Quantity": quantity, "Specification": door_spec},
            "waste_percent": 0,
            "material_takeoff": [{"item": door_spec, "unit": "EA", "quantity": quantity}],
            "note": "Verify handing, swing, size, jamb depth, hardware, and finish from the door schedule."
        }
