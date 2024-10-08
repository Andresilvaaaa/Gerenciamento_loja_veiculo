import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()


def enviar_email(destinatario, assunto, mensagem, anexo=None):
    try:
        # Definindo as variáveis de configuração do e-mail a partir do .env
        email = os.getenv('EMAIL_HOST_USER')
        senha_do_email = os.getenv('EMAIL_HOST_PASSWORD')
        smtp_server = os.getenv('EMAIL_HOST')
        smtp_port = int(os.getenv('EMAIL_PORT'))

        # Verificar se todas as variáveis estão definidas
        if not email or not senha_do_email or not smtp_server or not smtp_port:
            print(
                "Erro: Variáveis de configuração de e-mail ausentes no arquivo .env.")
            print(f"EMAIL_HOST_USER: {email}, EMAIL_HOST_PASSWORD: {
                  '*******' if senha_do_email else None}, EMAIL_HOST: {
                      smtp_server}, EMAIL_PORT: {smtp_port}")
            return False

        # Exibir as variáveis carregadas para conferência ()
        print(f"Conectando ao servidor {smtp_server}:{
              smtp_port} com o usuário {email}.")

        # Configuração básica do e-mail
        msg = EmailMessage()
        msg['Subject'] = assunto
        msg['From'] = email
        msg['To'] = destinatario
        msg.set_content(mensagem)

        # Adicionar anexo, se fornecido
        if anexo:
            try:
                with open(anexo, 'rb') as file:
                    file_data = file.read()
                    file_name = os.path.basename(anexo)
                    msg.add_attachment(
                        file_data, maintype='application', subtype='octet-stream', filename=file_name)
                    print(f"Anexo '{file_name}' adicionado com sucesso.")
            except FileNotFoundError:
                print(f"Erro: Arquivo '{anexo}' não encontrado.")
                return False

        # Conectar ao servidor SMTP do Gmail e enviar o e-mail
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            try:
                smtp.login(email, senha_do_email)
                smtp.send_message(msg)
                print("E-mail enviado com sucesso!")
                return True
            except smtplib.SMTPAuthenticationError:
                print("Erro de autenticação! Verifique o e-mail e a senha.")
            except smtplib.SMTPException as e:
                print(f"Erro no servidor SMTP: {e}")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    return False


def enviar_email_pos_fatura(destinatario, assunto, mensagem, anexos=None):
    try:
        # Definindo as variáveis de configuração do e-mail a partir do .env
        email = os.getenv('EMAIL_HOST_USER')
        senha_do_email = os.getenv('EMAIL_HOST_PASSWORD')
        smtp_server = os.getenv('EMAIL_HOST')
        smtp_port = int(os.getenv('EMAIL_PORT'))

        # Verificar se todas as variáveis estão definidas
        if not email or not senha_do_email or not smtp_server or not smtp_port:
            print("Erro: Variáveis de configuração de e-mail ausentes no arquivo .env.")
            print(f"EMAIL_HOST_USER: {email}, EMAIL_HOST_PASSWORD: {
                  '*******' if senha_do_email else None}, EMAIL_HOST: {smtp_server}, EMAIL_PORT: {smtp_port}")
            return False

        # Exibir as variáveis carregadas para conferência
        print(f"Conectando ao servidor {smtp_server}:{
              smtp_port} com o usuário {email}.")

        # Configuração básica do e-mail
        msg = EmailMessage()
        msg['Subject'] = assunto
        msg['From'] = email
        msg['To'] = destinatario
        msg.set_content(mensagem)

        # Adicionar anexos, se fornecidos
        if anexos:
            for anexo in anexos:
                try:
                    with open(anexo["caminho"], 'rb') as file:
                        file_data = file.read()
                        file_name = anexo["nome"]
                        msg.add_attachment(
                            file_data, maintype='application', subtype='octet-stream', filename=file_name)
                        print(f"Anexo '{file_name}' adicionado com sucesso.")
                except FileNotFoundError:
                    print(f"Erro: Arquivo '{
                          anexo['caminho']}' não encontrado.")
                    return False

        # Conectar ao servidor SMTP do Gmail e enviar o e-mail
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            try:
                smtp.login(email, senha_do_email)
                smtp.send_message(msg)
                print("E-mail enviado com sucesso!")
                return True
            except smtplib.SMTPAuthenticationError:
                print("Erro de autenticação! Verifique o e-mail e a senha.")
            except smtplib.SMTPException as e:
                print(f"Erro no servidor SMTP: {e}")

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
    return False
