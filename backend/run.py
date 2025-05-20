import uvicorn
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"서버 시작: {host}:{port} (디버그 모드: {debug})")
    uvicorn.run("app.main:app", host=host, port=port, reload=debug) 