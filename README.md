# Grafos Constructors (Cognee + FalkorDB)

Este projeto demonstra como construir grafos de conhecimento a partir de artigos
utilizando o Cognee como pipeline de ingestão e o FalkorDB como banco de grafos.
O objetivo é extrair entidades/relacionamentos do texto, persistir o grafo e
consultar insights via `search()`.

## Estrutura do projeto

- `main.py`: script principal com configuração do Cognee, ingestão e buscas.
- `Artigos/`: artigos em Markdown usados como fonte de dados.
- `docker-compose.yml`: sobe o FalkorDB local.
- `requirements.txt`: dependências Python.
- `Rules/`: regras/prompts para extração de entidades e relações.

## Requisitos

- Python 3.12+
- Docker + Docker Compose
- Chave de LLM configurada em `.env`

## Configuração do ambiente

1) Crie e ative um ambiente virtual:

```
python -m venv .venv
source .venv/bin/activate
```

2) Instale as dependências:

```
pip install -r requirements.txt
```

3) Configure o arquivo `.env` (exemplo):

```
FALKORDB_PASSWORD=suasenha
GRAPH_DB_URL=localhost
GRAPH_DB_PORT=6379
GRAPH_DATABASE_PASSWORD=suasenha

OPENAI_PROVIDER=openai
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=https://seu-endpoint.openai.azure.com/openai/v1
LLM_API_KEY=seu_token

EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_ENDPOINT=https://seu-endpoint.openai.azure.com/openai/v1
EMBEDDING_API_KEY=seu_token
EMBEDDING_DIMENSIONS=1536

ENABLE_BACKEND_ACCESS_CONTROL=false
```

> Dica: mantenha `ENABLE_BACKEND_ACCESS_CONTROL=false` ao usar FalkorDB local,
> pois o modo multi-usuário pode gerar erros de compatibilidade.

## Subindo o FalkorDB

```
docker compose up -d
```

O browser fica em `http://localhost:3000`.

## Executando o pipeline

1) Abra o `main.py` e defina os textos de entrada (ex.: `Artigos/text.md`).
2) Rode o script:

```
python main.py
```

### Fluxo básico do Cognee

- `add(...)`: adiciona textos ao pipeline de ingestão.
- `cognify()`: processa os textos, gera embeddings e constrói o grafo.
- `search(...)`: consulta o grafo e/ou os chunks.

## Exemplos de buscas

### GRAPH_COMPLETION
Perguntas com raciocínio e contexto do grafo.

```
await search(
  query_type=SearchType.GRAPH_COMPLETION,
  query_text="Quais conexões entre higiene do sono e saúde cardiovascular?"
)
```

### CHUNKS
Retorna trechos relevantes do texto (com score de similaridade).

```
await search(
  query_type=SearchType.CHUNKS,
  query_text="Recomendações de higiene do sono"
)
```

### SUMMARIES
Retorna resumos hierárquicos do conteúdo.

```
await search(
  query_type=SearchType.SUMMARIES,
  query_text="Resumo do artigo"
)
```

## Consultas no FalkorDB Browser

Para verificar se o grafo foi persistido:

```
MATCH (n) RETURN count(n) AS total_nos;
```

Para inspecionar relações:

```
MATCH (n)-[r]->(m)
RETURN n.name AS origem, type(r) AS rel, m.name AS destino
LIMIT 10;
```

## Solução de problemas

**Erro de multi-usuário / access control**
- Defina `ENABLE_BACKEND_ACCESS_CONTROL=false` no `.env`.

**Grafo vazio**
- Garanta que `cognify()` foi executado após `add(...)`.
- Confira se o container do FalkorDB está ativo.

**Erro no `SearchType.CYPHER`**
- A consulta via API pode falhar por incompatibilidade no adapter.
- Execute a query diretamente no FalkorDB Browser.

## Licença

Consulte `LICENSE`.
