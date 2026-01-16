from fastapi import APIRouter, Depends, HTTPException # 从 fastapi 库导入 APIRouter, Depends, HTTPException
from typing import List, Dict, Optional # 从 typing 模块导入 List, Dict, Optional
from services.history_services import HistoryService # 从 services.history_services 导入 HistoryService
from services.config import HISTORY_CONFIG
from pydantic import BaseModel # 从 pydantic 库导入 BaseModel


class ChatMessage(BaseModel):
    """
    表示单个聊天消息的模型。
    一个聊天消息包含发送者的角色、消息内容和可选的思考链。
    """
    role: str
    content: str
    thinkingData: Optional[List[str]] = None # 可选字段，用于存储消息生成过程中的思考链，默认为 None


class HistoryListItem(BaseModel):
    """
    表示历史记录列表中单个项目的模型。
    这个模型用于展示历史会话列表，可以是会话分隔符或具体的聊天会话。
    """
    type: str # 必需字段，表示列表项的类型（例如："separator" 表示分隔符，"session" 表示聊天会话）
    title: str # 必需字段，表示列表项的标题（对于会话是聊天标题，对于分隔符是日期信息）
    id: Optional[str] = None # 可选字段，当 type 为 "session" 时表示会话的唯一 ID，默认为 None

class SaveHistoryRequest(BaseModel):
    """
    用于保存历史记录请求体的数据模型。
    包含需要保存的消息列表和可选的会话ID。
    """
    messages: List[ChatMessage] # 消息列表，每个消息都是 ChatMessage 类型
    session_id: Optional[str] = None # 可选的会话ID，如果提供则更新现有会话，否则创建新会话

router = APIRouter() # 创建一个 FastAPI 路由器实例

from services.config import HISTORY_CONFIG

def get_history_service():
    """
    依赖注入函数，提供 HistoryService 实例。
    每次请求时都会创建一个新的 HistoryService 实例。
    """
    return HistoryService(history_dir=HISTORY_CONFIG["history_directory"])

@router.get("/", response_model=List[HistoryListItem])
async def get_history_list(
    history_service: HistoryService = Depends(get_history_service) # 通过依赖注入获取 HistoryService 实例
):
    """
    获取历史记录列表。
    返回一个包含所有历史会话概要的列表，按日期分类。
    """
    return history_service.load_history_list()

@router.post("/")
async def save_history_session(
    request: SaveHistoryRequest, # 请求体将自动解析为 SaveHistoryRequest 对象
    history_service: HistoryService = Depends(get_history_service) # 通过依赖注入获取 HistoryService 实例
):
    """
    保存或更新一个历史记录会话。
    如果请求中不包含 session_id，则创建一个新的会话。
    如果 session_id 为空且消息列表为空，则不执行任何操作。
    """
    # 如果 session_id 未提供且消息列表为空，则很可能是前端的冗余调用
    if not request.session_id and not request.messages:
        return {"message": "No action taken for empty history.", "session_id": None}

    try:
        session_id = history_service.save_history(request.messages, request.session_id)
        return {"message":"History session saved successfully.", "session_id": session_id}
    except Exception as e:
        # 如果保存失败，抛出 HTTP 500 错误
        raise HTTPException(status_code=500, detail=f"Failed to save history session: {e}")

@router.get("/{filename}", response_model=List[ChatMessage])
async def load_history_session(
    filename: str, # 从 URL 路径中获取会话文件名（通常是 session_id）
    history_service: HistoryService = Depends(get_history_service) # 通过依赖注入获取 HistoryService 实例
):
    """
    加载指定会话ID的历史记录。
    返回该会话中的所有聊天消息。
    """
    messages = history_service.load_history_session(filename)
    if not messages:
        # 如果未找到消息（即文件不存在或内容为空），则抛出 HTTP 404 错误
        raise HTTPException(status_code=404, detail="History session not found.")
    return messages

@router.delete('/')
async def clear_all_history(
    history_service: HistoryService = Depends(get_history_service) # 通过依赖注入获取 HistoryService 实例
):
    """
    清除所有存储的历史记录文件。
    """
    try:
        history_service.clear_history()
        return {"message": "All history cleared successfully"}
    except Exception as e:
        # 如果清除失败，抛出 HTTP 500 错误
        raise HTTPException(status_code=500, detail=f"Failed to clear history: {e}")