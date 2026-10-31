"""Aplicação de notificações"""

from fastapi import FastAPI

NOTIFICACAO = FastAPI()


@NOTIFICACAO.post("/notificar")
async def notificar(_id: int, titulo: str):
    """Rota para notificar"""
    print(f"Tarefa '{titulo}' (id={_id}) finalizada!")
    return {"mensagem": "OK"}
