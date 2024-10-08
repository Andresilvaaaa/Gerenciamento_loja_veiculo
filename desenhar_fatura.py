# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.graphics.barcode import code128
from reportlab.platypus import Table, TableStyle
from datetime import datetime


def desenhar_fatura(pdf, cliente, produtos, numero_fatura):
    width, height = A4
    pdf.setPageSize(A4)

    # Cabeçalho com cor de fundo e logo
    pdf.setFillColorRGB(0, 0.7, 1)  # Azul claro
    pdf.rect(0, height - 40 * mm, width, 40 * mm, fill=1)
    logo_path = 'static/logoagevec.png'  # Atualize o caminho se necessário
    pdf.drawImage(logo_path, 15 * mm, height - 30 *
                  mm, width=40 * mm, height=20 * mm)

    pdf.setFont("Helvetica-Bold", 12)
    pdf.setFillColorRGB(1, 1, 1)  # Texto branco
    pdf.drawString(80 * mm, height - 15 * mm,
                   "AgeVec Motors")  # Movido para cima
    pdf.setFont("Helvetica", 10)
    pdf.drawString(80 * mm, height - 20 * mm,
                   "CNPJ: 12.345.678/0001-99")  # Movido para cima
    pdf.drawString(80 * mm, height - 25 * mm,
                   "Endereço da Empresa")  # Movido para cima
    pdf.drawString(80 * mm, height - 30 * mm,
                   "Telefone: (11) 1234-5678")  # Movido para cima
    pdf.drawString(80 * mm, height - 35 * mm,
                   "Email: contato@agevec.com.br")  # Movido para cima

    # Número da fatura e data, alinhados à direita
    pdf.setFillColorRGB(0, 0, 0)  # Texto preto
    pdf.setFont("Helvetica", 10)
    pdf.drawRightString(width - 15 * mm, height - 20 *
                        mm, f"Fatura Nº: {numero_fatura}")
    pdf.drawRightString(width - 15 * mm, height - 25 * mm,
                        f"Data: {datetime.now().strftime('%d/%m/%Y')}")

    # Título da fatura centralizado
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2.0, height - 55 * mm, "FATURA")

    # Dados do cliente com espaçamento correto
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(15 * mm, height - 65 * mm, "Dados do Cliente:")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(15 * mm, height - 70 * mm, f"Nome: {cliente['nome']}")
    pdf.drawString(15 * mm, height - 75 * mm, f"CPF: {cliente['codigo']}")
    pdf.drawString(15 * mm, height - 80 * mm,
                   f"Endereço: {cliente['endereco']}")
    pdf.drawString(15 * mm, height - 85 * mm,
                   f"Telefone: {cliente['telefone']}")
    pdf.drawString(15 * mm, height - 90 * mm, f"Email: {cliente['email']}")

    # Tabela de produtos com ajustes no layout
    data = [["Descrição", "Preço Unitário", "Quantidade", "Subtotal"]]
    for produto in produtos:
        subtotal = produto['quantidade'] * produto['preco_unitario']
        data.append([
            produto['nome'],
            f"R$ {produto['preco_unitario']:.2f}",
            f"{produto['quantidade']}",
            f"R$ {subtotal:.2f}"
        ])

    # Estilizando a tabela com melhor alinhamento e espaçamento
    table = Table(data, colWidths=[90 * mm, 40 * mm, 30 * mm, 30 * mm])
    table.setStyle(TableStyle([
        # Cabeçalho azul claro
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00AEEF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 1), (-1, -1),
         colors.HexColor('#f2f2f2'))  # Linhas alternadas
    ]))

    table_width, table_height = table.wrap(0, 0)
    table.drawOn(pdf, 15 * mm, height - 120 * mm - table_height)

    # Calcular total com alinhamento à direita
    total = sum(produto['quantidade'] * produto['preco_unitario']
                for produto in produtos)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawRightString(195 * mm, height - 130 * mm -
                        table_height, f"Total: R$ {total:.2f}")

    # Métodos de pagamento alinhados
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(15 * mm, height - 150 * mm -
                   table_height, "Método de Pagamento:")
    pdf.setFont("Helvetica", 10)
    pdf.drawString(15 * mm, height - 155 * mm - table_height, "■ Dinheiro")
    pdf.drawString(70 * mm, height - 155 * mm -
                   table_height, "■ Cartão de Crédito")
    pdf.drawString(150 * mm, height - 155 * mm -
                   table_height, "■ Transferência Bancária")
    # pdf.drawString(70 * mm, height - 160 * mm -
    #                table_height, "■ Pagamento Online")

    # Detalhes do pagamento com espaçamento adequado
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(15 * mm, height - 170 * mm -
                   table_height, "Detalhes do Pagamento:")
    pdf.setFont("Helvetica", 9)
    pdf.drawString(15 * mm, height - 175 * mm - table_height,
                   f"Número do Cartão: **** **** **** 1234")
    pdf.drawString(15 * mm, height - 180 * mm - table_height,
                   f"Data de Expiração: 12/2030")
    pdf.drawString(15 * mm, height - 185 * mm - table_height,
                   f"Nome no Cartão: {cliente['nome']}")
    pdf.drawString(15 * mm, height - 190 * mm - table_height,
                   f"Assinatura: __________________________")

    # Código de barras e rodapé
    barcode_value = str(numero_fatura)  # Converter numero_fatura para string
    barcode = code128.Code128(barcode_value, barHeight=15 * mm, barWidth=0.5)
    barcode.drawOn(pdf, 15 * mm, height - 220 * mm - table_height)

    # Rodapé com alinhamento e espaçamento
    pdf.setFillColorRGB(0, 0.7, 1)
    pdf.rect(0, 0, width, 20 * mm, fill=1)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawCentredString(width / 2.0, 10 * mm,
                          "Obrigado por fazer negócio conosco!")

    # Número da página centralizado
    pdf.setFont("Helvetica", 8)
    pdf.drawRightString(195 * mm, 10 * mm, f"Página 1 de 1")
