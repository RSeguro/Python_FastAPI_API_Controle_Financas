from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from main import bcript_context
from models import Usuario
from schemas import UsuarioSchema, LoginSchema
from dependencies import pegar_sessao, criar_token, processar_login, verificar_token

auth_router = APIRouter(prefix="/auth", tags=["autentication"])

@auth_router.get("/")
async def main():
  """
  Está é a rota padrão do sistema.
  Esta é uma API criada para um sistema de controle de finanças pessoais.
  """
  return {"message": "Bem vindo!"}


@auth_router.post("/cadastro_usuario", status_code=201)
async def cadastro_usuario(usuarioSchema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
  """
  Rota padrão para criação de contas de usuário.
  """
  user_email = session.query(Usuario).filter(Usuario.email == usuarioSchema.email).first()

  if user_email:
    raise HTTPException(status_code=400, detail="E-mail de usuario já cadastrado")
  else:
    senha_criptografada = bcript_context.hash(usuarioSchema.senha)
    novo_usuario = Usuario(usuarioSchema.nome, usuarioSchema.email, senha_criptografada)
    session.add(novo_usuario)
    session.commit()
    return {"message": "usuario criado com sucesso",
            "nome": usuarioSchema.nome,
            "email": usuarioSchema.email
            }
  

@auth_router.post("/login")
async def login(loginSchema: LoginSchema, session: Session = Depends(pegar_sessao)):
  """
  Rota padrão de login de usuario
  """
  return processar_login(loginSchema.email, loginSchema.senha, session, refresh=True)
  

@auth_router.post("/login-form", include_in_schema=False)
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
  """
  Rota de autorizaçã de login para uso de dev
  """
  return processar_login(dados_formulario.username, dados_formulario.password, session, refresh=False)


@auth_router.get("/refresh")
async def refresh_token(usuario: Usuario = Depends(verificar_token)):
  """
  Rota de atualização do access_token do usuario.
  """
  access_token = criar_token(usuario.id)
  return {"access_token": access_token,
          "token_type": "Bearer"
          }