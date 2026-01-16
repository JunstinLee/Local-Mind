from fastapi import Request
from fastapi.responses import JSONResponse

# 1. 定义自定义异常
class APIException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

# 2. 创建异常处理程序
async def api_exception_handler(request: Request, exc: APIException):
    """
    处理 APIException 的全局异常处理器。
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "detail": exc.detail},
    )