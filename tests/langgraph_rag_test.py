from typing import TypedDict

from langgraph.graph import StateGraph, START, END

import rag_services


# -----------------------------------------
# 1. Define the state
# -----------------------------------------

class State(TypedDict):
    question: str
    answer: str


# -----------------------------------------
# 2. RAG node
# -----------------------------------------

def rag_node(state: State):

    question = state["question"]

    answer = rag_services.ask_rag(question)

    return {
        "answer": answer
    }


# -----------------------------------------
# 3. Build the graph
# -----------------------------------------

graph_builder = StateGraph(State)

graph_builder.add_node(
    "rag",
    rag_node
)

graph_builder.add_edge(
    START,
    "rag"
)

graph_builder.add_edge(
    "rag",
    END
)


# -----------------------------------------
# 4. Compile
# -----------------------------------------

graph = graph_builder.compile()


# -----------------------------------------
# 5. Test
# -----------------------------------------

question = "What is the GPA scale?"

result = graph.invoke({
    "question": question,
    "answer": ""
})


print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])