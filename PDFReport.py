from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Spacer,
    Paragraph,
    Table,
    TableStyle
)


def create_project_pdf(project, profile,material_takeoff):
    export_folder = Path(__file__).with_name("exports")
    export_folder.mkdir(exist_ok=True)

    safe_project_name = project["name"].replace(" ", "_").lower()
    pdf_path = export_folder / f"{safe_project_name}_material_report.pdf"

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

    story.append(
        Paragraph(proposal_title, styles["Title"])
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
        colWidths=[1.45 * inch, 5.6 * inch]
    )

    project_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0E8")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("PADDING", (0, 0), (-1, -1), 7)
        ])
    )

    story.append(project_table)
    story.append(Spacer(1, 0.25 * inch))

    story.append(
        Paragraph("Material Takeoff", styles["Heading2"])
    )

    material_rows = [["Material", "Quantity", "Unit"]]

    for item in material_takeoff:
        material_rows.append([
            str(item.get("item", "")),
            str(item.get("quantity", "")),
            str(item.get("unit", ""))
        ])

    if len(material_rows) == 1:
        material_rows.append([
            "No material takeoff items saved yet.",
            "",
            ""
        ])

    material_table = Table(
        material_rows,
        colWidths=[4.7 * inch, 1.1 * inch, 0.8 * inch]
    )

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

    proposal_notes = details.get("proposal_notes", "").strip()

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