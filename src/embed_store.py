from sentence_transformers import SentenceTransformer
import chromadb
from extract import load_all_pdfs, chunk_documents

# Load the embedding model (runs locally, free)
print("Loading embedding model (this may take a moment on first run)...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB (stores data locally in a folder called chroma_db)
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="placewise_docs")

def build_vector_store():
    print("\nLoading and chunking documents...")
    documents = load_all_pdfs()
    chunks = chunk_documents(documents)
    print(f"Total chunks to embed: {len(chunks)}\n")

    print("Generating embeddings and storing in ChromaDB...")
    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["chunk_id"] for chunk in chunks]
    metadatas = [{"source": chunk["source"]} for chunk in chunks]

    embeddings = embedder.encode(texts, show_progress_bar=True).tolist()

    # Clear old data first (so re-running doesn't duplicate entries)
    existing = collection.get()
    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

    print(f"\nDone! Stored {len(chunks)} chunks in ChromaDB at ./chroma_db")

if __name__ == "__main__":
    build_vector_store()