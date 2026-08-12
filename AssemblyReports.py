def create_backyard_studio_shell_report(estimate):
    """Return the plain-text report used by the terminal and browser chat."""
    dimensions = estimate["dimensions"]

    takeoff_lines = "\n".join(
        (
            f"    {item['item']}: "
            f"{item['quantity']} {item['unit']}"
        )
        for item in estimate["material_takeoff"]
    )

    exclusions = "\n".join(
        f"    - {item}"
        for item in estimate["exclusions"]
    )

    interior_finish = (
        f"Included ({estimate['insulation_r_value']} wall insulation)"
        if estimate["include_interior_finish"]
        else "Not included"
    )

    return f"""

                BACKYARD STUDIO SHELL ESTIMATE

        Type:
        {estimate['type']}

        DIMENSIONS:

        Length:
        {dimensions['length']} ft

        Width:
        {dimensions['width']} ft

        Wall Height:
        {dimensions['wall_height']} ft

        Slab Thickness:
        {estimate['slab_thickness_inches']} inches

        ASSEMBLY INCLUDES:

        - Standard concrete slab package
        - Exterior wall framing and wall sheathing
        - Roof sheathing and asphalt shingles
        - Interior finish: {interior_finish}

        MATERIAL TAKEOFF:

{takeoff_lines}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """


def create_exterior_wall_assembly_report(estimate):
    """Return a contractor-reviewable report for an exterior wall assembly."""
    dimensions = estimate["dimensions"]
    takeoff_lines = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate["material_takeoff"]
    )
    assumptions = "\n".join(
        f"    - {item}"
        for item in estimate["assumptions"]
    )
    exclusions = "\n".join(
        f"    - {item}"
        for item in estimate["exclusions"]
    )
    openings = estimate.get("openings", [])
    opening_lines = (
        "\n".join(
            (
                f"    - {opening['type'].title()}: "
                f"{opening['width_feet']} ft x "
                f"{opening['height_feet']} ft"
            )
            for opening in openings
        )
        if openings else
        "    - No openings entered"
    )
    header_detail = (
        f"{estimate['header_plies']} ply {estimate['header_spec']}"
        if estimate.get("header_plies") else
        (estimate.get("header_spec") or "Not applicable")
    )

    return f"""

                EXTERIOR WALL ASSEMBLY ESTIMATE

        Wall Size:
        {dimensions['length']} ft x {dimensions['height']} ft

        Identical Wall Segments:
        {estimate['quantity']}

        Gross Wall Area:
        {estimate['gross_wall_area_sqft']} sq ft

        Net Wall Area:
        {estimate['net_wall_area_sqft']} sq ft

        Stud Spacing:
        {estimate['stud_spacing_inches']}

        OPENINGS IN EACH IDENTICAL WALL:

{opening_lines}

        Header Specification:
        {header_detail}

        ASSEMBLY INCLUDES:

        - Wall framing and sheathing
        - Housewrap: {'Included' if estimate['include_housewrap'] else 'Not included'}
        - Insulation: {'Included (' + estimate['insulation_r_value'] + ')' if estimate['include_insulation'] else 'Not included'}
        - Interior drywall: {'Included' if estimate['include_drywall'] else 'Not included'}
        - Waste: {estimate['waste_percent']}%

        MATERIAL TAKEOFF:

{takeoff_lines}

        ASSUMPTIONS:

{assumptions}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """


def create_foundation_system_assembly_report(estimate):
    """Return a contractor-reviewable foundation system report."""
    run_lines = "\n".join(
        (
            f"    - {run['quantity']} run(s): {run['length']} ft x "
            f"{run['width_inches']} in wide x {run['depth_inches']} in deep"
        )
        for run in estimate["footing_runs"]
    )
    takeoff_lines = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate["material_takeoff"]
    )
    assumptions = "\n".join(
        f"    - {item}"
        for item in estimate["assumptions"]
    )
    exclusions = "\n".join(
        f"    - {item}"
        for item in estimate["exclusions"]
    )
    wall = estimate.get("foundation_wall")
    wall_detail = (
        f"    Included: {wall['length']} ft x {wall['height']} ft x "
        f"{wall['thickness_inches']} in\n"
        f"    Waterproofing: {'Included' if wall['waterproofing'] else 'Not included'}\n"
        f"    Concrete volume: {estimate['foundation_wall_cubic_yards']} CY\n"
        f"    Separate wall-pour order: {estimate['foundation_wall_order_quantity']} CY"
        if wall else
        "    Not included"
    )

    return f"""

                RESIDENTIAL FOUNDATION SYSTEM ASSEMBLY

        FOOTING RUNS:

{run_lines}

        Footing Runs Total:
        {estimate['footing_run_count']}

        Footing Concrete Volume:
        {estimate['footing_cubic_yards']} CY

        Footing Order Quantity:
        {estimate['footing_order_quantity']} CY

        FOUNDATION WALL:

{wall_detail}

        ASSEMBLY INCLUDES:

        - Reinforced: {'Yes - rebar remains plan-required' if estimate['reinforced'] else 'No'}
        - Footing forms: {'Included' if estimate['forms'] else 'Not included'}
        - Gravel base: {'Included' if estimate['gravel_base'] else 'Not included'}
        - Waste: {estimate['waste_percent']}%

        MATERIAL TAKEOFF:

{takeoff_lines}

        Concrete-pour reminder:
        Footing and foundation-wall concrete are separate pours. The Ready
        Mix Concrete total above combines both pours for project pricing;
        order each component using the separate quantities shown above.

        ASSUMPTIONS:

{assumptions}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """


def create_roof_covering_assembly_report(estimate):
    """Return a contractor-reviewable roof-covering assembly report."""
    dimensions = estimate["dimensions"]
    takeoff_lines = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate["material_takeoff"]
    )
    assumptions = "\n".join(
        f"    - {item}"
        for item in estimate["assumptions"]
    )
    exclusions = "\n".join(
        f"    - {item}"
        for item in estimate["exclusions"]
    )

    return f"""

                RESIDENTIAL ROOF COVERING ASSEMBLY

        Building Footprint:
        {dimensions['length']} ft x {dimensions['width']} ft

        Roof Type / Pitch:
        {estimate['roof_type'].title()} / {estimate['pitch_rise']}-in-12

        Overhang:
        {estimate['overhang_inches']} inches

        Sloped Roof Coverage:
        {estimate['roof_area_sqft']} sq ft

        Roof Length / Rafter Length:
        {estimate['roof_length_feet']} ft / {estimate['rafter_length_feet']} ft

        ASSEMBLY INCLUDES:

        - Roof sheathing, synthetic underlayment, and asphalt shingles
        - Drip edge: {'Included' if estimate['include_drip_edge'] else 'Not included'}
        - Ridge vent: {'Included' if estimate['include_ridge_vent'] else 'Not included'}
        - Ice and water shield: {estimate['ice_water_coverage_sqft']} sq ft entered
        - Flashing locations entered: {estimate['flashing_quantity']}
        - Waste: {estimate['waste_percent']}%

        MATERIAL TAKEOFF:

{takeoff_lines}

        ASSUMPTIONS:

{assumptions}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """


def create_floor_system_assembly_report(estimate):
    """Return a contractor-reviewable floor system assembly report."""
    dimensions = estimate["dimensions"]
    joist_spec = estimate["joist_spec"]
    rim_spec = estimate["rim_spec"]
    takeoff_lines = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate["material_takeoff"]
    )
    assumptions = "\n".join(
        f"    - {item}"
        for item in estimate["assumptions"]
    )
    exclusions = "\n".join(
        f"    - {item}"
        for item in estimate["exclusions"]
    )

    return f"""

                RESIDENTIAL FLOOR SYSTEM ASSEMBLY

        Floor Size:
        {dimensions['length']} ft x {dimensions['width']} ft

        Floor Area:
        {estimate['floor_area_sqft']} sq ft

        PLAN-CONFIRMED MEMBERS:

        Joists: {joist_spec['size']} x {joist_spec['member_length_feet']} ft
        Joists span the floor {estimate['joist_span_direction']}
        Joist spacing: {joist_spec['spacing_inches']} in OC
        Rim: {rim_spec['size']} x {rim_spec['stock_length_feet']} ft stock
        Blocking: {'Included (' + str(estimate['blocking_rows']) + ' row(s))' if estimate['include_blocking'] else 'Not included'}
        Waste: {estimate['waste_percent']}%

        MATERIAL TAKEOFF:

{takeoff_lines}

        ASSUMPTIONS:

{assumptions}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """


def create_interior_finish_assembly_report(estimate):
    """Return a contractor-reviewable interior finish assembly report."""
    takeoff_lines = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate["material_takeoff"]
    )
    assumptions = "\n".join(
        f"    - {item}"
        for item in estimate["assumptions"]
    )
    exclusions = "\n".join(
        f"    - {item}"
        for item in estimate["exclusions"]
    )

    return f"""

                INTERIOR FINISH ASSEMBLY

        MEASURED COVERAGE:

        Net Wall Area: {estimate['net_wall_area_sqft']} sq ft
        Ceiling Area: {estimate['ceiling_area_sqft']} sq ft
        Drywall Finish Area: {estimate['drywall_finish_area_sqft']} sq ft
        Flooring Area: {estimate['flooring_area_sqft']} sq ft
        Baseboard: {estimate['baseboard_linear_feet']} LF
        Interior Doors: {estimate['interior_door_quantity']}

        ASSEMBLY INCLUDES:

        - Wall insulation: {'Included (' + estimate['insulation_r_value'] + ')' if estimate['include_insulation'] else 'Not included'}
        - Drywall and finish materials: {'Included' if estimate['include_drywall'] else 'Not included'}
        - Primer and interior paint: {'Included' if estimate['include_primer_and_paint'] else 'Not included'}
        - Flooring: {estimate['flooring_type'] or 'Not included'}

        MATERIAL TAKEOFF:

{takeoff_lines}

        ASSUMPTIONS:

{assumptions}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """


def create_residential_house_takeoff_report(estimate):
    """Return the final, traceable summary for a whole-house takeoff."""
    component_lines = "\n".join(
        f"    - {name}: {component.get('type', 'Assembly')}"
        for name, component in estimate["component_estimates"].items()
    )
    takeoff_lines = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate["material_takeoff"]
    )
    assumptions = "\n".join(
        f"    - {item}" for item in estimate["assumptions"]
    )
    exclusions = "\n".join(
        f"    - {item}" for item in estimate["exclusions"]
    )

    return f"""

                RESIDENTIAL WHOLE-HOUSE TAKEOFF

        Project / Plan Name:
        {estimate['house_name']}

        Stories Entered:
        {estimate['story_count']}

        Components Included ({estimate['component_count']}):

{component_lines}

        COMBINED MATERIAL TAKEOFF:

{takeoff_lines}

        REVIEW ASSUMPTIONS:

{assumptions}

        EXCLUSIONS / PLAN-REQUIRED ITEMS:

{exclusions}

        Note:
        {estimate['scope_note']}
        """
