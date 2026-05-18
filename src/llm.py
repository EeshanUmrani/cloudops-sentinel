import os
from functools import lru_cache

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


FAST_MODEL_ENV = "FAST_MODEL_NAME"
SMART_MODEL_ENV = "SMART_MODEL_NAME"
DEFAULT_MODEL_ENV = "MODEL_NAME"


def get_model_name(model_tier: str = "fast") -> str:
    """
    Returns the model name for a given model tier.

    fast:
        Used for simpler, structured, lower-risk tasks such as planning,
        log extraction, metrics analysis, remediation drafting, and reporting.

    smart:
        Used for reasoning-heavy tasks such as root cause analysis and critique.
    """

    default_model = os.getenv(DEFAULT_MODEL_ENV, "gpt-4o-mini")

    if model_tier == "smart":
        return os.getenv(SMART_MODEL_ENV, default_model)

    if model_tier == "fast":
        return os.getenv(FAST_MODEL_ENV, default_model)

    return default_model


@lru_cache(maxsize=4)
def get_llm(model_tier: str = "fast"):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a local .env file or set the environment variable."
        )

    return ChatOpenAI(
        model=get_model_name(model_tier),
        temperature=0.2,
        api_key=api_key,
    )