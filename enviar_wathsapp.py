import pywhatkit as wapp
import pyautogui as pya
import time
# import os
# import pyperclip
# from flask import jsonify
import logging
from threading import Thread


# def enviar_arquivo_via_whatsapp(numero_telefone, caminho_arquivo):
#     mensagem = "Segue fatura referente a sua compra na AgeVec"
#     try:
#         if not numero_telefone.startswith('+'):
#             numero_telefone = '+' + '55' + numero_telefone

#         # Enviar a mensagem via WhatsApp
#         wapp.sendwhatmsg_instantly(numero_telefone, mensagem)
#         pya.sleep(4)
#         # time.sleep(5)

#         # Clique no ícone de anexar arquivo (posição da tela deve ser ajustada para o seu caso)
#         pya.click(x=2474, y=996)
#         pya.sleep(4)
#         # time.sleep(2)

#         # Clique para anexar documento (posição da tela deve ser ajustada para o seu caso)
#         pya.click(x=2590, y=746)
#         pya.sleep(4)
#         # time.sleep(3)

#         # # Digitar o caminho do arquivo e pressionar Enter
#         pya.write(caminho_arquivo)

#         # Copie o caminho do arquivo para a área de transferência
#         # pyperclip.copy(caminho_arquivo)

#         # Cole o caminho no WhatsApp
#         pya.hotkey('ctrl', 'v')

#         # time.sleep(3)
#         pya.sleep(4)
#         pya.press('enter')

#         # Esperar o envio do arquivo e a confirmação no WhatsApp
#         # time.sleep(3)
#         pya.sleep(4)
#         pya.press('enter')
#         # time.sleep(3)
#         pya.sleep(4)

#     except Exception as e:
#         logging.error(f"Erro ao enviar WhatsApp: {str(e)}", exc_info=True)
#         # jsonify(f"Erro ao enviar WhatsApp: {str(e)}", exc_info=True)


def enviar_fatura_whatsapp(numero_telefone, caminho_arquivo):
    try:
        if not numero_telefone.startswith('+'):
            numero_telefone = '+' + '55' + numero_telefone

        mensagem = "Segue fatura referente a sua compra na AgeVec."

        # Usar pywhatkit para enviar a mensagem instantaneamente
        wapp.sendwhatmsg_instantly(numero_telefone, mensagem)
        time.sleep(5)

        # Enviar o arquivo anexo via pyautogui
        pya.click(x=2474, y=996)
        time.sleep(3)
        pya.click(x=2590, y=746)
        time.sleep(3)
        pya.write(caminho_arquivo)
        pya.hotkey('ctrl', 'v')
        time.sleep(2)
        pya.press('enter')
        time.sleep(3)
        print(f"Fatura enviada para o WhatsApp: {numero_telefone}")
    except Exception as e:
        print(f"Erro ao enviar a fatura pelo WhatsApp: {str(e)}")

# Função que executa o envio do WhatsApp em uma nova thread


def iniciar_envio(numero_telefone, caminho_arquivo):
    thread = Thread(target=enviar_fatura_whatsapp,
                    args=(numero_telefone, caminho_arquivo))
    thread.start()
