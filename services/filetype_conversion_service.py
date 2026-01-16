
import os,json,shutil,uuid
from datetime import datetime
from pathlib import Path

from markitdown import MarkItDown

from services.config import BASE_DIRECTORIES
from services.fileinfo_service import file_info_service

# 定义日志和输出目录
CONVERTED_TEXTS_DIR = BASE_DIRECTORIES["extracted_texts"]
CONVERSION_LOG_DIR = CONVERTED_TEXTS_DIR / "Converfile_info"

# 在模块加载时确保目录存在
CONVERSION_LOG_DIR.mkdir(parents=True, exist_ok=True)

# 支持的文件类型
COPY_EXTENSIONS = {".md", ".txt", ".log"}
CONVERT_EXTENSIONS = {".docx", ".ppt", ".pptx", ".html", ".pdf"}
SUPPORTED_EXTENSIONS = COPY_EXTENSIONS.union(CONVERT_EXTENSIONS)        

def _log_conversion_event(log_data: dict):
    """将单次转换的详细日志记录到按源文件后缀分类的JSON文件中。"""
    try:
        source_extension = log_data.get("source_info", {}).get("file_extension", ".unknown").lstrip('.')
        log_filename = f"{source_extension}.json"
        log_filepath = CONVERSION_LOG_DIR / log_filename

        existing_logs = []
        if log_filepath.exists():
            with open(log_filepath, 'r', encoding='utf-8') as f:
                try:
                    existing_logs = json.load(f)
                except json.JSONDecodeError:
                    pass  # [自动清理] 已移除输出语句

        existing_logs.append(log_data)

        with open(log_filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_logs, f, ensure_ascii=False, indent=4)

    except Exception as e:
        pass  # [自动清理] 已移除输出语句


def _get_last_log_entry(source_path: Path):
    """获取指定源文件的最后一条日志记录"""
    try:
        # 从源文件路径获取扩展名
        source_extension = source_path.suffix.lstrip('.')
        if not source_extension:
            source_extension = "unknown"
        log_filename = f"{source_extension}.json"
        log_filepath = CONVERSION_LOG_DIR / log_filename

        if log_filepath.exists():
            with open(log_filepath, 'r', encoding='utf-8') as f:
                try:
                    logs = json.load(f)
                    # 找到与源路径匹配的最后一条记录
                    for log in reversed(logs):
                        if log.get("source_info", {}).get("file_path") == str(source_path):
                            return log
                except json.JSONDecodeError:
                    pass  # [自动清理] 已移除输出语句
    except Exception as e:
        pass  # [自动清理] 已移除输出语句
    
    return None

def process_file_task(source_path_obj: Path) -> str | None:
    """处理单个文件任务（复制或转换），并记录结果。"""
    log_entry = {
        "conversion_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "status": "failure",
        "source_info": None,
        "output_info": None,
        "action": "unknown",
        "error_message": None
    }

    try:
        # 1. 获取源文件信息
        log_entry["source_info"] = file_info_service.get_file_info(str(source_path_obj))
        file_ext = source_path_obj.suffix.lower()

        if file_ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"不支持的文件类型: {file_ext}")

        # 检查是否是空文件
        if source_path_obj.stat().st_size == 0:
            raise ValueError(f"空文件: {source_path_obj}")

        # 2. 计算相对于基础目录的路径，以保留目录结构
        source_relative_to_base = source_path_obj.relative_to(BASE_DIRECTORIES["forRubbables"])
        # 构建目标路径，保留原始目录结构
        target_path = CONVERTED_TEXTS_DIR / source_relative_to_base
        
        # 确保目标目录存在
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # 3. 执行复制或转换操作
        if file_ext in COPY_EXTENSIONS:
            log_entry["action"] = "copy"
            shutil.copy2(source_path_obj, target_path)
        else: # CONVERT_EXTENSIONS
            log_entry["action"] = "convert"
            # 将转换后的文件保存到对应位置，保持目录结构
            target_path = target_path.with_suffix('.md')
            
            md = MarkItDown()
            result = md.convert(str(source_path_obj))
            
            if result and result.text_content:
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(result.text_content)
            else:
                # 如果转换结果为空，创建一个空文件或记录警告（视需求而定，这里抛出异常更合适以便记录失败）
                raise ValueError("文件转换未能生成内容")

        # 4. 获取输出文件信息并更新日志
        log_entry["output_info"] = file_info_service.get_file_info(str(target_path))
        log_entry["status"] = "success"
        pass  # [自动清理] 已移除输出语句
        return str(target_path.resolve())

    except Exception as e:
        error_msg = f"处理文件 {source_path_obj} 时失败: {e}"
        pass  # [自动清理] 已移除输出语句
        log_entry["error_message"] = error_msg
        # 特别处理空文件错误
        if "空文件" in str(e):
            log_entry["status"] = "empty_file"
        return None
    
    finally:
        # 4. 无论成功或失败，都记录日志
        _log_conversion_event(log_entry)
