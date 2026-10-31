from fastapi.testclient import TestClient
from app.api import APP
from datetime import datetime

CLIENT = TestClient(APP)
DATA = None
DATA_CONCLUSAO = None


def test_index():
    resposta = CLIENT.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Olá, mundo!"}


# 1. Implementar um teste unitário para a rota /tarefas (GET)
def test_tarefas_get():
    resposta = CLIENT.get("/tarefas")
    assert resposta.status_code == 200

    # Testando se a rota retorna uma lista vazia
    assert resposta.json() == []


# 2. Implementar um teste unitário para a rota /tarefas (POST)
def test_tarefas_post():
    global DATA
    resposta = CLIENT.post("/tarefas?titulo=teste&descricao=teste")
    DATA = datetime.now().isoformat(timespec="seconds")

    assert resposta.status_code == 201
    assert resposta.json() == {"mensagem": "OK"}

    resposta = CLIENT.get("/tarefas")
    assert resposta.json() == [{"0": "teste"}]


def test_tarefa_criada():
    resposta = CLIENT.get("/tarefas/0")
    assert resposta.status_code == 200
    assert resposta.json() == {
        "_id": 0,
        "titulo": "teste",
        "descricao": "teste",
        "concluida": False,
        "data_criacao": str(DATA),
        "data_conclusao": None,
    }


# 3. Implementar um teste unitário para a rota /tarefas/{id} (PUT)
def test_tarefas_put():
    global DATA_CONCLUSAO
    resposta = CLIENT.put("/tarefas/0")
    DATA_CONCLUSAO = datetime.now().isoformat(timespec="seconds")
    assert resposta.json() == {"mensagem": "Tarefa atualizada"}

    resposta = CLIENT.put("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}


# 4. Implementar um teste unitário para a rota /tarefas/{id} (GET)
def test_tarefas_get_id():
    resposta = CLIENT.get("/tarefas/0")
    assert resposta.status_code == 200
    assert resposta.json() == {
        "_id": 0,
        "titulo": "teste",
        "descricao": "teste",
        "concluida": True,
        "data_criacao": str(DATA),
        "data_conclusao": str(DATA_CONCLUSAO),
    }

    resposta = CLIENT.get("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}


# 5. Implementar um teste unitário para a rota /tarefas/{id} (DELETE)
def test_tarefas_delete():
    resposta = CLIENT.delete("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}

    resposta = CLIENT.delete("/tarefas/0")
    assert resposta.json() == {"mensagem": "Tarefa apagada"}

    resposta = CLIENT.get("/tarefas")
    assert resposta.json() == []


def test_autor():
    resposta = CLIENT.get("/autor")

    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Pedro Rocha Horchulhack"}
