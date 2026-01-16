import logging
import ollama

# 配置日志记录器
logging.basicConfig(level=logging.INFO) # 设置日志级别为 INFO
logger = logging.getLogger(__name__) # 获取当前模块的日志记录器

async def get_available_models():
    """
    异步函数：获取 Ollama 可用的模型列表。
    尝试连接 Ollama 服务并列出所有可用的模型。
    如果连接失败或无法获取模型列表，则记录错误并返回空列表。

    Returns:
        list: 包含可用模型名称的字典列表，例如：[{'name': 'model1'}, {'name': 'model2'}]。
              如果出错则返回空列表。
    """
    try:
        models = ollama.list()['models'] # 调用 ollama.list() 获取模型信息
        # 从模型信息中提取 'model' 名称并格式化为字典列表
        return [{'name': m['model']} for m in models]
    except Exception as e:
        # 捕获任何异常，记录错误信息
        pass  # [自动清理] 已移除输出语句
        return [] # 出错时返回空列表
