"""Aplicação para o módulo de extensão DevOps"""

from datetime import datetime
from fastapi import FastAPI
import requests
from requests.exceptions import ConnectionError as RequestConnectionError

from .modelo import Tarefa

APP = FastAPI()
TAREFAS = []


# GET /tarefas: Lista todas as tarefas (somente id e titulo)
@APP.get("/tarefas")
async def tarefas():
    """Rota para listar as tarefas."""
    lista_somente_id_titulo = []

    for tarefa in TAREFAS:
        lista_somente_id_titulo.append(tarefa.resumir())

    return lista_somente_id_titulo


# POST /tarefas: Cria tarefa
@APP.post("/tarefas", status_code=201)
async def post_tarefa(titulo: str, descricao: str = None):
    """Rota para criar uma tarefa."""
    tarefa_nova = Tarefa(
        _id=len(TAREFAS),
        titulo=titulo,
        descricao=descricao,
        data_criacao=datetime.now().isoformat(timespec="seconds"),
    )

    TAREFAS.append(tarefa_nova)

    return {"mensagem": "OK"}


# GET /tarefas/{id_tarefa}: Visualizar tarefa específica
@APP.get("/tarefas/{id_tarefa}")
async def tarefa_especifica(id_tarefa: int):
    """Rota para visualizar uma tarefa específica"""
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Retornar todos os dados da tarefa
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    for tarefa in TAREFAS:
        if id_tarefa == tarefa.get_id():
            return tarefa

    return {"mensagem": "Tarefa não existe"}


# PUT /tarefas/{id}: Atualiza tarefa específica
@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(id_tarefa: int):
    """Rota para concluir uma tarefa."""
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Marcar a tarefa como concluída
    # 3. Você deve armazenar o horário de conclusão da tarefa
    # 4. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    for tarefa in TAREFAS:
        if id_tarefa == tarefa.get_id() and tarefa.concluida is False:
            tarefa.finalizar()
            titulo = tarefa.titulo

            try:
                _ = requests.post(
                    f"http://localhost:8000/notificar?id={tarefa.get_id()}&titulo={titulo}",
                    timeout=1,
                )
            except RequestConnectionError as e:
                print(e)

            return {"mensagem": "Tarefa atualizada"}

    return {"mensagem": "Tarefa não existe"}


# DELETE /tarefas/{id_tarefa}: Exclui tarefa
@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(id_tarefa: int):
    """Rota para apagar tarefa."""
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Remover tarefa da lista de tarefas
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    indice = 0
    for tarefa in TAREFAS:
        if id_tarefa == tarefa.get_id():
            TAREFAS.pop(indice)
            return {"mensagem": "Tarefa apagada"}

        indice += 1

    return {"mensagem": "Tarefa não existe"}


@APP.get("/")
async def index():
    """Rota raíz."""
    return {"mensagem": "Olá, mundo!"}


# 1. Implementar uma rota chamada "/autor" que retorna
# um dicionário no formato {"mensagem": SEU NOME COMPLETO}
@APP.get("/autor")
async def autor():
    """Rota para retornar o autor da aplicação"""
    return {"mensagem": "Pedro Rocha Horchulhack"}


# 2. Criar um teste unitário para verificar se a rota
# está produzindo o resultado esperado

# 3. Verificar se o código está no padrão do PyLint

# 4. Enviar o código para o repositório (git push)
