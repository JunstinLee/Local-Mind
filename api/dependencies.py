from services.EmbServ import get_embedding_model

def get_embedding_model_override():
    """依赖覆盖函数，返回已加载的全局嵌入模型实例。"""
    # 调用 services.EmbServ 中的函数来获取模型
    return get_embedding_model()

def get_chroma_collection_override():
    """依赖覆盖函数，返回已初始化的 ChromaDB 集合实例。"""
    # 从 app.state 中获取在 lifespan 中初始化的集合
    from main import app
    return app.state.chroma_collection