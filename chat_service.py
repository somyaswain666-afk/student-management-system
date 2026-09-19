import langgraph_service


def process_chat(question: str, db):
    return langgraph_service.process_question(question)