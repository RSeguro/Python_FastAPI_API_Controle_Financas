from jose import jwt
from main import SECRET_KEY, ALGORITHM

def test_cadastrar_usuario(client):
  payload = {"nome": "TestUser", "email": "testuser@teste", "senha": "123456"}

  response = client.post("/auth/cadastro_usuario", json=payload)

  assert response.status_code == 201
  data = response.json()
  assert data["nome"] == "TestUser"
  assert data["email"] == "testuser@teste"


def test_login(client, usuario_teste):
  payload = {
    "email": "tester@test",
    "senha": "123456"
  }

  response = client.post("/auth/login", json=payload)
  assert response.status_code == 200

  data = response.json()
  token = data["access_token"]
  decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

  assert decode.get("sub") == str(usuario_teste.id)
  assert data["token_type"].lower() == "bearer"


def test_login_incorreto(client, usuario_teste):
  payload = {
    "email": "email-errado@test",
    "senha": "123456"
  }

  response = client.post("/auth/login", json=payload)
  assert response.status_code == 400
  assert response.json()["detail"].lower() == "usuario ou senha incorretos."

