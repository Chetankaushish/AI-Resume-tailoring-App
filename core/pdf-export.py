from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def export_pdf(
    content,
    output_file
):

    doc = SimpleDocTemplate(
        output_file
    )

    styles = (
        getSampleStyleSheet()
    )

    story = []

    for line in content.split("\n"):

        story.append(
            Paragraph(
                line,
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1,6)
        )

    doc.build(story)

    return output_file