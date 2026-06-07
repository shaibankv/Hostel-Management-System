import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.conf import settings

def generate_receipt_pdf(fee, total_paid, balance_fee):
    buffer = io.BytesIO()
    
    # Page setup
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    
    # Styles Setup
    styles = getSampleStyleSheet()
    
    # Colors
    PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep navy
    SECONDARY_COLOR = colors.HexColor("#2B6CB0") # Slate blue
    DARK_TEXT = colors.HexColor("#2D3748")       # Off black
    LIGHT_BG = colors.HexColor("#F7FAFC")        # Soft gray
    LINE_COLOR = colors.HexColor("#E2E8F0")      # Table grid color
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        textColor=PRIMARY_COLOR,
        alignment=1, # Center
        spaceAfter=5
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=12,
        textColor=SECONDARY_COLOR,
        alignment=1, # Center
        spaceAfter=25
    )
    
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=PRIMARY_COLOR,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=colors.HexColor("#4A5568")
    )
    
    value_style = ParagraphStyle(
        'Value',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        textColor=DARK_TEXT
    )

    value_bold_style = ParagraphStyle(
        'ValueBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=DARK_TEXT
    )

    # 1. Header Section
    story.append(Paragraph("SEA HOSTEL MANAGEMENT SYSTEM", title_style))
    story.append(Paragraph("Official Fee Payment Receipt", subtitle_style))
    
    # 2. Student & Document Metadata Table
    student = fee.student
    room_str = f"{student.room.block} - {student.room.room_no}" if student.room else "Not Assigned"
    
    # Left column: Student Details, Right column: Receipt Metadata
    meta_data = [
        [
            Paragraph("Student Name:", label_style), Paragraph(student.name, value_style),
            Paragraph("Receipt No:", label_style), Paragraph(f"REC-FEE-{fee.id or 'TEMP'}", value_style)
        ],
        [
            Paragraph("Reg. Number:", label_style), Paragraph(student.reg_number, value_style),
            Paragraph("Payment Date:", label_style), Paragraph(fee.payment_date.strftime("%b %d, %Y"), value_style)
        ],
        [
            Paragraph("Course / Year:", label_style), Paragraph(f"{student.course} / Year {student.year}", value_style),
            Paragraph("Academic Year:", label_style), Paragraph(fee.academic_year, value_style)
        ],
        [
            Paragraph("Room Assigned:", label_style), Paragraph(room_str, value_style),
            Paragraph("Payment Status:", label_style), Paragraph(fee.status, value_bold_style)
        ]
    ]
    
    meta_table = Table(meta_data, colWidths=[100, 160, 90, 180])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, LINE_COLOR),
    ]))
    story.append(Paragraph("Receipt & Student Information", section_heading))
    story.append(meta_table)
    story.append(Spacer(1, 15))
    
    # 3. Fee & Payment Details Table
    story.append(Paragraph("Payment Breakdown", section_heading))
    
    # We display: Fee Component, Payment Method, Transaction ID, and Amount
    breakdown_data = [
        [
            Paragraph("Description", label_style),
            Paragraph("Payment Method", label_style),
            Paragraph("Transaction/Ref ID", label_style),
            Paragraph("Amount", label_style)
        ],
        [
            Paragraph(f"Hostel Fee Payment ({fee.academic_year})", value_style),
            Paragraph(fee.payment_method, value_style),
            Paragraph(fee.transaction_id or "-", value_style),
            Paragraph(f"Rs. {fee.amount:,.2f}", value_bold_style)
        ]
    ]
    
    breakdown_table = Table(breakdown_data, colWidths=[200, 110, 110, 110])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BG),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, LINE_COLOR),
        ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
    ]))
    story.append(breakdown_table)
    story.append(Spacer(1, 15))
    
    # 4. Financial Summary Card / Table
    story.append(Paragraph("Fee Balance Summary", section_heading))
    
    summary_data = [
        [Paragraph("Total Hostel Fee:", label_style), Paragraph(f"Rs. {student.hostel_fee:,.2f}", value_style)],
        [Paragraph("Total Amount Paid:", label_style), Paragraph(f"Rs. {total_paid:,.2f}", value_style)],
        [Paragraph("Remaining Balance:", label_style), Paragraph(f"Rs. {balance_fee:,.2f}", value_bold_style)]
    ]
    
    summary_table = Table(summary_data, colWidths=[150, 100])
    summary_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('LINEBELOW', (0, 0), (-1, -1), 0.5, LINE_COLOR),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor("#FED7D7") if balance_fee > 0 else colors.HexColor("#C6F6D5")),
    ]))
    
    # We float the summary to the right by using a master table
    master_summary = Table([[Spacer(1, 1), summary_table]], colWidths=[280, 250])
    master_summary.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(master_summary)
    story.append(Spacer(1, 30))
    
    # 5. Signature Area
    signature_path = os.path.join(settings.BASE_DIR, 'accounts', 'static', 'accounts', 'signature.jpg')
    if not os.path.exists(signature_path):
        signature_path = os.path.join(settings.BASE_DIR, 'accounts', 'static', 'accounts', 'signature.png')
    
    sig_elements = []
    if os.path.exists(signature_path):
        try:
            # Load the signature image
            sig_img = Image(signature_path, width=120, height=50)
            sig_img.hAlign = 'RIGHT'
            sig_elements.append(sig_img)
        except Exception:
            # Fallback spacer if image load fails
            sig_elements.append(Spacer(1, 40))
    else:
        sig_elements.append(Spacer(1, 40))
        
    sig_line = Table([[""]], colWidths=[150])
    sig_line.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), 1, PRIMARY_COLOR),
    ]))
    sig_elements.append(sig_line)
    
    sig_label = ParagraphStyle(
        'SigLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        textColor=PRIMARY_COLOR,
        alignment=1 # Center
    )
    sig_elements.append(Spacer(1, 4))
    sig_elements.append(Paragraph("Authorized Warden Signature", sig_label))
    
    # Master signature layout to align it to the bottom-right
    sig_container = Table([[Spacer(1, 1), sig_elements]], colWidths=[380, 150])
    sig_container.setStyle(TableStyle([
        ('VALIGN', (1, 0), (1, -1), 'BOTTOM'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    
    story.append(KeepTogether([sig_container]))
    
    # Build Document
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
