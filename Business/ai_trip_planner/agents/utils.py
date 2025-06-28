import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

from pydantic import BaseModel, Field
from typing_extensions import Literal, Optional, Any

from langchain_groq import ChatGroq

import yaml

def load_config(config_path: str= r"Business\ai_trip_planner\agents\configs.yaml")->dict:
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

class ConfigLoader:
    def __init__(self):
        print("Loading config...")
        self.config = load_config()

    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    model_provider: Literal["groq","ollama"] = "groq"
    config: Optional[ConfigLoader] = Field(default=None, exclude=True)

    def model_post_init(self, context: Any)-> None:
        self.config = ConfigLoader()

    class Config:
        arbitrary_type_allowed = True

    def load_llm(self):
        """loads the LLM model"""
        print("Loading LLM.....")

        if self.model_provider == "groq":
            model_name = self.Config["llm"]["provider"]["model_name"]
            llm = ChatGroq(model=model_name)
        return llm