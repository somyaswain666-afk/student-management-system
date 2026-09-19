from typing import TypedDict

from langgraph.graph import StateGraph, START, END

import crud
from database import SessionLocal


# -----------------------------------------
# 1. Define the state
# -----------------------------------------

class State(TypedDict):
    question: str
    answer: str


# -----------------------------------------
# 2. Database node
# -----------------------------------------

def database_node(state: State):

    question = state["question"].lower()

    db = SessionLocal()

    try:

        # Highest GPA
        if "highest gpa" in question or "top gpa" in question:

            student = crud.get_top_gpa_student(db)

            if student is None:
                answer = "There are no students in the database."
            else:
                answer = (
                    f"{student.name} has the highest GPA "
                    f"of {student.gpa}."
                )

        # Average GPA
        elif "average gpa" in question or "avg gpa" in question:

            average_gpa = crud.get_average_gpa(db)

            if average_gpa is None:
                answer = "There are no students in the database."
            else:
                answer = (
                    f"The average GPA of all students is "
                    f"{average_gpa:.2f}."
                )

        else:
            answer = "Database question not handled yet."

        return {
            "answer": answer
        }

    finally:
        db.close()


# -----------------------------------------
# 3. Build the graph
# -----------------------------------------

graph_builder = StateGraph(State)

graph_builder.add_node(
    "database",
    database_node
)

graph_builder.add_edge(
    START,
    "database"
)

graph_builder.add_edge(
    "database",
    END
)


# -----------------------------------------
# 4. Compile
# -----------------------------------------

graph = graph_builder.compile()


# -----------------------------------------
# 5. Test
# -----------------------------------------

question = "Who has the highest GPA?"

result = graph.invoke({
    "question": question,
    "answer": ""
})


print("\nQuestion:")
print(question)

print("\nAnswer:")
print(result["answer"])