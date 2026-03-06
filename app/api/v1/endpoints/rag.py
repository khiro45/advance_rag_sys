from fastapi import APIRouter, HTTPException
from app.schemas.rag import RagQueryRequest, RagQueryResponse, RagIngestRequest, RagIngestResponse
from app.orchestrators.rag_orchestrator import RagOrchestrator

router = APIRouter()
orchestrator = RagOrchestrator()

@router.post("/query", response_model=RagQueryResponse)
async def query_rag(request: RagQueryRequest):
    """
    Endpoint to process a RAG query through the full pipeline.
    """
    try:
        answer = orchestrator.process_query(request.query)
        return RagQueryResponse(answer=answer)
    except Exception as e:
        print(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ingest", response_model=RagIngestResponse)
async def ingest_docs(request: RagIngestRequest):
    """
    Endpoint to ingest documents into the vector store.
    """
    try:
        result = orchestrator.ingest_documents(request.documents, request.metadata)
        return RagIngestResponse(**result)
    except Exception as e:
        print(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
