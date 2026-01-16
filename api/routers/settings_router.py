from fastapi import APIRouter, HTTPException, Request
from typing import Dict, Any

from schemas.settings import Settings
from services.settings_service import settings_service
from services.db_service import DBService
from services.vector_store_service import VectorStoreService

router = APIRouter()

@router.get("/settings", response_model=Settings)
async def get_current_settings():
    """
    Retrieve the current application settings.
    """
    return settings_service.get_settings()

@router.put("/settings", response_model=Settings)
async def update_application_settings(settings_update: Dict[str, Any]):
    """
    Update one or more application settings.
    
    Only the provided fields will be updated.
    """
    try:
        updated_settings = settings_service.update_settings(settings_update)
        return updated_settings
    except Exception as e:
        # Catch potential validation errors or other issues
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/settings/knowledge-base-cache")
async def clear_knowledge_base_cache(request: Request):
    """
    清除知识库缓存，包括：
    - ChromaDB向量数据库中的所有数据
    - SQLite元数据库中的所有记录
    """
    try:
        # 获取chroma_client和app_state
        chroma_client = getattr(request.app.state, 'chroma_client', None)
        app_state = request.app.state
        
        if not chroma_client:
            raise HTTPException(
                status_code=500, 
                detail="ChromaDB client not initialized"
            )
        
        # 创建服务实例
        db_service = DBService()
        vector_store_service = VectorStoreService(
            chroma_client=chroma_client,
            app_state=app_state
        )
        
        # 清空SQLite数据库
        db_result = db_service.clear_all_knowledge_base_data()
        
        # 清空ChromaDB集合
        vector_result = vector_store_service.clear_all_collections()
        
        return {
            "message": "知识库缓存已成功清除",
            "database": db_result,
            "vector_store": vector_result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"清除知识库缓存失败: {str(e)}"
        )
