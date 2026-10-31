from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.api import APP, criar_sessao

# Banco em memória: criado do zero a cada execução dos testes
ENGINE_TESTE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SQLModel.metadata.create_all(ENGINE_TESTE)


def sessao_teste():
    with Session(ENGINE_TESTE) as sessao:
        yield sessao


APP.dependency_overrides[criar_sessao] = sessao_teste
CLIENT = TestClient(APP)


def test_index():
    resposta = CLIENT.get("/")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Olá, mundo!"}


# 1. GET /tarefas com o banco vazio
def test_tarefas_get():
    resposta = CLIENT.get("/tarefas")
    assert resposta.status_code == 200
    assert resposta.json() == []


# 2. POST /tarefas
def test_tarefas_post():
    resposta = CLIENT.post("/tarefas?titulo=teste&descricao=teste")
    assert resposta.status_code == 201
    assert resposta.json() == {"mensagem": "OK"}


def test_tarefas_get_com_tarefa():
    resposta = CLIENT.get("/tarefas")
    assert resposta.status_code == 200

    dados = resposta.json()
    assert len(dados) == 1
    assert dados[0]["id"] == 1
    assert dados[0]["titulo"] == "teste"


def test_tarefa_criada():
    resposta = CLIENT.get("/tarefas/1")
    assert resposta.status_code == 200

    dados = resposta.json()
    assert dados["id"] == 1
    assert dados["titulo"] == "teste"
    assert dados["descricao"] == "teste"
    assert dados["concluida"] is False
    assert dados["data_criacao"] is not None
    assert dados["data_conclusao"] is None


def test_tarefa_inexistente():
    resposta = CLIENT.get("/tarefas/99")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Tarefa não existe"}


# 3. PUT /tarefas/{id}
def test_tarefas_put():
    resposta = CLIENT.put("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa atualizada"}

    # Tarefa inexistente
    resposta = CLIENT.put("/tarefas/99")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}

    # Tarefa já concluída não é encontrada pelo filtro
    resposta = CLIENT.put("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}


# 4. GET /tarefas/{id} depois de concluir
def test_tarefas_get_id():
    resposta = CLIENT.get("/tarefas/1")
    assert resposta.status_code == 200

    dados = resposta.json()
    assert dados["concluida"] is True
    assert dados["data_conclusao"] is not None


# 5. DELETE /tarefas/{id}
def test_tarefas_delete():
    resposta = CLIENT.delete("/tarefas/99")
    assert resposta.json() == {"mensagem": "Tarefa não existe"}

    resposta = CLIENT.delete("/tarefas/1")
    assert resposta.json() == {"mensagem": "Tarefa apagada"}

    resposta = CLIENT.get("/tarefas")
    assert resposta.json() == []


def test_autor():
    resposta = CLIENT.get("/autor")
    assert resposta.status_code == 200
    assert resposta.json() == {"mensagem": "Andrey Favarim"}