""" Aplicação para o módulo de extensão DevOps """

from datetime import datetime
from fastapi import FastAPI
import requests
from requests.exceptions import ConnectionError as RequestConnectionError

APP = FastAPI()
TAREFAS = []

# Estrutura da tarefa
""" 
{
    "id" -> int,
    "titulo" -> str,
    "descricao" -> str,
    "concluida" -> bool,
    "criada_em" -> datetime
}
"""

def criar_tarefa(titulo, descricao):
    """ Função para criar uma tarefa e retorna um dicionário. """

    return {
        "id": len(TAREFAS),
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False,
        "criada_em": datetime.now().isoformat(timespec="seconds")
    }

# GET /tarefas: Lista todas as tarefas (somente id e titulo)
@APP.get("/tarefas")
async def tarefas():
    """ Rota para listar as tarefas. """
    lista_somente_id_titulo = []

    for tarefa in TAREFAS:
        id_tarefa = tarefa['id']
        titulo_tarefa = tarefa['titulo']

        lista_somente_id_titulo.append({id_tarefa: titulo_tarefa})

    return lista_somente_id_titulo

# POST /tarefas: Cria tarefa
@APP.post("/tarefas", status_code=201)
async def post_tarefa(titulo: str, descricao: str):
    """ Rota para criar uma tarefa. """
    tarefa_nova = criar_tarefa(titulo, descricao)

    TAREFAS.append(tarefa_nova)

    return {"mensagem": "OK"}

# GET /tarefas/{id_tarefa}: Visualizar tarefa específica
@APP.get("/tarefas/{id_tarefa}")
async def tarefa_especifica(id_tarefa: int):
    """ Rota para visualizar uma tarefa específica """
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Retornar todos os dados da tarefa
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    for tarefa in TAREFAS:
        if id_tarefa == int(tarefa["id"]):
            return tarefa

    return {"mensagem": "Tarefa não existe"}

# PUT /tarefas/{id}: Atualiza tarefa específica
@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(id_tarefa: int):
    """ Rota para concluir uma tarefa. """
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Marcar a tarefa como concluída
    # 3. Você deve armazenar o horário de conclusão da tarefa
    # 4. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    for tarefa in TAREFAS:
        if id_tarefa == int(tarefa['id']) and tarefa['concluida'] is False:
            tarefa['concluida'] = True
            tarefa['concluida_em'] = datetime.now().isoformat(timespec='seconds')
            titulo = tarefa['titulo']

            try:
                _ = requests.post(
                    f"http://localhost:8000/notificar?id={id}&titulo={titulo}",
                    timeout=1
                )
            except RequestConnectionError as e:
                print(e)

            return {"mensagem": "Tarefa atualizada"}

    return {"mensagem": "Tarefa não existe"}

# DELETE /tarefas/{id_tarefa}: Exclui tarefa
@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(id_tarefa: int):
    """ Rota para apagar tarefa. """
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Remover tarefa da lista de tarefas
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    indice = 0
    for tarefa in TAREFAS:
        if id_tarefa == int(tarefa['id']):
            TAREFAS.pop(indice)
            return {"mensagem": "Tarefa apagada"}

        indice += 1

    return {"mensagem": "Tarefa não existe"}

@APP.get("/")
async def index():
    """ Rota raíz. """
    return {"mensagem": "Olá, mundo!"}
