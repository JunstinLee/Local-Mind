# Backend/api/routers/EMmodel.py

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
import json
import asyncio
from fastapi.responses import StreamingResponse

# 从服务层导入所需函数和数据
from services.EmbServ import (
    get_local_supported_models,
    get_active_model_name,
    update_active_model,
    download_model_from_hub,
    get_download_progress
)

router = APIRouter(
    prefix="/api/Embedding",
    tags=["Model Management"],
)

class ModelUpdateRequest(BaseModel):
    model_name: str

class ModelDownloadRequest(BaseModel):
    model_name: str
    use_custom_dir: bool = False

@router.get("/EmModel", response_model=List[dict])
async def get_supported_models():
    """返回所有支持的嵌入模型列表。"""
    return get_local_supported_models()

@router.get("/active")
async def get_active_model():
    """返回当前在 .env 文件中配置的活动模型名称。"""
    model_name = get_active_model_name()
    return {"active_model": model_name}

@router.post("/download")
async def download_model(request: ModelDownloadRequest, background_tasks: BackgroundTasks):
    """
    触发一个后台任务来从 Hugging Face Hub 下载模型。
    这是一个耗时操作，API 会立即返回，下载将在后台进行。
    
    Args:
        request: 包含模型名称和是否使用自定义目录的请求体
        background_tasks: FastAPI的后台任务管理器
    """
    try:
        # 将下载任务添加到后台
        background_tasks.add_task(download_model_from_hub, request.model_name, request.use_custom_dir)
        download_location = "自定义目录" if request.use_custom_dir else "HuggingFace缓存"
        return {"message": f"模型 '{request.model_name}' 的下载任务已在后台启动，将下载到{download_location}。"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动模型下载任务失败: {e}")

@router.get("/download-progress/{model_name:path}")
async def get_model_download_progress(model_name: str):
    """获取指定模型的下载进度"""
    progress_info = get_download_progress(model_name)
    return progress_info

@router.get("/download-progress-sse/{model_name:path}")
async def get_model_download_progress_sse(model_name: str):
    """通过SSE实时获取指定模型的下载进度"""
    async def event_generator():
        last_progress = -1
        while True:
            progress_info = get_download_progress(model_name)
            if progress_info['status'] in ['completed', 'error']:
                yield f"data: {json.dumps(progress_info)}\n\n"
                break
            if progress_info['progress'] != last_progress:
                yield f"data: {json.dumps(progress_info)}\n\n"
                last_progress = progress_info['progress']
            await asyncio.sleep(0.01)  # 避免过于频繁的检查
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.post("/active")
async def set_active_model(request: ModelUpdateRequest):
    """
    更新 .env 文件来切换活动模型。
    注意：此操作完成后，需要重启后端服务才能加载新模型。
    """
    try:
        success = update_active_model(request.model_name)
        if success:
            return {
                "message": "活动模型配置已更新。",
                "new_active_model": request.model_name,
                "notice": "请务必重启后端服务以使更改生效。"
            }
    except ValueError as e:
        # 捕获不支持模型的错误
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新配置文件失败: {e}")
