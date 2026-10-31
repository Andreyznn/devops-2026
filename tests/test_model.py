from datetime import datetime
from app.modelo import Tarefa


def criar_tarefa_mock():
    return Tarefa(
        _id=0,
        titulo="Tarefa teste",
        data_criacao=datetime.now().isoformat(timespec="seconds"),
    )


def test_nova_tarefa():
    t = criar_tarefa_mock()

    assert t.get_id() == 0
    assert t.titulo == "Tarefa teste"
    assert t.descricao == None
    assert t.data_criacao.isoformat() == datetime.now().isoformat(timespec="seconds")
    assert t.data_conclusao == None
    assert t.concluida == False


# Implementar teste unitário para verificar se a tarefa foi concluida


def test_tarefa_concluida():
    t = criar_tarefa_mock()

    t.finalizar()
    assert t.concluida == True
    assert t.data_conclusao == datetime.now().isoformat(timespec="seconds")
