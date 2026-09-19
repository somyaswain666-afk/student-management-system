from typing import TypedDict

from langgraph.graph import StateGraph, START, END

import crud
import rag_services

from database import SessionLocal


# -----------------------------------------
# 1. Define the state
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

    # Questions that clearly belong to the
    # Student Management System knowledge base
    rag_keywords = [
        "gpa scale",
        "enrollment",
        "enroll",
        "required information",
        "authorized users",
        "system allows",
        "knowledge base",
    ]

    if any(keyword in question for keyword in rag_keywords):
        route = "rag"

    else:
        route = "database"

    print(f"Router selected: {route}")

    return {
        "route": route
    }


# -----------------------------------------
# 3. Decide which node runs next
# -----------------------------------------

def decide_route(state: State):

    return state["route"]


# -----------------------------------------
# 4. Database node
# -----------------------------------------

def database_node(state: State):

    question = state["question"].lower()

    db = SessionLocal()

    try:

        # Highest GPA
        if (
            "highest gpa" in question
            or "top gpa" in question
        ):

            student = crud.get_top_gpa_student(db)

            if student is None:
                answer = "There are no students in the database."

            else:
                answer = (
                    f"{student.name} has the highest GPA "
                    f"of {student.gpa}."
                )

        # Average GPA
        elif (
            "average gpa" in question
            or "avg gpa" in question
        ):

            average_gpa = crud.get_average_gpa(db)

            if average_gpa is None:
                answer = "There are no students in the database."

            else:
                answer = (
                    f"The average GPA of all students is "
                    f"{average_gpa:.2f}."
                )

        else:
            answer = (
                "This database question is not handled yet."
            )

        return {
            "answer": answer
        }

    finally:
        db.close()


# -----------------------------------------
# 5. RAG node
# -----------------------------------------

def rag_node(state: State):

    question = state["question"]

    answer = rag_services.ask_rag(question)

    return {
        "answer": answer
    }


# -----------------------------------------
# 6. Build the graph
# -----------------------------------------

graph_builder = StateGraph(State)


# Add nodes
graph_builder.add_node(
    "router",
    router
)

graph_builder.add_node(
    "database",
    database_node
)

graph_builder.add_node(
    "rag",
    rag_node
)


# Start → Router
graph_builder.add_edge(
    START,
    "router"
)


# Router → Database OR RAG
graph_builder.add_conditional_edges(
    "router",
    decide_route,
    {
        "database": "database",
        "rag": "rag"
    }
)


# Both paths → End
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

questions = [
    "Who has the highest GPA?",
    "What is the GPA scale?",
    "What is the tuition fee?"
]


for question in questions:

    print("\n" + "=" * 50)

    result = graph.invoke({
        "question": question,
        "route": "",
        "answer": ""
    })

    print("\nQuestion:")
    print(question)

    print("\nAnswer:")
    print(result["answer"])