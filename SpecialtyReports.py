def create_specialty_report(estimate):
    details = "\n".join(
        f"    {label}: {value}"
        for label, value in estimate.get("details", {}).items()
    )

    takeoff = "\n".join(
        f"    {item['item']}: {item['quantity']} {item['unit']}"
        for item in estimate.get("material_takeoff", [])
    )

    return f"""

                {estimate['type'].upper()} ESTIMATE

        Material:
        {estimate['material']}

        DETAILS:

{details}

        Waste:
        {estimate.get('waste_percent', 0)}%

        MATERIAL TAKEOFF:

{takeoff}

        Note:
        {estimate['note']}
        """
