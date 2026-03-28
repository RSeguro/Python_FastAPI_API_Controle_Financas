from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.db")
Base = declarative_base()

TIPOS_ESCOLHAS = [
  ('salario', 'salario'),
  ('contas', 'contas'),
  ('alimentacao', 'alimentacao'),
  ('transporte', 'transporte'),
  ('lazer', 'lazer'),
  ('saude', 'saude'),
  ('outros', 'outros')
]

class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  nome = Column("nome", String, nullable=False)
  email = Column("email", String, nullable=False, unique=True)
  senha = Column("senha", String, nullable=False)
  admin = Column("admin", Boolean, default=False)

  def __init__(self, nome, email, senha, admin=False):
    self.nome = nome
    self.email = email
    self.senha = senha
    self.admin = admin

class Transacao(Base):
  __tablename__ = "transacoes"

  id = Column("id", Integer, primary_key=True, autoincrement=True)
  tipo = Column("tipo", ChoiceType(TIPOS_ESCOLHAS), nullable=False)
  descricao = Column("descricao", String, nullable=False)
  valor = Column("valor", Float, nullable=False)
  data = Column("data", DateTime, nullable=False)
  id_usuario = Column("id_usuario", ForeignKey("usuarios.id"), nullable=False)
  

  def __init__(self, tipo, descricao, valor, data, id_usuario):
    self.tipo = tipo
    self.descricao = descricao
    self.valor = valor
    self.data = data
    self.id_usuario = id_usuario
