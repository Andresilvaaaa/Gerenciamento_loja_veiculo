import datetime
from io import BytesIO
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
# from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend para uso sem interface gráfica


def desenhar_dashboard(pdf, dados_dashboard, nome_empresa="AgeVec Motors"):
    desenhar_pagina_inicial(pdf, nome_empresa)

    # Página 1: Resumo
    desenhar_pagina_resumo(pdf, dados_dashboard, nome_empresa)
    pdf.showPage()

    # Página 2: Gráficos de Faturamento
    desenhar_pagina_faturamento(pdf, dados_dashboard)
    pdf.showPage()

    # Página 3: Vendas por Estado e Top Vendedores
    desenhar_pagina_vendas(pdf, dados_dashboard)
    pdf.showPage()

    desenhar_pagina_clientes(pdf, dados_dashboard)
    pdf.showPage()


def desenhar_pagina_resumo(pdf, dados_dashboard, nome_empresa):
    desenhar_cabecalho(pdf, nome_empresa, "Relatório de Dashboard - Resumo")
    width, height = A4

    # Dados Resumo
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(15 * mm, height - 80 * mm, "Resumo de Vendas e Faturamento")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(15 * mm, height - 90 * mm,
                   f"Total de Carros Vendidos: {
                       dados_dashboard.get('total_vendidos', 0)}")
    pdf.drawString(15 * mm, height - 100 * mm, f"Total de Carros Disponíveis: {
                   dados_dashboard.get('total_disponiveis', 0)}")
    pdf.drawString(15 * mm, height - 110 * mm,
                   f"Clientes Ativos: {
                       dados_dashboard.get('total_clientes_ativos', 0)}")
    pdf.drawString(15 * mm, height - 120 * mm, f"Faturamento Total: R$ {
                   dados_dashboard.get('total_faturamento', 0.0):.2f}")

    desenhar_rodape(pdf)


def desenhar_pagina_faturamento(pdf, dados_dashboard):
    desenhar_cabecalho(pdf, "AgeVec Motors", "Gráficos de Faturamento")
    width, height = A4
    y_position = height - 80 * mm

    # Faturamento por Dia
    if dados_dashboard['faturamento_por_dia']:
        y_position -= 60 * mm
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(15 * mm, y_position, "Faturamento por Dia")
        y_position -= 10 * mm
        y_position = desenhar_grafico_faturamento(
            pdf, dados_dashboard[
                'faturamento_por_dia'], "Faturamento por Dia", y_position)

    # Faturamento por Mês
    if dados_dashboard['faturamento_por_mes']:
        y_position -= 70 * mm  # Adicionar espaçamento entre os gráficos
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(15 * mm, y_position, "Faturamento por Mês")
        y_position -= 10 * mm
        y_position = desenhar_grafico_faturamento(
            pdf, dados_dashboard[
                'faturamento_por_mes'], "Faturamento por Mês", y_position)

    desenhar_rodape(pdf)


def desenhar_pagina_vendas(pdf, dados_dashboard):
    desenhar_cabecalho(pdf, "AgeVec Motors", "Análise de Vendas")
    width, height = A4
    y_position = height - 80 * mm

    # Vendas por Estado
    if dados_dashboard['vendas_por_estado']:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(15 * mm, y_position, "Vendas por Estado")
        y_position -= 10 * mm
        y_position = desenhar_grafico_estado(
            pdf, dados_dashboard['vendas_por_estado'], y_position)

    # Top Vendedores
    if dados_dashboard['vendas_por_vendedor']:
        y_position -= 20 * mm
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(15 * mm, y_position, "Top Vendedores")
        y_position -= 10 * mm
        y_position = desenhar_tabela_vendedores(
            pdf, dados_dashboard['vendas_por_vendedor'], y_position)

    desenhar_rodape(pdf)


def desenhar_pagina_clientes(pdf, dados_dashboard):
    desenhar_cabecalho(pdf, "AgeVec Motors", "Clientes Ativos")
    width, height = A4
    y_position = height - 80 * mm

    if dados_dashboard.get('clientes_ativos_detalhes'):
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(15 * mm, y_position, "Lista de Clientes Ativos")
        y_position -= 10 * mm
        y_position = desenhar_tabela_clientes(
            pdf, dados_dashboard['clientes_ativos_detalhes'], y_position)
    else:
        pdf.setFont("Helvetica", 12)
        pdf.drawString(15 * mm, y_position, "Nenhum cliente ativo encontrado.")

    desenhar_rodape(pdf)


def desenhar_grafico_estado(pdf, dados, y_position):
    try:
        estados = [item['cliente_estado'] for item in dados]
        vendas = [int(item['total_vendas']) for item in dados]

        plt.figure(figsize=(5, 3))
        plt.barh(estados, vendas, color='skyblue')
        plt.xlabel('Total de Vendas')
        plt.ylabel('Estado')
        plt.tight_layout()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')
        img_buffer.seek(0)
        plt.close()

        pdf.drawImage(ImageReader(img_buffer), 15 * mm,
                      y_position - 60 * mm, width=170 * mm, height=60 * mm)
        return y_position - 70 * mm

    except Exception as e:
        print(f"Erro ao desenhar gráfico de vendas por estado: {e}")
        return y_position


def desenhar_tabela_clientes(pdf, dados, y_position):
    data = [["CPF", "Nome", "Gênero", "Estado Civil",
             "Data de Nascimento", "Estado"]]
    for item in dados:
        data.append([
            item.get('cpf', ''),
            item.get('nome_completo', ''),
            item.get('genero', ''),
            item.get('estadocivil', ''),
            item.get('dataNascimento', '').strftime(
                '%d/%m/%Y') if item.get('dataNascimento') else '',
            item.get('estado', '')
        ])

    table = Table(data, colWidths=[
                  30 * mm, 50 * mm, 20 * mm, 30 * mm, 30 * mm, 20 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#00AEEF')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))

    table.wrapOn(pdf, 15 * mm, y_position)
    table_height = len(data) * 12  # Ajuste conforme necessário
    table.drawOn(pdf, 15 * mm, y_position - table_height)
    return y_position - table_height - 10 * mm


def desenhar_cabecalho(pdf, nome_empresa, titulo_pagina):
    width, height = A4
    pdf.setFillColorRGB(0.18, 0.45, 0.71)  # Azul escuro
    pdf.rect(0, height - 50 * mm, width, 50 * mm, fill=1)
    logo_path = 'static/logoagevec.png'
    pdf.drawImage(logo_path, 15 * mm, height - 45 * mm,
                  width=40 * mm, height=30 * mm, mask='auto')

    pdf.setFont("Helvetica-Bold", 16)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(60 * mm, height - 20 * mm, nome_empresa)
    pdf.setFont("Helvetica", 10)
    pdf.drawString(60 * mm, height - 30 * mm, "CNPJ: 12.345.678/0001-99")
    pdf.drawString(60 * mm, height - 35 * mm, "Endereço da Empresa")
    pdf.drawString(60 * mm, height - 40 * mm, "Telefone: (11) 1234-5678")
    pdf.drawString(60 * mm, height - 45 * mm, "Email: contato@agevec.com.br")

    pdf.setFillColorRGB(0, 0, 0)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawCentredString(width / 2.0, height - 60 * mm, titulo_pagina)


def desenhar_rodape(pdf):
    width, _ = A4
    pdf.setFillColorRGB(0.18, 0.45, 0.71)
    pdf.rect(0, 0, width, 15 * mm, fill=1)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.setFont("Helvetica-Oblique", 8)
    pdf.drawCentredString(width / 2.0, 5 * mm,
                          "Obrigado por fazer negócio conosco!")


def desenhar_tabela_vendedores(pdf, dados, y_position):
    data = [["Vendedor", "Total de Vendas", "Total Faturado (R$)"]]
    for idx, item in enumerate(dados):
        vendedor = item.get('vendedor_username', 'Desconhecido')
        total_vendas = item.get('total_vendas', 0)
        total_faturado = item.get('total_faturado', 0.0)
        data.append([
            vendedor,
            str(total_vendas),
            f"{float(total_faturado):.2f}"
        ])

    table = Table(data, colWidths=[70 * mm, 50 * mm, 50 * mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003B6F')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F2F2F2')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ]))

    table.wrapOn(pdf, 15 * mm, y_position)
    table_height = len(data) * 15
    table.drawOn(pdf, 15 * mm, y_position - table_height)
    return y_position - table_height - 10 * mm


plt.style.use('ggplot')  # Escolha um estilo que você goste


def desenhar_pagina_inicial(pdf, nome_empresa):
    width, height = A4
    pdf.setFillColorRGB(1, 1, 1)
    pdf.rect(0, 0, width, height, fill=1)

    logo_path = 'static/logoagevec.png'
    pdf.drawImage(logo_path, width / 2 - 50 * mm, height - 100 *
                  mm, width=100 * mm, height=50 * mm, mask='auto')

    pdf.setFont("Helvetica-Bold", 24)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawCentredString(width / 2.0, height - 150 *
                          mm, "Relatório de Dashboard")

    pdf.setFont("Helvetica", 16)
    pdf.drawCentredString(width / 2.0, height - 170 *
                          mm, f"Empresa: {nome_empresa}")

    data_atual = datetime.datetime.now().strftime('%d/%m/%Y')
    pdf.setFont("Helvetica", 12)
    pdf.drawCentredString(width / 2.0, height - 190 *
                          mm, f"Data: {data_atual}")

    pdf.showPage()


def desenhar_grafico_faturamento(pdf, dados, titulo, y_position):
    try:
        datas = []
        valores = []
        for item in dados:
            data_value = item.get('data') or item.get(
                'data_faturamento') or item.get('mes')
            total_faturado = item.get('total_faturado') or item.get('total')

            if data_value and total_faturado is not None:
                # Processar data
                if isinstance(data_value, datetime.date):
                    data_str = data_value.strftime('%Y-%m')
                else:
                    data_str = str(data_value)
                datas.append(data_str)
                valores.append(float(total_faturado))

        if not datas or not valores:
            return y_position

        plt.figure(figsize=(6, 4))
        plt.plot(datas, valores, marker='o')
        plt.title(titulo)
        plt.xlabel('Mês')
        plt.ylabel('Faturamento (R$)')
        plt.xticks(rotation=0)
        plt.tight_layout()

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')
        img_buffer.seek(0)
        plt.close()

        pdf.drawImage(ImageReader(img_buffer), 15 * mm,
                      y_position, width=180 * mm, height=70 * mm)
        y_position -= 100  # Ajustar a posição Y para o próximo gráfico
        return y_position

    except Exception as e:
        print(f"Erro ao desenhar gráfico de faturamento: {e}")
        return y_position
