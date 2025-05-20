from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

router = APIRouter(
    prefix="/prompt",
    tags=["prompt"],
    responses={404: {"description": "Not found"}},
)

class PromptInput(BaseModel):
    keywords: str
    model: Optional[str] = None
    additional_info: Optional[Dict[str, str]] = None
    additionalInfo: Optional[Dict[str, str]] = Field(None, alias="additional_info")

    class Config:
        populate_by_name = True

class PromptOutput(BaseModel):
    prompt: str
    description: str

class Question(BaseModel):
    id: str
    question: str
    answer: str = ""
    options: Optional[List[str]] = None
    explanation: Optional[str] = None

class PromptResponseSuccess(BaseModel):
    prompts: List[PromptOutput]
    needMoreInfo: bool = False

class PromptResponseNeedInfo(BaseModel):
    needMoreInfo: bool = True
    feedback: str
    questions: List[Question]
    prompts: List[PromptOutput] = []

PromptResponse = Union[PromptResponseSuccess, PromptResponseNeedInfo]

def evaluate_requirement_clarity(keywords: str, additional_info: Optional[Dict[str, str]] = None) -> dict:
    """
    LLM을 사용하여 사용자 요구사항의 명확성을 평가하고, 필요한 추가 정보를 결정합니다.
    실제 구현에서는 OpenAI API 또는 다른 LLM API를 호출합니다.

    Returns:
        dict: {
            'is_clear': bool - 요구사항이 충분히 명확한지 여부
            'feedback': str - 피드백 메시지
            'missing_info': list - 부족한 정보 유형 목록
        }
    """
    # 실제 구현에서는 LLM API 호출로 대체됩니다
    # 현재는 간단한 키워드 기반 평가로 더미 구현
    
    # 1. 기본 정보가 이미 제공되었는지 확인
    has_target_audience = additional_info and 'target' in additional_info and additional_info['target']
    has_tone = additional_info and 'tone' in additional_info and additional_info['tone']
    has_goal = additional_info and 'goal' in additional_info and additional_info['goal']
    
    # 2. 키워드 길이 체크 (너무 짧으면 불명확할 가능성 높음)
    keyword_too_short = len(keywords.strip()) < 5
    
    # 목적이나 대상 관련 키워드가 포함되어 있는지 확인
    purpose_keywords = ['위한', '목적', '만들기', '생성', '개발', '작성', '분석']
    has_purpose_hint = any(kw in keywords for kw in purpose_keywords)
    
    audience_keywords = ['사용자', '고객', '독자', '학생', '개발자', '비즈니스', '전문가']
    has_audience_hint = any(kw in keywords for kw in audience_keywords)
    
    # 부족한 정보 결정
    missing_info = []
    if not has_target_audience and not has_audience_hint:
        missing_info.append('target')
    
    if not has_tone:
        missing_info.append('tone')
        
    if not has_goal and not has_purpose_hint:
        missing_info.append('goal')
        
    if keyword_too_short and len(missing_info) > 0:
        missing_info.append('detail')
    
    # 명확성 판단 (필요한 정보가 없으면 불명확)
    is_clear = len(missing_info) == 0
    
    # 피드백 메시지 생성
    if not is_clear:
        if 'detail' in missing_info:
            feedback = f"'{keywords}' 키워드가 너무 짧거나 모호합니다. 더 구체적인 정보가 필요합니다."
        elif 'target' in missing_info and 'goal' in missing_info:
            feedback = f"'{keywords}'에 대한 대상 독자와 생성 목적을 알려주시면 더 최적화된 프롬프트를 생성할 수 있습니다."
        elif 'target' in missing_info:
            feedback = f"'{keywords}'에 대한 타겟 대상이 누구인지 알려주시면 더 적합한 프롬프트를 생성할 수 있습니다."
        elif 'goal' in missing_info:
            feedback = f"'{keywords}'에 대한 프롬프트의 목적이 무엇인지 알려주시면 더 효과적인 프롬프트를 생성할 수 있습니다."
        else:
            feedback = "더 명확한 프롬프트를 생성하기 위해 추가 정보가 필요합니다."
    else:
        feedback = "충분한 정보가 제공되었습니다."
    
    return {
        'is_clear': is_clear,
        'feedback': feedback,
        'missing_info': missing_info
    }

def get_questions_for_missing_info(missing_info: List[str]) -> List[Question]:
    """
    부족한 정보 유형에 따라 사용자에게 요청할 질문 목록을 반환합니다.
    """
    all_questions = {
        'target': Question(
            id='target',
            question='대상 독자/고객은 누구인가요?',
            options=['일반 사용자', '전문가/개발자', '학생', '비즈니스 리더'],
            explanation='대상을 명확히 하면 더 적절한 언어와 전문성 수준을 선택할 수 있습니다.'
        ),
        'tone': Question(
            id='tone',
            question='어떤 톤과 스타일로 작성할까요?',
            options=['전문적/학술적', '친근한/대화체', '간결한/명확한', '창의적/영감을 주는'],
            explanation='글의 톤은 메시지 전달 방식에 큰 영향을 미칩니다.'
        ),
        'goal': Question(
            id='goal',
            question='주요 목표는 무엇인가요?',
            options=['정보 제공', '설득/제안', '문제 해결', '아이디어 브레인스토밍'],
            explanation='목표에 따라 프롬프트의 구조와 접근 방식이 달라집니다.'
        ),
        'detail': Question(
            id='detail',
            question='주제에 대해 더 구체적인 설명을 해주세요.',
            explanation='구체적인 정보가 많을수록 더 정확한 프롬프트를 생성할 수 있습니다.'
        )
    }
    
    return [all_questions[info_type] for info_type in missing_info if info_type in all_questions]

@router.post("/generate", response_model=PromptResponse)
async def generate_prompt(input_data: PromptInput):
    """
    키워드 및 추가 정보를 기반으로 최적화된 프롬프트를 생성합니다.
    요구사항이 불명확한 경우 추가 정보를 요청합니다.
    """
    try:
        print(f"Received request: {input_data}")
        
        # Use additionalInfo if provided, fall back to additional_info
        additional_info = input_data.additionalInfo or input_data.additional_info
        
        # 요구사항 명확성 평가
        clarity_result = evaluate_requirement_clarity(input_data.keywords, additional_info)
        
        # 요구사항이 충분히 명확한지 확인
        if not clarity_result['is_clear']:
            # 추가 정보 요청
            questions = get_questions_for_missing_info(clarity_result['missing_info'])
            
            # 사용자가 이미 답변한 질문은 업데이트
            if additional_info:
                for q in questions:
                    if q.id in additional_info and additional_info[q.id]:
                        q.answer = additional_info[q.id]
            
            return PromptResponseNeedInfo(
                needMoreInfo=True,
                feedback=clarity_result['feedback'],
                questions=questions
            )
        
        # 요구사항이 명확한 경우 프롬프트 생성
        # 실제 프롬프트 생성 로직은 추후 Langchain/Langgraph로 구현
        # 현재는 더미 데이터 반환
        model_info = f" using {input_data.model}" if input_data.model else ""
        
        target_audience = additional_info.get('target', '일반 독자') if additional_info else '일반 독자'
        tone = additional_info.get('tone', '전문적') if additional_info else '전문적'
        goal = additional_info.get('goal', '정보 제공') if additional_info else '정보 제공'
        
        return PromptResponseSuccess(
            prompts=[
                {
                    "prompt": f"당신은 전문 {input_data.keywords} 전문가입니다. {target_audience}를 위해 {tone} 톤으로 {goal}을 목적으로 하는 콘텐츠를 작성해주세요.",
                    "description": "맞춤형 전문가 프롬프트"
                },
                {
                    "prompt": f"{input_data.keywords}에 대한 장점과 단점을 5가지씩 구체적인 예시와 함께 {target_audience}가 이해하기 쉬운 {tone} 방식으로 설명해주세요.",
                    "description": "장단점 분석 프롬프트"
                },
                {
                    "prompt": f"{input_data.keywords}에 대한 최신 트렌드와 미래 전망을 {tone} 스타일로 {target_audience}를 위해 분석해주세요. {goal}에 초점을 맞춰주세요.",
                    "description": "트렌드 분석 프롬프트"
                }
            ],
            needMoreInfo=False
        )
    except Exception as e:
        print(f"Error: {str(e)}")
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