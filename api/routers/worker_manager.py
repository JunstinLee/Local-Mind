from fastapi import APIRouter, Request, HTTPException, status
from multiprocessing import Process, Manager

from services.worker import run_worker

router = APIRouter(
    prefix="/api/worker",
    tags=["Worker Management"]
)

@router.post("/start", status_code=status.HTTP_200_OK)
def start_worker(request: Request):
    """启动后台文件处理工作进程。"""
    if request.app.state.worker_process and request.app.state.worker_process.is_alive():
        return {"message": "后台工作进程已在运行中。"}

    pass  # [自动清理] 已移除输出语句
    manager = Manager()
    task_queue = manager.Queue()
    worker_process = Process(target=run_worker, args=(task_queue,), daemon=True)
    
    request.app.state.task_queue = task_queue
    request.app.state.worker_process = worker_process
    
    worker_process.start()
    
    return {"message": "后台工作进程已成功启动。"}

@router.post("/stop", status_code=status.HTTP_200_OK)
def stop_worker(request: Request):
    """停止后台文件处理工作进程。"""
    worker_process = request.app.state.worker_process
    if not worker_process or not worker_process.is_alive():
        return {"message": "后台工作进程当前未运行。"}

    pass  # [自动清理] 已移除输出语句
    worker_process.terminate()
    worker_process.join() # 等待进程完全终止

    request.app.state.task_queue = None
    request.app.state.worker_process = None
    
    return {"message": "后台工作_进程已成功停止。"}

@router.get("/status", status_code=status.HTTP_200_OK)
def get_worker_status(request: Request):
    """获取后台文件处理工作进程的当前状态。"""
    worker_process = request.app.state.worker_process
    if worker_process and worker_process.is_alive():
        return {"status": "running"}
    else:
        return {"status": "stopped"}
