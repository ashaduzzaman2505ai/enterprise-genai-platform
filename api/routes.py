from fastapi import APIRouter, HTTPException
from api.schemas import QueryRequest, QueryResponse
from generation.answer_generator import AnswerGenerator
from monitoring.latency_tracker import track_latency

router = APIRouter()
agent = AnswerGenerator()

@router.get("/health")
def health_check():
    return {"status": "healthy"}

@router.post("/query", response_model=QueryResponse)
def query_llm(request: QueryRequest):
    try:
        answer = agent.answer(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")
