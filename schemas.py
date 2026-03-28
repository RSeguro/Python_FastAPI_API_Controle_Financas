from pydantic import BaseModel, ConfigDict
from enum import Enum
from datetime import datetime
from typing import Optional

class TipoTransacao(str, Enum):
  salario = 'salario',
  contas = 'contas',
  alimentacao = 'alimentacao',
  transporte = 'transporte',
  lazer = 'lazer',
  saude = 'saude',
  outros = 'outros'

class UsuarioSchema(BaseModel):
  nome: str
  email: str
  senha: str
  admin: Optional[bool] = False

  model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
  email: str
  senha: str

  model_config = ConfigDict(from_attributes=True)

class TransactionSchema(BaseModel):
  tipo: TipoTransacao
  descricao: str
  valor: float
  data: Optional[datetime]

  model_config = ConfigDict(from_attributes=True)

class AlterDescriptionSchema(BaseModel):
  id: int
  descricao: str

  model_config = ConfigDict(from_attributes=True)

class AlterValueSchema(BaseModel):
  id: int
  valor: float

  model_config = ConfigDict(from_attributes=True)


class DeleteTransactionSchema(BaseModel):
  id: int

  model_config = ConfigDict(from_attributes=True)