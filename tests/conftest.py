import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from main import app, bcript_context
from models import Base, Usuario, Transacao
from dependencies import pegar_sessao
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
  # Base.metadata.drop_all(bind=engine)
  Base.metadata.create_all(bind=engine)
  db = SessionTesting()
  try:
    yield db
  finally:
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(session):
  def override_pegar_sessao():
    try:
      yield session
    finally:
      pass

  app.dependency_overrides[pegar_sessao] = override_pegar_sessao
  with TestClient(app) as c:
    yield c
  app.dependency_overrides.clear()

@pytest.fixture
def usuario_teste(session):
  novo_usuario = Usuario(
    nome="Tester",
    email="tester@test",
    senha=bcript_context.hash("123456")
  )
  session.add(novo_usuario)
  session.commit()
  session.refresh(novo_usuario)
  return novo_usuario

@pytest.fixture
def auth_headers(client, usuario_teste):
  payload = {
    "email": "tester@test",
    "senha": "123456"
  }

  response = client.post("/auth/login", json=payload)
  token = response.json()["access_token"]
  return {"Authorization": f"Bearer {token}"}
  
@pytest.fixture
def transacao_teste(session, usuario_teste):
  nova_transacao = Transacao(
    tipo = "contas",
    descricao = "internet",
    valor = 99.90,
    data = datetime.now(),
    id_usuario = usuario_teste.id
  )
  session.add(nova_transacao)
  session.commit()
  session.refresh(nova_transacao)
  return nova_transacao

@pytest.fixture
def lista_transacoes_teste(session, usuario_teste):
  transacao_01 = Transacao(tipo = "alimentacao", descricao = "docinho saindo do trabalho", valor = 5.50, data = datetime.now(), id_usuario = usuario_teste.id)
  transacao_02 = Transacao(tipo = "transporte", descricao = "uber voltando do mercado", valor = 19.85, data = datetime.now(), id_usuario = usuario_teste.id)
  transacao_03 = Transacao(tipo = "lazer", descricao = "assinatura netflix", valor = 59.90, data = datetime.now(), id_usuario = usuario_teste.id)
  
  lista = [transacao_01, transacao_02, transacao_03]
  session.add_all(lista)
  session.commit()
  for i in lista:
    session.refresh(i)
  
  return lista
