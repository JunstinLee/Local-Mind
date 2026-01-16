from fastapi import FastAPI
from api.routers import history, file, filetree, search, typechange, worker_manager, settings_router, indexing_router
from api.routers import EMmodel as model_router
from api.routers import file_metadata
from api.routers import status
from api.routers import enhanced_chat

def configure_routers(app: FastAPI):
    app.include_router(history.router, prefix="/api/history")
    app.include_router(file.router, prefix="/api/file")
    app.include_router(filetree.router, prefix="/api/filetree")
    app.include_router(model_router.router)
    app.include_router(search.router, prefix="/api/search") # 确保前缀正确
    app.include_router(typechange.router)
    app.include_router(worker_manager.router) # 注册新的 worker 管理路由
    app.include_router(settings_router.router, prefix="/api") # 注册设置路由
    app.include_router(indexing_router.router, prefix="/api") # 注册索引路由
    app.include_router(file_metadata.router, prefix="") # 注册文件元数据API路由
    app.include_router(status.router) # 注册状态路由
    app.include_router(enhanced_chat.router, prefix="/api/enhanced") # 注册增强聊天路由