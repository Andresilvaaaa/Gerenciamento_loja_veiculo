# 🚗 Sistema de Gestão de Veículos

Este projeto é um **sistema de gerenciamento de veículos** desenvolvido com **Flask** e **MySQL**, que permite o cadastro, consulta e venda de veículos, além de geração automática de faturas e relatórios. O sistema também realiza controle de usuários e clientes, além de exibir um dashboard com métricas de vendas e faturamento.

## 📋 Funcionalidades

- **Cadastro de Clientes**: Permite cadastrar clientes PF e PJ com dados detalhados.
- **Cadastro de Veículos**: Inclusão de veículos com características como marca, modelo, cor, e valor.
- **Consulta de Veículos e Clientes**: Realiza buscas filtradas por marca, estado, e outras características.
- **Controle de Vendas**: Geração de faturas, cálculo de valores e atribuição de vendedores responsáveis.
- **Dashboard**: Exibe gráficos e métricas de vendas, faturamento e desempenho dos vendedores.
- **Geração de Relatórios PDF**: Permite exportar relatórios de vendas e métricas para arquivos PDF.
- **Integração com E-mail**: Envia faturas e relatórios por e-mail.
- **Integração com WhatsApp**: Envio automatizado de documentos via WhatsApp.

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask, Flask-JWT-Extended
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Banco de Dados**: MySQL / MariaDB
- **Relatórios e PDFs**: ReportLab
- **Autenticação e Segurança**: JWT (JSON Web Tokens)
- **Integração**: PyWhatKit para envio de mensagens e PDFs via WhatsApp
- **Gerenciamento de Sessão**: Flask-Session

## ⚙️ Como Executar o Projeto Localmente

1. **Clone o repositório**:
   ```bash
  git clone https://github.com/seu-usuario/meu-projeto-flask.git

2. Navegue até o diretório do projeto:
  cd meu-projeto-flask
3. Crie um ambiente virtual e ative:
  python -m venv venv
  source venv/bin/activate  # Para Windows: venv\Scripts\activate
4. Instale as dependências:
  pip install -r requirements.txt
5. Crie um arquivo .env e defina as variáveis de ambiente:
Crie um arquivo chamado .env no diretório raiz do projeto e adicione as seguintes variáveis:
    FLASK_APP=app.py
    FLASK_ENV=development
    DB_HOST=localhost
    DB_USER=root
    DB_PASSWORD=sua_senha
    DB_NAME=banco_de_dados
    SECRET_KEY=sua_chave_secreta_flask
    APP_SECRET_KEY=sua_chave_secreta_aplicacao
6. Inicie o servidor Flask:
   flask run
7. Acesse o sistema no navegador:
   http://127.0.0.1:5000

🗂️ Estrutura de Diretórios
meu-projeto-flask/
├── app.py                     # Arquivo principal do Flask
├── .env                       # Arquivo de variáveis de ambiente
├── requirements.txt           # Dependências do projeto
├── enviar_email.py            # Módulo para envio de e-mails
├── enviar_wathsapp.py         # Módulo para integração com WhatsApp
├── desenhar_fatura.py         # Geração de faturas em PDF
├── templates/                 # Arquivos HTML para templates
│   ├── index.html
│   ├── dashboard.html
│   ├── cliente_pf.html
│   └── ...
├── static/                    # Arquivos estáticos como CSS e JavaScript
│   ├── dashboard.css
│   ├── chaticon.css
│   └── ...
├── pdfs/                      # Diretório para armazenar faturas e relatórios
└── dashboards/                # Diretório para relatórios gerados de dashboard

📈 Dashboard
O sistema inclui um dashboard interativo com gráficos que exibem as seguintes métricas:

Faturamento por Dia: Total de faturamento por dia no período selecionado.
Faturamento por Mês: Faturamento acumulado mês a mês.
Total de Vendas por Estado: Visualização de vendas por localização.
Top Vendedores: Ranking dos vendedores com maior volume de vendas.

🤝 Contribuições
Contribuições são bem-vindas! Se desejar colabore com o projeto! 

