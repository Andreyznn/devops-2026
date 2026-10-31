"""Aplicação para o módulo de extensão DevOps"""

import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated

import requests
from fastapi import FastAPI, Depends
from requests.exceptions import RequestException
from sqlalchemy import false
from sqlmodel import SQLModel, Session, create_engine, select

from .modelo import Tarefa


def ler_variavel(nome):
    """Lê uma variável de ambiente obrigatória ou encerra a aplicação."""
    valor = os.environ.get(nome)
    if valor is None:
        print(f"{nome} está faltando")
        sys.exit(1)
    return valor


DATABASE_USERNAME = ler_variavel("DATABASE_USERNAME")
DATABASE_PASSWORD = ler_variavel("DATABASE_PASSWORD")
DATABASE_ADDRESS = ler_variavel("DATABASE_ADDRESS")
DATABASE = ler_variavel("DATABASE")

URL_BANCO = (
    f"postgresql+psycopg://{DATABASE_USERNAME}:{DATABASE_PASSWORD}"
    f"@{DATABASE_ADDRESS}/{DATABASE}"
)
ENGINE = create_engine(URL_BANCO)


def criar_sessao():
    """Abre uma sessão com o banco e a fecha ao fim da requisição."""
    with Session(ENGINE) as sessao:
        yield sessao


SESSAO = Annotated[Session, Depends(criar_sessao)]


@asynccontextmanager
async def inicializacao(_api: FastAPI):
    """Cria as tabelas do banco ao iniciar a aplicação."""
    SQLModel.metadata.create_all(ENGINE)
    yield


APP = FastAPI(lifespan=inicializacao)


# GET /tarefas: Lista todas as tarefas
@APP.get("/tarefas")
async def tarefas(sessao: SESSAO) -> list[Tarefa]:
    """Rota para listar as tarefas."""
    return sessao.exec(select(Tarefa)).all()


# POST /tarefas: Cria tarefa
@APP.post("/tarefas", status_code=201)
async def post_tarefa(sessao: SESSAO, titulo: str, descricao: str | None = None):
    """Rota para criar uma tarefa."""
    tarefa_nova = Tarefa(
        titulo=titulo,
        descricao=descricao,
        data_criacao=datetime.now(timezone.utc),
    )

    sessao.add(tarefa_nova)
    sessao.commit()
    sessao.refresh(tarefa_nova)

    return {"mensagem": "OK"}


# GET /tarefas/{id_tarefa}: Visualizar tarefa específica
@APP.get("/tarefas/{id_tarefa}")
async def tarefa_especifica(sessao: SESSAO, id_tarefa: int):
    """Rota para visualizar uma tarefa específica."""
    # select * from tarefa where id = id_tarefa
    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    tarefa = sessao.exec(regra).first()

    if tarefa is None:
        return {"mensagem": "Tarefa não existe"}

    return tarefa


# PUT /tarefas/{id_tarefa}: Conclui tarefa específica
@APP.put("/tarefas/{id_tarefa}")
async def concluir_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para concluir uma tarefa."""
    # select * from tarefa where id = id_tarefa and concluida = false
    regra = select(Tarefa).where(
        Tarefa.id == id_tarefa,
        Tarefa.concluida == false(),
    )
    tarefa = sessao.exec(regra).first()

    if tarefa is None:
        return {"mensagem": "Tarefa não existe"}

    tarefa.finalizar()
    sessao.add(tarefa)
    sessao.commit()
    sessao.refresh(tarefa)

    try:
        requests.post(
            "http://localhost:8000/notificar",
            params={"id": tarefa.id, "titulo": tarefa.titulo},
            timeout=1,
        )
    except RequestException as erro:
        print(erro)

    return {"mensagem": "Tarefa atualizada"}


# DELETE /tarefas/{id_tarefa}: Exclui tarefa
@APP.delete("/tarefas/{id_tarefa}")
async def apagar_tarefa(sessao: SESSAO, id_tarefa: int):
    """Rota para apagar tarefa."""
    # select * from tarefa where id = id_tarefa
    regra = select(Tarefa).where(Tarefa.id == id_tarefa)
    tarefa = sessao.exec(regra).first()

    if tarefa is None:
        return {"mensagem": "Tarefa não existe"}

    sessao.delete(tarefa)
    sessao.commit()

    return {"mensagem": "Tarefa apagada"}


@APP.get("/")
async def index():
    """Rota raiz."""
    return {"mensagem": "Olá, mundo!"}


# Rota "/autor" que retorna {"mensagem": NOME COMPLETO}
@APP.get("/autor")
async def autor():
    """Rota para retornar o autor da aplicação."""
    return {"mensagem": "Andrey Favarim"}
