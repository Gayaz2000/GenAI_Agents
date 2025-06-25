import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class GroqLLM:
    """
    A python class that give the methods neccessery to load the required llm models from groq
    """
    def __init__(self, model_name: str = "llama3-8b-8192"):
        self.model_name = model_name
        self.llm = None

    async def load_llm(self, temperature: float = 0, max_tokens: int = 1000):
        """A method that loads llm models from groq cloud"""
        try:
            if "llama" in self.model_name:
                self.llm = ChatGroq(model="llama3-70b-8192")
                #return llm
            elif "deepseek" in self.model_name:
                self.llm = ChatGroq(model="deepseek-r1-distill-llama-70b")
                #return llm
            elif "gemma" in self.model_name:
                self.llm = ChatGroq(model="gemma2-9b-it")
                #return llm
            elif "qwen" in self.model_name:
                self.llm = ChatGroq(model="qwen-qwq-32b")
            else:
                raise f"model name was not given"
            
            return self.llm
        except Exception as e:
            raise f"model not found: {e}"

