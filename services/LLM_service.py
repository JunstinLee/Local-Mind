import json, logging
import time
import re
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# 配置日志记录器
logging.basicConfig(level=logging.INFO) # 设置日志级别为 INFO
logger = logging.getLogger(__name__) # 获取当前模块的日志记录器
def is_english_text(text):
    """检查文本是否主要是英文"""
    if not text:
        return False
    # 计算英文字符的比例
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    total_chars = len([c for c in text if c.strip()])
    if total_chars == 0:
        return False
    return english_chars / total_chars > 0.5

async def chat_stream_generator(model: str, prompt: str, history: list = None):
    """
    异步生成器函数：与 Ollama 模型进行流式聊天交互，使用LangChain的ChatOllama类。
    直接输出模型生成的原始数据，不进行格式转换。
    """
    # 准备消息列表
    messages = []
    if history:
        # 如果存在历史记录，则将其转换为LangChain格式
        for msg in history:
            if msg.get('role') == 'user':
                messages.append(HumanMessage(content=msg.get('content', '')))
            elif msg.get('role') == 'assistant':
                messages.append(SystemMessage(content=msg.get('content', '')))

    # 添加当前用户提示到消息列表
    messages.append(HumanMessage(content=prompt))

    # 初始化模型
    llm = ChatOllama(
        model=model,
        validate_model_on_init=True,
        temperature=0.0,
        reasoning=True,           # 捕捉 reasoning_content
        stream=True               # 真正的流式输出
    )

    try:
        # 真正的流式输出
        full_response = ""  # 用于累积完整响应
        full_reasoning = ""  # 用于累积思考内容

        async for chunk in llm.astream(messages):
            # 关键修复：确保在同一个chunk中，reasoning优先于content处理
            reasoning_piece = None
            content_piece = None
            
            # 先检查并收集reasoning内容
            if "reasoning_content" in chunk.additional_kwargs:
                reasoning_piece = chunk.additional_kwargs["reasoning_content"]
                full_reasoning += reasoning_piece
            
            # 再检查并收集content内容
            if chunk.content:
                content_piece = chunk.content
                full_response += content_piece
            
            # 按正确顺序输出：先reasoning，后content
            if reasoning_piece:
                yield f"data: {json.dumps({'reasoning': reasoning_piece})}\n\n"
            
            if content_piece:
                yield f"data: {json.dumps({'content': content_piece})}\n\n"

        # 完成后发送最终数据
        final_data = {
            'done': True,  # 标记为完成
            'full_message': full_response,  # 返回完整的消息
            'full_reasoning': full_reasoning  # 返回完整的思考链
        }
        yield f"data: {json.dumps(final_data)}\n\n"

    except Exception as e:
        # 捕获 Ollama API 调用过程中发生的任何异常
        pass  # [自动清理] 已移除输出语句
        error_data = {
            'error': True,  # 标记为错误
            'message': str(e),  # 返回错误信息
            'model': model,
            'prompt': prompt,
            'history_length': len(history) if history else 0  # 添加历史记录长度用于调试
        }
        # 将错误信息封装为 JSON 并以 SSE 格式返回
        yield f"data: {json.dumps(error_data)}\n\n"
