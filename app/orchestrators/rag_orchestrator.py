from app.services.agentic.workflows.sub_queries_agent.graph import sub_queries_agent
from app.services.agentic.workflows.question_response_agent.graph import question_response_agent
from app.services.rag_sys.vector_store.vector_store import VectorStore
from app.services.rag_sys.vector_store.embedding_model import Embedding_model
from app.services.rag_sys.vector_store.data_processing import ProcessorFactory
from app.configs.config import settings

class RagOrchestrator:
    def __init__(self):
        # Initialize Vector Store with its dependencies
        self.embedding_model = lambda: Embedding_model(model_name=settings.vector_store.EMBEDDING_MODEL_NAME)
        self.vector_store = VectorStore(
            embedding_model=self.embedding_model,
            data_processor=ProcessorFactory
        )

    def process_query(self, user_query: str):
        """
        Executes the full RAG pipeline:
        1. Sub-query expansion
        2. Vector retrieval for each sub-query
        3. Reranking of results
        4. Final response generation
        """
        print(f"Starting RAG pipeline for query: {user_query}")

        # Step 1: Sub-query expansion
        sub_queries_state = {"user_query": user_query, "sub_queries": []}
        expanded_state = sub_queries_agent.invoke(sub_queries_state)
        sub_queries = [sq.query for sq in expanded_state["sub_queries"]]
        
        if not sub_queries:
            sub_queries = [user_query]
            
        print(f"Expanded into sub-queries: {sub_queries}")

        # Step 2: Vector retrieval
        all_docs = []
        for query in sub_queries:
            results = self.vector_store.get_document(query, n_results=5)
            # results['documents'] is a list of lists (one list per query_text)
            if results and results.get("documents"):
                for doc in results["documents"][0]:
                    all_docs.append({"doc": doc})

        print(f"Retrieved {len(all_docs)} documents.")

        # Step 3: Reranking (if we have results)
        if all_docs:
            reranked_docs = self.vector_store.cross_encoder_reranking(user_query, all_docs, n_results=5)
            # cross_encoder_reranking returns list of [[doc_dict, score], ...]
            # We want just the doc_dict for the final step
            final_context_docs = [item[0] for item in reranked_docs]
        else:
            final_context_docs = []

        # Step 4: Final response generation
        response_state = {
            "messages": [{"role": "user", "content": user_query}],
            "docs": final_context_docs
        }
        final_response = question_response_agent.invoke(response_state)
        
        return final_response["messages"][-1].content

    def ingest_documents(self, documents: list[str], metadata: list[dict]):
        """Ingests documents into the vector store."""
        # Ensure metadata is provided for each document
        if not metadata:
            metadata = [{}] * len(documents)
            
        self.vector_store.seed_data(documents, metadata)
        return {"status": "success", "count": len(documents)}
