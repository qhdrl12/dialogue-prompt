from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
    responses={404: {"description": "Not found"}},
)

class PromptInput(BaseModel):
    keywords: str
    additional_info: Optional[dict] = None

class PromptOutput(BaseModel):
    prompt: str
    description: str

class PromptResponse(BaseModel):
    prompts: List[PromptOutput]

@router.post("/generate", response_model=PromptResponse)
async def generate_prompt(input_data: PromptInput):
    """
    키워드 및 추가 정보를 기반으로 최적화된 프롬프트를 생성합니다.
    """
    try:
        # 실제 프롬프트 생성 로직은 추후 Langchain/Langgraph로 구현
        # 현재는 더미 데이터 반환
        return {
            "prompts": [
                {
                    "prompt": f"당신은 전문 {input_data.keywords} 전문가입니다. 다음 주제에 대해 상세하고 유용한 정보를 제공해주세요.",
                    "description": "전문가 역할을 부여하는 기본 프롬프트"
                },
                {
                    "prompt": f"{input_data.keywords}에 대한 장점과 단점을 5가지씩 구체적인 예시와 함께 설명해주세요.",
                    "description": "장단점 분석을 요청하는 프롬프트"
                },
                {
                    "prompt": f"{input_data.keywords}에 대한 최신 트렌드와 미래 전망을 데이터와 함께 분석해주세요.",
                    "description": "트렌드 분석을 요청하는 프롬프트"
                }
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"프롬프트 생성 중 오류 발생: {str(e)}")

@router.post("/test", response_model=dict)
async def test_prompt(prompt: str, model: Optional[str] = None):
    """
    생성된 프롬프트를 LLM API로 테스트하고 결과를 반환합니다.
    """
    try:
        # 실제 LLM API 호출 로직은 추후 구현
        # 현재는 더미 데이터 반환
        return {
            "result": f"프롬프트 '{prompt}'에 대한 LLM 응답 결과입니다. 모델: {model or '기본 모델'}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM API 호출 중 오류 발생: {str(e)}") 