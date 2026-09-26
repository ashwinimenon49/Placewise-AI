import os
import pdfplumber
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = "data"

def extract_text_and_tables(pdf_path):
    """Extract text AND tables from a PDF, formatting tables cleanly."""
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # Extract regular text (headers, titles, etc.)
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

            # Extract tables separately and format them as readable rows
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    # Join cells with " | " and skip empty rows
                    clean_row = [cell.strip() if cell else "" for cell in row]
                    if any(clean_row):
                        full_text += " | ".join(clean_row) + "\n"

    return full_text

def load_all_pdfs(data_dir=DATA_DIR):
    """Read every PDF in the data folder and return their text, tagged with filename."""
    documents = []
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(data_dir, filename)
            print(f"Extracting: {filename}")
            text = extract_text_and_tables(path)
            documents.append({
                "source": filename,
                "text": text
            })
    return documents

def chunk_documents(documents, chunk_size=400, chunk_overlap=50):
    """Split each document's text into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )

    all_chunks = []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["source"],
                "chunk_id": f"{doc['source']}_{i}",
                "text": chunk
            })
    return all_chunks

if __name__ == "__main__":
    print("Loading PDFs from data/ folder...\n")
    documents = load_all_pdfs()
    print(f"\nLoaded {len(documents)} PDF(s).\n")

    print("Chunking text...\n")
    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks total.\n")

    print("--- Sample chunk (first one) ---")
    print(f"Source: {chunks[0]['source']}")
    print(f"Text:\n{chunks[0]['text']}")

    print("\n--- Sample chunk (a middle one, likely table data) ---")
    mid = len(chunks) // 2
    print(f"Source: {chunks[mid]['source']}")
    print(f"Text:\n{chunks[mid]['text']}")