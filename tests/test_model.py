from datetime import datetime, timedelta, timezone

from app.modelo import Tarefa

DATA_CRIACAO = datetime.now(timezone.utc)


def criar_tarefa_mock():
    return Tarefa(
        id=0,
        titulo="Tarefa teste",
        data_criacao=DATA_CRIACAO,
    )


def test_nova_tarefa():
    t = criar_tarefa_mock()

    assert t.get_id() == 0
    assert t.titulo == "Tarefa teste"
    assert t.descricao is None
    assert t.data_criacao == DATA_CRIACAO
    assert t.data_conclusao is None
    assert t.concluida is False


# Teste unitário para verificar se a tarefa foi concluída
def test_tarefa_concluida():
    t = criar_tarefa_mock()

    antes = datetime.now(timezone.utc)
    t.finalizar()
    depois = datetime.now(timezone.utc)

    assert t.concluida is True
    assert isinstance(t.data_conclusao, datetime)
    assert antes <= t.data_conclusao <= depois
    assert t.data_conclusao - t.data_criacao < timedelta(seconds=5)