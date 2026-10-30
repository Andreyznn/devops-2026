from fastapi import FastAPI

NOTIFICACAO = FastAPI()

@NOTIFICACAO.post("/notificar")
async def notificar(id: int, titulo: str):
    print(f"Tarefa '{titulo}' (id={id}) finalizada!")
    return {"mensagem": "OK"}