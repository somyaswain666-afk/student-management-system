from rag_services import ask_rag


question = "What is the GPA scale?"

answer = ask_rag(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)