import os
# ==============================================================================
# [新增] 禁用所有已知遥测与数据收集 (必须在导入其他库之前设置)
# ==============================================================================
os.environ["LANGCHAIN_TRACING_V2"] = "false"
os.environ["LANGCHAIN_TRACING"] = "false"  # [新增] 禁用旧版追踪
os.environ["LANGSMITH_TRACING"] = "false"  # [新增] 显式禁用 LangSmith
os.environ["LANGCHAIN_PROJECT"] = "local-mind-api"
# 禁用 ChromaDB 遥测
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY_IMPL"] = "api.telemetry.NoOpTelemetry" 
# 禁用 HuggingFace 遥测
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
# 通用防追踪标准
os.environ["DO_NOT_TRACK"] = "1"
# 禁用 PostHog (Chroma 内部可能使用)
os.environ["POSTHOG_DISABLED"] = "1"

# ==============================================================================
# [新增] 遥测屏蔽状态自检
# ==============================================================================
_telemetry_vars = {
    "LANGCHAIN_TRACING_V2": "false",
    "LANGCHAIN_TRACING": "false",
    "LANGSMITH_TRACING": "false",
    "ANONYMIZED_TELEMETRY": "False",
    "HF_HUB_DISABLE_TELEMETRY": "1",
    "POSTHOG_DISABLED": "1"
}

_telemetry_errors = []
for _var, _expected in _telemetry_vars.items():
    _actual = os.environ.get(_var)
    if _actual != _expected:
        _telemetry_errors.append(f"{_var} (Expected: {_expected}, Got: {_actual})")

if _telemetry_errors:
    pass  # [自动清理] 已移除输出语句
else:
    pass  # [自动清理] 已移除输出语句

import logging,sys,json,uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from api.lifespan import lifespan
from api.routers.HandleError import APIException, api_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request

app = FastAPI(
    title="Local Mind API",
    description="API for interacting with a local Ollama instance and semantic search",
    version="1.0.0",
    lifespan=lifespan
)



# 从 middleware 模块配置中间件
from api.middleware import configure_middleware
configure_middleware(app)

# 从 routers_config 模块配置路由
from api.routers_config import configure_routers
configure_routers(app)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Ollama Chat API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
