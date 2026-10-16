from fastapi import FastAPI
from datetime import datetime
import requests

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
    return {
        "id": len(TAREFAS),
        "titulo": titulo,
        "descricao": descricao,
        "concluida": False,
        "criada_em": datetime.now()
    }

# GET /tarefas: Lista todas as tarefas (somente id e titulo)
@APP.get("/tarefas")
async def tarefas():
    lista_somente_id_titulo = []

    for tarefa in TAREFAS:
        id_tarefa = tarefa['id']
        titulo_tarefa = tarefa['titulo']

        lista_somente_id_titulo.append({id_tarefa: titulo_tarefa})

    return lista_somente_id_titulo

# POST /tarefas: Cria tarefa
@APP.post("/tarefas")
async def post_tarefa(titulo: str, descricao: str):
    global TAREFAS

    tarefa_nova = criar_tarefa(titulo, descricao)

    TAREFAS.append(tarefa_nova)

    return {"mensagem": "OK"}

# GET /tarefas/{id}: Visualizar tarefa específica
@APP.get("/tarefas/{id}")
async def tarefa_especifica(id: int):
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Retornar todos os dados da tarefa
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe

    for tarefa in TAREFAS:
        if id == int(tarefa["id"]):
            return tarefa

    return {"mensagem": "Tarefa não existe"}

# PUT /tarefas/{id}: Atualiza tarefa específica
@APP.put("/tarefas/{id}")
async def concluir_tarefa(id: int):
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Marcar a tarefa como concluída
    # 3. Você deve armazenar o horário de conclusão da tarefa
    # 4. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe
    
    for tarefa in TAREFAS:
        if id == int(tarefa['id']) and tarefa['concluida'] == False:
            tarefa['concluida'] = True
            tarefa['concluida_em'] = datetime.now()
            titulo = tarefa['titulo']
            
            resp = requests.post(f"http://localhost:8000/notificar?id={id}&titulo={titulo}")

            print(resp.json())
            return {"mensagem": "Tarefa atualizada"}
    
    return {"mensagem": "Tarefa não existe"}

# DELETE /tarefas/{id}: Exclui tarefa
@APP.delete("/tarefas/{id}")
async def apagar_tarefa(id: int):
    # 1. Selecionar a tarefa de ID recebido como parâmetro
    # 2. Remover tarefa da lista de tarefas
    # 3. Caso a tarefa não exista, você tem que mostrar que a tarefa não existe
    global TAREFAS

    indice = 0
    for tarefa in TAREFAS:
        if id == int(tarefa['id']):
            TAREFAS.pop(indice)
            return {"mensagem": "Tarefa apagada"}

        indice += 1
    
    return {"mensagem": "Tarefa não existe"}

@APP.get("/")
async def index():
    return {"mensagem": "Olá, mundo!"}