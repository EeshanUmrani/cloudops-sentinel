import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a local .env file or set the environment variable."
        )

    return ChatOpenAI(
        model=model_name,
        temperature=0.2,
        api_key=api_key,
    )