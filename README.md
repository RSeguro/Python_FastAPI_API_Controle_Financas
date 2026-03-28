
# 🚀API de Controle de Finanças (FastAPI)

Olá a todos!!!

Este é uma API robusta criada pensando em um sistema de gerenciamento de finanças pessoais. O projeto foi criado com o intuito de estudar mais a fundo sobre as tecnologias envoltas na criação de APIs utilizando o framework FastAPI.

## ✨Funcionalidades:
- **Autenticação Segura**: Registro e login de usuários com senhas criptografadas (bcrypt) e tokens JWT.

- **Gestão de Transações**: CRUD completo para receitas e despesas.

- **Controle de Acesso**: Rotas protegidas que garantem que cada usuário veja apenas seus próprios dados.

- **Documentação automática**: Interface interativa via Swagger UI e ReDoc.

## 🛠️Tecnologias Utilizadas:
- [Python 3.14+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web de alta performance.
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM para interação com o banco de dados.
- [SQLite](https://www.sqlite.org/) - Banco de dados relacional (em arquivo).
- [Pytest](https://docs.pytest.org/) - Framework para testes automatizados.
- [Passlib](https://passlib.readthedocs.io/) - Criptografia de senhas.
- [Python-jose](https://python-jose.readthedocs.io/) - Implementação de tokens JWT.

## 📦Como Instalar e Rodar:
1. **Clone o repositório**:
```bash
git clone https://github.com/RSeguro/Python_FastAPI_API_Controle_Financas.git
cd Python_FastAPI_API_Controle_Financas
```

2. **Crie um ambiente virtual**:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente:**
Crie um arquivo `.env` na raiz do projeto com as seguintes chaves:
```text
SECRET_KEY = "sua_chave_secreta_aqui"
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

5. **Execute migrações do banco de dados:**
```bash
alembic upgrade head
```

6. **Inicie o servidor:**
```bash
uvicorn main:app --reload
```
Acesse a API em: `http://127.0.0.1:8000` *(Ou na URL que o uvicorn informar no seu terminal)*


## 📖 Documentação da API:
Após ter inicado o servidor, você pode visualizar e testar todos os endpoints diretamente pelo seu navegado:
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **Redoc:** `http://127.0.0.1:8000/redoc`


## 🧪 Rodando os Testes:
Neste projeto, utilizei o **Pytest** nos testes unitários, para garantir a qualidade do código. Os testes cobrem a criação de usuário, login e validação de tokens, e o CRUD das transações.

Para rodar todos os testes: 
```bash
python -m pytest -v
# Ou caso queira testar apenas um arquivo de testes em especifico
python -m pytest path_completo_do_arquivo
```

## 📂 Estrutura do Projeto
```text
├── migrations/             # Scripts de evolução do banco
├── tests/                  # Testes automatizados(Pytest)
├── auth_routes.py          # Rotas de criação e login de usuario.
├── dependencies.py         # Injeção de dependências
├── main.py                 # Inicialização e rotas da aplicação
├── models.py               # Modelos do Banco de Dados (SQLAlchemy)
├── requirements.txt        # Lista de dependências do projeto
├── schemas.py              # Modelos de dados e validação (Pydantic)
└── transaction_route.py    # Rotas de finanças
