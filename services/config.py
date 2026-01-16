"""
配置文件
集中管理所有路径配置，避免硬编码路径问题
"""

import os
import logging
import sys
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

load_dotenv()

# [统一修改] 无论开发还是生产环境，统一将数据存储在用户的 AppData 目录下
# 避免数据分散，同时解决权限问题
DATA_ROOT = Path(os.getenv('APPDATA')) / "Local Knowledge Base" / ".LocalValut"

# .env 文件路径
ENV_PATH = DATA_ROOT / ".env"


def ensure_env_file() -> Path:
    """
    确保 .env 文件存在，如果不存在则创建一个默认的 .env 文件
    
    Returns:
        Path: .env 文件的路径
    """
    logger = logging.getLogger(__name__)
    
    # 确保 .LocalValut 目录存在
    env_dir = ENV_PATH.parent
    env_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查 .env 文件是否存在
    if not ENV_PATH.exists():
        pass  # [自动清理] 已移除输出语句
        
        # 创建默认的 .env 文件内容
        default_env_content = """# 嵌入模型配置
ACTIVE_MODEL_NAME="Qwen/Qwen3-Embedding-0.6B"

# 自定义模型目录（可选）
# CUSTOM_MODEL_DIR=/path/to/your/custom/models/directory

# API配置
API_HOST=0.0.0.0
API_PORT=8000

# 日志级别
LOG_LEVEL=INFO
"""
        # 写入默认内容到 .env 文件
        with open(ENV_PATH, 'w', encoding='utf-8') as f:
            f.write(default_env_content)
        
        pass  # [自动清理] 已移除输出语句
    else:
        pass  # [自动清理] 已移除输出语句
    
    return ENV_PATH


# 基础目录配置 - 以前端指向为准
BASE_DIRECTORIES = {
    "forRubbables": DATA_ROOT / "forRubbables",
    "uploads": DATA_ROOT / "forRubbables" / "uploads",
    "docs": DATA_ROOT / "forRubbables" / "Docs",  # 新增Docs目录
    "logs": DATA_ROOT / "logs",
    "file_info": DATA_ROOT / "file_info",
    "extracted_texts": DATA_ROOT / "extracted_texts",
    "chunked_outputs": DATA_ROOT / "chunked_outputs",
    "history": DATA_ROOT / "history"
}

# 数据库路径配置
DB_PATH = str(DATA_ROOT / "file_info" / "meta.db")
FILE_INFO_DB_PATH = str(DATA_ROOT / "file_info" / "file_info.db")
SETTINGS_FILE_PATH = DATA_ROOT / "settings.json"


def get_safe_path(path_str: str = "") -> Path:
    """
    获取安全的文件路径，确保在允许的目录内。 (最终修复版)
    该版本能正确处理绝对路径、指向根目录的相对路径、以及指向子目录的相对路径。
    
    Args:
        path_str: 相对或绝对路径字符串
        
    Returns:
        Path: 安全的绝对路径
        
    Raises:
        ValueError: 当路径不安全或无效时抛出异常
    """
    security_base = BASE_DIRECTORIES["forRubbables"].resolve()

    if not path_str:
        return security_base

    requested_path = Path(path_str)

    # 根据路径类型（绝对/相对）决定如何构建最终路径
    if requested_path.is_absolute():
        # 如果是绝对路径，直接使用其解析后的路径
        final_path = requested_path.resolve()
    else:
        # 如果是相对路径，直接在安全基准目录下进行拼接
        final_path = (security_base / requested_path).resolve()

    # 最终安全校验：确保最终路径在允许的 security_base 目录之内
    try:
        final_path.relative_to(security_base)
        return final_path
    except ValueError:
        raise ValueError(f"不安全的路径: '{path_str}' 解析后超出了允许的范围。")


def is_path_in_knowledge_base_work_area(path_str: str) -> Path:
    """
    专门为知识库构建流程验证路径，确保路径在允许的多个工作区内。
    允许的目录包括: forRubbables, extracted_texts, chunked_outputs, 和 chroma_db。
    """
    allowed_bases = [
        BASE_DIRECTORIES["forRubbables"].resolve(),
        BASE_DIRECTORIES["extracted_texts"].resolve(),
        BASE_DIRECTORIES["chunked_outputs"].resolve(),
        Path(CHROMA_DB_CONFIG["persist_directory"]).resolve()
    ]

    if not path_str:
        raise ValueError("路径字符串不能为空。")

    # 创建 Path 对象
    path_obj = Path(path_str)
    
    # 解析为绝对路径
    if path_obj.is_absolute():
        final_path = path_obj.resolve()
    else:
        # 如果是相对路径，尝试在允许的基准目录中查找
        final_path = None
        for base in allowed_bases:
            try_path = (base / path_obj).resolve()
            try:
                try_path.relative_to(base)
                final_path = try_path
                break
            except ValueError:
                continue
        
        # 如果在任何基准目录中都找不到，则使用相对于数据根目录的路径
        if final_path is None:
            final_path = (DATA_ROOT / path_obj).resolve()

    # 检查 final_path 是否位于任何一个允许的基准目录内
    for base in allowed_bases:
        try:
            # 如果 final_path 是 base 的子路径或就是 base 本身，则不会抛出异常
            final_path.relative_to(base)
            return final_path  # 路径安全，返回解析后的绝对路径
        except ValueError:
            # 如果不在当前基准目录内，继续检查下一个
            continue
    
    # 扩展检查：如果路径包含允许的目录名，可能是在不同机器或环境下存储的
    # 检查 path_str 中是否包含允许目录名，如果是，则尝试重建路径
    path_str_lower = path_str.lower()
    for base in allowed_bases:
        base_name = base.name.lower()  # 获取目录名，如 'extracted_texts'
        if base_name in path_str_lower:
            # 尝试从允许的目录重建路径
            try:
                # 尝试找到路径中包含允许目录的部分并重建
                parts = Path(path_str).parts
                for i, part in enumerate(parts):
                    if part.lower() == base_name:
                        # 从匹配的目录开始重建路径
                        reconstructed_path = base / Path(*parts[i+1:])
                        if reconstructed_path.exists():
                            return reconstructed_path
            except:
                continue
    
    # 如果循环结束都没有找到匹配的基准目录，则路径不安全
    raise ValueError(f"不安全的路径: '{path_str}' 解析后超出了知识库允许的所有工作区范围。")


def ensure_directories_exist() -> None:
    """
    确保所有配置的目录存在，如果不存在则自动创建
    
    Raises:
        OSError: 当目录创建失败时抛出异常
    """
    logger = logging.getLogger(__name__)
    
    for dir_name, dir_path in BASE_DIRECTORIES.items():
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            pass  # [自动清理] 已移除输出语句
        except OSError as e:
            pass  # [自动清理] 已移除输出语句
            raise OSError(f"无法创建目录 {dir_name}: {dir_path}") from e


# 初始化时确保所有基础目录存在
# ensure_directories_exist()

# API配置
API_CONFIG = {
    "host": os.getenv("API_HOST", "0.0.0.0"),
    "port": int(os.getenv("API_PORT", 8000)),
    "cors_origins": ["*"],
    "docs_url": "/docs",
    "redoc_url": "/redoc"
}

# 文件上传配置
UPLOAD_CONFIG = {
    "max_file_size": 100 * 1024 * 1024,  # 100MB
    "allowed_extensions": {
        '.txt', '.log', '.md', '.docx', '.html', '.pdf','.pptx'
    },
    "chunk_size": 1024 * 1024  # 1MB chunks for large files
}

# 日志配置
LOGGING_CONFIG = {
    "level": os.getenv("LOG_LEVEL", "INFO").upper(),
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": BASE_DIRECTORIES["logs"] / "app.log"
}

# ChromaDB配置
CHROMA_DB_CONFIG = {
    "persist_directory": str(DATA_ROOT / "chroma_db"),
    "default_collection_name": "knowledge_base_main"
}

# 历史记录配置
HISTORY_CONFIG = {
    "history_directory": str(BASE_DIRECTORIES["history"])
}