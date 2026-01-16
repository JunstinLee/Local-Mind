# Backend/services/thinking_parser_service.py

import json
from typing import AsyncGenerator
import logging
import time

logger = logging.getLogger(__name__)

async def parse_thinking_stream(stream_generator: AsyncGenerator) -> AsyncGenerator[str, None]:
    """
    解析包含分离的 reasoning 和 content 的流，并生成结构化的 SSE 事件。
    支持接收字典对象或SSE格式字符串
    """
    pass  # [自动清理] 已移除输出语句
    
    chunk_count = 0
    reasoning_count = 0
    content_count = 0

    async for chunk in stream_generator:
        chunk_count += 1
        # 处理字符串类型的chunk（如果接收的是SSE格式字符串）
        if isinstance(chunk, str):
            try:
                # 尝试从SSE格式中提取JSON数据 ("data: {...}\n\n")
                if chunk.startswith("data: "):
                    json_str = chunk[6:].rstrip('\n')  # 去除 "data: " 前缀并去掉换行符
                    chunk_data = json.loads(json_str)
                else:
                    # 如果是纯JSON字符串，直接解析
                    chunk_data = json.loads(chunk)
            except json.JSONDecodeError:
                pass  # [自动清理] 已移除输出语句
                continue
        else:
            # 如果已经是字典类型，直接使用
            chunk_data = chunk

        # 检查是否是完成事件
        if chunk_data.get('done'):
            # 生成元数据事件
            yield f"data: {json.dumps({'type': 'meta', 'data': {'done': True}})}\n\n"
        # 检查是否是错误事件
        elif chunk_data.get('error'):
            # 生成错误事件
            yield f"data: {json.dumps({'type': 'error', 'message': chunk_data.get('message', 'Unknown error')})}\n\n"
        # 关键修复：使用if而不是elif，确保同一chunk中的reasoning和content都能被处理
        # 并且reasoning优先于content输出
        
        reasoning_processed = False
        content_processed = False
        
        # 先处理思考内容
        if 'reasoning' in chunk_data:
            reasoning_content = chunk_data.get('reasoning', '')
            if reasoning_content:
                reasoning_count += 1
                reasoning_processed = True
                if reasoning_count <= 5 or content_count == 0:
                    pass
                    # 生成思考令牌事件
                yield f"data: {json.dumps({'type': 'thinking_token', 'token': reasoning_content})}\n\n"
        
        # 再处理正文内容
        if 'content' in chunk_data:
            content = chunk_data.get('content', '')
            if content:
                content_count += 1
                content_processed = True
                if content_count <= 5:
                    pass                # 生成最终令牌事件
                yield f"data: {json.dumps({'type': 'final_token', 'token': content})}\n\n"
        
        # 记录同时包含两种内容的chunk
        if reasoning_processed and content_processed:
            pass  # [自动清理] 已移除输出语句
     

        # 添加对已格式化类型的支持，以防传入已经是正确格式的数据
        elif chunk_data.get('type') == 'final_token' and 'token' in chunk_data:
            yield f"data: {json.dumps(chunk_data)}\n\n"
        elif chunk_data.get('type') == 'thinking_token' and 'token' in chunk_data:
            yield f"data: {json.dumps(chunk_data)}\n\n"
        elif chunk_data.get('type') == 'meta':
            yield f"data: {json.dumps(chunk_data)}\n\n"
        elif chunk_data.get('type') == 'error':
            yield f"data: {json.dumps(chunk_data)}\n\n"

    pass  # [自动清理] 已移除输出语句
