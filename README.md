# devops-2026

API de gerenciamento de tarefas desenvolvida no módulo de extensão de DevOps. O projeto aplica, sobre uma aplicação simples, um fluxo completo de DevOps: testes automatizados, análise estática de código, integração contínua, publicação de imagem Docker e implantação automática em nuvem.

## Descrição da aplicação

A aplicação é uma API REST construída com FastAPI que permite criar, listar, consultar, concluir e excluir tarefas. Cada tarefa possui título, descrição opcional, situação (concluída ou não), data de criação e data de conclusão. Os dados são persistidos em um banco PostgreSQL por meio do SQLModel.

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Rota raiz, retorna uma mensagem de boas-vindas |
| GET | `/tarefas` | Lista todas as tarefas |
| POST | `/tarefas?titulo=...&descricao=...` | Cria uma tarefa |
| GET | `/tarefas/{id_tarefa}` | Retorna os dados de uma tarefa |
| PUT | `/tarefas/{id_tarefa}` | Marca a tarefa como concluída e registra a data de conclusão |
| DELETE | `/tarefas/{id_tarefa}` | Exclui uma tarefa |
| GET | `/autor` | Retorna o nome do autor |

Ao concluir uma tarefa, a API envia uma requisição para o serviço de notificação (`app/notificacao.py`), que registra a conclusão no log. Se esse serviço não estiver disponível, a tarefa é concluída normalmente e o erro é apenas registrado.

A documentação interativa (Swagger) fica disponível em `/docs`.

**Aplicação implantada:** https://tarefas-2-0-0cfs.onrender.com/docs

## Estrutura do projeto

```
devops-2026/
├── app/
│   ├── __init__.py
│   ├── api.py              # Rotas da API e conexão com o banco
│   ├── modelo.py           # Modelo Tarefa (SQLModel)
│   └── notificacao.py      # Serviço de notificação
├── tests/
│   ├── __init__.py
│   ├── test_app.py         # Testes das rotas da API
│   └── test_model.py       # Testes do modelo Tarefa
├── .github/workflows/
│   └── python-app.yml      # Pipeline de CI/CD
├── Dockerfile
└── requirements.txt
```

## Execução local

### Pré-requisitos

- Python 3.14
- Docker (para o banco PostgreSQL)
- Git

### 1. Clonar o repositório e instalar as dependências

```bash
git clone https://github.com/Andreyznn/devops-2026.git
cd devops-2026

python -m venv .venv
source .venv/bin/activate        # No Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Subir o banco de dados PostgreSQL

```bash
docker run -d --name postgres -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=devops \
  postgres
```

Aguarde alguns segundos até o banco aceitar conexões (`docker logs -f postgres` deve mostrar `database system is ready to accept connections`). Nas execuções seguintes, basta rodar `docker start postgres`.

### 3. Configurar as variáveis de ambiente

A aplicação lê os dados de conexão de variáveis de ambiente obrigatórias e encerra com erro se alguma estiver faltando.

| Variável | Descrição | Exemplo local |
|---|---|---|
| `DATABASE_USERNAME` | Usuário do banco | `postgres` |
| `DATABASE_PASSWORD` | Senha do banco | `postgres` |
| `DATABASE_ADDRESS` | Endereço do servidor | `localhost` |
| `DATABASE` | Nome do banco | `devops` |

```bash
export DATABASE_USERNAME=postgres
export DATABASE_PASSWORD=postgres
export DATABASE_ADDRESS=localhost
export DATABASE=devops
```

### 4. Executar a API

```bash
fastapi dev app/api.py --port 8001
```

A API fica disponível em http://localhost:8001 e a documentação em http://localhost:8001/docs. As tabelas do banco são criadas automaticamente na inicialização.

Para usar o serviço de notificação, execute-o em outro terminal:

```bash
fastapi dev app/notificacao.py --port 8002
```

### Executar com Docker

```bash
docker build -t tarefas .

docker run -it --rm --network host \
  -e DATABASE_USERNAME=postgres \
  -e DATABASE_PASSWORD=postgres \
  -e DATABASE_ADDRESS=127.0.0.1 \
  -e DATABASE=devops \
  tarefas
```

Com `--network host`, a API usa a porta 8000 da máquina e acessa o PostgreSQL em `127.0.0.1`. A imagem publicada pela pipeline também pode ser usada diretamente: `docker pull andreyznnn/tarefas:2.0`.

### Testes e análise de código

Os testes usam um banco SQLite em memória, então não dependem do PostgreSQL. As variáveis de ambiente precisam estar definidas, mas podem ter qualquer valor:

```bash
export DATABASE_USERNAME=teste DATABASE_PASSWORD=teste DATABASE_ADDRESS=localhost DATABASE=teste

pytest --cov=app --cov-report=term-missing     # testes com cobertura
pylint app                                     # análise estática
```

## Pipeline de CI/CD

A pipeline, definida em `.github/workflows/python-app.yml`, é executada a cada push ou pull request na branch `main` e possui dois jobs:

1. **build (integração contínua):** instala as dependências, executa o Pylint e roda os testes com relatório de cobertura.
2. **entrega (entrega e implantação contínuas):** executado somente se o job `build` passar. Constrói a imagem Docker, publica no Docker Hub como `andreyznnn/tarefas:2.0` e aciona o Deploy Hook do Render, que implanta a nova versão automaticamente.

## Tecnologias utilizadas

- **Python 3.14**: linguagem da aplicação
- **FastAPI**: framework web da API e documentação automática (Swagger)
- **SQLModel / SQLAlchemy**: modelagem dos dados e acesso ao banco
- **PostgreSQL 18** (driver psycopg): banco de dados da aplicação, hospedado no Render
- **Requests**: comunicação com o serviço de notificação
- **Pytest e pytest-cov**: testes automatizados e cobertura de código
- **Pylint**: análise estática e padronização do código
- **Docker**: empacotamento da aplicação em imagem
- **GitHub Actions**: pipeline de integração e entrega contínuas
- **Docker Hub**: registro da imagem publicada
- **Render**: hospedagem da aplicação e do banco em nuvem

