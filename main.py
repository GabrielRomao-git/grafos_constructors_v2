import asyncio
import os
import pathlib
from os import path
from cognee import config, prune, add, cognify, search, SearchType

#Import the register module to enable FalkorDB support
import cognee_community_hybrid_adapter_falkor.register

from extract_from_text import load_env_file
# Carrega o .env antes de importar o Cognee
load_env_file(pathlib.Path(__file__).parent / ".env")

async def main():
    # Set up local directories
    system_path = pathlib.Path(__file__).parent
    config.system_root_directory(path.join(system_path, ".cognee_system"))
    config.data_root_directory(path.join(system_path, ".cognee_data"))
    
    # Configure relational database
    config.set_relational_db_config({
        "db_provider": "sqlite",
    })

    # Configure OpenAI as the LLM
    config.set_llm_config({
    "llm_provider": os.getenv("OPENAI_PROVIDER"),
    "llm_model": os.getenv("OPENAI_MODEL"),
    "llm_temperature": 0.7
    })
    
    # Configure FalkorDB as both vector and graph database
    config.set_vector_db_config({
        "vector_db_provider": "falkor",
        "vector_db_url": os.getenv("GRAPH_DB_URL"),
        "vector_db_port": int(os.getenv("GRAPH_DB_PORT")),
        "vector_db_name": "demo",
        "vector_dataset_database_handler": "falkor_vector_local",
        "vector_db_key": os.getenv("FALKORDB_PASSWORD"),
    })
    config.set_graph_db_config({
        "graph_database_provider": "falkor",
        "graph_database_url": os.getenv("GRAPH_DB_URL"),
        "graph_database_port": int(os.getenv("GRAPH_DB_PORT")),
        "graph_database_name": "demo",
        "graph_dataset_database_handler": "falkor_graph_local",
        "graph_database_password": os.getenv("GRAPH_DATABASE_PASSWORD"),
    })
    
    # Optional: Use se quiser limpar os dados anteriores do banco de dados
    # await prune.prune_data()
    # await prune.prune_system()
    
    # Add and process your content
    for file in os.listdir(system_path / "Artigos"):
        text_data = (system_path / "Artigos" / file).read_text(encoding="utf-8")
        await add(text_data)
    
    await cognify()
    
    # # Natural language Q&A using full graph context and LLM reasoning.
    # # Best for: Complex questions, analysis, summaries, insights.
    # # Returns: Conversational AI responses with graph-backed context.
    search_results = await search(
        query_type=SearchType.GRAPH_COMPLETION,
        query_text="Quais conexões principais o grafo constrói entre higiene do sono, saúde cardiovascular e saúde mental?"
    )
    
    # print("Search Results GRAPH_COMPLETION:")
    # for result in search_results:
    #     print("\n" + result)

# Run the example
asyncio.run(main())
