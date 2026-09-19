from langgraph_service import process_question


questions = [
    "Who has the highest GPA?",
    "What is the average GPA?",
    "How many CSE students are there?",
    "What is the GPA scale?",
    "What is the tuition fee?"
]


for question in questions:

    print("\n" + "=" * 50)

    print("Question:")
    print(question)

    answer = process_question(question)

    print("\nAnswer:")
    print(answer)