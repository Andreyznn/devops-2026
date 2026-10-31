"""Modelos da aplicação de tarefas"""

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class Tarefa(SQLModel, table=True):
    """Modelo de tarefa"""

    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False
    data_criacao: datetime
    data_conclusao: Optional[datetime] = None

    def finalizar(self):
        """Método para finalizar tarefa"""
        self.concluida = True
        self.data_conclusao = datetime.now(timezone.utc)

    def resumir(self):
        """Resume tarefa em `id: titulo`"""
        return {self.id: self.titulo}

    def get_id(self):
        """Retorna ID da tarefa"""
        return self.id