from fastapi.encoders import jsonable_encoder

def test_registrar_transacao(client, usuario_teste, auth_headers):
  payload = {
    "tipo": "salario",
    "descricao": "pagamento",
    "valor": 1200,
    "data": "2026-03-21 13:16:50.396629",
    "id": usuario_teste.id
  }

  response = client.post("/transaction/registrar-transacao", json=payload, headers= auth_headers)
  assert response.status_code == 201
  assert response.json()["message"].lower() == "transação adicionada com sucesso."


def test_listar_transacoes(client, lista_transacoes_teste, auth_headers):
  response = client.get("/transaction/listar-transacoes", headers=auth_headers)
  assert response.status_code == 200
  data = response.json()
  data_hora_esperada = jsonable_encoder(lista_transacoes_teste[2].data)
  assert len(data) == 3
  assert data[0]["descricao"] == lista_transacoes_teste[0].descricao
  assert data[1]["valor"] == lista_transacoes_teste[1].valor
  assert data[2]["data"] == data_hora_esperada


def test_alterar_descricao(client, usuario_teste, transacao_teste, auth_headers):
  payload = {
    "id": usuario_teste.id,
    "descricao": "conta da net"
  }
  response = client.post("/transaction/alterar-descricao", json=payload, headers=auth_headers)
  assert response.status_code == 200
  assert response.json()["message"].lower() == "descrição alterada com sucesso!"


def test_alterar_valor(client, usuario_teste, transacao_teste, auth_headers):
  payload = {
    "id": usuario_teste.id,
    "valor": 69.90
  }
  response = client.post("/transaction/alterar-valor", json=payload, headers=auth_headers)
  assert response.status_code == 200
  assert response.json()["message"].lower() == "valor alterado com sucesso!"


def test_deletar_transacao(client, transacao_teste, auth_headers):
  payload = {
    "id": transacao_teste.id
  }
  response = client.post("/transaction/deletar-transacao", json=payload, headers=auth_headers)
  assert response.status_code == 204
  

