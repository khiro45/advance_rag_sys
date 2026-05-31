from app.services.agentic.workflows.question_response_agent.graph import question_response_agent
from app.services.rag_sys.vector_store.vector_store import VectorStore
from app.services.rag_sys.vector_store.embedding_model import Embedding_model
from app.services.rag_sys.vector_store.data_processing import ProcessorFactory
from app.services.rag_sys.schemas import BaseMetaData

from app.configs.config import settings
from fastapi import UploadFile, HTTPException
from datetime import datetime, timezone

class RagOrchestrator:
    def __init__(self):
        # Initialize dependencies
        self.embedding_model = lambda: Embedding_model(model_name=settings.vector_store.EMBEDDING_MODEL_NAME)
        self.data_processor: ProcessorFactory = ProcessorFactory()
        self.vector_store = VectorStore(
            embedding_model=self.embedding_model,
            data_processor=self.data_processor
        )
        if settings.mlflow_tracking :
            self.init_mlflow_tracker()
           

    def init_mlflow_tracker(self  ,experiment_name:str  = "Gemini_Agent_Experiments" ):
        import mlflow
        import mlflow.langchain


        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        mlflow.set_experiment(experiment_name)
        mlflow.langchain.autolog(run_tracer_inline=True)


    async def process_query(self, user_query: str):
        print(f"Starting RAG pipeline for query: {user_query}")

        # Step 1: Sub-query expansion
        sub_queries_state = {"user_query": user_query, "sub_queries": []}
        expanded_state = sub_queries_agent.invoke(sub_queries_state)
        sub_queries = [sq.query for sq in expanded_state["sub_queries"]]
        
        if not sub_queries:
            sub_queries = [user_query]

        all_docs = []
        for query in sub_queries:
            results = await self.vector_store.get_document(query, n_results=5)
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
        final_response = await question_response_agent.invoke(response_state)
        
        return final_response["messages"][-1].content

    async def ingest_documents(self, file: UploadFile, processing_type: str ):

        if not processing_type:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Undefiend processing  format. {processing_type}"
                )

        processor = self.data_processor.get_processor(processing_type)
        
        meta_data = BaseMetaData(
            source=file.filename ,
            processor_type=processing_type , 
            date=datetime.now(timezone.utc),
            title=(file.filename ),
            tags=[],
            keywords=[]
        )
        
        text_chunks, chunk_metadatas = await processor.run_pipeline(file, meta_data)
        
        # Seed the chunks into the vector store
        self.vector_store.add_document(text_chunks, chunk_metadatas)
        
        return {"status": "success", "count": len(text_chunks)}

