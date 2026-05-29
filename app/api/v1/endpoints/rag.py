from fastapi import APIRouter, HTTPException , UploadFile, File, Form
from app.schemas.rag import RagQueryRequest, RagQueryResponse, RagIngestRequest, RagIngestResponse , ChatInput
from app.orchestrators.rag_orchestrator import RagOrchestrator
from pydantic import ValidationError
router = APIRouter()
orchestrator = RagOrchestrator()

@router.post("/query")
async def query_rag(request: RagQueryRequest):
    """
    Endpoint to process a RAG query through the full pipeline.
    """
    try:
        answer = await  orchestrator.process_query(request.query)
        return RagQueryResponse(answer=answer)
    except Exception as e:
        print(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/Chat')
async def chat(req:ChatInput ):
    pass


@router.post("/ingest")
async def ingest_docs(
    file:UploadFile = File()):

    try:

    
        result =  await orchestrator.ingest_documents(file)
        return RagIngestResponse(**result)
    except Exception as e:
        print(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
