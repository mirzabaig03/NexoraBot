from langchain_experimental.agents import create_csv_agent
from langchain_openai import ChatOpenAI
from src.config.index import appConfig

def create_project_csv_agent(file_paths: list[str], model_name: str = "gpt-4o"):
    """
    Creates a CSV agent for handling structured data (CSV, Excel).
    
    Args:
        file_paths: List of absolute paths to the CSV/Excel files.
        model_name: The OpenAI model to use.
        
    Returns:
        An agent executor ready to be invoked.
    """
    llm = ChatOpenAI(
        model=model_name,
        api_key=appConfig["openai_api_key"],
        temperature=0
    )

    return create_csv_agent(
        llm,
        file_paths,
        verbose=True,
        allow_dangerous_code=True,
    )
