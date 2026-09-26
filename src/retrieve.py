from sentence_transformers import SentenceTransformer
import chromadb

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="placewise_docs")

BROAD_KEYWORDS = ["all", "every", "list", "total", "any year", "across", "each", "compare"]

def is_broad_question(question):
    q = question.lower()
    return any(kw in q for kw in BROAD_KEYWORDS)

def retrieve_relevant_chunks(question, top_k=None):
    if top_k is None:
        top_k = 15 if is_broad_question(question) else 5

    question_embedding = embedder.encode([question]).tolist()
    results = collection.query(query_embeddings=question_embedding, n_results=top_k)

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })
    return chunks