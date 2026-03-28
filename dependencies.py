from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session, sessionmaker
from main import bcript_context, oauth2_schema, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from models import db, Usuario, Transacao
from datetime import timedelta, datetime, timezone
from jose import jwt, JWTError

def pegar_sessao():
  try:
    Session = sessionmaker(bind= db)
    session = Session()
    yield session
  finally:
    session.close()


def autenticar_usuario(email, senha, session):
  usuario = session.query(Usuario).filter(Usuario.email == email).first()
  if not usuario:
    return False
  elif not bcript_context.verify(senha, usuario.senha):
    return False
  return usuario


def criar_token(id_usuario, duracao_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
  data_expiracao = datetime.now(timezone.utc) + duracao_token
  dicionario_infos = {"sub": str(id_usuario), "exp": data_expiracao}
  jwt_codificado = jwt.encode(dicionario_infos, SECRET_KEY, ALGORITHM)
  return jwt_codificado


def processar_login(email, senha, session, refresh):
  usuario = autenticar_usuario(email, senha, session)
  if not usuario:
    raise HTTPException(status_code=400, detail="Usuario ou senha incorretos.")
  else:
    acess_token = criar_token(usuario.id)
    refres_token = criar_token(usuario.id, duracao_token= timedelta(days=7))
    if refresh:
      return {"access_token": acess_token,
              "refresh_token": refres_token,
              "token_type": "Bearer"
              }
    else:
      return {"access_token": acess_token,
              "token_type": "Bearer"
              }


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)):
  try:
    dicionario_infos = jwt.decode(token, SECRET_KEY, ALGORITHM)
    id_usuario = int(dicionario_infos.get("sub"))
  except JWTError:
    raise HTTPException(status_code=401, detail="Acesso negado. verifique a validade do token.")
  
  usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
  if not usuario:
    raise HTTPException(status_code=401, detail="Acesso Inválido.")
  return usuario


def verificar_usuario(id_transacao, id_usuario, session: Session = Depends(pegar_sessao)):
  consulta = session.query(Transacao).filter(Transacao.id == id_transacao).first()
  if not consulta:
    raise HTTPException(status_code=400, detail="Transação não encontrada.")
  if not id_usuario == consulta.id_usuario:
    raise HTTPException(status_code=401, detail="Você não tem permissão para realizar esta ação.")
  return consulta