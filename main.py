import asyncio
import os
import pathlib
from os import path
from cognee import config, prune, add, cognify, search, SearchType
from extract_from_text import load_env_file

load_env_file()
# Import the register module to enable FalkorDB support
import cognee_community_hybrid_adapter_falkor.register

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
        "vector_db_name": "cognee_graph",
        "vector_dataset_database_handler": "falkor_vector_local",
        "vector_db_key": os.getenv("FALKORDB_PASSWORD"),
    })
    config.set_graph_db_config({
        "graph_database_provider": "falkor",
        "graph_database_url": os.getenv("GRAPH_DB_URL"),
        "graph_database_port": int(os.getenv("GRAPH_DB_PORT")),
        "graph_database_name": "cognee_graph",
        "graph_dataset_database_handler": "falkor_graph_local",
        "graph_database_password": os.getenv("GRAPH_DATABASE_PASSWORD"),
    })
    
    # Optional: Clean previous data
    await prune.prune_data()
    await prune.prune_system()
    
    # Add and process your content
    text_data = """
    Sarah is a software engineer at TechCorp. She specializes in machine learning
    and has been working on implementing graph-based recommendation systems.
    Sarah recently collaborated with Mike on a new project using FalkorDB.
    Mike is the lead data scientist at TechCorp.
    """
    
    await add(text_data)
    await cognify()
    
    # # Search using graph completion
    # search_results = await search(
    #     query_type=SearchType.GRAPH_COMPLETION,
    #     query_text="What does Sarah work on?"
    # )
    
    # print("Search Results:")
    # for result in search_results:
    #     print("\n" + result)

# Run the example
asyncio.run(main())
