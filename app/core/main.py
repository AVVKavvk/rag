from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from dotenv import load_dotenv
from app.core.routes.rag.rag_route import router as v1_rag_router
from app.core.routes.prompt_route import router as v1_prompt_router
from app.core.routes.tool_route import router as v1_tool_router
app = FastAPI()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

load_dotenv()

app.include_router(v1_rag_router, prefix="/api/v1/r")
app.include_router(v1_prompt_router, prefix="/api/v1/p")
app.include_router(v1_tool_router, prefix="/api/v1/t")


@app.get("/")
def index():
    return {"server is running"}
