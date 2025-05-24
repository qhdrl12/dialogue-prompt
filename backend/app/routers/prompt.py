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
    # LLM을 사용하여 요구사항 명확성 평가
    # TODO: Replace placeholder LLM calls with actual API calls using a library like 'openai'.
    # Ensure your OPENAI_API_KEY is set as an environment variable.
    # Example:
    # import os
    # import openai
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    #
    # client = openai.OpenAI() # Initialize client
    #
    # response = client.chat.completions.create(
    # model="gpt-3.5-turbo", # Or another suitable model
    # messages=[...] # Construct your messages for the LLM
    # )
    # result = response.choices[0].message.content

    # ---- LLM 호출 placeholder ----
    try:
        # 개념적 LLM 프롬프트 구성
        prompt_to_llm = f"""사용자 입력 키워드: "{keywords}"
사용자 추가 정보: {additional_info if additional_info else "없음"}

위 사용자 입력을 분석하여 고품질의 구체적인 프롬프트를 생성하기에 정보가 충분한지 판단해주세요.
만약 정보가 불충분하다면, 어떤 유형의 정보가 누락되었거나 불명확한지 다음 식별자 목록에서 선택하여 알려주세요:
['topic', 'target_audience', 'goal', 'tone', 'format', 'context', 'specific_details']

응답은 다음 JSON 형식으로 제공해주세요:
{{
  "is_clear": true/false,
  "missing_info_types": ["type1", "type2", ...], // is_clear가 false일 경우에만 포함
  "reason_if_unclear": "한국어로 작성된 설명" // is_clear가 false일 경우에만 포함
}}

예시 1 (불명확):
입력: "블로그 게시물 작성"
응답:
{{
  "is_clear": false,
  "missing_info_types": ["topic", "target_audience", "tone", "goal"],
  "reason_if_unclear": "블로그 게시물을 작성하기 위한 주제, 대상 독자, 원하는 어조, 게시물의 구체적인 목표 등의 정보가 필요합니다."
}}

예시 2 (명확):
입력: "인공지능 마케팅 자동화 도구에 대한 블로그 게시물 작성. 대상은 IT 전문가. 어조는 전문적이고 분석적으로. 목표는 최신 기술 동향 소개."
응답:
{{
  "is_clear": true
}}
"""
        
        # --- 시뮬레이션된 LLM 응답 ---
        # 실제 LLM API 호출 결과를 이 구조에 맞게 파싱해야 합니다.
        # 이 부분은 실제 LLM 연동 시 API 응답을 기반으로 수정됩니다.
        # 여기서는 입력 키워드 길이를 기반으로 간단히 시뮬레이션합니다.
        if len(keywords.strip()) < 10 and not additional_info: # 매우 기본적인 조건으로 시뮬레이션
            simulated_llm_response = {
                "is_clear": False,
                "missing_info_types": ["topic", "target_audience", "specific_details"],
                "reason_if_unclear": f"'{keywords}'에 대한 주제, 대상 독자, 그리고 더 구체적인 내용이 필요합니다. 어떤 종류의 콘텐츠를 원하시는지, 누구를 위한 것인지 알려주세요."
            }
        elif '목표' not in (additional_info.keys() if additional_info else []) and 'goal' not in (additional_info.keys() if additional_info else []):
             simulated_llm_response = {
                "is_clear": False,
                "missing_info_types": ["goal"],
                "reason_if_unclear": "콘텐츠 생성의 주요 목표(예: 정보 제공, 설득, 문제 해결 등)를 알려주시면 좋겠습니다."
            }
        else:
            simulated_llm_response = {
                "is_clear": True
            }
        # --- LLM 호출 placeholder 끝 ---

        is_clear = simulated_llm_response.get('is_clear', False)
        
        if not is_clear:
            missing_info = simulated_llm_response.get('missing_info_types', [])
            feedback = simulated_llm_response.get('reason_if_unclear', "요청을 처리하기 위한 추가 정보가 필요합니다. 어떤 종류의 콘텐츠를 원하시는지, 누구를 위한 것인지, 무엇을 위한 것인지 등을 더 자세히 알려주세요.")
        else:
            missing_info = []
            feedback = "충분한 정보가 제공되어 프롬프트 생성 준비가 되었습니다."

    except Exception as e:
        # LLM API 호출 중 오류 발생 시 처리 (실제 구현에서는 로깅 등을 추가)
        print(f"LLM API 호출 중 오류 발생 (시뮬레이션): {str(e)}") # 실제 운영에서는 더 견고한 로깅 필요
        is_clear = False # 오류 발생 시 불명확으로 간주하고 일반적인 추가 정보 요청
        missing_info = ['target_audience', 'goal', 'specific_details'] # 일반적인 누락 정보
        feedback = "요구사항을 분석하는 중 오류가 발생했습니다. 콘텐츠의 대상, 목적, 그리고 구체적인 내용을 알려주시면 진행에 도움이 됩니다."

    return {
        'is_clear': is_clear,
        'feedback': feedback,
        'missing_info': missing_info
    }

# 기존 all_questions는 LLM 실패 시 fallback으로 사용하기 위해 유지
PREDEFINED_QUESTIONS = {
    'target_audience': Question(
        id='target_audience', # ID 통일성을 위해 'target' -> 'target_audience'
        question='대상 독자/고객은 누구인가요? (예: 일반 사용자, 전문가, 학생 등)',
        options=['일반 사용자', '전문가/개발자', '학생', '비즈니스 리더', '특정 연령대'],
        explanation='타겟 독자/고객을 명확히 하면 콘텐츠의 언어, 깊이, 스타일을 최적화할 수 있습니다.'
    ),
    'tone': Question(
        id='tone',
        question='원하는 콘텐츠의 톤앤매너는 무엇인가요? (예: 전문적, 친근한, 유머러스 등)',
        options=['전문적/학술적', '친근한/대화체', '간결한/명확한', '창의적/영감을 주는', '유머러스한'],
        explanation='콘텐츠의 톤은 독자에게 전달되는 느낌과 메시지 수용 방식에 큰 영향을 미칩니다.'
    ),
    'goal': Question(
        id='goal',
        question='이 콘텐츠를 통해 달성하고자 하는 주요 목표는 무엇인가요? (예: 정보 제공, 설득, 문제 해결 등)',
        options=['정보 제공', '제품/서비스 홍보', '설득/제안', '문제 해결', '아이디어 브레인스토밍', '교육/학습'],
        explanation='명확한 목표 설정은 콘텐츠의 방향성과 구조를 결정하는 데 도움을 줍니다.'
    ),
    'specific_details': Question( # ID 통일성을 위해 'detail' -> 'specific_details'
        id='specific_details',
        question='콘텐츠에 포함되어야 할 구체적인 내용, 주제, 또는 키워드가 있나요?',
        explanation='구체적인 정보가 많을수록 사용자의 의도에 더 부합하는 콘텐츠를 생성할 수 있습니다.'
    ),
    'topic': Question(
        id='topic',
        question=f"주요 주제나 아이템이 무엇인지 명확히 알려주세요.",
        explanation="생성할 콘텐츠의 핵심 주제를 알아야 합니다."
    ),
    'format': Question(
        id='format',
        question='원하는 콘텐츠의 형식이나 구조가 있나요? (예: 블로그 글, 보고서, 이메일, 목록 형식 등)',
        options=['블로그 게시물', 'SNS 게시물', '이메일 초안', '보고서 형식', 'Q&A 형식', '목록/요약'],
        explanation='콘텐츠의 형식을 지정하면 의도한 목적과 플랫폼에 더 적합한 결과물을 얻을 수 있습니다.'
    ),
    'context': Question(
        id='context',
        question='콘텐츠가 사용될 배경이나 맥락에 대해 추가적으로 알려주실 정보가 있나요?',
        explanation='배경 정보를 이해하면 더욱 관련성 높고 효과적인 콘텐츠를 생성하는 데 도움이 됩니다.'
    )
}

def get_questions_for_missing_info(missing_info: List[str], keywords: str) -> List[Question]:
    """
    부족한 정보 유형과 사용자 키워드를 기반으로 LLM을 사용하여 질문 목록을 생성합니다.
    LLM 실패 시 미리 정의된 질문으로 대체(fallback)합니다.
    """
    generated_questions: List[Question] = []

    for info_type in missing_info:
        llm_generated_question = None
        try:
            # ---- LLM 호출 placeholder ----
            # TODO: Replace placeholder LLM calls with actual API calls using a library like 'openai'.
            # Ensure your OPENAI_API_KEY is set as an environment variable. (See example in evaluate_requirement_clarity)
            # 실제 LLM API 호출로 대체되어야 합니다.
            
            # 개념적 LLM 프롬프트 구성 (info_type과 keywords 사용)
            prompt_to_llm_for_question = f"""사용자 주요 키워드: "{keywords}"
부족한 정보 유형: "{info_type}"

위 정보를 바탕으로, 사용자에게 '{info_type}'에 대해 구체적으로 질문하여 명확한 답변을 유도할 수 있는 질문을 한국어로 생성해주세요.
질문은 사용자가 쉽게 이해하고 답변할 수 있도록 명확하고 간결해야 합니다.
가능하다면, 답변 선택에 도움이 될 수 있는 예시 옵션(options)과 질문의 필요성에 대한 간단한 설명(explanation)도 한국어로 함께 제공해주세요.

응답은 다음 JSON 형식으로 제공해주세요:
{{
  "question": "생성된 질문 내용",
  "options": ["옵션1", "옵션2", ...], // 선택 사항, 없을 경우 빈 리스트 또는 null
  "explanation": "질문의 필요성에 대한 설명" // 선택 사항
}}

예시:
키워드: "친환경 세제 개발"
부족한 정보 유형: "target_audience"
LLM 응답:
{{
  "question": "개발하시는 친환경 세제의 주요 타겟 고객층은 누구인가요? (예: 영유아 가정, 특정 피부 타입을 가진 사람들 등)",
  "options": ["영유아를 둔 가정", "민감성 피부를 가진 성인", "환경 의식이 높은 1인 가구", "특정 알러지가 있는 사람"],
  "explanation": "타겟 고객을 명확히 하면 제품의 특징과 마케팅 방향을 더 효과적으로 설정할 수 있습니다."
}}
"""
            # --- 시뮬레이션된 LLM 응답 ---
            # 이 부분은 실제 LLM 연동 시 API 응답을 기반으로 수정됩니다.
            simulated_llm_responses = {
                "target_audience": {
                    "question": f"'{keywords}' 관련하여 생각하시는 주요 대상 고객은 누구인가요? 구체적인 그룹을 알려주시면 좋습니다 (예: 20대 여성, IT 개발자 등).",
                    "options": ["10대 학생", "20-30대 직장인", "자영업자", "특정 산업 전문가", "주부"],
                    "explanation": "대상 고객을 명확히 하면 콘텐츠의 어투, 스타일, 채널 선택에 도움이 됩니다."
                },
                "goal": {
                    "question": f"'{keywords}'를 통해 궁극적으로 달성하고자 하는 목표는 무엇인가요? (예: 정보 전달, 제품 판매 증진, 브랜드 인지도 향상 등)",
                    "options": ["정보 공유 및 확산", "학습 및 지식 전달", "제품/서비스 홍보", "고객 문의 해결", "특정 행동 유도"],
                    "explanation": "목표를 알아야 해당 목표 달성에 가장 효과적인 콘텐츠 방향을 설정할 수 있습니다."
                },
                "specific_details": { # 'detail' 대신 'specific_details' 사용 가정
                    "question": f"'{keywords}'에 대해 반드시 포함되어야 하거나 강조하고 싶은 세부 사항이 있나요?",
                    "explanation": "구체적인 요구사항을 알려주시면 더욱 만족스러운 결과물을 만들 수 있습니다."
                }
                # 다른 info_type에 대한 시뮬레이션 응답도 필요에 따라 추가 가능
            }

            if info_type in simulated_llm_responses:
                # 간단한 시뮬레이션: info_type에 따라 미리 정의된 "LLM 응답"을 사용
                # 실제로는 여기서 LLM API를 호출하고 그 결과를 파싱합니다.
                # Randomly simulate LLM failure for demonstration
                # import random
                # if random.random() < 0.3: # 30% chance of simulated failure
                #     raise Exception("Simulated LLM API error")

                response_data = simulated_llm_responses[info_type]
                llm_generated_question = Question(
                    id=info_type,
                    question=response_data["question"],
                    options=response_data.get("options"),
                    explanation=response_data.get("explanation")
                )
                print(f"LLM (simulated) generated question for {info_type} based on '{keywords}'")
            else:
                # 시뮬레이션에서 해당 info_type에 대한 응답이 없으면 "실패"로 간주
                print(f"LLM (simulated) did not provide a question for {info_type}, attempting fallback.")
                pass # Fallback to predefined will be handled outside this if/else

        except Exception as e:
            print(f"LLM (simulated) call failed for info_type '{info_type}' with keywords '{keywords}': {str(e)}")
            # LLM 호출 실패 시 llm_generated_question은 None으로 유지되어 fallback 로직이 실행됨

        if llm_generated_question:
            generated_questions.append(llm_generated_question)
        else:
            # LLM 실패 또는 부적절한 응답 시, 미리 정의된 질문으로 fallback
            if info_type in PREDEFINED_QUESTIONS:
                print(f"Using predefined question for {info_type}")
                generated_questions.append(PREDEFINED_QUESTIONS[info_type])
            else:
                # PREDEFINED_QUESTIONS에도 없는 경우, 기본적인 질문 생성 또는 경고
                print(f"Warning: No predefined question found for {info_type}. Creating a generic one.")
                generated_questions.append(Question(
                    id=info_type,
                    question=f"{info_type}에 대해 더 자세한 정보를 알려주세요.",
                    explanation="이 정보는 콘텐츠의 품질을 높이는 데 도움이 됩니다."
                ))
                
    return generated_questions

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
            # Bug Fix: Pass input_data.keywords to get_questions_for_missing_info
            questions = get_questions_for_missing_info(clarity_result['missing_info'], input_data.keywords)
            
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
        
        # 요구사항이 명확한 경우 LLM을 사용하여 프롬프트 생성
        generated_prompts: List[PromptOutput] = []
        try:
            # ---- LLM 호출 placeholder ----
            # TODO: Replace placeholder LLM calls with actual API calls using a library like 'openai'.
            # Ensure your OPENAI_API_KEY is set as an environment variable. (See example in evaluate_requirement_clarity)
            # 실제 LLM API 호출로 대체되어야 합니다. (e.g., using OpenAI client)
            # conceptual_prompt_for_llm 구성
            llm_instruction = (
                "당신은 사용자의 요구사항에 맞춰 다양하고 창의적인 LLM 프롬프트를 생성하는 전문가입니다. "
                "각 프롬프트는 고유한 접근 방식이나 관점을 가져야 하며, 한국어로 작성되어야 합니다. "
                "각 프롬프트에 대해 해당 프롬프트의 유용성이나 특징을 설명하는 짧은 한국어 설명을 함께 제공해주세요."
            )
            user_model_preference = f" (선호 모델: {input_data.model})" if input_data.model else ""

            # additional_info에서 주요 정보 추출 (예시, 실제로는 더 많은 정보를 활용할 수 있음)
            target_audience_info = additional_info.get('target_audience', '지정되지 않음')
            goal_info = additional_info.get('goal', '지정되지 않음')
            tone_info = additional_info.get('tone', '지정되지 않음')
            format_info = additional_info.get('format', '지정되지 않음')
            context_info = additional_info.get('context', '없음')
            specific_details_info = additional_info.get('specific_details', '없음')


            conceptual_prompt_for_llm = f"""{llm_instruction}

사용자 주요 키워드: "{input_data.keywords}"{user_model_preference}
사용자 제공 추가 정보:
- 대상: {target_audience_info}
- 목표: {goal_info}
- 어조: {tone_info}
- 형식: {format_info}
- 맥락: {context_info}
- 세부사항: {specific_details_info}

위 정보를 바탕으로, 사용자가 최종 목표를 달성하는 데 도움이 될 만한 LLM용 프롬프트 2-3개를 생성해주세요.
각 프롬프트는 'prompt' 필드에, 설명은 'description' 필드에 담아 JSON 객체 리스트 형태로 반환해주세요.

예시 JSON 응답 형식:
[
    {{
        "prompt": "생성된 프롬프트 텍스트...",
        "description": "프롬프트에 대한 설명..."
    }},
    {{
        "prompt": "다른 관점의 프롬프트 텍스트...",
        "description": "이 프롬프트의 특징 설명..."
    }}
]
"""
            print(f"--- Conceptual LLM Prompt for Prompt Generation ---\n{conceptual_prompt_for_llm}\n-------------------------------------------------")

            # --- 시뮬레이션된 LLM 응답 ---
            # 실제 LLM API 호출 결과를 이 구조에 맞게 파싱해야 합니다.
            # 이 부분은 실제 LLM 연동 시 API 응답을 기반으로 수정됩니다.
            if "학습 계획" in input_data.keywords and target_audience_info == "대학생":
                simulated_llm_output = [
                    {
                        "prompt": f"당신은 '{target_audience_info}'들의 학습 효율을 극대화하는 AI 학습 플래너입니다. '{input_data.keywords}' 주제에 대해, '{goal_info}'을 달성할 수 있도록, '{tone_info}' 어조로 개인화된 1주 학습 계획을 한국어로 작성해주세요. 매일의 학습 목표, 추천 자료, 복습 팁을 포함해야 합니다.",
                        "description": "AI 학습 플래너 역할을 부여하여, 사용자의 구체적인 목표와 대상에 맞춘 상세 학습 계획 생성을 유도하는 프롬프트입니다."
                    },
                    {
                        "prompt": f"'{input_data.keywords}' 관련하여 '{target_audience_info}'이 겪을 수 있는 주요 어려움 3가지를 식별하고, 각 어려움에 대한 실질적인 해결책과 '{tone_info}' 격려 메시지를 포함한 조언을 한국어로 제공해주세요. '{goal_info}' 달성에 초점을 맞춥니다.",
                        "description": "문제 해결 중심적 접근으로, 사용자의 잠재적 어려움을 예측하고 극복 방안을 제시하는 지원형 프롬프트입니다."
                    },
                    {
                        "prompt": f"'{input_data.keywords}'를 주제로 '{target_audience_info}' 대상의 창의적인 아이디어 발상 세션을 진행한다고 가정합니다. '{goal_info}'를 돕기 위해, 브레인스토밍을 촉진하는 독특한 질문 5가지를 '{tone_info}' 스타일로 한국어로 제시해주세요.",
                        "description": "창의적 사고와 아이디어 발상을 자극하기 위한 질문 생성 프롬프트입니다."
                    }
                ]
            elif "보고서" in input_data.keywords:
                 simulated_llm_output = [
                    {
                        "prompt": f"'{input_data.keywords}'에 대한 전문적인 보고서를 작성해야 합니다. 주요 분석 내용, 데이터 시각화 제안, 그리고 결론 및 권장 사항을 포함한 상세 목차를 '{target_audience_info}'를 고려하여 '{tone_info}' 톤으로 한국어로 구성해주세요.",
                        "description": "보고서 작성을 위한 체계적인 목차 구성을 돕는 프롬프트입니다."
                    },
                    {
                        "prompt": f"'{input_data.keywords}'의 핵심 내용을 요약하고, 이와 관련된 통계 자료나 최신 연구 결과를 3가지 이상 인용하여 간결한 요약 보고서를 '{goal_info}' 목적으로 한국어로 작성해주세요. '{format_info}' 형식을 고려해주세요.",
                        "description": "데이터 기반의 요약 보고서 생성을 위한 프롬프트입니다."
                    }
                ]
            else: # 일반적인 경우
                simulated_llm_output = [
                    {
                        "prompt": f"'{input_data.keywords}'에 대해 {target_audience_info}를 대상으로 하여 {goal_info}을 이루기 위한 핵심 아이디어를 {tone_info} 어조로 설명하는 글을 작성해주세요.",
                        "description": "기본 정보를 바탕으로 콘텐츠 초안 생성을 유도하는 일반적인 프롬프트입니다."
                    },
                    {
                        "prompt": f"'{input_data.keywords}'의 주요 장점과 단점을 각각 3가지씩 {target_audience_info}가 이해하기 쉽게 {tone_info} 어조로 비교 분석하는 내용을 작성해주세요. {goal_info}에 부합하도록 해주세요.",
                        "description": "장단점 비교 분석을 통해 균형 잡힌 시각을 제공하는 프롬프트입니다."
                    }
                ]
            # --- LLM 호출 placeholder 끝 ---

            for item in simulated_llm_output:
                generated_prompts.append(PromptOutput(prompt=item["prompt"], description=item["description"]))
            
            if not generated_prompts: # LLM이 빈 결과를 반환한 경우 (시뮬레이션에서는 거의 발생 안함)
                 print("LLM (simulated) returned no prompts. Providing a default prompt.")
                 generated_prompts.append(PromptOutput(
                     prompt=f"'{input_data.keywords}'에 대한 일반적인 정보를 생성해주세요.",
                     description="기본 요청을 처리하기 위한 일반 프롬프트입니다."
                 ))

        except Exception as e_llm:
            print(f"LLM (simulated) call for prompt generation failed: {str(e_llm)}")
            # LLM 호출 실패 시, 사용자에게 안내할 수 있는 기본 프롬프트 또는 빈 리스트 반환
            # 여기서는 빈 리스트를 반환하고, 실제 운영 시에는 좀 더 사용자 친화적인 처리가 필요할 수 있음
            generated_prompts = [] # 오류 발생 시 빈 리스트로 초기화
            # 또는 오류 상황을 알리는 특정 프롬프트를 추가할 수도 있습니다.
            # generated_prompts.append(PromptOutput(
            #     prompt="프롬프트 생성 중 오류가 발생했습니다. 다시 시도해주세요.",
            #     description="오류 안내"
            # ))

        return PromptResponseSuccess(
            prompts=generated_prompts,
            needMoreInfo=False
        )
    except Exception as e:
        print(f"Error in generate_prompt: {str(e)}") # generate_prompt 함수의 전반적인 오류
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