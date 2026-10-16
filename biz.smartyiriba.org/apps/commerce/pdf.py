from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

def invoice_pdf(invoice):
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='SmallBiz', parent=styles['Normal'], fontSize=8, leading=11, splitLongWords=True))
    styles.add(ParagraphStyle(name='RightBiz', parent=styles['Normal'], alignment=TA_RIGHT))
    def p(text, style='Normal'):
        return Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])
    doc = SimpleDocTemplate(buffer, pagesize=(210*mm, 297*mm), rightMargin=18*mm, leftMargin=18*mm, topMargin=18*mm, bottomMargin=20*mm, title='Facture ' + invoice.number, author=invoice.issuer.get('name') or 'Smart YIRIBA')
    content = [p('SMART YIRIBA', 'Heading2'), p('FACTURE', 'Title'), p(invoice.number, 'SmallBiz'), p('Émise le ' + invoice.issued_at.strftime('%d/%m/%Y')), Spacer(1, 6*mm)]
    issuer = invoice.issuer
    if not issuer.get('name') or not issuer.get('address'):
        content += [p('DOCUMENT DE DÉVELOPPEMENT - Coordonnées de l’émetteur à configurer.', 'Heading3')]
    content += [p('Émetteur', 'Heading3')]
    for key in ('name', 'address', 'registration', 'email'):
        if issuer.get(key): content.append(p(issuer[key]))
    content += [Spacer(1, 4*mm), p('Facturé à', 'Heading3'), p(invoice.customer_name), p(invoice.customer_address), p(invoice.customer_email), Spacer(1, 6*mm)]
    data = [[p(label, 'SmallBiz') for label in ('Prestation', 'Qté', 'Prix unit.', 'Remise HT', 'Taxe %', 'Total TTC')]]
    for item in invoice.items:
        data.append([p(item.get(key, ''), 'SmallBiz') for key in ('description', 'quantity', 'unit_price', 'discount', 'tax_rate', 'total')])
    table = Table(data, colWidths=[60*mm, 12*mm, 27*mm, 25*mm, 18*mm, 32*mm], repeatRows=1, hAlign='LEFT')
    table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#eaf0e6')), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('LINEBELOW', (0,0), (-1,0), .6, colors.HexColor('#214d36')), ('LINEBELOW', (0,1), (-1,-1), .3, colors.HexColor('#d6dfd8')), ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8)]))
    content += [p('Montants en ' + invoice.currency, 'SmallBiz'), table, Spacer(1, 5*mm), KeepTogether([p('Total : ' + str(invoice.total) + ' ' + invoice.currency, 'Heading2'), p('Modalités de paiement', 'Heading3'), p(invoice.payment_terms)])]
    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(colors.HexColor('#52685d'))
        canvas.drawString(18*mm, 12*mm, 'Smart YIRIBA - Facture')
        canvas.drawRightString(192*mm, 12*mm, 'Page ' + str(document.page))
        canvas.restoreState()
    # Document d'émission stable : les encaissements ultérieurs sont consultables dans le portail.
    doc.build(content, onFirstPage=footer, onLaterPages=footer)
    return buffer.getvalue()
