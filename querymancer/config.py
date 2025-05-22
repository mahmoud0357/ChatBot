import os
import random
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ModelProvider(str, Enum):
    OLLAMA = "ollama"
    GROQ = "groq"
    OPENROUTER = "openrouter"

@dataclass
class ModelConfig:
    name: str
    temperature: float
    provider: ModelProvider


QWEN_2_5 = ModelConfig("qwen2.5", 0.0, ModelProvider.OLLAMA)
GEMMA_3 = ModelConfig("PetrosStav/gemma3-tools:12b", 0.7, ModelProvider.OLLAMA)
LLAMA_3_3 = ModelConfig("llama-3.3-70b-versatile", 0.0, ModelProvider.GROQ)
OPENROUTER_MISTRAL = ModelConfig("mistralai/mistral-small-24b-instruct-2501", 0.7, ModelProvider.OPENROUTER)

OPENROUTER_NOUS = ModelConfig(
    name="nousresearch/nous-hermes-2-mixtral-8x7b-dpo",
    temperature=0.7,
    provider=ModelProvider.OPENROUTER
)

class Config:
    SEED = 42
    MODEL = OPENROUTER_MISTRAL 
    OLLAMA_CONTEXT_WINDOW = 2048

    class Path:
        APP_HOME = Path(os.getenv("APP_HOME", Path(__file__).parent.parent))
        DATA_DIR = APP_HOME / "data"
        DATABASE_PATH = DATA_DIR / "banking.sqlite"


def seed_everything(seed: int = Config.SEED):
    random.seed(seed)
