from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# -----------------------------------------
# 1. Define the state
# -----------------------------------------

class State(TypedDict):
    question: str
    answer: str


# -----------------------------------------
# 2. First node
# -----------------------------------------

def receive_question(state: State):
    print("Node 1: Received question")

    return {
        "answer": "Question received successfully."
    }


# -----------------------------------------
# 3. Second node
# -----------------------------------------

def generate_answer(state: State):
    print("Node 2: Generating answer")

    return {
        "answer": f"You asked: {state['question']}"
    }


# -----------------------------------------
# 4. Create the graph
# -----------------------------------------

graph_builder = StateGraph(State)


# Add nodes
graph_builder.add_node(
    "receive_question",
    receive_question
)

graph_builder.add_node(
    "generate_answer",
    generate_answer
)


# -----------------------------------------
# 5. Connect the nodes
# -----------------------------------------

graph_builder.add_edge(
    START,
    "receive_question"
)

graph_builder.add_edge(
    "receive_question",
    "generate_answer"
)

graph_builder.add_edge(
    "generate_answer",
    END
)


# -----------------------------------------
# 6. Compile the graph
# -----------------------------------------

graph = graph_builder.compile()


# -----------------------------------------
# 7. Run the graph
# -----------------------------------------

result = graph.invoke({
    "question": "What is the GPA scale?",
    "answer": ""
})


print("\nFinal Result:")
print(result)