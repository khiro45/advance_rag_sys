from sentence_transformers import CrossEncoder

# 1. Load a pre-trained reranker model
model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

query = "How do I implement a cross-encoder?"
# These would be the results returned from your Vector DB
retrieved_chunks = [
    "To implement a cross-encoder, you need a pair of sentences...",
    "Apples are generally red or green and grow on trees.",
    "Reranking helps improve RAG accuracy by re-evaluating retrieved docs."
]

# 2. Score the pairs
# The model expects a list of [query, document] pairs
pairs = [[query, chunk] for chunk in retrieved_chunks]
scores = model.predict(pairs)

# 3. Sort chunks by highest score
reranked_results = sorted(zip(scores, retrieved_chunks), reverse=True)

for score, chunk in reranked_results:
    print(f"{score:.4f} -> {chunk}")