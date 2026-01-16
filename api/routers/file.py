# Backend/api/routers/file.py

import os
import tkinter as tk
from tkinter import filedialog
from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
from services.fileMA_service import file_manager
from services.fileinfo_service import file_info_service
from services.db_service import DBService
from .HandleError import APIException
# 新增导入，用于调用其他模块的逻辑
from .filetree import generate_tree_json
from services.config import BASE_DIRECTORIES
from pathlib import Path
import logging

router = APIRouter(prefix="/files", tags=["FileManager"])

# --- Pydantic 模型定义 --- 

class CreateFolderRequest(BaseModel):
    folder_name: str

# 修正后的CopyFileRequest，增加了save_info
class CopyFileRequest(BaseModel):
    source_path: str
    destination_folder: str
    new_name: str = None
    save_info: bool = False # 新增字段，默认为False

class CopyFolderRequest(BaseModel):
    source_path: str
    new_name: str = None

class BatchCopyRequest(BaseModel):
    file_paths: List[str]
    destination_folder: str

class FileInfoRequest(BaseModel):
    file_path: str

class BatchFileInfoRequest(BaseModel):
    file_paths: List[str]

class FileFilterOptions(BaseModel):
    search_term: str = None
    file_types: List[str] = None

class ListFilesRequest(BaseModel):
    base_path: str
    filters: FileFilterOptions = None
    sort_by: str = 'name'
    sort_order: str = 'asc'
    timestamp: Optional[int] = None  # 用于缓存破坏

class UploadResponse(BaseModel):
    success: bool
    message: str
    uploaded_files: List[dict]
    failed_files: List[dict] = []

# --- 精简后的API端点 ---

@router.post("/create-folder")
async def create_folder(request: CreateFolderRequest):
    try:
        folder_path = file_manager.create_folder(request.folder_name)
        return {"success": True, "message": "文件夹创建成功", "folder_path": folder_path}
    except OSError as e:
        raise APIException(status_code=400, detail=f"创建文件夹失败: {e}")

# 已改造为调用新的服务方法
@router.post("/copy-file")
async def copy_file(request: CopyFileRequest):
    try:
        result = file_manager.copy_file(
            source_path=request.source_path, 
            destination_folder=request.destination_folder, 
            new_name=request.new_name, 
            save_info=request.save_info
        )
        message = "文件复制成功。"
        if result.get("json_file_path"):
            message = "文件复制并保存信息成功。"
        
        return {"success": True, "message": message, **result}

    except (FileNotFoundError, OSError) as e:
        raise APIException(status_code=400, detail=f"复制文件失败: {e}")

@router.post("/copy-folder")
async def copy_folder(request: CopyFolderRequest):
    try:
        result = file_manager.copy_folder(
            source_folder_path=request.source_path,
            new_name=request.new_name
        )
        return {"success": True, "message": "文件夹复制成功，并已保存文件信息。", **result}
    except (ValueError, OSError) as e:
        raise APIException(status_code=400, detail=f"复制文件夹失败: {e}")

@router.post("/batch-copy")
async def batch_copy_files(request: BatchCopyRequest):
    copied_files = file_manager.copy_multiple_files(request.file_paths, request.destination_folder)
    return {
        "success": True,
        "message": f"成功复制 {len(copied_files)} 个文件",
        "copied_files": copied_files,
        "failed_count": len(request.file_paths) - len(copied_files)
    }

@router.post("/get-file-info")
async def get_file_info(request: FileInfoRequest):
    try:
        info = file_info_service.get_file_info(request.file_path)
        return {"success": True, "file_info": info}
    except FileNotFoundError as e:
        raise APIException(status_code=404, detail=str(e))

@router.post("/save-file-info")
async def save_file_info(request: FileInfoRequest):
    try:
        path = file_info_service.save_file_info_to_db(request.file_path)
        return {"success": True, "message": "文件信息保存成功", "json_file_path": path}
    except FileNotFoundError as e:
        raise APIException(status_code=404, detail=str(e))

@router.post("/batch-save-info")
async def batch_save_files_info(request: BatchFileInfoRequest):
    results = file_info_service.batch_save_files_info(request.file_paths)
    success_count = sum(1 for v in results.values() if not str(v).startswith("错误"))
    return {
        "success": True,
        "message": f"成功处理 {success_count} 个文件",
        "results": results,
        "success_count": success_count,
        "failed_count": len(request.file_paths) - success_count
    }

@router.get("/info-by-extension/{extension}")
async def get_files_by_extension(extension: str):
    files_info = file_info_service.get_files_by_extension(f".{extension}")
    return {
        "success": True,
        "extension": extension,
        "files_count": len(files_info),
        "files_info": files_info
    }

# copy-and-save-info 端点已移除，功能合并到 copy-file

@router.post("/list")
async def list_files(request: ListFilesRequest):
    try:
        # 记录请求信息，包括时间戳
        import logging
        logger = logging.getLogger(__name__)
        pass  # [自动清理] 已移除输出语句
        
        files = file_manager.list_files(
            base_path=request.base_path,
            search_term=request.filters.search_term if request.filters else None,
            file_types=request.filters.file_types if request.filters else None,
            sort_by=request.sort_by,
            sort_order=request.sort_order
        )
        
        pass  # [自动清理] 已移除输出语句
        return {"success": True, "files": files}
    except ValueError as e:
        raise APIException(status_code=400, detail=str(e))

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    destination_folder: str = Form(...),
    save_info: bool = Form(False)
):
    """
    上传文件到指定文件夹，并能根据相对路径创建子目录。
    
    Args:
        files: 上传的文件列表 (file.filename 包含相对路径时将创建目录结构)。
        destination_folder: 目标文件夹名称。
        save_info: 是否保存文件信息到JSON。
    
    Returns:
        UploadResponse: 上传结果。
    """
    uploaded_files = []
    failed_files = []
    
    try:
        for file in files:
            try:
                # 基本验证
                if not file.filename:
                    failed_files.append({
                        "filename": "unknown",
                        "error": "文件名为空"
                    })
                    continue
                
                # 读取文件内容
                file_content = await file.read()
                
                # 使用新的、能处理目录结构的服务方法
                # file.filename 此时会包含相对路径，如 "folder/file.txt"
                result = file_manager.save_uploaded_file_with_structure(
                    file_content=file_content,
                    relative_path=file.filename,
                    destination_folder=destination_folder,
                    content_type=file.content_type,
                    save_info=save_info
                )
                
                uploaded_files.append(result)
                
            except ValueError as e:
                # 验证错误
                failed_files.append({
                    "filename": file.filename if file.filename else "unknown",
                    "error": str(e)
                })
            except Exception as e:
                # 其他错误
                failed_files.append({
                    "filename": file.filename if file.filename else "unknown",
                    "error": f"上传失败: {str(e)}"
                })
    
    except Exception as e:
        raise APIException(status_code=500, detail=f"上传过程中发生错误: {str(e)}")
    
    success_count = len(uploaded_files)
    
    if success_count == 0:
        raise APIException(status_code=400, detail="所有文件上传失败")
    
    # --- 新增逻辑：上传成功后，立即获取最新的文件数据 --- 
    new_tree = []
    new_file_list = []
    try:
        # 硬编码路径以匹配前端的请求
        tree_path = file_manager.base_directory
        base_path = str(BASE_DIRECTORIES["forRubbables"])
        new_tree = generate_tree_json(base_path, "")
        new_file_list = file_manager.list_files(base_path=str(tree_path))
    except Exception as e:
        # 如果获取最新数据失败，不应中断整个上传流程，但需要记录错误
        import logging
        logger = logging.getLogger(__name__)
        pass  # [自动清理] 已移除输出语句
    # --- 新增逻辑结束 ---

    # --- 新增调试日志 ---
    import logging
    logger = logging.getLogger(__name__)
    pass  # [自动清理] 已移除输出语句
    # --- 调试日志结束 ---

    message = f"成功上传 {success_count} 个文件"
    if failed_files:
        message += f"，{len(failed_files)} 个文件失败"
    
    return {
        "success": True,
        "message": message,
        "uploaded_files": uploaded_files,
        "failed_files": failed_files,
        # --- 在响应中加入新数据 ---
        "new_tree": new_tree,
        "new_file_list": new_file_list
    }

def get_hf_cache_path():
    """
    返回Hugging Face缓存的默认位置。
    """
    # 导入Hugging Face缓存路径常量
    from huggingface_hub.constants import HF_HUB_CACHE
    
    # 确保目录存在
    import os
    os.makedirs(HF_HUB_CACHE, exist_ok=True)
    
    return {"success": True, "path": HF_HUB_CACHE}


@router.post("/select-folder")
def select_folder():
    """
    返回Hugging Face缓存的默认位置。
    """
    return get_hf_cache_path()


@router.post("/unvectorized_list")
async def list_unvectorized_files(request: ListFilesRequest):
    try:
        logger = logging.getLogger(__name__)
        pass  # [自动清理] 已移除输出语句
        
        all_files = file_manager.list_files(
            base_path=request.base_path,
            search_term=request.filters.search_term if request.filters else None,
            file_types=request.filters.file_types if request.filters else None,
            sort_by = request.sort_by,
            sort_order=request.sort_order
        )
        db_services = DBService()
        processed_paths = db_services.get_all_processed_file_paths()
        unvectorized_files = [
            file_info for file_info in all_files
            if file_info['path'] not in processed_paths
        ]
        pass  # [自动清理] 已移除输出语句
        return {"success": True, "files": unvectorized_files}
    
    except Exception as e:
        pass  # [自动清理] 已移除输出语句
        raise APIException(status_code=500, detail=f"获取未向量化文件列表失败: {str(e)}")


