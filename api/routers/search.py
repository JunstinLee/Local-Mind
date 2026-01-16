# api/routers/search.py

from fastapi import APIRouter, Depends, status, Request
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import chromadb,time,os,logging
from typing import Optional, List, Dict, Any

# 从你项目中的错误处理模块导入自定义异常
from .HandleError import APIException 
from services.config import is_path_in_knowledge_base_work_area
from services.filter_utils import build_where_clause
from services.search_service import SearchService

# --- 1. 创建路由器实例 ---
router = APIRouter(
    tags=["Semantic Search"]
)

# --- 2. 定义请求的数据模型 ---
class SearchFilters(BaseModel):
    fileType: Optional[List[str]] = None
    dateRange: Optional[str] = None
    modifiedDate: Optional[str] = None
    fileSize: Optional[str] = None
    RelevanceSorting: Optional[str] = None

class SearchRequest(BaseModel):
    query: str
    n_results: int = 10
    filters: Optional[SearchFilters] = None

# --- 3. 定义依赖项 (Dependencies) ---
def get_embedding_model() -> SentenceTransformer:
    pass

def get_search_service(request: Request) -> SearchService:
    # 直接从 app.state 返回在启动时创建的单例
    return request.app.state.search_service

# --- 4. 定义 API 端点 ---

@router.get("/count")
def get_document_count(
    search_service: SearchService = Depends(get_search_service)
):
    """
    返回当前向量数据库中小块集合的文档总数。
    """
    try:
        collection = search_service.vector_store_service.get_collection("knowledge_base_small")
        # 修复：使用LangChain Chroma实例的count方法
        count = collection._collection.count() if hasattr(collection, '_collection') and collection._collection else 0
        return {"count": count}
    except Exception as e:
        raise APIException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=f"Failed to get document count: {str(e)}"
        )

@router.post("/")
def perform_search(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service)
):
    """
    接收查询文本，返回语义搜索结果（专注在小块集合中检索）。
    根据文档总数动态调整返回结果数量。
    """
    if not request.query or not request.query.strip():
        raise APIException(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Query text cannot be empty."
        )

    pass  # [自动清理] 已移除输出语句
    if request.filters:
        pass  # [自动清理] 已移除输出语句

    query_start_time = time.time()

    # 调用新的服务层进行小块集合的语义搜索
    search_filters = request.filters.dict(exclude_none=True) if request.filters else None
    results = search_service.semantic_search(
        query=request.query,
        n_results=request.n_results,
        filters=search_filters
    )

    query_end_time = time.time()
    pass  # [自动清理] 已移除输出语句

    # 进行安全验证，确保路径在知识库工作区域内
    validated_results = []
    for result in results:
        source_path_str = result.get("source_file")
        try:
            is_path_in_knowledge_base_work_area(source_path_str)
            validated_results.append(result)
        except (ValueError, TypeError) as e:
            pass  # [自动清理] 已移除输出语句
            continue

    pass  # [自动清理] 已移除输出语句
    return validated_results
