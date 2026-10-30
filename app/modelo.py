""" Modelos da aplicação de tarefas """

from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str] = None
    concluida: bool = False
    data_criacao: datetime
    data_conclusao: Optional[datetime] = None

    def finalizar(self):
        """ Método para finalizar tarefa """
        self.concluida = True
        self.data_conclusao = datetime.now().isoformat(timespec='seconds')
