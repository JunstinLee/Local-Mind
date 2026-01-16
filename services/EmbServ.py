# Backend/services/EmbServ.py

import os,time,shutil,sys,threading
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from huggingface_hub import scan_cache_dir,snapshot_download
from pathlib import Path
from typing import List
from langchain_core.embeddings import Embeddings
from services.config import ENV_PATH
load_dotenv(dotenv_path=ENV_PATH)
# 添加用于跟踪下载进度的字典
download_progress = {}

# 用于存储已加载模型的全局单例
embedding_model_instance = None

# 用于更新模型列表的锁
model_list_lock = threading.Lock()

def get_local_supported_models():
    """
    扫描本地Hugging Face缓存，动态生成支持的模型列表。
    """
    try:
        pass  # [自动清理] 已移除输出语句
        local_models = []
        
        # 扫描HuggingFace缓存中的模型
        cached_models = scan_cache_dir()
        for repo in cached_models.repos:
            if repo.repo_type == 'model':
                local_models.append({
                    "name": repo.repo_id,
                    "description": f"HuggingFace缓存模型，占用磁盘 {repo.size_on_disk / (1024**2):.2f} MB。",
                    "url": f"https://huggingface.co/{repo.repo_id}",
                    "location": "huggingface_cache"
                })
        
        if not local_models:
             pass  # [自动清理] 已移除输出语句
        
        pass  # [自动清理] 已移除输出语句
        return local_models
    except Exception as e:
        pass  # [自动清理] 已移除输出语句
        return []  # 返回空列表而不是默认模型，因为默认模型可能并未实际下载

# 动态生成支持的模型列表
SUPPORTED_MODELS = get_local_supported_models()

def refresh_supported_models():
    """
    重新扫描本地模型并更新 SUPPORTED_MODELS 全局变量
    """
    global SUPPORTED_MODELS
    with model_list_lock:
        pass  # [自动清理] 已移除输出语句
        SUPPORTED_MODELS = get_local_supported_models()
        pass  # [自动清理] 已移除输出语句

# 注释：要启用自定义模型目录功能，请在 .env 文件中添加以下行：
# CUSTOM_MODEL_DIR=/path/to/your/custom/models/directory
# 注意：路径应为绝对路径，或相对于项目根目录的路径

# 自定义异常
class ModelNotFoundError(Exception):
    """当模型在本地未找到时抛出此异常。"""
    pass

def get_active_model_name() -> str:
    """从 .env 文件读取并返回当前激活的模型名称。"""

    return os.getenv("ACTIVE_MODEL_NAME", "Qwen/Qwen3-Embedding-0.6B")

def get_custom_model_dir() -> str:
    """从 .env 文件读取并返回自定义模型存储目录。如果未设置，则返回 None。"""
    model_dir = os.getenv("CUSTOM_MODEL_DIR", "")
    return model_dir if model_dir.strip() != "" else None

def _load_embedding_model_from_local():
    """
    加载 .env 文件中指定的嵌入模型。
    首先尝试从自定义目录加载，如果未找到或未设置自定义目录，则尝试从本地文件加载。
    """
    model_name = get_active_model_name()
    custom_model_dir = get_custom_model_dir()
    
    pass  # [自动清理] 已移除输出语句
    
    # 首先尝试从自定义目录加载（如果设置了自定义目录）
    if custom_model_dir:
        custom_model_path = os.path.join(custom_model_dir, model_name)
        if os.path.exists(custom_model_path):
            pass  # [自动清理] 已移除输出语句
            try:
                model = SentenceTransformer(custom_model_path, local_files_only=True)
                pass  # [自动清理] 已移除输出语句
                return model
            except Exception as e:
                pass  # [自动清理] 已移除输出语句
                # 继续尝试从HuggingFace缓存加载
    
    # 如果自定义目录加载失败或未设置自定义目录，尝试从HuggingFace缓存加载
    try:
        model = SentenceTransformer(model_name, local_files_only=True)
        pass  # [自动清理] 已移除输出语句
        return model
    except OSError:
        # OSError 通常表示模型文件在 huggingface 缓存目录中不存在
        error_message = (
            f"模型 '{model_name}' 未在本地缓存或自定义目录中找到。\n"
            f"请尝试以下步骤解决:\n"
            f"1. 确认模型名称拼写是否正确。\n"
            f"2. 如果您是第一次使用此模型，请确保有网络连接，并调用 /api/Embedding/download 接口来下载它。\n"
            f"3. 检查 Hugging Face 缓存目录或自定义模型目录的权限是否正确。\n"
            f"4. 如果使用自定义模型目录，请确保 CUSTOM_MODEL_DIR 环境变量已正确设置。"
        )
        raise ModelNotFoundError(error_message)

def initialize_global_model():
    """加载嵌入模型并将其存储在全局变量中。此函数应在应用启动时调用。"""
    global embedding_model_instance
    if embedding_model_instance is None:
        embedding_model_instance = _load_embedding_model_from_local()
    else:
        pass  # [自动清理] 已移除输出语句

def get_embedding_model():
    """获取已加载的全局模型实例。"""
    if embedding_model_instance is None:
        raise RuntimeError("模型尚未在应用启动时初始化，请检查 main.py 中的 lifespan 配置。")
    return embedding_model_instance

def update_active_model(model_name: str) -> bool:
    """
    更新 .env 文件中的 ACTIVE_MODEL_NAME。

    Args:
        model_name: 要设置的新的模型名称。

    Returns:
        bool: 如果更新成功则返回 True。
    
    Raises:
        ValueError: 如果模型名称不受支持。
    """
    # 重新扫描本地模型以获取最新列表
    supported_models = get_local_supported_models()
    supported_names = [m['name'] for m in supported_models]
    if model_name not in supported_names:
        raise ValueError(f"不支持的模型: {model_name}。请先下载该模型或检查模型名称是否正确。")

    from services.config import ENV_PATH
    
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    else:
        lines = []

    new_lines = []
    found = False
    for line in lines:
        if line.strip().startswith('ACTIVE_MODEL_NAME='):
            new_lines.append(f'ACTIVE_MODEL_NAME="{model_name}"\n')
            found = True
        else:
            new_lines.append(line)
    
    if not found:
        new_lines.append(f'\nACTIVE_MODEL_NAME="{model_name}"\n')

    with open(ENV_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return True

def get_folder_size(path: str) -> int:
    """计算文件夹总大小"""
    total = 0
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                if os.path.exists(fp):
                    total += os.path.getsize(fp)
    return total

def download_model_from_hub(model_name: str, use_custom_dir: bool = False):
    """
    从 Hugging Face Hub 下载模型。
    
    Args:
        model_name: 要下载的模型名称
        use_custom_dir: 是否下载到自定义目录，默认为 False（下载到HuggingFace缓存）
    """
    # 初始化进度跟踪
    download_progress[model_name] = {'progress': 0, 'status': 'downloading'}
    
    def _download_with_progress():

        try:
            pass  # [自动清理] 已移除输出语句

            # 使用 model_size_utils 中的方法获取模型大小
            total_size, success = get_model_size_with_fs(model_name)
            if success and total_size > 0:
                pass  # [自动清理] 已移除输出语句
            else:
                pass  # [自动清理] 已移除输出语句
                total_size = None

            # 根据模型名称计算预期的下载路径
            expected_path = os.path.join(os.path.expanduser("~/.cache/huggingface/hub"), f"models--{model_name.replace('/', '--')}")

            # 在一个线程中执行下载
            def do_download():
                pass  # [自动清理] 已移除输出语句
                snapshot_download(
                    repo_id=model_name,
                    resume_download=True
                )

            # 启动下载线程
            download_thread = threading.Thread(target=do_download)
            download_thread.start()

            # 在主线程中轮询已下载大小
            last_known_size = 0
            while download_thread.is_alive():
                # 计算当前已下载的大小
                current_size = get_folder_size(expected_path)
                
                # 更新已知大小
                if current_size > last_known_size:
                    last_known_size = current_size
                
                # 计算进度百分比
                if total_size and total_size > 0:
                    progress_percent = min(99.9, (current_size / total_size) * 100)
                    download_progress[model_name]['progress'] = int(progress_percent)  # 取整
                else:
                    # 如果无法获取总大小，则使用本地扫描方法估算进度
                    # 由于我们不知道总大小，使用模拟进度，但会参考已知的下载大小
                    if current_size > 0:
                        # 假设模型大小为1.21GB作为估算基准（Qwen/Qwen3-Embedding-0.6B的实际大小）
                        estimated_total_size = 1.21 * 1024 * 1024 * 1024  # 1.21GB in bytes
                        progress_percent = (current_size / estimated_total_size) * 100
                        if progress_percent <= 100:
                            download_progress[model_name]['progress'] = int(min(progress_percent, 99.9))  # 取整
                        else:
                            download_progress[model_name]['progress'] = 99
                
                time.sleep(0.5)  # 每0.5秒更新一次进度

            # 下载完成后将进度更新为100%
            download_progress[model_name]['progress'] = 100
            download_progress[model_name]['status'] = 'completed'
            pass  # [自动清理] 已移除输出语句
            
            # 在模型下载完成后，刷新支持的模型列表
            refresh_supported_models()
            
        except Exception as e:
            download_progress[model_name] = {'progress': 0, 'status': 'error', 'error': str(e)}
            pass  # [自动清理] 已移除输出语句
            raise

    # 在单独的线程中执行下载任务
    download_thread = threading.Thread(target=_download_with_progress)
    download_thread.daemon = True
    download_thread.start()

def get_download_progress(model_name: str):
    """获取指定模型的下载进度"""
    return download_progress.get(model_name, {'progress': 0, 'status': 'not_found'})


# 从 model_size_utils.py 引入的函数
from huggingface_hub import HfFileSystem, HfApi

def get_model_size_with_fs(model_name: str, token: str | None = None):
    """
    使用 HfFileSystem 获取模型大小。
    model_name 示例: "Qwen/Qwen3-Embedding-0.6B"
    如果仓库受限，请传入 huggingface 访问 token。
    """
    # 1) 优先用 HfFileSystem（fsspec 接口）
    fs = HfFileSystem(token=token) if token else HfFileSystem()
    path = f"hf://{model_name}"  # models 不加前缀，直接放在 hf:// 后面
    try:
        files = fs.ls(path, detail=True, refresh=True)  # detail=True 得到 size 等元数据
        total = sum(f.get("size", 0) or 0 for f in files)
        if total == 0:
            pass  # [自动清理] 已移除输出语句
            return 0, False
        pass  # [自动清理] 已移除输出语句
        return total, True
    except Exception as e:
        # 常见原因：路径写错、仓库不存在或没有权限
        pass  # [自动清理] 已移除输出语句
        # 2) fallback: 使用 HfApi.list_repo_files / repo_info（性能通常更好）
        try:
            api = HfApi(token=token) if token else HfApi()
            # list_repo_files 获取路径列表，repo_info 可返回 siblings（含 size）
            info = api.repo_info(repo_id=model_name, repo_type="model")
            sizes = [f.size for f in getattr(info, "siblings", []) if getattr(f, "size", None) is not None]
            if sizes:
                total = sum(sizes)
                pass  # [自动清理] 已移除输出语句
                return total, True
            pass  # [自动清理] 已移除输出语句
            return 0, False
        except Exception as e2:
            pass  # [自动清理] 已移除输出语句
            return 0, False


class CustomEmbeddingFunction(Embeddings):
    def __init__(self, model: SentenceTransformer):
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents."""
        return self.model.encode(texts).tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query."""
        return self.model.encode(text).tolist()
