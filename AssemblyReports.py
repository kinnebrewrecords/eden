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
