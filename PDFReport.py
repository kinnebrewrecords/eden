from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
    Table,
    TableStyle
)


def create_project_pdf(
        project,
        profile,
        material_takeoff,
        priced_takeoff=None,
        bid_summary=None
):
    export_folder = Path(__file__).with_name("exports")
    export_folder.mkdir(exist_ok=True)

    safe_project_name = project["name"].replace(" ", "_").lower()
    pdf_path = export_folder / f"{safe_project_name}_internal_cost_sheet.pdf"

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch
    )

    styles = getSampleStyleSheet()
    story = []

    details = project.get("details", {})

    company = profile.get("company", "Your Company")
    name = profile.get("name", "")
    phone = profile.get("phone", "")
    email = profile.get("email", "")
    address = profile.get("address", "")

    proposal_title = details.get(
        "proposal_title",
        ""
    ) or "Construction Material Estimate"

    story.append(Paragraph("Internal Cost Sheet", styles["Title"]))
    story.append(
        Paragraph(escape(proposal_title), styles["Heading2"])
    )
    story.append(Spacer(1, 0.15 * inch))

    story.append(
        Paragraph(f"<b>{company}</b>", styles["Heading2"])
    )

    company_lines = [
        line for line in [name, phone, email, address] if line
    ]

    for line in company_lines:
        story.append(Paragraph(line, styles["Normal"]))

    story.append(Spacer(1, 0.2 * inch))

    customer_name = details.get("customer_name", "")
    customer_email = details.get("customer_email", "")
    project_address = details.get("project_address", "")

    project_info = [
        ["Project", project["name"]],
        ["Customer", customer_name or "Not specified"],
        ["Customer Email", customer_email or "Not specified"],
        ["Project Address", project_address or "Not specified"]
    ]

    project_table = Table(
        project_info,
        colWidths=[1.6 * inch, 6.5 * inch]
    )
    project_table.hAlign = "LEFT"

    project_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0E8")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
        ])
    )

    story.append(project_table)
    story.append(Spacer(1, 0.25 * inch))

    story.append(Paragraph("Material Takeoff", styles["Heading2"]))

    table_cell_style = ParagraphStyle(
        "InternalCostTableCell",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11
    )

    def table_cell(value):
        return Paragraph(escape(str(value)), table_cell_style)

    material_rows = [["Material", "Qty", "Unit"]]

    if priced_takeoff is not None:
        material_rows[0] = [
            "Material", "Qty", "Unit", "Unit Price",
            "Total", "Supplier"
        ]

    if priced_takeoff is not None:
        for item in priced_takeoff.get("priced_items", []):
            unit_cost = item.get("unit_cost")
            extended_cost = item.get("extended_cost")

            material_rows.append([
                table_cell(item.get("item", "")),
                table_cell(item.get("quantity", "")),
                table_cell(item.get("unit", "")),
                table_cell(
                    f"${unit_cost:,.2f}"
                    if unit_cost is not None
                    else "Price needed"
                ),
                table_cell(
                    f"${extended_cost:,.2f}"
                    if extended_cost is not None
                    else "-"
                ),
                table_cell(item.get("supplier", "Not recorded"))
            ])
    else:
        for item in material_takeoff:
            material_rows.append([
                table_cell(item.get("item", "")),
                table_cell(item.get("quantity", "")),
                table_cell(item.get("unit", ""))
            ])

    if len(material_rows) == 1:
        material_rows.append(
            [table_cell("No material takeoff items saved yet.")] +
            [""] * (len(material_rows[0]) - 1)
        )

    material_widths = (
        [2.25 * inch, 0.45 * inch, 0.8 * inch, 0.85 * inch,
         0.95 * inch, 2.8 * inch]
        if priced_takeoff is not None
        else [6.9 * inch, 1.5 * inch, 1.2 * inch]
    )

    material_table = Table(
        material_rows,
        colWidths=material_widths,
        repeatRows=1
    )
    material_table.hAlign = "LEFT"

    material_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#315C3B")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )

    story.append(material_table)
    story.append(Spacer(1, 0.25 * inch))

    if bid_summary is not None:
        story.append(Paragraph("Bid Summary", styles["Heading2"]))

        material_complete = bid_summary.get(
            "materials_complete",
            False
        )
        customer_price = bid_summary.get("customer_price", 0.0)

        bid_rows = [
            ["Priced Material Cost", f"${bid_summary.get('material_cost', 0.0):,.2f}"],
            ["Labor Cost", f"${bid_summary.get('labor_cost', 0.0):,.2f}"],
            ["Overhead", f"${bid_summary.get('overhead_cost', 0.0):,.2f}"],
            ["Profit", f"${bid_summary.get('profit_amount', 0.0):,.2f}"],
            [
                "Customer Price" if material_complete else "Customer Price Status",
                (
                    f"${customer_price:,.2f}"
                    if material_complete
                    else "Not finalized - supplier prices are missing"
                )
            ]
        ]

        bid_table = Table(bid_rows, colWidths=[3.2 * inch, 6.5 * inch])
        bid_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#315C3B")),
                ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("PADDING", (0, 0), (-1, -1), 7)
            ])
        )
        story.append(bid_table)

        labor_trades = bid_summary.get("labor_trades", [])
        if labor_trades:
            story.append(Spacer(1, 0.16 * inch))
            story.append(Paragraph("Project Labor Plan", styles["Heading3"]))
            labor_rows = [["Trade", "Hours", "Loaded Hourly Cost"]]

            for trade in labor_trades:
                labor_rows.append([
                    str(trade.get("trade", "")),
                    f"{float(trade.get('labor_hours', 0.0)):,.1f}",
                    f"${float(trade.get('hourly_rate', 0.0)):,.2f}"
                ])

            labor_table = Table(
                labor_rows,
                colWidths=[3.2 * inch, 1.2 * inch, 2.0 * inch]
            )
            labor_table.setStyle(
                TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#315C3B")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("PADDING", (0, 0), (-1, -1), 7)
                ])
            )
            story.append(labor_table)

        if not material_complete:
            missing_count = len(
                priced_takeoff.get("unpriced_items", [])
            ) if priced_takeoff is not None else 0
            story.append(Spacer(1, 0.16 * inch))
            story.append(
                Paragraph(
                    f"Pricing is incomplete: {missing_count} material item(s) "
                    "need a saved supplier price before a customer price "
                    "can be finalized.",
                    styles["Normal"]
                )
            )

        story.append(Spacer(1, 0.25 * inch))

    proposal_notes = details.get("proposal_notes", "").strip()
    proposal_scope = details.get("proposal_scope", "").strip()
    proposal_exclusions = details.get("proposal_exclusions", "").strip()
    proposal_expiration_date = details.get(
        "proposal_expiration_date",
        ""
    ).strip()

    if proposal_expiration_date:
        story.append(
            Paragraph(
                f"<b>Quote valid through:</b> "
                f"{escape(proposal_expiration_date)}",
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 0.16 * inch))

    if proposal_scope:
        story.append(Paragraph("Scope of Work", styles["Heading2"]))
        story.append(
            Paragraph(
                escape(proposal_scope).replace("\n", "<br/>"),
                styles["Normal"]
            )
        )

    if proposal_exclusions:
        story.append(Spacer(1, 0.2 * inch))
        story.append(
            Paragraph("Exclusions and Assumptions", styles["Heading2"])
        )
        story.append(
            Paragraph(
                escape(proposal_exclusions).replace("\n", "<br/>"),
                styles["Normal"]
            )
        )

    if proposal_notes:
        story.append(Spacer(1, 0.25 * inch))
        story.append(
            Paragraph("Notes", styles["Heading2"])
        )
        story.append(
            Paragraph(
                escape(proposal_notes).replace("\n", "<br/>"),
                styles["Normal"]
            )
        )

    story.append(
        Paragraph(
            "This report is a material estimate. Final design, "
            "quantities, specifications, and installation must follow "
            "approved plans and applicable code requirements.",
            styles["Normal"]
        )
    )

    document.build(story)

    return pdf_path


def create_customer_proposal_pdf(project, profile, bid_summary):
    """Create a customer-safe proposal with no internal costs or markups."""
    export_folder = Path(__file__).with_name("exports")
    export_folder.mkdir(exist_ok=True)

    safe_project_name = project["name"].replace(" ", "_").lower()
    pdf_path = export_folder / f"{safe_project_name}_customer_proposal.pdf"

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=landscape(letter),
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()
    story = []
    details = project.get("details", {})

    company = profile.get("company", "Your Company")
    company_lines = [
        line for line in [
            profile.get("name", ""),
            profile.get("phone", ""),
            profile.get("email", ""),
            profile.get("address", "")
        ] if line
    ]

    proposal_title = details.get(
        "proposal_title",
        ""
    ) or "Construction Proposal"

    story.append(Paragraph(escape(proposal_title), styles["Title"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph(f"<b>{escape(company)}</b>", styles["Heading2"]))

    for line in company_lines:
        story.append(Paragraph(escape(str(line)), styles["Normal"]))

    story.append(Spacer(1, 0.22 * inch))

    customer_name = details.get("customer_name", "") or "Not specified"
    customer_email = details.get("customer_email", "") or "Not specified"
    project_address = details.get("project_address", "") or "Not specified"
    proposal_expiration_date = details.get(
        "proposal_expiration_date",
        ""
    ) or "Not specified"

    project_info = [
        ["Project", project["name"]],
        ["Prepared For", customer_name],
        ["Customer Email", customer_email],
        ["Project Address", project_address],
        ["Quote Valid Through", proposal_expiration_date]
    ]

    project_table = Table(
        project_info,
        colWidths=[1.6 * inch, 5.3 * inch]
    )
    project_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0E8")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5)
        ])
    )
    story.append(project_table)
    story.append(Spacer(1, 0.28 * inch))

    proposal_scope = details.get("proposal_scope", "").strip()
    proposal_exclusions = details.get("proposal_exclusions", "").strip()
    proposal_notes = details.get("proposal_notes", "").strip()

    if proposal_scope:
        story.append(Paragraph("Scope of Work", styles["Heading2"]))
        story.append(
            Paragraph(
                escape(proposal_scope).replace("\n", "<br/>"),
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 0.2 * inch))

    customer_price = float(bid_summary.get("customer_price", 0.0))
    price_table = Table(
        [["Total Proposed Price", f"${customer_price:,.2f}"]],
        colWidths=[3.7 * inch, 3.2 * inch]
    )
    price_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#315C3B")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 13),
            ("ALIGN", (1, 0), (1, -1), "RIGHT"),
            ("PADDING", (0, 0), (-1, -1), 10)
        ])
    )
    story.append(price_table)
    story.append(Spacer(1, 0.25 * inch))

    if proposal_exclusions:
        story.append(
            Paragraph("Exclusions and Assumptions", styles["Heading2"])
        )
        story.append(
            Paragraph(
                escape(proposal_exclusions).replace("\n", "<br/>"),
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 0.2 * inch))

    if proposal_notes:
        story.append(Paragraph("Additional Notes", styles["Heading2"]))
        story.append(
            Paragraph(
                escape(proposal_notes).replace("\n", "<br/>"),
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 0.2 * inch))

    story.append(Paragraph("Acceptance", styles["Heading2"]))
    story.append(
        Paragraph(
            "By signing below, the customer accepts this proposal subject "
            "to the scope, exclusions, and assumptions listed above.",
            styles["Normal"]
        )
    )
    story.append(Spacer(1, 0.4 * inch))

    acceptance_table = Table(
        [
            ["Customer Signature: __________________________", "Date: __________"],
            ["Printed Name: _______________________________", ""]
        ],
        colWidths=[4.8 * inch, 2.1 * inch]
    )
    acceptance_table.setStyle(
        TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12)
        ])
    )
    story.append(acceptance_table)

    document.build(story)
    return pdf_path


def create_change_order_pdf(
        project,
        profile,
        change_order,
        change_order_number,
        original_contract_price,
        approved_change_total
):
    """Create a customer-safe change order without internal cost data."""
    export_folder = Path(__file__).with_name("exports")
    export_folder.mkdir(exist_ok=True)

    safe_project_name = project["name"].replace(" ", "_").lower()
    pdf_path = export_folder / (
        f"{safe_project_name}_change_order_{change_order_number}.pdf"
    )

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch
    )

    styles = getSampleStyleSheet()
    story = []
    details = project.get("details", {})
    company = profile.get("company", "Your Company")
    customer_name = details.get("customer_name", "") or "Not specified"
    project_address = details.get("project_address", "") or "Not specified"
    change_amount = float(change_order.get("amount", 0.0))
    revised_contract_price = (
        float(original_contract_price) +
        float(approved_change_total) +
        change_amount
    )

    story.append(Paragraph("Change Order", styles["Title"]))
    story.append(Spacer(1, 0.12 * inch))
    story.append(Paragraph(f"<b>{escape(company)}</b>", styles["Heading2"]))

    for line in [
        profile.get("name", ""),
        profile.get("phone", ""),
        profile.get("email", ""),
        profile.get("address", "")
    ]:
        if line:
            story.append(Paragraph(escape(str(line)), styles["Normal"]))

    story.append(Spacer(1, 0.22 * inch))

    information = [
        ["Change Order", f"#{change_order_number}"],
        ["Date", change_order.get("date", "") or "Not specified"],
        ["Project", project.get("name", "")],
        ["Prepared For", customer_name],
        ["Project Address", project_address],
        ["Status", change_order.get("status", "Draft")]
    ]
    information_table = Table(information, colWidths=[1.6 * inch, 5.3 * inch])
    information_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0E8")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7)
    ]))
    story.append(information_table)
    story.append(Spacer(1, 0.28 * inch))

    story.append(Paragraph("Change Description", styles["Heading2"]))
    story.append(Paragraph(
        escape(change_order.get("description", "")).replace("\n", "<br/>"),
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.25 * inch))

    pricing_table = Table(
        [
            ["Original Contract Price", f"${float(original_contract_price):,.2f}"],
            ["Previously Approved Changes", f"${float(approved_change_total):,.2f}"],
            ["This Change Order", f"${change_amount:,.2f}"],
            ["Revised Contract Price", f"${revised_contract_price:,.2f}"]
        ],
        colWidths=[4.3 * inch, 2.6 * inch]
    )
    pricing_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#315C3B")),
        ("TEXTCOLOR", (0, 3), (-1, 3), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8)
    ]))
    story.append(pricing_table)
    story.append(Spacer(1, 0.25 * inch))

    notes = change_order.get("notes", "").strip()
    if notes:
        story.append(Paragraph("Notes and Assumptions", styles["Heading2"]))
        story.append(Paragraph(
            escape(notes).replace("\n", "<br/>"),
            styles["Normal"]
        ))
        story.append(Spacer(1, 0.22 * inch))

    story.append(Paragraph("Customer Authorization", styles["Heading2"]))
    story.append(Paragraph(
        "By signing below, the customer authorizes this change and the "
        "revised contract price shown above.",
        styles["Normal"]
    ))
    story.append(Spacer(1, 0.4 * inch))
    signature_table = Table(
        [
            ["Customer Signature: __________________________", "Date: __________"],
            ["Printed Name: _______________________________", ""]
        ],
        colWidths=[4.8 * inch, 2.1 * inch]
    )
    signature_table.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12)
    ]))
    story.append(signature_table)

    document.build(story)
    return pdf_path
