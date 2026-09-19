from pathlib import Path


# Read the document
text = Path("student_handbook.txt").read_text()


# Split the document into paragraphs
chunks = [
    chunk.strip()
    for chunk in text.split("\n\n")
    if chunk.strip()
]


# Display the chunks
for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)