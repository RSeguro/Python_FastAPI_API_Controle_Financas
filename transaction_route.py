from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from dependencies import pegar_sessao, verificar_token, verificar_usuario
from models import Transacao, Usuario
from schemas import TransactionSchema,AlterDescriptionSchema, AlterValueSchema, DeleteTransactionSchema

transaction_router = APIRouter(prefix="/transaction", tags=["transaction"], dependencies=[Depends(verificar_token)])

@transaction_router.get("/")
async def main():
  return {"message": "Bem vindo!"}

@transaction_router.post("/registrar-transacao", status_code= 201)
async def registrar_transacao(transaction_schema:TransactionSchema, usuario:Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
  """
  Rota padrão de cadastro de novas transações.
  Quando registrada uma nova transação, deve-se atentar aos "tipos" pré-definidos, visiveis abaixo, na aba de Schemas -> TransactionSchemas -> tipo -> Enum.
  """
  nova_transacao = Transacao(transaction_schema.tipo,
                             transaction_schema.descricao,
                             float(transaction_schema.valor),
                             transaction_schema.data,
                             usuario.id,
                             )
  session.add(nova_transacao)
  session.commit()

  return {"message": "Transação adicionada com sucesso."}

@transaction_router.get("/listar-transacoes")
async def listar_transacoes(usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
  """
  Rota para listagem de todas as transações realizadas pelo usuario atual.
  """
  lista_transacoes = session.query(Transacao).filter(Transacao.id_usuario == usuario.id).all()
  return lista_transacoes

@transaction_router.post("/alterar-descricao")
async def alterar_descricao(alter_desc_schema: AlterDescriptionSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
  """
  Rota para alterar a descrição de uma transação.
  """
  consulta = verificar_usuario(alter_desc_schema.id, usuario.id, session)
  if consulta:
    consulta.descricao = alter_desc_schema.descricao
    session.add(consulta)
    session.commit()
    return {"message": "Descrição alterada com sucesso!"}

@transaction_router.post("/alterar-valor")
async def alterar_valor(alter_value_schema: AlterValueSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
  """
  Rota para alterar o valor de uma transação.
  """
  consulta = verificar_usuario(alter_value_schema.id, usuario.id, session)
  if consulta:
    consulta.valor = alter_value_schema.valor
    session.add(consulta)
    session.commit()
    return {"message": "Valor alterado com sucesso!"}


@transaction_router.post("/deletar-transacao", status_code=204)
async def deletar_transacao(delete_schema: DeleteTransactionSchema, usuario: Usuario = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
  """
  Rota para deletar uma transação.
  """
  consulta = verificar_usuario(delete_schema.id, usuario.id, session)
  if consulta:
    session.delete(consulta)
    session.commit()
    return None