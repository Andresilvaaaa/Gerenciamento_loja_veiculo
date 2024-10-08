import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
# from flask.wrappers import Response
from flask_cors import CORS
from mysql.connector import Error
import mysql.connector
from flask import Flask, request, jsonify, render_template, make_response
from flask import url_for, flash, redirect, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import set_access_cookies, unset_jwt_cookies
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
# from reportlab.lib.utils import ImageReader
# import matplotlib.pyplot as plt
from io import BytesIO
from flask import session
# from enviar_wathsapp import enviar_arquivo_via_whatsapp
# from threading import Thread
from desenhar_fatura import desenhar_fatura
from desenhar_dashboard import desenhar_dashboard
import json
from reportlab.lib.pagesizes import A4
from enviar_email import enviar_email, enviar_email_pos_fatura
# from werkzeug.utils import secure_filename
# import smtplib
# from enviar_wathsapp import iniciar_envio
import time

load_dotenv()

app = Flask(__name__)
# CORS(app)
CORS(app, supports_credentials=True)

# Definir a chave secreta

# app.config["JWT_TOKEN_LOCATION"] = [
#     "headers", "cookies", "json", "query_string"]
# app.config["JWT_COOKIE_SECURE"] = False
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')  # Chave secreta do JWT
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # Deve ser True em produção (HTTPS)
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.secret_key = os.getenv('APP_SECRET_KEY')

jwt = JWTManager(app)


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            return connection, None
    except Error as e:
        return None, f"DB_CONNECTION_ERROR: {str(e)}"


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, _jwt_payload):
    # Redireciona diretamente para a página de login ao invés de retornar JSON
    return redirect(url_for('index')), 302


@app.route('/confirme_login', methods=['POST'])
def confirme_login():
    try:
        confirme_login_data = request.get_json()
        identifier = confirme_login_data.get('identifier')
        senha = confirme_login_data.get('password')

    except Exception as e:
        print(f"Erro ao interpretar JSON: {str(e)}")  # Log do erro
        return jsonify({"Erro": f"API_JSON_PARSE_ERROR: {str(e)}",
                        "stage": "JSON Parsing"}), 400

    # identifier = confirme_login_data.get('identifier')
    # senha = confirme_login_data.get('password')

    if not identifier or not senha:
        print("Erro de validação: Username ou senha ausentes")  # Log do erro
        return jsonify({
            "message": "API_VALIDATION_ERROR: Username e senha obrigatórios.",
            "stage": "API Validation"}), 400

    connection, conn_error = get_db_connection()
    if not connection:
        return jsonify({"message": f"{conn_error}", "stage":
                        "Database Connection"}), 500

    cursor = connection.cursor()

    try:
        # Chamando a procedure com o identificador e senha
        cursor.callproc('confirme_login', [identifier, senha])

        # Captura o resultado da stored procedure
        for result in cursor.stored_results():
            output = result.fetchone()  # Captura a primeira linha do resultado

        connection.commit()

        user_found, senha_correta = output[0], output[1]

        if user_found and senha_correta:  # Altere para sua lógica de validação
            access_token = create_access_token(identity=identifier)

            # Crie a resposta JSON usando make_response
            response = make_response(jsonify({
                "message": "Login bem-sucedido",
                "stage": "Login Success"
            }))

            # Define o token JWT como cookie
            set_access_cookies(response, access_token)

            # Define o código de status como 200
            response.status_code = 200

            return response
        else:
            # Log do erro de usuário não encontrado
            print("Usuário não encontrado")
            return jsonify({"message": "Usuário não encontrado",
                            "stage": "Login Failed"}), 404

    except mysql.connector.Error as err:
        return jsonify({"message": f"SQL_QUERY_ERROR: {str(err)}",
                        "stage": "Query Execution"}), 500

    except Exception as e:
        return jsonify({"message": f"UNKNOWN_ERROR: {str(e)}",
                        "stage": "Unknown"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/consult_user', methods=['POST'])
def consulta_usuario():
    try:
        data = request.get_json()
    except Exception as e:
        return jsonify({"Erro": f"API_JSON_PARSE_ERROR: {str(e)}",
                        "stage": "JSON Parsing"}), 400

    username = data.get('username')
    fullname = data.get('full_name')
    email = data.get('email')
    password = data.get('new_password')
    cellphone = data.get('cellphone')

    # Obtendo data, hora e IP
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    user_ip = request.remote_addr  # Obtém o IP do usuário que fez a requisição

    if not username or not fullname:
        return jsonify({
            "message": "API_VALIDATION_ERROR: Username ou nome completo.",
            "stage": "API Validation"}), 400

    connection, conn_error = get_db_connection()

    if not connection:
        return jsonify({"message": f"{conn_error}",
                        "stage": "Database Connection"}), 500

    cursor = connection.cursor()

    try:
        cursor.callproc('consulta_usuario', [username, fullname, email,
                                             current_date, current_time,
                                             user_ip, cellphone, password])

        # Captura o resultado da stored procedure
        for result in cursor.stored_results():
            output = result.fetchone()

        connection.commit()

        if output and output[0] == 1:  # Verifica se o resultado é verdadeiro
            return jsonify({
                "message": f"Usuário {username} processados com sucesso.",
                "stage": "Stored Procedure Execution"}), 200
        else:
            return jsonify({
                "message": "Falha ao processar usuário via stored procedure.",
                "stage": "Stored Procedure Execution"}), 400

    except mysql.connector.Error as err:
        if err.errno == 1062:
            message = f"SQL_QUERY_ERROR: Usuário '{username}' já existe."
        else:
            message = f"SQL_QUERY_ERROR: {str(err)}"
        return jsonify({"message": message, "stage": "Query Execution"}), 500

    except Exception as e:
        return jsonify({"message": f"UNKNOWN_ERROR: {str(e)}",
                        "stage": "Unknown"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/')
def index():
    print("Rota / (INDEX) foi acessada")
    return render_template('index.html')


@app.route('/contato')
def contato():
    print("Rota / (CONTATO) foi acessada")
    return render_template('contato.html')


@app.route('/quem_somos')
def quem_somos():
    print("Rota / (QUEM SOMOS) foi acessada")
    return render_template('quem_somos.html')


@app.route('/cadastrando')
def cadastrando():
    print("Rota / (CADASTRANDO) foi acessada")
    return render_template('cadastrando.html')


@app.route('/pagina_logada', methods=['GET'])
@jwt_required(locations=["cookies"])
def pagina_logada():
    current_user = get_jwt_identity()
    return render_template('pagina_logada.html', username=current_user)


@app.route("/logout", methods=["POST"])
# Garante que o token JWT seja lido dos cookies
# @jwt_required(locations=["cookies"])
def logout():
    response = jsonify({"msg": "Logout realizado com sucesso"})
    unset_jwt_cookies(response)  # Remove o JWT do cookie
    return response, 200


@app.route('/home', methods=['GET'])
@jwt_required(locations=["cookies"])
def home():
    current_user = get_jwt_identity()
    return render_template('home.html', username=current_user)


# @app.route('/dashboard', methods=['GET'])
# @jwt_required(locations=["cookies"])
# def dashboard():
#     current_user = get_jwt_identity()
#     return render_template('dashboard.html', username=current_user)


@app.route('/services', methods=['GET'])
@jwt_required(locations=["cookies"])
def services():
    current_user = get_jwt_identity()
    return render_template('services.html', username=current_user)


@app.route('/minha_conta', methods=['GET'])
@jwt_required(locations=["cookies"])
def minha_conta():
    current_user = get_jwt_identity()
    return render_template('minha_conta.html', username=current_user)


@app.route('/clientepf', methods=['GET'])
@jwt_required(locations=["cookies"])
def clientepf():
    current_user = get_jwt_identity()
    print("Rota / (clientepf) foi acessada")
    return render_template('cliente_pf.html', username=current_user)


# @app.route('/clientepj', methods=['GET'])
# @jwt_required(locations=["cookies"])
# def clientepj():
#     current_user = get_jwt_identity()
#     return render_template('cliente_pj.html', username=current_user)


@app.route('/Veiculo', methods=['GET'])
@jwt_required(locations=["cookies"])
def Veiculo():
    current_user = get_jwt_identity()
    return render_template('veiculo.html', username=current_user)


@app.route('/feedback', methods=['GET'])
@jwt_required(locations=["cookies"])
def feedback():
    current_user = get_jwt_identity()
    return render_template('feedback.html', username=current_user)


@app.route('/cadastro_clientepf', methods=['POST'])
# @jwt_required()
@jwt_required(locations=["cookies"])
def cadastro_clientepf():
    try:
        current_user = get_jwt_identity()
        # Log para verificar o usuário autenticado
        print(f"Usuário autenticado: {current_user}")

        data = request.get_json()

        print("Dados recebidos na API:", data)  # Log dos dados recebidos
        print("Rota / (cadastro_clientepf) foi acessada")
    except Exception as e:
        return jsonify({"Erro": f"API_JSON_PARSE_ERROR: {str(e)}",
                        "stage": "JSON Parsing"}), 400

    nome = data.get('nome')
    cpf = data.get('cpf')
    genero = data.get('genero')
    estadocivil = data.get('estadocivil')
    dataNascimento = data.get('dataNascimento')
    telefone = data.get('telefone')
    email = data.get('email')
    estado = data.get('estado')
    cidade = data.get('cidade')
    bairro = data.get('bairro')
    endereco = data.get('endereco')
    complemento = data.get('complemento')

    # Obtendo data, hora e IP
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    user_ip = request.remote_addr

    if not nome or not cpf:
        return jsonify({
            "message": "API_VALIDATION_ERROR: Username ou nome completo.",
            "stage": "API Validation"}), 400

    connection, conn_error = get_db_connection()

    if not connection:
        return jsonify({"message": f"{conn_error}",
                        "stage": "Database Connection"}), 500

    cursor = connection.cursor()

    try:
        cursor.callproc('cadastro_clientepf', [
            cpf,             # p_cpf
            nome,            # p_nome_completo
            genero,          # p_genero
            estadocivil,     # p_estadocivil
            dataNascimento,  # p_dataNascimento
            current_date,    # p_data_cadastro
            current_time,    # p_hora_cadastro
            user_ip,         # p_ip_cadastro
            email,           # p_email
            telefone,        # p_num_celular
            endereco,        # p_endereco
            bairro,          # p_bairro
            cidade,          # p_cidade
            complemento,     # p_complemento
            estado,          # p_estado
            current_user
        ])

        # Captura o resultado da stored procedure
        for result in cursor.stored_results():
            output = result.fetchone()

        connection.commit()

        if output and output[0] == 1:  # Verifica se o resultado é verdadeiro
            return jsonify({
                "message": f"Usuário {cpf} processados com sucesso.",
                "stage": "Stored Procedure Execution"}), 200
        else:
            return jsonify({
                "message": "Falha ao processar usuário via stored procedure.",
                "stage": "Stored Procedure Execution"}), 400

    except mysql.connector.Error as err:
        print(f"Erro MySQL: {err}")  # Log para capturar o erro exato do MySQL
        if err.errno == 1062:
            message = f"Erro 1 SQL_QUERY_ERROR: Usuário '{cpf}' já existe."
        else:
            message = f"Erro 2 SQL_QUERY_ERROR: {str(err)}"
        return jsonify({"message": message, "stage": "Query Execution"}), 500

    except Exception as e:
        return jsonify({"message": f"UNKNOWN_ERROR: {str(e)}",
                        "stage": "Unknown"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/cadastro_veiculos', methods=['POST'])
@jwt_required(locations=["cookies"])
def cadastrar_veiculo():
    try:
        current_user = get_jwt_identity()
        # Log para verificar o usuário autenticado
        print(f"Usuário autenticado: {current_user}")

        data = request.get_json()

        print("Dados recebidos na API:", data)  # Log dos dados recebidos
        print("Rota / (cadastro_veiculos) foi acessada")
    except Exception as e:
        return jsonify({"Erro": f"API_JSON_PARSE_ERROR: {str(e)}",
                        "stage": "JSON Parsing"}), 400

    categoria = data.get('categoria')
    marca = data.get('marca')
    estado = data.get('estado')
    ano_fabricacao = data.get('anoFabricacao')
    ano_modelo = data.get('ano_modelo')
    renavam = data.get('renavam')
    numero_chassi = data.get('numeroChassi')
    modelo = data.get('modelo')
    cor = data.get('cor')
    placa = data.get('placa')
    preco_aquisicao = data.get('precoAquisicao')
    laudo_cautelar = data.get('laudoCautelar')
    procedencia = data.get('procedencia')
    disponibilidade = data.get('disponibilidade')
    print(type(preco_aquisicao))

    # Obtendo data, hora e IP
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    user_ip = request.remote_addr

    if not renavam:
        return jsonify({
            "message": "API_VALIDATION_ERROR: Renavam Invalido ou Ausente!.",
            "stage": "API Validation"}), 400

    connection, conn_error = get_db_connection()

    if not connection:
        return jsonify({"message": f"{conn_error}",
                        "stage": "Database Connection"}), 500

    cursor = connection.cursor()

    try:
        print(f"Valores para a procedure: categoria={categoria}"
              f"marca={marca}, estado={estado}",
              f"ano_fabricacao={ano_fabricacao}",
              f"ano_modelo={ano_modelo}, renavam={renavam}",
              f"numero_chassi={numero_chassi}, modelo={modelo}",
              f"cor={cor}, placa={placa}",
              f"preco_aquisicao={preco_aquisicao}",
              f"laudo_cautelar={laudo_cautelar}",
              f"procedencia={procedencia}, data={current_date}",
              f"hora={current_time}, ip={user_ip}")

        cursor.callproc('cadastrar_veiculo', [
            renavam,
            numero_chassi,         # Número do chassi
            modelo,                # Modelo
            cor,                   # Cor
            placa,                 # Placa
            preco_aquisicao,       # Preço de aquisição
            laudo_cautelar,        # Laudo Cautelar
            marca,                 # Marca
            procedencia,           # Procedência
            ano_fabricacao,        # Ano de fabricação
            ano_modelo,            # Ano do modelo
            estado,                # Estado
            categoria,
            current_date,          # Data de cadastro
            current_time,          # Hora de cadastro
            user_ip,               # IP de cadastro
            current_user,           # Responsável pelo cadastro
            disponibilidade
        ])

        # Captura o resultado da stored procedure
        for result in cursor.stored_results():
            output = result.fetchone()

        connection.commit()

        if output and output[0] == 1:  # Verifica se o resultado é verdadeiro
            return jsonify({"message": "Veículo cadastrado com sucesso!"}), 200
        else:
            return jsonify({
                "message": "Falha ao processar usuário via stored procedure.",
                "stage": "Stored Procedure Execution"}), 400

    except mysql.connector.Error as err:
        print(f"Erro MySQL: {err}")  # Log para capturar o erro exato do MySQL
        if err.errno == 1062:
            message = f"Erro 1 SQL_QUERY_ERROR: renavam '{
                renavam}' já cadastrado."
        else:
            message = f"Erro 2 SQL_QUERY_ERROR: {str(err)}"
        return jsonify({"message": message, "stage": "Query Execution"}), 500

    except Exception as e:
        return jsonify({"message": f"UNKNOWN_ERROR: {str(e)}",
                        "stage": "Unknown"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/consultar_veiculos', methods=['POST'])
@jwt_required(locations=["cookies"])
def consultar_veiculos():
    cursor = None
    connection = None
    try:
        # Captura os filtros da requisição
        filtros = request.get_json()

        renavam = filtros.get('renavam', None)
        marca = filtros.get('marca', None)
        modelo = filtros.get('modelo', None)
        cor = filtros.get('cor', None)
        categoria = filtros.get('categoria', None)

        connection, conn_error = get_db_connection()
        if not connection:
            return jsonify({"message": f"{conn_error}",
                            "stage": "Database Connection"}), 500

        cursor = connection.cursor()

        # Chamando a procedure com os parâmetros de filtros
        cursor.callproc('consultar_veiculos', [
                        renavam, marca, modelo, cor, categoria])

        # Capturando os resultados da procedure
        veiculos = []
        for result in cursor.stored_results():
            rows = result.fetchall()
            for row in rows:
                veiculo = {
                    "renavam": row[0],
                    "marca": row[1],
                    "modelo": row[2],
                    "cor": row[3],
                    "categoria": row[4]
                }
                veiculos.append(veiculo)

        if veiculos:
            return jsonify({"veiculos": veiculos}), 200
        else:
            return jsonify({"message": "Nenhum veiculo encontrado"}), 404

    except mysql.connector.Error as err:
        app.logger.error(f"Erro no servidor ao consultar veículos: {err}")
        return jsonify({"message": f"Erro no servidor: {str(err)}"}), 500

    except Exception as e:
        app.logger.error(f"Erro desconhecido: {e}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/consultar_cliente', methods=['POST'])
@jwt_required(locations=["cookies"])
def consultar_cliente():
    try:
        # Captura os filtros da requisição
        filtros = request.get_json()

        cpf = filtros.get('cpf', None)
        nome_completo = filtros.get('nome_completo', None)
        email = filtros.get('email', None)
        cidade = filtros.get('cidade', None)

    except Exception as e:
        print(f"Erro ao interpretar JSON: {str(e)}")  # Log do erro
        return jsonify({"Erro": f"API_JSON_PARSE_ERROR: {str(e)}",
                        "stage": "JSON Parsing"}), 400

    connection, conn_error = get_db_connection()
    if not connection:
        return jsonify({"message": f"{conn_error}",
                        "stage": "Database Connection"}), 500

    cursor = connection.cursor()

    try:
        # Chamando a procedure com os parâmetros de filtros
        print(f"Parâmetros recebidos: cpf={cpf}, nome_completo={
              nome_completo}, email={email}, cidade={cidade}")
        cursor.callproc('consultar_cliente', [
                        cpf, nome_completo, email, cidade])

        # Capturando os resultados da procedure
        clientes = []
        for result in cursor.stored_results():
            rows = result.fetchall()  # Captura todas as linhas
            for row in rows:
                cliente = {
                    "cpf": row[0],
                    "nome_completo": row[1],
                    "telefone": row[2],
                    "email": row[3],
                    "cidade": row[4]
                }
                clientes.append(cliente)

        connection.commit()

        if clientes:
            return jsonify({"clientes": clientes}), 200
        else:
            return jsonify({"message": "Nenhum cliente encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"message": f"SQL_QUERY_ERROR: {str(err)}",
                        "stage": "Query Execution"}), 500

    except Exception as e:
        return jsonify({"message": f"UNKNOWN_ERROR: {str(e)}",
                        "stage": "Unknown"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/faturamento', methods=['POST'])
@jwt_required(locations=["cookies"])
def faturamento():
    try:
        data = request.get_json()
        renavam = data.get('renavam')
        cpf = data.get('cpf')

        if not renavam or not cpf:
            return jsonify({"message": "Dados inválidos."}), 400

        # Armazenar os dados na sessão
        session['faturamento_data'] = {
            'renavam': renavam,
            'cpf': cpf
        }

        return jsonify({
            "message": "Dados de faturamento armazenados com sucesso."}), 200

    except Exception as e:
        app.logger.error(f"Erro ao definir dados de faturamento: {e}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500


@app.route('/faturamento', methods=['GET'])
@jwt_required(locations=["cookies"])
def faturamento_page():
    current_user = get_jwt_identity()
    faturamento_data = session.get('faturamento_data')

    if faturamento_data:
        # Busque o cliente e o veículo no banco de dados, CPF e RENAVAM
        connection, conn_error = get_db_connection()
        if conn_error:
            return jsonify({"message":
                            f"Erro na conexão com o banco de dados: {
                                conn_error}"}), 500

        cursor = connection.cursor(dictionary=True)

        try:
            # Buscar o cliente
            cursor.callproc('obter_cliente_por_cpf', [faturamento_data['cpf']])

            for result in cursor.stored_results():
                cliente = result.fetchone()

            if not cliente:
                return jsonify({"message": "Cliente não encontrado"}), 404

            # Buscar o veículo
            cursor.callproc('obter_veiculo_por_renavam', [
                            faturamento_data['renavam']])
            veiculo = None
            for result in cursor.stored_results():
                veiculo = result.fetchone()

            if not veiculo:
                return jsonify({"message": "Veículo não encontrado"}), 404

            # # Verificar se o veículo está disponível
            # if veiculo['disponibilidade'] != 'disponível':
            #     return jsonify({"message":
            #                     "Veículo já vendido ou indisponível"}), 400

            # Verificar se o veículo está disponível
            if veiculo['disponibilidade'] != 'disponível':
                flash("Veículo já vendido ou indisponível", "warning")
                # Redirecionar para a lista de veículos disponíveis
                return redirect(url_for('listar_veiculos'))

            # Renderizar a página com os dados do cliente e veículo
            return render_template('faturamento.html', username=current_user,
                                   cliente=cliente, veiculo=veiculo)

        except Exception as e:
            app.logger.error(f"Erro ao buscar cliente ou veículo: {e}")
            return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

        finally:
            cursor.close()
            connection.close()

    else:
        return jsonify({"message":
                        "Dados de faturamento não encontrados"}), 400


@app.route('/gerar_fatura', methods=['POST'])
@jwt_required(locations=["cookies"])
def gerar_fatura():
    try:
        data = request.get_json()
        cliente_data = data.get('cliente')
        veiculo_data = data.get('veiculo')
        detalhes_fatura = data.get('detalhesFatura')

        if not cliente_data or not veiculo_data or not detalhes_fatura:
            return jsonify({"message": "Dados incompletos."}), 400

        # Obter a data atual
        data_cadastro = datetime.now().date()
        hora_cadastro = datetime.now().time()

        # Conexão com o banco de dados
        connection, conn_error = get_db_connection()
        if not connection:
            return jsonify({"message": f"{
                conn_error}", "stage": "Conexão com o Banco de Dados"}), 500

        cursor = connection.cursor()

        # Montar os produtos
        produtos = [
            {
                "nome": f"{veiculo_data['marca']} {veiculo_data['modelo']}",
                "quantidade": float(detalhes_fatura['quantidade']),
                "unidade": "unidade",
                "preco_unitario": float(detalhes_fatura['preco_unitario'])
            }
        ]

        # Cálculo do valor total da fatura
        valor_total = sum(
            produto['quantidade'] * produto[
                'preco_unitario'] for produto in produtos
        )

        # Dados de cadastro da fatura
        ip_cadastro = request.remote_addr  # IP da requisição
        current_user = get_jwt_identity()

        # Recuperar o renavam da sessão
        faturamento_data = session.get('faturamento_data')
        if not faturamento_data or 'renavam' not in faturamento_data:
            # if not faturamento_data or not faturamento_data:
            return jsonify({"message":
                            "Dados de faturamento não encontrados na sessão."
                            }), 400

        renavam = faturamento_data['renavam']

        # Chamar a stored procedure para vender o veículo e cadastrar a fatura
        cursor.callproc('vender_veiculo_e_cadastrar_fatura', [
            cliente_data['cpf'],         # CPF do cliente
            renavam,                     # Renavam do veículo
            data_cadastro,               # Data de cadastro
            hora_cadastro,               # Hora de cadastro
            valor_total,                 # Valor total da fatura
            ip_cadastro,                 # IP de cadastro
            current_user                 # Responsável pelo cadastro
        ])

        # Capturar o resultado da stored procedure
        numero_fatura = None
        nome_fatura = None
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                numero_fatura = row[0]  # numero_fatura
                nome_fatura = row[1]    # nome_fatura

        if not numero_fatura or not nome_fatura:
            return jsonify({"message": "Erro ao obter dados da fatura."}), 500

        # Buscar os dados completos do cliente a partir do CPF
        cursor.callproc('obter_dados_cliente', [cliente_data['cpf']])

        # Capturar os dados completos do cliente
        cliente_completo = None
        for result in cursor.stored_results():
            cliente_completo = result.fetchone()

        if not cliente_completo:
            return jsonify({"message": "Cliente não encontrado."}), 404

        # Montar os dados do cliente
        cliente = {
            "codigo": cliente_data['cpf'],
            "nome": cliente_completo[0],
            "endereco": cliente_completo[1],
            "telefone": cliente_completo[2],
            "email": cliente_completo[3]
        }

        # Diretório para salvar o PDF
        pdf_dir = os.path.join(os.getcwd(), 'pdfs')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)
        pdf_path = os.path.join(pdf_dir, nome_fatura)

        # Gerar o PDF em memória
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Usar o numero_fatura correto ao desenhar o PDF
        desenhar_fatura(pdf, cliente, produtos, numero_fatura)

        pdf.showPage()
        pdf.save()

        # Salvar o PDF
        with open(pdf_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        pdf_buffer.seek(0)

        # Limpar dados de faturamento da sessão
        session.pop('faturamento_data', None)

        print({
            "message": "Fatura gerada com sucesso",
            "nome_fatura": nome_fatura
        }), 200

        app.logger.info(f"Nome da fatura gerado: {nome_fatura}")
        app.logger.info(f"Caminho do PDF: {pdf_path}")

        # Chamada para enviar o e-mail
        destinatario = cliente['email']
        assunto = f"Fatura #{numero_fatura} - {cliente['nome']}"
        corpo_mensagem = "Segue em anexo a fatura AGEVEC."

        # Anexar o arquivo gerado no e-mail
        sucesso_envio = enviar_email_pos_fatura(
            destinatario=destinatario,
            assunto=assunto,
            mensagem=corpo_mensagem,
            anexos=[{"caminho": pdf_path, "nome": nome_fatura}]
        )

        if not sucesso_envio:
            return jsonify({
                "message": f"Erro ao enviar e-mail para: {destinatario}"}), 500

        return jsonify({
            "message": "Fatura gerada e enviada com sucesso",
            "nome_fatura": nome_fatura
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao gerar fatura: {e}, Dados Recebidos: {data}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/dashboard', methods=['GET'])
@jwt_required(locations=["cookies"])
def dashboard():
    current_user = get_jwt_identity()
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    # Se as datas não forem fornecidas, usar um período padrão
    if not data_inicio or not data_fim:
        data_fim = datetime.today().strftime('%Y-%m-%d')
        data_inicio = (datetime.today() - timedelta(days=30)
                       ).strftime('%Y-%m-%d')

    app.logger.info(f"Usuário: {
        current_user} acessou o dashboard com período de {
        data_inicio} até {data_fim}")

    try:
        # Conectar ao banco de dados
        connection, conn_error = get_db_connection()
        if conn_error:
            app.logger.error(
                f"Erro na conexão com o banco de dados: {conn_error}")
            return jsonify({
                "message": f"Erro na conexão com o banco de dados: {
                    conn_error}"}), 500

        cursor = connection.cursor(dictionary=True)
        app.logger.info("Conexão com o banco de dados estabelecida.")

        # Total de carros vendidos no período
        cursor.callproc('obter_total_vendidos_periodo',
                        [data_inicio, data_fim])
        total_vendidos = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_vendidos = row['total']
        app.logger.info(f"Total de carros vendidos no período: {
                        total_vendidos}")

        # Total de carros disponíveis
        cursor.callproc('obter_total_disponiveis')
        total_disponiveis = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_disponiveis = row['total']
        app.logger.info(f"Total de carros disponíveis: {total_disponiveis}")

        # Clientes Ativos
        cursor.callproc('obter_total_clientes_ativos')
        total_clientes_ativos = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_clientes_ativos = row['total_clientes_ativos']
        app.logger.info(f"Total de clientes ativos: {total_clientes_ativos}")

        # Faturamento por Dia
        cursor.callproc('obter_faturamento_por_dia', [data_inicio, data_fim])
        faturamento_por_dia = []
        for result in cursor.stored_results():
            faturamento_por_dia.extend(result.fetchall())
        app.logger.info(f"Faturamento por dia: {faturamento_por_dia}")

        # Faturamento por Mês
        cursor.callproc('obter_faturamento_por_mes', [data_inicio, data_fim])
        faturamento_por_mes = []
        for result in cursor.stored_results():
            faturamento_por_mes.extend(result.fetchall())
        app.logger.info(f"Faturamento por mês: {faturamento_por_mes}")

        # Obter vendas por data
        cursor.callproc('obter_vendas_por_data', [data_inicio, data_fim])
        vendas_por_data = []
        for result in cursor.stored_results():
            vendas_por_data.extend(result.fetchall())
        app.logger.info(f"Vendas por data: {vendas_por_data}")

        # Obter vendas detalhadas
        cursor.callproc('obter_vendas_detalhadas', [data_inicio, data_fim])
        vendas_detalhadas = []
        for result in cursor.stored_results():
            vendas_detalhadas.extend(result.fetchall())
        app.logger.info(f"Vendas detalhadas: {vendas_detalhadas}")

        # Vendas por Estado
        cursor.callproc('obter_vendas_por_estado', [data_inicio, data_fim])
        vendas_por_estado = []
        for result in cursor.stored_results():
            vendas_por_estado.extend(result.fetchall())
        app.logger.info(f"Vendas por estado: {vendas_por_estado}")

        # Obter vendas por vendedor
        cursor.callproc('obter_vendas_por_vendedor', [data_inicio, data_fim])
        vendas_por_vendedor = []
        for result in cursor.stored_results():
            vendas_por_vendedor.extend(result.fetchall())
        app.logger.info(f"Vendas por vendedor: {vendas_por_vendedor}")

        # Faturamento Total
        cursor.callproc('obter_faturamento_total')
        total_faturamento = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_faturamento = row['total_faturamento']
        app.logger.info(f"Total de faturamento: {total_faturamento}")

        # Renderizar o template com os dados e incluir logs de cada variável
        app.logger.info(
            "Preparando para renderizar o template com os seguintes dados:")
        app.logger.info(f"Total Vendidos: {
            total_vendidos}, Total Disponíveis: {
            total_disponiveis}, Clientes Ativos: {
            total_clientes_ativos}")
        app.logger.info(f"Faturamento por Dia: {
                        faturamento_por_dia}, Faturamento por Mês: {
                            faturamento_por_mes}")
        app.logger.info(f"Vendas por Data: {
                        vendas_por_data}, Vendas Detalhadas: {
                            vendas_detalhadas}")
        app.logger.info(f"Vendas por Estado: {
                        vendas_por_estado}, Vendas por Vendedor: {
                            vendas_por_vendedor}")

        return render_template('dashboard.html', username=current_user,
                               total_vendidos=total_vendidos,
                               total_disponiveis=total_disponiveis,
                               vendas_por_data=vendas_por_data,
                               vendas_detalhadas=vendas_detalhadas,
                               vendas_por_vendedor=vendas_por_vendedor,
                               data_inicio=data_inicio,
                               data_fim=data_fim,
                               total_clientes_ativos=total_clientes_ativos,
                               total_faturamento=total_faturamento,
                               #    faturamento_por_dia=faturamento_por_dia,
                               #    faturamento_por_mes=faturamento_por_mes,
                               faturamento_por_dia=json.dumps(
                                   faturamento_por_dia, default=str),
                               faturamento_por_mes=json.dumps(
                                   faturamento_por_mes, default=str),
                               #    vendas_por_estado=vendas_por_estado,
                               vendas_por_estado=json.dumps(
                                   vendas_por_estado, default=str),

                               )
    except Exception as e:
        app.logger.error(f"Erro ao gerar dados do dashboard: {e}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/gerar_relatorio_dashboard', methods=['GET'])
@jwt_required(locations=["cookies"])
def gerar_relatorio_dashboard():
    current_user = get_jwt_identity()
    data_inicio = request.args.get('dataInicio')
    data_fim = request.args.get('dataFim')

    # Se as datas não forem fornecidas, usar um período padrão
    if not data_inicio or not data_fim:
        data_fim = datetime.today().strftime('%Y-%m-%d')
        data_inicio = (datetime.today() - timedelta(days=30)
                       ).strftime('%Y-%m-%d')

    app.logger.info(f"Usuário: {
        current_user} solicitou a geração do relatório com período de {
        data_inicio} até {data_fim}")

    try:
        # Conectar ao banco de dados
        connection, conn_error = get_db_connection()
        if conn_error:
            app.logger.error(
                f"Erro na conexão com o banco de dados: {conn_error}")
            return jsonify({
                "message": f"Erro na conexão com o banco de dados: {
                    conn_error}"}), 500

        cursor = connection.cursor(dictionary=True)
        app.logger.info(
            "Conexão com o banco de dados estabelecida para relatório.")

        # Obter os dados do dashboard
        cursor.callproc('obter_total_vendidos_periodo',
                        [data_inicio, data_fim])
        total_vendidos = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_vendidos = row['total']

        cursor.callproc('obter_total_disponiveis')
        total_disponiveis = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_disponiveis = row['total']

        cursor.callproc('obter_total_clientes_ativos')
        total_clientes_ativos = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_clientes_ativos = row['total_clientes_ativos']

        cursor.callproc('obter_faturamento_por_dia', [data_inicio, data_fim])
        faturamento_por_dia = []
        for result in cursor.stored_results():
            faturamento_por_dia.extend(result.fetchall())

        cursor.callproc('obter_faturamento_por_mes', [data_inicio, data_fim])
        faturamento_por_mes = []
        for result in cursor.stored_results():
            faturamento_por_mes.extend(result.fetchall())

        cursor.callproc('obter_vendas_por_estado', [data_inicio, data_fim])
        vendas_por_estado = []
        for result in cursor.stored_results():
            vendas_por_estado.extend(result.fetchall())

        cursor.callproc('obter_faturamento_total')
        total_faturamento = 0
        for result in cursor.stored_results():
            row = result.fetchone()
            if row:
                total_faturamento = row['total_faturamento']

        # Obter vendas por vendedor
        cursor.callproc('obter_vendas_por_vendedor', [data_inicio, data_fim])
        vendas_por_vendedor = []
        for result in cursor.stored_results():
            vendas_por_vendedor.extend(result.fetchall())

        app.logger.info(f"Dados de vendas_por_vendedor: {vendas_por_vendedor}")
        if vendas_por_vendedor:
            app.logger.info(f"Chaves disponíveis em vendas_por_vendedor[0]: {
                            vendas_por_vendedor[0].keys()}")

        # Clientes Ativos com detalhes
        cursor.callproc('obter_clientes_ativos_detalhes')
        clientes_ativos_detalhes = []
        for result in cursor.stored_results():
            clientes_ativos_detalhes.extend(result.fetchall())
        app.logger.info(f"Clientes ativos detalhes: {
                        clientes_ativos_detalhes}")

        cursor.callproc('obter_faturamento_por_mes', [data_inicio, data_fim])
        faturamento_por_mes = []
        for result in cursor.stored_results():
            faturamento_por_mes.extend(result.fetchall())
        app.logger.info(f"Faturamento por mês: {faturamento_por_mes}")

        dados_dashboard = {
            'total_vendidos': total_vendidos,
            'total_disponiveis': total_disponiveis,
            'total_clientes_ativos': total_clientes_ativos,
            'total_faturamento': total_faturamento,
            'faturamento_por_dia': faturamento_por_dia,
            'faturamento_por_mes': faturamento_por_mes,
            'vendas_por_estado': vendas_por_estado,
            'vendas_por_vendedor': vendas_por_vendedor,
            'clientes_ativos_detalhes': clientes_ativos_detalhes  # Adicionado
        }

        app.logger.info("Dados do dashboard coletados com sucesso.")

        # Diretório para salvar o PDF
        pdf_dir = os.path.join(os.getcwd(), 'dashboards')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Nome do arquivo PDF
        nome_relatorio = f"relatorio_dashboard_{
            datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf_path = os.path.join(pdf_dir, nome_relatorio)

        # Gerar o PDF com a função `desenhar_dashboard`
        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)

        # Passar o dicionário de dados e o nome da empresa para o relatório
        desenhar_dashboard(pdf, dados_dashboard, nome_empresa="AgeVec Motors")

        pdf.showPage()
        pdf.save()

        # Salvar o PDF no diretório especificado
        with open(pdf_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())

        pdf_buffer.seek(0)

        return jsonify({
            "message": "Relatório de dashboard gerado com sucesso.",
            "nome_relatorio": nome_relatorio
        }), 200

    except Exception as e:
        app.logger.error(f"Erro ao gerar o relatório do dashboard: {e}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/download_pdf', methods=['GET'])
def download_pdf():
    filename = request.args.get('filename')
    file_path = os.path.join(os.getcwd(), 'dashboards', filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"message": "Arquivo não encontrado."}), 404


@app.route('/consultar_cliente_documentos', methods=['POST'])
@jwt_required(locations=["cookies"])
def consultar_cliente_documentos():
    try:
        # Captura os filtros da requisição
        filtros = request.get_json()

        cpf = filtros.get('cpf', None)
        nome_completo = filtros.get('nome_completo', None)
        email = filtros.get('email', None)
        cidade = filtros.get('cidade', None)
        print(f"Parâmetros recebidos 00 : cpf={cpf}, nome_completo={
              nome_completo}, email={email}, cidade={cidade}")

    except Exception as e:
        print(f"Erro ao interpretar JSON: {str(e)}")  # Log do erro
        return jsonify({"Erro": f"API_JSON_PARSE_ERROR: {str(e)}",
                        "stage": "JSON Parsing"}), 400

    connection, conn_error = get_db_connection()
    if not connection:
        return jsonify({"message": f"{conn_error}",
                        "stage": "Database Connection"}), 500

    cursor = connection.cursor()

    try:
        # Chamando a procedure com os parâmetros de filtros
        print(f"Parâmetros recebidos: cpf={cpf}, nome_completo={
              nome_completo}, email={email}, cidade={cidade}")
        cursor.callproc('consultar_cliente', [
                        cpf, nome_completo, email, cidade])

        # Capturando os resultados da procedure
        clientes = []
        for result in cursor.stored_results():
            rows = result.fetchall()  # Captura todas as linhas
            for row in rows:
                cliente = {
                    "cpf": row[0],
                    "nome_completo": row[1],
                    "telefone": row[2],
                    "email": row[3],
                    "cidade": row[4]
                }
                clientes.append(cliente)

        connection.commit()

        if clientes:
            return jsonify({"clientes": clientes}), 200
        else:
            return jsonify({"message": "Nenhum cliente encontrado"}), 404

    except mysql.connector.Error as err:
        return jsonify({"message": f"SQL_QUERY_ERROR: {str(err)}",
                        "stage": "Query Execution"}), 500

    except Exception as e:
        return jsonify({"message": f"UNKNOWN_ERROR: {str(e)}",
                        "stage": "Unknown"}), 500

    finally:
        cursor.close()
        connection.close()


@app.route('/enviar_relatorio_email', methods=['POST'])
@jwt_required(locations=["cookies"])
def enviar_relatorio_email():
    try:
        # Certifique-se de que o arquivo foi recebido corretamente no request
        if 'arquivo' not in request.files:
            return jsonify({
                "message": "Arquivo não encontrado no request."}), 400

        arquivo = request.files['arquivo']
        # Os clientes são enviados como uma string JSON
        clientes = request.form.get('clientes')
        if not clientes:
            return jsonify({"message": "Nenhum cliente selecionado."}), 400

        # Converter de string para lista de dicionários
        clientes = json.loads(clientes)

        # Caminho onde o arquivo será salvo
        pdf_dir = os.path.join(os.getcwd(), 'pdfs')
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Salvar temporariamente o arquivo recebido
        caminho_arquivo = os.path.join(pdf_dir, arquivo.filename)
        arquivo.save(caminho_arquivo)

        # Esperar um momento para garantir que o arquivo foi salvo corretamente
        time.sleep(1)

        assunto = 'Relatório de Dashboard'
        corpo_mensagem = 'Segue em anexo o relatório solicitado.'

        # Enviar e-mails para cada cliente selecionado
        for cliente in clientes:
            # Modificar a chamada para enviar um único arquivo como anexo
            sucesso = enviar_email(
                cliente['email'], assunto, corpo_mensagem,
                anexo=caminho_arquivo)

            if not sucesso:
                return jsonify({
                    "message": f"Erro ao enviar e-mail para: {
                        cliente['email']}"}), 500

        return jsonify({"message": "E-mails enviados com sucesso."}), 200

    except Exception as e:
        app.logger.error(f"Erro ao enviar relatório: {e}")
        return jsonify({"message": f"Erro no servidor: {str(e)}"}), 500


@app.route('/enviar_documentos', methods=['GET'])
@jwt_required(locations=["cookies"])
def enviar_documentos():
    current_user = get_jwt_identity()
    return render_template('enviar_documentos.html', username=current_user)


if __name__ == '__main__':
    app.run(debug=True)
