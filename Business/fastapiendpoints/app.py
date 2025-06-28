from fastapi import FastAPI
from pydantic import BaseModel
from ai_trip_planner.agents.workflow_agents import Graph_Builder
import os

app = FastAPI()

class QueryRequest(BaseModel):
    query: str


@app.post("/query")
async def travel_agent_query(query:QueryRequest):
    try:
        print(query)
        graph = Graph_Builder("groq")
        react_app = graph()

        graph_png = react_app.get_graph().draw_mermaid_png()

        with open("my_graph.png", "wb") as file:
            file.write(graph_png)

        print(f"Graph saved as 'my_graph.png' in {os.getcwd()} ")

        messages = {"messages": [query.query]}
        output = react_app.invoke(messages)

        if isinstance(output, dict) and "messages" in output:
            final_output = output["messages"][-1].content
        else:
            final_output = str(output)
        return {"answer": final_output}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})