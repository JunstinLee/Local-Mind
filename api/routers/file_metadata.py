from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uuid

from services.db_service import DBService
from services.vector_store_service import VectorStoreService

class FileInfo(BaseModel):
    file_id: str
    file_name: str
    path: str
    created_at: str
    total_chunks_large: int
    total_chunks_small: int

class ChunkInfo(BaseModel):
    chunk_uuid: str
    file_id: str
    chunk_index: int
    chunk_size: int
    offset: int
    collection_name: str

class FileInfoResponse(BaseModel):
    file_info: FileInfo
    chunks: List[ChunkInfo]

class FileContentResponse(BaseModel):
    content: str
    metadata: Dict[str, Any]

router = APIRouter(prefix="/api", tags=["File Management"])

@router.get("/files", response_model=List[FileInfo])
async def list_all_files():
    """
    获取所有已入库文件的列表
    """
    from services.db_service import DBService
    db_service = DBService()
    
    # 直接查询数据库获取所有文件信息
    from services.secure_db import get_db_connection
    conn = get_db_connection(db_service.db_path)
    c = conn.cursor()
    c.execute("SELECT * FROM files")
    rows = c.fetchall()
    conn.close()
    
    files_info = []
    for row in rows:
        files_info.append(FileInfo(
            file_id=row[0],
            file_name=row[1],
            path=row[2],
            created_at=row[3],
            total_chunks_large=row[4],
            total_chunks_small=row[5]
        ))
    
    return files_info

@router.get("/files/{file_id}", response_model=FileInfo)
async def get_file_info(file_id: str):
    """
    获取特定文件的详细信息
    """
    from services.db_service import DBService
    db_service = DBService()
    
    file_info = db_service.get_file_info_by_id(file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found in database")
    
    return FileInfo(
        file_id=file_info["file_id"],
        file_name=file_info["file_name"],
        path=file_info["path"],
        created_at=file_info["created_at"],
        total_chunks_large=file_info["total_chunks_large"],
        total_chunks_small=file_info["total_chunks_small"]
    )

@router.get("/files/{file_id}/chunks", response_model=List[ChunkInfo])
async def get_file_chunks(file_id: str):
    """
    获取特定文件的所有分块信息
    """
    from services.db_service import DBService
    db_service = DBService()
    
    chunks = db_service.get_chunks_by_file_id(file_id)
    if not chunks:
        raise HTTPException(status_code=404, detail="No chunks found for this file")
    
    chunks_info = []
    for chunk in chunks:
        chunks_info.append(ChunkInfo(
            chunk_uuid=chunk["chunk_uuid"],
            file_id=chunk["file_id"],
            chunk_index=chunk["chunk_index"],
            chunk_size=chunk["chunk_size"],
            offset=chunk["offset"],
            collection_name=chunk["collection_name"]
        ))
    
    return chunks_info

@router.get("/files/{file_id}/content")
async def get_file_content_in_vector_store(file_id: str, 
                                          collection_name: str = "knowledge_base_small",
                                          limit: int = 100):
    """
    获取特定文件在向量存储中的内容
    """
    from services.vector_store_service import VectorStoreService
    vector_service = VectorStoreService()
    
    try:
        # 查询指定文件ID在向量存储中的内容
        results = vector_service.query_by_file_id(
            file_id=file_id,
            collection_name=collection_name,
            n_results=limit
        )
        
        if not results or not results.get('documents', []):
            raise HTTPException(status_code=404, detail="No content found for this file in vector store")
        
        # 为每个文档准备内容和元数据
        content_list = []
        for i in range(len(results['documents'][0])):
            doc_content = results['documents'][0][i] if i < len(results['documents'][0]) else ""
            metadata = results['metadatas'][0][i] if i < len(results['metadatas'][0]) else {}
            
            content_list.append({
                "content": doc_content,
                "metadata": metadata
            })
        
        return {"contents": content_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving content from vector store: {str(e)}")

# 工具函数：获取文件在双层索引中的状态
@router.get("/files/{file_id}/status")
async def get_file_status_in_dual_index(file_id: str):
    """
    获取文件在双层索引中的状态
    """
    from services.db_service import DBService
    from services.vector_store_service import VectorStoreService
    db_service = DBService()
    vector_service = VectorStoreService()
    
    # 从数据库获取文件信息
    file_info = db_service.get_file_info_by_id(file_id)
    if not file_info:
        raise HTTPException(status_code=404, detail="File not found in database")
    
    # 检查向量存储中是否包含此文件
    large_results = vector_service.query_by_file_id(
        file_id=file_id,
        collection_name="knowledge_base_large",
        n_results=1  # 只需要确认存在性
    )
    
    small_results = vector_service.query_by_file_id(
        file_id=file_id,
        collection_name="knowledge_base_small",
        n_results=1  # 只需要确认存在性
    )
    
    return {
        "file_info": file_info,
        "stored_in_large_collection": len(large_results.get('documents', [])) > 0,
        "stored_in_small_collection": len(small_results.get('documents', [])) > 0,
        "num_chunks_in_large": len(large_results.get('documents', [])),
        "num_chunks_in_small": len(small_results.get('documents', []))
    }