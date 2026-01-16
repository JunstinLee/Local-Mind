import os,json
from fastapi import APIRouter, HTTPException, status, Request
from pydantic import BaseModel, Field
from typing import List
from services.config import BASE_DIRECTORIES
from services.filetype_conversion_service import SUPPORTED_EXTENSIONS

router = APIRouter(
    prefix="/api/convert",
    tags=["File Conversion"]
)

class ConversionRequest(BaseModel):
    relative_paths: List[str] = Field(..., min_length=1, description="要处理的文件路径列表，相对于data目录。")

@router.post("/files", status_code=status.HTTP_202_ACCEPTED)
def submit_conversion_tasks(request: ConversionRequest, fastapi_request: Request):
    """接收一个或多个文件路径，将它们作为任务添加到处理队列中。"""
    task_queue = fastapi_request.app.state.task_queue
    if task_queue is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="文件处理服务当前未启用。请使用 --enable-worker 参数启动后端。"
        )

    data_directory = BASE_DIRECTORIES.get("data", "./data")
    queued_files = []
    errors = []

    for rel_path in request.relative_paths:
        source_path = os.path.join(data_directory, rel_path)
        
        if not os.path.isfile(source_path):
            errors.append({"file": rel_path, "error": "文件未找到"})
            continue

        file_ext = os.path.splitext(rel_path)[1].lower()
        if file_ext not in SUPPORTED_EXTENSIONS:
            errors.append({"file": rel_path, "error": f"不支持的文件类型: {file_ext}"})
            continue

        task = {'source_path': source_path}
        task_queue.put(task)
        queued_files.append(rel_path)

    if not queued_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "没有有效的文件可供处理。", "errors": errors}
        )

    return {
        "message": f"成功将 {len(queued_files)} 个文件任务加入处理队列。",
        "queued_files": queued_files,
        "errors": errors
    }

@router.get("/log/{extension}", status_code=status.HTTP_200_OK)
def get_conversion_log(extension: str):
    """根据文件后缀名获取分类的转换日志。"""
    log_dir = os.path.join(BASE_DIRECTORIES.get("extracted_texts", "./extracted_texts"), "Converfile_info")
    log_filename = f"{extension.lstrip('.')}.json"
    log_filepath = os.path.join(log_dir, log_filename)

    if not os.path.isfile(log_filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"未找到 {extension} 类型的日志文件。"
        )

    try:
        with open(log_filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"读取日志文件时发生错误: {e}"
        )