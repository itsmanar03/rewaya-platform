from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.platypus import Image
from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from bidi.algorithm import get_display
import arabic_reshaper

from datetime import datetime

def ar(text):

    reshaped_text = arabic_reshaper.reshape(
        str(text)
    )

    return get_display(
        reshaped_text
    )

def generate_executive_report(
    filename,
    total_projects,
    total_budget,
    total_beneficiaries,
    total_volunteers,
    projects
):

    pdfmetrics.registerFont(
        TTFont(
            "Amiri",
            "assets/fonts/Amiri-Regular.ttf"
        )   
    )

    doc = SimpleDocTemplate(
        filename,
        topMargin=20
    )

    styles = getSampleStyleSheet()

    arabic_style = ParagraphStyle(
        "Arabic",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=22,
        alignment=2
    )

    title_style = ParagraphStyle(
        "TitleArabic",
        parent=styles["Title"],
        fontName="Amiri"
    )

    content = []

    logo = Image(
        "assets/logo_used.png",
        width=500,
        height=80
    )

    content.append(logo)

    content.append(
    Spacer(1, 5)
    )

    content.append(
        Paragraph(
            ar("تقرير تنفيذي - منصة حصادنا"),
            title_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d')}"),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            ar(f"عدد المشاريع: {total_projects}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"إجمالي الميزانية: {total_budget:,.0f}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"إجمالي المستفيدين: {total_beneficiaries}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"إجمالي المتطوعين: {total_volunteers}"),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar("المشاريع المسجلة"),
            title_style
        )
    )

    content.append(
        Spacer(1, 10)
    )

    table_data = [
        [
            Paragraph(ar("الميزانية"), arabic_style),
            Paragraph(ar("الحالة"), arabic_style),
            Paragraph(ar("اسم المشروع"), arabic_style)
        ]
    ]

    for project in projects:

        table_data.append([
            Paragraph(f"{project[10]:,.0f}", arabic_style),
            Paragraph(ar(project[7]), arabic_style),
            Paragraph(ar(project[1]), arabic_style)
        ])

    table = Table(
        table_data,
        colWidths=[100, 120, 220]
    )

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Amiri')
        ])
    )

    content.append(table)

    doc.build(content)

def generate_donor_report(
    filename,
    total_projects,
    total_budget,
    total_beneficiaries,
    projects
):

    pdfmetrics.registerFont(
        TTFont(
            "Amiri",
            "assets/fonts/Amiri-Regular.ttf"
        )
    )

    doc = SimpleDocTemplate(
        filename,
        topMargin=20
    )
    
    styles = getSampleStyleSheet()

    arabic_style = ParagraphStyle(
        "Arabic",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=22,
        alignment=2
    )

    title_style = ParagraphStyle(
        "TitleArabic",
        parent=styles["Title"],
        fontName="Amiri"
    )

    content = []

    logo = Image(
        "assets/logo_used.png",
        width=500,
        height=80
    )

    content.append(logo)

    content.append(
        Spacer(1, 5)
    )

    content.append(
        Paragraph(
            ar("تقرير المانحين"),
            title_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d')}"),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            ar(f"عدد المشاريع المنفذة: {total_projects}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"إجمالي المستفيدين: {total_beneficiaries}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"إجمالي الميزانية: {total_budget:,.0f} ريال"),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar("المشاريع المدعومة"),
            title_style
        )
    )

    content.append(
        Spacer(1, 10)
    )

    table_data = [
        [
            Paragraph(ar("الميزانية"), arabic_style),
            Paragraph(ar("الحالة"), arabic_style),
            Paragraph(ar("اسم المشروع"), arabic_style)
        ]
    ]

    for project in projects:

        table_data.append([
            Paragraph(f"{project[10]:,.0f}", arabic_style),
            Paragraph(ar(project[7]), arabic_style),
            Paragraph(ar(project[1]), arabic_style)
        ])

    table = Table(
        table_data,
        colWidths=[100, 120, 220]
    )

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'Amiri')
        ])
    )

    content.append(table)

    doc.build(content)

def generate_impact_report(
    filename,
    total_projects,
    total_beneficiaries,
    total_volunteers,
    kpis
):

    pdfmetrics.registerFont(
        TTFont(
            "Amiri",
            "assets/fonts/Amiri-Regular.ttf"
        )
    )

    doc = SimpleDocTemplate(
        filename,
        topMargin=20
    )

    styles = getSampleStyleSheet()

    arabic_style = ParagraphStyle(
        "Arabic",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=22,
        alignment=2
    )

    title_style = ParagraphStyle(
        "TitleArabic",
        parent=styles["Title"],
        fontName="Amiri"
    )

    content = []

    logo = Image(
        "assets/logo_used.png",
        width=500,
        height=80
    )

    content.append(logo)

    content.append(
        Spacer(1, 5)
    )

    content.append(
        Paragraph(
            ar("تقرير الأثر التنموي"),
            title_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar(f"تاريخ التقرير: {datetime.now().strftime('%Y-%m-%d')}"),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    content.append(
        Paragraph(
            ar(f"إجمالي المستفيدين: {total_beneficiaries}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"إجمالي المتطوعين: {total_volunteers}"),
            arabic_style
        )
    )

    content.append(
        Paragraph(
            ar(f"عدد المشاريع ذات الأثر: {total_projects}"),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar("تعكس هذه النتائج الأثر التنموي الذي حققته المؤسسة من خلال برامجها ومشاريعها المختلفة."),
            arabic_style
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            ar("مؤشرات الأداء"),
            title_style
        )
    )

    content.append(
        Spacer(1, 10)
    )

    table_data = [
        [
            Paragraph(ar("نسبة الإنجاز"), arabic_style),
            Paragraph(ar("المتحقق"), arabic_style),
            Paragraph(ar("المستهدف"), arabic_style),
            Paragraph(ar("المؤشر"), arabic_style)
        ]
    ]

    for kpi in kpis:

        target = kpi[3] or 0
        actual = kpi[4] or 0

        percentage = 0

        if target > 0:
            percentage = round(
                (actual / target) * 100,
                1
            )

        table_data.append([
            Paragraph(f"{percentage}%", arabic_style),
            Paragraph(str(actual), arabic_style),
            Paragraph(str(target), arabic_style),
            Paragraph(ar(kpi[2]), arabic_style)
        ])

    table = Table(
        table_data,
        colWidths=[100, 100, 100, 180]
    )

    table.setStyle(
        TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Amiri')
        ])
    )

    content.append(table)

    doc.build(content)

def generate_text_report(
    filename,
    report_text
):

    pdfmetrics.registerFont(
        TTFont(
            "Amiri",
            "assets/fonts/Amiri-Regular.ttf"
        )
    )

    doc = SimpleDocTemplate(
        filename,
        topMargin=20
    )

    styles = getSampleStyleSheet()

    arabic_style = ParagraphStyle(
        "Arabic",
        parent=styles["Normal"],
        fontName="Amiri",
        fontSize=12,
        leading=24,
        alignment=2
    )

    content = []

    logo = Image(
        "assets/logo_used.png",
        width=500,
        height=80
    )

    content.append(logo)

    content.append(
        Spacer(1, 10)
    )

    for line in report_text.split("\n"):

        if line.strip():

            content.append(
                Paragraph(
                    ar(line),
                    arabic_style
                )
            )

            content.append(
                Spacer(1, 3)
            )

    doc.build(content)