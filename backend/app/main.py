from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# 라우터 임포트
from app.routers import prompt

# 환경 변수 로드
load_dotenv() # This loads variables from a .env file into environment variables.

# --- LLM Integration Note ---
# For the LLM features in this application (e.g., in app.routers.prompt) to function
# when integrated with a real LLM provider like OpenAI, an API key is required.
# The application expects the API key to be available as an environment variable.
#
# For OpenAI, set the OPENAI_API_KEY environment variable.
# If you are using a .env file (as `python-dotenv` is used here), add a line like:
# OPENAI_API_KEY="your_actual_openai_api_key_here"
#
# Make sure this key is kept secret and not committed to version control.
# The LLM client (e.g., openai.OpenAI()) will typically automatically
# detect this environment variable.
# --- End LLM Integration Note ---

app = FastAPI(
    title="프롬프트 생성기 API",
    description="사용자 입력을 바탕으로 최적화된 프롬프트를 생성하는 API",
    version="0.1.0",
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발 환경에서는 모든 출처 허용, 프로덕션에서는 특정 도메인으로 제한해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(prompt.router)

@app.get("/")
async def root():
    return {"message": "프롬프트 생성기 API에 오신 것을 환영합니다"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    uvicorn.run("app.main:app", host=host, port=port, reload=debug) 