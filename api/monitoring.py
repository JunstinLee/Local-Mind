"""
API监控和指标追踪模块
用于记录API调用指标、响应时间等
"""
import time
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


@dataclass
class APIMetric:
    """API指标数据类"""
    endpoint: str
    method: str
    status_code: int
    response_time: float
    timestamp: datetime
    user_id: Optional[str] = None
    conversation_id: Optional[str] = None


class MetricsTracker:
    """指标跟踪器"""
    
    def __init__(self):
        self.metrics: list[APIMetric] = []
        self.call_count = 0
        self.error_count = 0
    
    def record_metric(self, metric: APIMetric):
        """记录指标"""
        self.metrics.append(metric)
        self.call_count += 1
        if metric.status_code >= 400:
            self.error_count += 1
        
        # 为演示目的，只保留最近1000条记录
        if len(self.metrics) > 1000:
            self.metrics = self.metrics[-1000:]
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.metrics:
            return {
                "total_calls": 0,
                "error_count": 0,
                "error_rate": 0.0,
                "avg_response_time": 0.0,
                "p95_response_time": 0.0
            }
        
        response_times = [m.response_time for m in self.metrics]
        avg_response_time = sum(response_times) / len(response_times)
        
        # 计算P95响应时间
        sorted_times = sorted(response_times)
        p95_index = int(0.95 * len(sorted_times))
        p95_response_time = sorted_times[p95_index] if sorted_times else 0.0
        
        error_rate = (self.error_count / self.call_count) * 100 if self.call_count > 0 else 0.0
        
        return {
            "total_calls": self.call_count,
            "error_count": self.error_count,
            "error_rate": round(error_rate, 2),
            "avg_response_time": round(avg_response_time, 3),
            "p95_response_time": round(p95_response_time, 3)
        }


# 全局指标跟踪器实例
metrics_tracker = MetricsTracker()


class MonitoringMiddleware(BaseHTTPMiddleware):
    """监控中间件，用于记录API调用指标"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        response_time = time.time() - start_time
        
        # 获取请求信息
        method = request.method
        path = request.url.path
        
        # 创建指标记录
        metric = APIMetric(
            endpoint=path,
            method=method,
            status_code=response.status_code,
            response_time=response_time,
            timestamp=datetime.now()
        )
        
        metrics_tracker.record_metric(metric)
        
        return response


def monitor_api_call(endpoint: str, method: str, user_id: Optional[str] = None, 
                     conversation_id: Optional[str] = None):
    """装饰器：监控API调用"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                response_time = time.time() - start_time
                
                # 记录指标
                metric = APIMetric(
                    endpoint=endpoint,
                    method=method,
                    status_code=200,
                    response_time=response_time,
                    timestamp=datetime.now(),
                    user_id=user_id,
                    conversation_id=conversation_id
                )
                metrics_tracker.record_metric(metric)
                
                return result
            except Exception as e:
                response_time = time.time() - start_time
                status_code = 500  # 假设为内部服务器错误
                
                # 记录错误指标
                metric = APIMetric(
                    endpoint=endpoint,
                    method=method,
                    status_code=status_code,
                    response_time=response_time,
                    timestamp=datetime.now(),
                    user_id=user_id,
                    conversation_id=conversation_id
                )
                metrics_tracker.record_metric(metric)
                
                raise e
        return wrapper
    return decorator