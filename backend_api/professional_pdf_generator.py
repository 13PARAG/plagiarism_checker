from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak,
    KeepTogether, Image
)
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from datetime import datetime
import io
import logging
import re

logger = logging.getLogger(__name__)

def add_color_to_text(text, similarity_score):
    if similarity_score >= 0.75:
        color = "#F44336"  # Red
    elif similarity_score >= 0.50:
        color = "#FF9800"  # Orange
    elif similarity_score >= 0.25:
        color = "#FFC107"  # Yellow
    elif similarity_score > 0.00:
        color = "#4CAF50"  # Green
    else:
        color = "#2196F3"  # Blue
    return f'<font color="{color}"><b>{text}</b></font>'

def render_highlighted_text(text):
    # Convert <mark>...</mark> into ReportLab highlighted spans (yellow background)
    pattern = r"<mark>(.*?)</mark>"
    # Replace <mark> spans with yellow highlight and black text
    return re.sub(pattern, r'<font backcolor="#FFEB3B" color="#000000">\1</font>', text)

def generate_professional_plagiarism_report(data, mode="local"):
    try:
        pdf_buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )

        elements = []
        styles = getSampleStyleSheet()

        # Styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        heading_style = ParagraphStyle(
            'Heading',
            parent=styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold',
            borderPadding=10,
            borderColor=colors.HexColor('#1f77b4'),
            borderWidth=1
        )

        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        )

        # Cover page
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("PLAGIARISM VERIFICATION REPORT", title_style))
        elements.append(Spacer(1, 0.1*inch))
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        metadata = [
            ["Report Generated:", timestamp],
            ["Report Type:", "LOCAL COMPARISON" if mode == "local" else "INTERNET SEARCH"],
            ["System:", "Advanced Plagiarism Checker v3.0"],
            ["Institution:", "RAIT/Your Institution Name"],
        ]
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
        ]))
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.2*inch))

        if mode == "local":
            similarity_score = data.get('similarity_score', 0)
            probability = data.get('probability', 0)
            if similarity_score >= 0.75:
                verdict_text = "🔴 PLAGIARIZED (High Similarity)"
                verdict_color = colors.HexColor('#F44336')
            elif similarity_score >= 0.50:
                verdict_text = "🟠 SUSPICIOUS (Medium-High Similarity)"
                verdict_color = colors.HexColor('#FF9800')
            elif similarity_score >= 0.25:
                verdict_text = "🟡 CAUTION (Medium Similarity)"
                verdict_color = colors.HexColor('#FFC107')
            elif similarity_score > 0.00:
                verdict_text = "🟢 LOW PLAGIARISM (Low Similarity)"
                verdict_color = colors.HexColor('#4CAF50')
            else:
                verdict_text = "🔵 ORIGINAL (No Plagiarism)"
                verdict_color = colors.HexColor('#2196F3')
            summary_data = [
                ["SIMILARITY INDEX", f"{similarity_score * 100:.2f}%"],
                ["ML PROBABILITY", f"{probability * 100:.2f}%"],
                ["STATUS", verdict_text],
            ]
            summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f77b4')),
                ('BACKGROUND', (0, 2), (1, 2), verdict_color),
                ('TEXTCOLOR', (0, 2), (1, 2), colors.white),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("DOCUMENT DETAILS", heading_style))
            doc_details = [
                ["Original File:", data.get('original_filename', 'N/A')],
                ["Original Format:", data.get('original_type', 'N/A').upper()],
                ["Submission File:", data.get('submission_filename', 'N/A')],
                ["Submission Format:", data.get('submission_type', 'N/A').upper()],
            ]
            doc_table = Table(doc_details, colWidths=[2*inch, 4*inch])
            doc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(doc_table)
            elements.append(Spacer(1, 0.2*inch))
            elements.append(Paragraph("DETAILED TEXT COMPARISON", heading_style))
            elements.append(Paragraph("<b>ORIGINAL DOCUMENT:</b> (Highlighted sections indicate matches)", normal_style))
            original_highlighted = data.get('highlighted_original', '')
            elements.append(Paragraph(render_highlighted_text(original_highlighted), normal_style))
            elements.append(Spacer(1, 0.15*inch))
            elements.append(PageBreak())
            elements.append(Paragraph("<b>SUBMISSION DOCUMENT:</b> (Highlighted sections indicate matches)", normal_style))
            submission_highlighted = data.get('highlighted_submission', '')
            elements.append(Paragraph(render_highlighted_text(submission_highlighted), normal_style))

        else:  # Internet mode
            # --- Summary ---
            verdict = data.get('overall_verdict', 'UNKNOWN')
            total_matches = data.get('total_matches_found', 0)
            highest_sim = data.get('highest_similarity', 0)
            if highest_sim >= 0.75:
                verdict_color = colors.HexColor('#F44336')
            elif highest_sim >= 0.50:
                verdict_color = colors.HexColor('#FF9800')
            elif highest_sim >= 0.25:
                verdict_color = colors.HexColor('#FFC107')
            else:
                verdict_color = colors.HexColor('#4CAF50')
            summary_data = [
                ["TOTAL MATCHES", str(total_matches)],
                ["HIGHEST SIMILARITY", f"{highest_sim * 100:.2f}%"],
                ["STATUS", verdict],
            ]
            summary_table = Table(summary_data, colWidths=[2.5*inch, 3.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9f9f9')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#1f77b4')),
                ('BACKGROUND', (0, 2), (1, 2), verdict_color),
                ('TEXTCOLOR', (0, 2), (1, 2), colors.white),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 0.2*inch))
            # --- Submission Details ALWAYS ---
            elements.append(Paragraph("SUBMISSION DETAILS", heading_style))
            doc_details = [
                ["Submission File:", data.get('submission_filename', 'N/A')],
                ["File Format:", data.get('submission_type', 'N/A').upper()],
                ["File Size:", f"{data.get('submission_size', 0)} characters"],
            ]
            doc_table = Table(doc_details, colWidths=[2*inch, 4*inch])
            doc_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            elements.append(doc_table)
            elements.append(Spacer(1, 0.2*inch))
            # --- Internet Matches section ---
            elements.append(Paragraph("TOP MATCHING SOURCES FROM INTERNET", heading_style))
            matches = data.get('internet_matches', [])
            if matches:
                for idx, match in enumerate(matches, 1):
                    match_sim = match.get('similarity_score', 0) * 100
                    if match_sim >= 75:
                        source_color = colors.HexColor('#FFCCCC')
                    elif match_sim >= 50:
                        source_color = colors.HexColor('#FFE0B2')
                    elif match_sim >= 25:
                        source_color = colors.HexColor('#FFF9C4')
                    else:
                        source_color = colors.HexColor('#C8E6C9')
                    match_header = f"""
                    <b>Match #{idx}: {match.get('title', 'Unknown')}</b><br/>
                    <b>URL:</b> <font color="blue"><u>{match.get('url', 'N/A')}</u></font><br/>
                    <b>Similarity: {match_sim:.2f}% | Probability: {match.get('probability', 0)*100:.2f}%</b>
                    """
                    source_data = [[Paragraph(match_header, normal_style)]]
                    source_table = Table(source_data, colWidths=[6*inch])
                    source_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), source_color),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTSIZE', (0, 0), (-1, -1), 9),
                        ('PADDING', (0, 0), (-1, -1), 10),
                        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                    ]))
                    elements.append(source_table)
                    elements.append(Spacer(1, 0.05*inch))
                    snippet = match.get('snippet', 'N/A')[:300]
                    elements.append(Paragraph(f"<i>Snippet: {snippet}...</i>", normal_style))
                    elements.append(Spacer(1, 0.1*inch))
            else:
                elements.append(Paragraph("<i>No significant matching sources found on the internet for this document.</i>", normal_style))

        # Legend/footer (unchanged)
        elements.append(PageBreak())
        elements.append(Paragraph("COLOR CODING LEGEND", heading_style))
        legend_text = """
        <b>Similarity Score Interpretation (Standard Plagiarism Detection Format):</b><br/><br/>
        <font color="red"><b>🔴 RED (75-100%):</b></font> High plagiarism - Exact or near-exact matches from sources<br/>
        <font color="orange"><b>🟠 ORANGE (50-74%):</b></font> Medium-High similarity - Significant portions match<br/>
        <font color="#DAA520"><b>🟡 YELLOW (25-49%):</b></font> Medium similarity - Notable matches found<br/>
        <font color="green"><b>🟢 GREEN (1-24%):</b></font> Low plagiarism - Minor matches detected<br/>
        <font color="blue"><b>🔵 BLUE (0%):</b></font> No plagiarism - Original content<br/><br/>
        <b>Note:</b> This report uses standard color-coding similar to Turnitin and other professional
        plagiarism detection systems. Color indicates the degree of textual similarity found during analysis.
        """
        elements.append(Paragraph(legend_text, normal_style))
        elements.append(Spacer(1, 0.2*inch))
        footer_text = """
        <hr/>
        <font size="8" color="#666666">
        <b>REPORT INFORMATION:</b><br/>
        This report was generated by Advanced Plagiarism Checker v3.0.<br/>
        Generated on: """ + datetime.now().strftime('%d-%m-%Y %H:%M:%S') + """<br/>
        System: Institution-Standard Plagiarism Detection<br/>
        B.Tech Computer Science - Semester 7 Final Project<br/><br/>
        <b>DISCLAIMER:</b><br/>
        This report is for academic and institutional use only. The color-coding and similarity percentages
        are indicators of textual similarity and require human interpretation. Matches may include proper citations,
        quotes, and references which are not considered plagiarism.<br/>
        The institution reserves the right to withdraw/revoke degree if plagiarism is found after award.
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_LEFT
        )))

        doc.build(elements)
        pdf_buffer.seek(0)
        pdf_content = pdf_buffer.getvalue()
        logger.info("✅ Professional plagiarism report generated successfully")
        return pdf_content

    except Exception as e:
        logger.error(f"❌ Error generating professional report: {str(e)}")
        raise
