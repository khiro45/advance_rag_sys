from fastapi import APIRouter, HTTPException , UploadFile, File, Form
from app.schemas.rag import RagQueryRequest, RagQueryResponse, RagIngestRequest, RagIngestResponse , ChatInput
from app.services.rag_sys.schemas import BaseMetaData
from app.orchestrators.rag_orchestrator import RagOrchestrator
from app.services.rag_sys.vector_store.data_processing import ProcessorType 
from pydantic import BaseModel, Json, Field
router = APIRouter()
orchestrator = RagOrchestrator()

@router.post("/query")
async def query_rag(request: RagQueryRequest):
    try:
        answer = await  orchestrator.process_query(request.query)
        return RagQueryResponse(answer=answer)
    except Exception as e:
        print(f"Error processing RAG query: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/Chat')
async def chat(req:ChatInput ):
    try:
        responce = await orchestrator.chat(input_text , session_id )
    except Exception as e :
        raise HTTPException(status_code=500 , detail=str(e))


@router.post("/ingest")
async def ingest_docs(
    file:UploadFile = File()  , 
    data_processors_type= Form(...)
    ):
    try:

        if data_processors_type in ProcessorType._value2member_map_:
            result =  await orchestrator.ingest_documents(file  , data_processors_type)
            return RagIngestResponse(**result)
        else:
            raise HTTPException(status_code=400, detail="inserted data_processors_type is not supported ")

    except Exception as e:
        print(f"Error ingesting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
