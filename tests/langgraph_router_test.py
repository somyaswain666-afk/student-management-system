from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# -----------------------------------------
# 1. Define state
# -----------------------------------------

class State(TypedDict):
    question: str
    route: str
    answer: str


# -----------------------------------------
# 2. Router node
# -----------------------------------------

def router(state: State):

    question = state["question"].lower()

    if "gpa" in question or "student" in question:
        route = "database"
    else:
        route = "rag"

    print(f"Router selected: {route}")

    return {
        "route": route
    }


# -----------------------------------------
# 3. Database node
# -----------------------------------------

def database_node(state: State):

    print("Database node running")

    return {
        "answer": "This question should be handled using the student database."
    }


# -----------------------------------------
# 4. RAG node
# -----------------------------------------

def rag_node(state: State):

    print("RAG node running")

    return {
        "answer": "This question should be handled using the RAG knowledge base."
    }


# -----------------------------------------
# 5. Decide where to go
# -----------------------------------------

def decide_route(state: State):

    return state["route"]


# -----------------------------------------
# 6. Build graph
# -----------------------------------------

graph_builder = StateGraph(State)

graph_builder.add_node("router", router)
graph_builder.add_node("database", database_node)
graph_builder.add_node("rag", rag_node)


graph_builder.add_edge(
    START,
    "router"
)


graph_builder.add_conditional_edges(
    "router",
    decide_route,
    {
        "database": "database",
        "rag": "rag"
    }
)


graph_builder.add_edge(
    "database",
    END
)

graph_builder.add_edge(
    "rag",
    END
)


# -----------------------------------------
# 7. Compile
# -----------------------------------------

graph = graph_builder.compile()


# -----------------------------------------
# 8. Test
# -----------------------------------------

question = "Who has the highest GPA?"

result = graph.invoke({
    "question": question,
    "route": "",
    "answer": ""
})


print("\nFinal Result:")
print(result)