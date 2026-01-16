from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(
    prefix="/api/status",
    tags=["Status"],
)

class BackendStatus(BaseModel):
    model_loaded: bool
    chroma_db_initialized: bool
    search_service_initialized: bool
    status: str  # "loading", "ready", "error"

@router.get("/backend", response_model=BackendStatus)
async def get_backend_status(request: Request):
    """获取后端服务的加载状态"""
    try:
        # 检查模型是否已加载
        model_loaded = hasattr(request.app.state, 'embedding_model') and request.app.state.embedding_model is not None
        
        # 检查 ChromaDB 是否已初始化
        chroma_db_initialized = hasattr(request.app.state, 'chroma_collection')
        
        # 检查搜索服务是否已初始化
        search_service_initialized = hasattr(request.app.state, 'search_service') and request.app.state.search_service is not None
        
        # 确定整体状态
        if not model_loaded or not chroma_db_initialized:
            status = "loading"
        elif not search_service_initialized:
            # 如果模型和DB都已加载，但搜索服务未初始化，可能还在初始化过程中
            status = "loading"
        else:
            status = "ready"
        
        return BackendStatus(
            model_loaded=model_loaded,
            chroma_db_initialized=chroma_db_initialized,
            search_service_initialized=search_service_initialized,
            status=status
        )
    except Exception as e:
        # 如果出现异常，返回错误状态
        return BackendStatus(
            model_loaded=False,
            chroma_db_initialized=False,
            search_service_initialized=False,
            status="error"
        )