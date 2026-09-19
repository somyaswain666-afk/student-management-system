from typing import TypedDict

from langgraph.graph import StateGraph, START, END

import crud
import rag_services
import ai_service

from database import SessionLocal


# --------------------------------------------------
# 1. Graph State
# --------------------------------------------------

class State(TypedDict):
    question: str
    route: str
    answer: str


# --------------------------------------------------
# 2. Router
# --------------------------------------------------

def router(state: State):

    question = state["question"].lower()

    # Knowledge-base questions should go to RAG first
    rag_keywords = [
        "gpa scale",
        "enrollment",
        "enroll",
        "required information",
        "authorized users",
        "system allows",
    ]

    if any(keyword in question for keyword in rag_keywords):
        route = "rag"

    # Student/database questions
    else:
        database_keywords = [
            "highest gpa",
            "top gpa",
            "average gpa",
            "avg gpa",
            "how many",
            "student",
            "students",
            "gpa",
        ]

        if any(keyword in question for keyword in database_keywords):
            route = "database"
        else:
            route = "rag"

    return {
        "route": route
    }


# --------------------------------------------------
# 3. Decide route
# --------------------------------------------------

def decide_route(state: State):

    return state["route"]


# --------------------------------------------------
# 4. Database Node
# --------------------------------------------------

def database_node(state: State):

    question = state["question"]
    question_lower = question.lower()

    db = SessionLocal()

    try:

        # Highest GPA
        if (
            "highest gpa" in question_lower
            or "top gpa" in question_lower
        ):

            student = crud.get_top_gpa_student(db)

            if student is None:
                return {
                    "answer": "There are no students in the database."
                }

            return {
                "answer": (
                    f"{student.name} has the highest GPA "
                    f"of {student.gpa}."
                )
            }

        # Average GPA
        if (
            "average gpa" in question_lower
            or "avg gpa" in question_lower
        ):

            average_gpa = crud.get_average_gpa(db)

            if average_gpa is None:
                return {
                    "answer": "There are no students in the database."
                }

            return {
                "answer": (
                    f"The average GPA of all students is "
                    f"{average_gpa:.2f}."
                )
            }

        # Department count
        if (
            "how many" in question_lower
            and "student" in question_lower
        ):

            departments = crud.get_departments(db)

            for department_tuple in departments:

                department = department_tuple[0]

                if department.lower() in question_lower:

                    count = crud.count_students_by_department(
                        db,
                        department
                    )

                    return {
                        "answer": (
                            f"There are {count} students "
                            f"in the {department} department."
                        )
                    }

        # Students by department
        departments = crud.get_departments(db)

        for department_tuple in departments:

            department = department_tuple[0]

            if (
                department.lower() in question_lower
                and "student" in question_lower
            ):

                students = crud.get_students_by_department(
                    db,
                    department
                )

                if not students:
                    return {
                        "answer": (
                            f"No students found in the "
                            f"{department} department."
                        )
                    }

                student_data = "\n".join([
                    f"Student ID: {student.student_id}, "
                    f"Name: {student.name}, "
                    f"Age: {student.age}, "
                    f"Gender: {student.gender}, "
                    f"Department: {student.department}, "
                    f"GPA: {student.gpa}, "
                    f"Enrollment Date: {student.enrollment_date}"
                    for student in students
                ])

                answer = ai_service.ask_gemini(
                    question,
                    student_data
                )

                return {
                    "answer": answer
                }

        # Student-specific question
        students = crud.search_students(
            db,
            question
        )

        if students:

            # Direct GPA question
            if "gpa" in question_lower:

                student = students[0]

                return {
                    "answer": (
                        f"{student.name}'s GPA is "
                        f"{student.gpa}."
                    )
                }

            # Other student questions
            student_data = "\n".join([
                f"Student ID: {student.student_id}, "
                f"Name: {student.name}, "
                f"Age: {student.age}, "
                f"Gender: {student.gender}, "
                f"Department: {student.department}, "
                f"GPA: {student.gpa}, "
                f"Enrollment Date: {student.enrollment_date}"
                for student in students
            ])

            answer = ai_service.ask_gemini(
                question,
                student_data
            )

            return {
                "answer": answer
            }

        return {
            "answer": "No database information was found."
        }

    finally:
        db.close()

# --------------------------------------------------
# 5. RAG Node
# --------------------------------------------------

def rag_node(state: State):

    question = state["question"]

    try:

        answer = rag_services.ask_rag(question)

        return {

            "answer": answer

        }

    except Exception:

        return {

            "answer": (

                "I could not generate the answer right now. "

                "The AI service is temporarily unavailable. "

                "Please try again later."

            )

        }

# --------------------------------------------------
# 6. Build Graph
# --------------------------------------------------

graph_builder = StateGraph(State)


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


# START → Router

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


# Nodes → END

graph_builder.add_edge(
    "database",
    END
)

graph_builder.add_edge(
    "rag",
    END
)


# --------------------------------------------------
# 7. Compile
# --------------------------------------------------

graph = graph_builder.compile()


# --------------------------------------------------
# 8. Public function
# --------------------------------------------------

def process_question(question: str):

    result = graph.invoke({
        "question": question,
        "route": "",
        "answer": ""
    })

    return result["answer"]