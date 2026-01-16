from fastapi.middleware.cors import CORSMiddleware
from api.monitoring import MonitoringMiddleware

def configure_middleware(app):
    # 添加监控中间件（需要在CORS中间件之前添加以确保正确记录）
    app.add_middleware(MonitoringMiddleware)

    # 添加 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8080", "http://127.0.0.1:8080", "*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )