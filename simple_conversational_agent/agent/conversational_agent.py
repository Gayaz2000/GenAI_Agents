import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from simple_conversational_agent.llm_model.groq_llm import GroqLLM

from langchain_core.runnables.history import RunnableWithMessageHistory
#from langchain_core.runnables import RunnableLambda
from langchain.memory import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class Agents:
    def __init__(self, llm):
        self.llm = GroqLLM().load_llm() # provide model you want to use
        self.store = {}


    async def call_chain(self, session_id: int):
        """builds a chain using prompt and llm to provide sequencial execution"""

        def get_session_history(self):
            """Gets the history of a particular session given session id"""
            if session_id not in self.store:
                self.store[session_id] = ChatMessageHistory()
            return self.store[session_id]
        
        prompt = ChatPromptTemplate(
            [
                ("system","You are an helpful assistant"),
                MessagesPlaceholder(variable_name="history"),
                ("user", "{input}")
            ]
        )

        chain = prompt| self.llm
        chat_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history"
        )
        return chat_with_history

async def main(input, session_id):
    """returns the response"""
    agent_obj = Agents().call_chain()
    response = await agent_obj.ainvoke({"input": input}, config={"configuration":{"session_id": session_id}})
    return response.content


if __name__ == "__main__":
    input = "Hello! How are you?"
    session_id = "user_123"
    import asyncio
    asyncio.run(main())
    