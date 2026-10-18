
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
)


def create_storybook_pdf(storybook: dict) -> Path:
    output_dir = Path(storybook["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = output_dir / "storybook.pdf"

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    )

    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="BookTitle",
            parent=styles["Title"],
            fontSize=28,
            leading=34,
            textColor=colors.HexColor("#26345C"),
            alignment=1,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="StoryText",
            parent=styles["BodyText"],
            fontSize=13,
            leading=19,
            spaceBefore=12,
        )
    )

    story = []

    cover_path = Path(storybook["cover_path"])
    if cover_path.is_file():
        story.append(
            Image(str(cover_path), width=6.5 * inch, height=5.3 * inch)
        )
        story.append(Spacer(1, 16))

    story.append(
        Paragraph(storybook["book_title"], styles["BookTitle"])
    )
    story.append(
        Paragraph(
            f"A storybook for ages {storybook['target_age']}",
            styles["Normal"],
        )
    )
    story.append(PageBreak())

    for page in storybook["pages"]:
        story.append(
            Paragraph(page["title"], styles["Heading1"])
        )

        image_path = Path(page["image_path"])
        if image_path.is_file():
            story.append(
                Image(
                    str(image_path),
                    width=6.5 * inch,
                    height=4.4 * inch,
                )
            )

        story.append(Spacer(1, 12))
        story.append(
            Paragraph(page["story_text"], styles["StoryText"])
        )
        story.append(PageBreak())

    doc.build(story)
    return pdf_path
