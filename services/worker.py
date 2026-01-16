import time
import json
from services.filetype_conversion_service import process_file_task

def run_worker(queue):
    """一个简单的工作进程函数，持续从队列中获取并处理任务。"""
    pass  # [自动清理] 已移除输出语句
    while True:
        try:
            task = queue.get()
            if task is None:
                pass  # [自动清理] 已移除输出语句
                break

            source_path = task.get('source_path')
            if source_path:
                pass  # [自动清理] 已移除输出语句
                process_file_task(source_path)
            else:
                pass  # [自动清理] 已移除输出语句

        except KeyboardInterrupt:
            pass  # [自动清理] 已移除输出语句
            break
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            time.sleep(1)

if __name__ == '__main__':
    # 此部分仅用于可能的直接测试，实际由 main.py 启动
    pass  # [自动清理] 已移除输出语句
