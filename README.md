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

Backend:
Python: Linguagem de programação principal utilizada para implementar a lógica de negócios e operações do servidor.
Flask: Microframework utilizado para desenvolver a API e gerenciar as rotas do backend. Possui suporte a templates, gerenciamento de sessões e integração com diversos módulos.
Flask-JWT-Extended: Biblioteca utilizada para implementar autenticação baseada em JWT (JSON Web Tokens), oferecendo suporte completo para geração e verificação de tokens, armazenamento seguro em cookies e controle de permissões.

Frontend:
HTML: Estruturação e marcação das páginas web para exibir informações ao usuário.
CSS: Estilização visual das páginas, com personalização de cores, layouts e responsividade.
JavaScript: Adicionado para manipulação de eventos, validação de formulários, chamadas dinâmicas à API e navegação entre as páginas.
Bootstrap: Biblioteca front-end baseada em CSS e JavaScript para design responsivo, utilizada para criar componentes visuais como botões, cards, tabelas, modais e menus de navegação.

Banco de Dados:
MySQL / MariaDB: Sistemas de gerenciamento de banco de dados relacionais usados para armazenamento e recuperação de dados. Suporte a procedures e triggers para automatização de tarefas e consultas complexas.

Relatórios e Geração de PDFs:
ReportLab: Biblioteca de geração de documentos PDF em Python, usada para criar faturas e relatórios personalizados diretamente a partir dos dados do sistema, com gráficos, tabelas e layouts dinâmicos.

Autenticação e Segurança:
JWT (JSON Web Tokens): Utilizado para gerenciamento de autenticação e autorização, permitindo que as rotas sejam protegidas por tokens seguros e temporários, evitando acessos não autorizados.
Flask-Session: Gerenciamento de sessão para armazenar e compartilhar informações temporárias durante a navegação dos usuários, como dados de login e detalhes de operações.

Integração e Comunicação:
PyWhatKit: Biblioteca de automação para enviar mensagens e arquivos PDF pelo WhatsApp, utilizada para integração com serviços de comunicação e envio automatizado de relatórios e faturas para clientes.

Armazenamento de Configurações e Variáveis:
dotenv: Biblioteca utilizada para carregar variáveis de ambiente a partir de um arquivo .env, mantendo as credenciais e configurações de forma segura e fora do código-fonte.

Controle de Versão e Colaboração:
Git: Sistema de controle de versão utilizado para rastrear alterações no código, possibilitando colaboração em equipe e gerenciamento de versões.
GitHub: Plataforma de hospedagem de repositórios Git para compartilhamento do código, versionamento e controle de mudanças.

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

