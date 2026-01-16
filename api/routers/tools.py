from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import jsonschema

class VerifyFileRequest(BaseModel):
    file_name: str

class VerifyFileResponse(BaseModel):
    exists: bool
    file_id: str = None

class CrossCheckRequest(BaseModel):
    retrieved_items: List[Dict[str, Any]]
    available_files: List[str]

class CrossCheckResponse(BaseModel):
    valid_files: List[str]
    invalid_files: List[str]
    reason: str = None

class FormatAnswerRequest(BaseModel):
    raw_answer: str
    schema: Dict[str, Any] = None

class FormatAnswerResponse(BaseModel):
    ok: bool
    parsed: Dict[str, Any] = None
    errors: List[str] = []

router = APIRouter(prefix="/api", tags=["Tools"])

@router.post("/verify_file", response_model=VerifyFileResponse)
async def verify_file(request: VerifyFileRequest):
    """
    验证文件是否存在，并返回file_id
    """
    pass  # [自动清理] 已移除输出语句
    from services.db_service import DBService
    db_service = DBService()
    
    # 查找所有匹配的文件
    import sqlite3
    conn = sqlite3.connect(db_service.db_path)
    c = conn.cursor()
    c.execute("SELECT file_id, file_name FROM files WHERE file_name = ?", (request.file_name,))
    rows = c.fetchall()
    conn.close()
    
    if rows:
        pass  # [自动清理] 已移除输出语句
        return VerifyFileResponse(exists=True, file_id=rows[0][0])
    
    pass  # [自动清理] 已移除输出语句
    return VerifyFileResponse(exists=False, file_id=None)

@router.post("/cross_check_retrieval", response_model=CrossCheckResponse)
async def cross_check_retrieval(request: CrossCheckRequest):
    """
    交叉验证检索结果的有效性
    """
    pass  # [自动清理] 已移除输出语句
    from services.db_service import DBService
    db_service = DBService()
    
    valid_files = []
    invalid_files = []
    
    for item in request.retrieved_items:
        file_id = item.get("file_id")
        if file_id:
            # 检查文件是否存在
            file_info = db_service.get_file_info_by_id(file_id)
            if file_info:
                valid_files.append(file_info["file_name"])
            else:
                invalid_files.append(file_id)
    
    pass  # [自动清理] 已移除输出语句
    return CrossCheckResponse(
        valid_files=valid_files,
        invalid_files=invalid_files,
        reason=f"验证完成：{len(valid_files)} 个有效文件，{len(invalid_files)} 个无效文件"
    )

@router.post("/format_answer", response_model=FormatAnswerResponse)
async def format_answer(request: FormatAnswerRequest):
    """
    格式化或修复答案的JSON格式
    """
    pass  # [自动清理] 已移除输出语句
    try:
        # 尝试直接解析JSON
        parsed_data = json.loads(request.raw_answer)
        
        # 如果提供了schema，则验证数据
        if request.schema:
            try:
                jsonschema.validate(parsed_data, request.schema)
                pass  # [自动清理] 已移除输出语句
                return FormatAnswerResponse(ok=True, parsed=parsed_data, errors=[])
            except jsonschema.ValidationError as e:
                # 如果验证失败，尝试修复
                pass  # [自动清理] 已移除输出语句
                return FormatAnswerResponse(
                    ok=False,
                    parsed=parsed_data,
                    errors=[f"Schema validation error: {str(e)}"]
                )
        else:
            pass  # [自动清理] 已移除输出语句
            return FormatAnswerResponse(ok=True, parsed=parsed_data, errors=[])
    except json.JSONDecodeError as e:
        # JSON格式错误，标记为失败
        pass  # [自动清理] 已移除输出语句
        return FormatAnswerResponse(
            ok=False,
            errors=[f"JSON decode error: {str(e)}"]
        )
