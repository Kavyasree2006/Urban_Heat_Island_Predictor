from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(df, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>Urban Heat Island Analysis Report</b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            f"Total Locations : {len(df)}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Average Temperature : {df['Predicted Temperature'].mean():.2f}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Average Heat Risk Score : {df['Heat Risk Score'].mean():.2f}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    for _, row in df.head(20).iterrows():

        story.append(

            Paragraph(

                f"<b>{row['City Name']}</b>",

                styles["Heading2"]

            )

        )

        story.append(

            Paragraph(

                f"Heat Risk : {row['Heat Risk']}",

                styles["Normal"]

            )

        )

        story.append(

            Paragraph(

                row["Recommendations"],

                styles["Normal"]

            )

        )

        story.append(Spacer(1, 12))

    doc.build(story)