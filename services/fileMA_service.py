"""
文件管理服务
用于创建文件夹并复制文件到指定文件夹内
"""
import os,shutil,logging,mimetypes,chroma_db
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from datetime import datetime
import mimetypes

# 导入另一个服务
from .fileinfo_service import file_info_service, FileInfoService
# 导入配置
from .config import BASE_DIRECTORIES, UPLOAD_CONFIG, get_safe_path, ensure_directories_exist

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileManagerService:
    def __init__(self, 
                file_info_service_instance: FileInfoService, 
                base_directory: str = None):
        """
        初始化文件管理服务
        
        Args:
            file_info_service_instance: 文件信息服务的实例
            base_directory: 基础目录路径（可选，默认使用配置文件中的路径）
        
        Raises:
            ValueError: 当配置验证失败时抛出异常
            OSError: 当目录创建失败时抛出异常
        """
        try:
            # 使用配置文件中定义的安全路径
            if base_directory is None:
                # 默认使用forRubbables基础目录，但可以通过参数指定其他基础目录
                self.base_directory = BASE_DIRECTORIES["forRubbables"]
            else:
                # 如果提供了base_directory参数，需要确保它是安全的
                self.base_directory = get_safe_path(base_directory)
            pass  # [自动清理] 已移除输出语句
            
            # 确保目标目录存在且可写
            self.base_directory.mkdir(parents=True, exist_ok=True)
            if not os.access(self.base_directory, os.W_OK):
                raise OSError(f"目标目录不可写: {self.base_directory}")
            
            self.file_info_service = file_info_service_instance
            
            # 从配置文件加载文件验证配置
            self.MAX_FILE_SIZE = UPLOAD_CONFIG["max_file_size"]
            self.ALLOWED_EXTENSIONS = UPLOAD_CONFIG["allowed_extensions"]
            
            pass  # [自动清理] 已移除输出语句
            
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            raise ValueError(f"文件管理服务初始化失败: {str(e)}") from e
        
    def create_folder(self, folder_name: str) -> str:
        # ... (此方法保持不变) ...
        try:
            folder_path = self.base_directory / folder_name
            folder_path.mkdir(parents=True, exist_ok=True)
            pass  # [自动清理] 已移除输出语句
            return str(folder_path)
        except OSError as e:
            pass  # [自动清理] 已移除输出语句
            raise OSError(f"创建文件夹失败: {str(e)}")
    
    def copy_file(self, source_path: str, destination_folder: str, new_name: Optional[str] = None, save_info: bool = False) -> Dict[str, Any]:
        """
        复制文件到指定文件夹，并根据需要保存文件信息。
        
        Args:
            source_path: 源文件路径
            destination_folder: 目标文件夹名称
            new_name: 新文件名（可选）
            save_info: 是否同时保存文件信息到JSON
            
        Returns:
            Dict[str, Any]: 包含操作结果的字典
        """
        try:
            source = Path(source_path)
            if not source.exists():
                raise FileNotFoundError(f"源文件不存在: {source_path}")
            
            # 验证文件
            validation_result = self.validate_file(source)
            if not validation_result["is_valid"]:
                raise ValueError(validation_result["error_message"])
            
            # 硬编码目标文件夹为服务的基础目录，忽略前端传入的路径
            # 使用前端传入的destination_folder参数
            destination_dir = get_safe_path(destination_folder)
            destination_dir.mkdir(parents=True, exist_ok=True)

            
            # 获取唯一的文件名
            target_filename = new_name or source.name
            destination_file = self.get_unique_filename(destination_dir, target_filename)
            
            shutil.copy2(source, destination_file)
            pass  # [自动清理] 已移除输出语句
            
            # 处理文件元数据
            result = self.process_file_metadata(
                destination_file, 
                save_info=save_info,
                additional_info={
                    "copied_file_path": str(destination_file),
                    "source_path": str(source),
                    "operation": "copy"
                }
            )

            return result
            
        except (FileNotFoundError, OSError, ValueError) as e:
            pass  # [自动清理] 已移除输出语句
            raise
    
    def save_uploaded_file(self, file_content: bytes, filename: str, destination_folder: str, 
                          content_type: Optional[str] = None, save_info: bool = False) -> Dict[str, Any]:
        """
        保存上传的文件内容到指定文件夹
        
        Args:
            file_content: 文件内容（字节）
            filename: 文件名
            destination_folder: 目标文件夹名称
            content_type: 文件MIME类型
            save_info: 是否保存文件信息到JSON
            
        Returns:
            Dict[str, Any]: 包含操作结果的字典
        """
        try:
            # 验证文件
            validation_result = self.validate_file(filename, len(file_content))
            if not validation_result["is_valid"]:
                raise ValueError(validation_result["error_message"])
            
            # 使用前端传入的 destination_folder 作为目标目录
            destination_dir = get_safe_path(destination_folder)
            destination_dir.mkdir(parents=True, exist_ok=True)
            
            # 获取唯一的文件名
            destination_file = self.get_unique_filename(destination_dir, filename)
            
            # 保存文件
            with open(destination_file, 'wb') as f:
                f.write(file_content)
            
            pass  # [自动清理] 已移除输出语句
            
            # 处理文件元数据
            result = self.process_file_metadata(
                destination_file,
                save_info=save_info,
                additional_info={
                    "original_filename": filename,
                    "content_type": content_type,
                    "operation": "upload"
                }
            )
            
            return result
            
        except (OSError, ValueError) as e:
            pass  # [自动清理] 已移除输出语句
            raise

    def save_uploaded_file_with_structure(self, file_content: bytes, relative_path: str, destination_folder: str, 
                                          content_type: Optional[str] = None, save_info: bool = False) -> Dict[str, Any]:
        """
        保存上传的文件，并根据其相对路径创建子目录结构。

        Args:
            file_content: 文件内容（字节）。
            relative_path: 文件在上传文件夹中的相对路径 (e.g., 'subfolder/image.png')。
            destination_folder: 基础目标文件夹。
            content_type: 文件MIME类型。
            save_info: 是否保存文件信息到JSON。

        Returns:
            Dict[str, Any]: 包含操作结果的字典。
        """
        try:
            # 对相对路径进行安全验证
            safe_relative_path = Path(relative_path.replace('..', ''))
            
            # 验证文件本身（基于文件名和内容）
            validation_result = self.validate_file(safe_relative_path.name, len(file_content))
            if not validation_result["is_valid"]:
                raise ValueError(validation_result["error_message"])

            # 构建完整的目标路径
            # 使用前端传入的 destination_folder 作为基础路径
            destination_path = get_safe_path(destination_folder) / safe_relative_path
            
            # 创建父目录
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            with open(destination_path, 'wb') as f:
                f.write(file_content)
            
            pass  # [自动清理] 已移除输出语句
            
            # 处理文件元数据
            result = self.process_file_metadata(
                destination_path,
                save_info=save_info,
                additional_info={
                    "original_filename": safe_relative_path.name,
                    "relative_path": str(relative_path),
                    "content_type": content_type,
                    "operation": "upload_with_structure"
                }
            )
            
            return result

        except (OSError, ValueError) as e:
            pass  # [自动清理] 已移除输出语句
            raise
    
    def copy_multiple_files(self, file_paths: List[str], destination_folder: str) -> List[str]:
        # ... (此方法保持不变) ...
        copied_files = []
        for file_path in file_paths:
            try:
                # 注意：此处的批量复制暂未接入save_info功能
                result = self.copy_file(file_path, destination_folder, save_info=False)
                copied_files.append(result["copied_file_path"])
            except (FileNotFoundError, OSError) as e:
                pass  # [自动清理] 已移除输出语句
                continue
        return copied_files

    def copy_folder(self, source_folder_path: str, new_name: Optional[str] = None) -> Dict[str, Any]:
        """
        复制整个文件夹到基础目录，并自动保存其中所有文件的元数据。

        Args:
            source_folder_path: 源文件夹的完整路径。
            new_name: 文件夹的新名称（可选）。

        Returns:
            Dict[str, Any]: 包含操作结果的字典。
        """
        try:
            source_folder = Path(source_folder_path)
            if not source_folder.is_dir():
                raise ValueError(f"源路径不是一个有效的文件夹: {source_folder_path}")

            # 修正路径：目标父目录硬编码为 self.base_directory
            dest_parent_dir = self.base_directory
            dest_parent_dir.mkdir(parents=True, exist_ok=True)

            # 确定新文件夹的名称和路径
            target_folder_name = new_name or source_folder.name
            destination_folder = self.get_unique_foldername(dest_parent_dir, target_folder_name)

            # 执行复制
            shutil.copytree(source_folder, destination_folder)
            pass  # [自动清理] 已移除输出语句

            # 固定行为：开始批量保存文件信息
            try:
                pass  # [自动清理] 已移除输出语句
                files_to_process = []
                # 遍历新创建的文件夹，收集所有文件的路径
                for root, _, files in os.walk(destination_folder):
                    for name in files:
                        files_to_process.append(os.path.join(root, name))
                
                if files_to_process:
                    self.file_info_service.batch_save_files_info(files_to_process)
                    pass  # [自动清理] 已移除输出语句
            
            except Exception as e:
                pass  # [自动清理] 已移除输出语句

            return {
                "new_folder_path": str(destination_folder),
                "new_folder_name": destination_folder.name,
                "source_path": str(source_folder_path),
                "operation": "copy_folder"
            }

        except (OSError, ValueError) as e:
            pass  # [自动清理] 已移除输出语句
            raise

    def get_unique_foldername(self, destination_dir: Path, foldername: str) -> Path:
        """
        获取唯一的文件夹名，如果文件夹已存在则添加数字后缀。

        Args:
            destination_dir: 目标目录。
            foldername: 原始文件夹名。

        Returns:
            Path: 唯一的文件夹路径。
        """
        folder_path = destination_dir / foldername
        if not folder_path.exists():
            return folder_path

        counter = 1
        while folder_path.exists():
            new_foldername = f"{foldername}_{counter}"
            folder_path = destination_dir / new_foldername
            counter += 1
        
        return folder_path
    
    def validate_file(self, file_path: Union[str, Path], file_size: Optional[int] = None) -> Dict[str, Any]:
        """
        验证文件是否符合安全和类型要求
        
        Args:
            file_path: 文件路径
            file_size: 文件大小（字节），如果为None则从文件系统获取
            
        Returns:
            Dict[str, Any]: 验证结果，包含 is_valid, error_message, file_info
        """
        try:
            file_path = Path(file_path)
            
            # 检查文件扩展名
            file_ext = file_path.suffix.lower()
            if file_ext not in self.ALLOWED_EXTENSIONS:
                return {
                    "is_valid": False,
                    "error_message": f"不支持的文件类型: {file_ext}",
                    "file_info": None
                }
            
            # 检查文件名安全性
            safe_filename = file_path.name.replace('..', '').replace('/', '').replace('\\', '')
            if not safe_filename or safe_filename != file_path.name:
                return {
                    "is_valid": False,
                    "error_message": "文件名包含不安全字符",
                    "file_info": None
                }
            
            # 获取文件大小
            if file_size is None and file_path.exists():
                file_size = file_path.stat().st_size
            
            # 检查文件大小
            if file_size and file_size > self.MAX_FILE_SIZE:
                return {
                    "is_valid": False,
                    "error_message": f"文件大小超过限制 ({self.MAX_FILE_SIZE // (1024*1024)}MB)",
                    "file_info": None
                }
            
            # 获取MIME类型
            mime_type, _ = mimetypes.guess_type(str(file_path))
            
            return {
                "is_valid": True,
                "error_message": None,
                "file_info": {
                    "filename": file_path.name,
                    "extension": file_ext,
                    "size": file_size,
                    "mime_type": mime_type,
                    "safe_filename": safe_filename
                }
            }
            
        except Exception as e:
            return {
                "is_valid": False,
                "error_message": f"文件验证失败: {str(e)}",
                "file_info": None
            }
    
    def get_unique_filename(self, destination_dir: Path, filename: str) -> Path:
        """
        获取唯一的文件名，如果文件已存在则添加数字后缀
        
        Args:
            destination_dir: 目标目录
            filename: 原始文件名
            
        Returns:
            Path: 唯一的文件路径
        """
        file_path = destination_dir / filename
        
        if not file_path.exists():
            return file_path
        
        # 如果文件已存在，添加数字后缀
        counter = 1
        stem = Path(filename).stem
        suffix = Path(filename).suffix
        
        while file_path.exists():
            new_filename = f"{stem}_{counter}{suffix}"
            file_path = destination_dir / new_filename
            counter += 1
        
        return file_path
    
    def process_file_metadata(self, file_path: Path, save_info: bool = False, additional_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        处理文件元数据，统一保存文件信息的逻辑
        
        Args:
            file_path: 文件路径
            save_info: 是否保存文件信息到JSON
            additional_info: 额外的文件信息
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        result = {
            "file_path": str(file_path),
            "filename": file_path.name,
            "size": file_path.stat().st_size if file_path.exists() else 0,
            "json_file_path": None,
            "json_error": None
        }
        
        # 添加额外信息
        if additional_info:
            result.update(additional_info)
        
        # 如果需要保存文件信息
        if save_info:
            try:
                json_path = self.file_info_service.save_file_info_to_db(str(file_path))
                result["json_file_path"] = json_path
                pass  # [自动清理] 已移除输出语句
            except Exception as e:
                result["json_error"] = f"保存文件信息失败: {str(e)}"
                pass  # [自动清理] 已移除输出语句
        
        return result

    def list_files(
        self,
        base_path: str = None,
        search_term: str = None,
        file_types: List[str] = None,
        sort_by: str = 'name',
        sort_order: str = 'asc'
    ) -> List[dict]:
        """
        列出指定路径下的文件
        
        Args:
            base_path: 基础路径（可选，默认使用配置的基础目录）
            search_term: 搜索关键词
            file_types: 文件类型过滤
            sort_by: 排序方式
            sort_order: 排序顺序
            
        Returns:
            List[dict]: 文件列表
        """
        try:
            # 使用配置化的路径处理
            if base_path is None:
                search_path = self.base_directory
            else:
                search_path = get_safe_path(base_path)
            
            if not search_path.is_dir():
                raise ValueError(f"指定的路径不是一个有效的文件夹: {search_path}")
            
            matched_files = []
            for root, dirs, files in os.walk(search_path):
                for name in files:
                    if file_types:
                        file_ext = os.path.splitext(name)[1].lower()
                        if file_ext not in [ft.lower() for ft in file_types]:
                            continue
                    if search_term:
                        if search_term.lower() not in name.lower():
                            continue
                    file_path = os.path.join(root, name)
                    try:
                        stat = os.stat(file_path)
                        matched_files.append({
                            "name": name,
                            "path": file_path,
                            "size": stat.st_size,
                            "modified_date": datetime.fromtimestamp(stat.st_mtime)
                        })
                    except FileNotFoundError:
                        continue
            
            reverse_order = sort_order == 'desc'
            if sort_by == 'date':
                matched_files.sort(key=lambda f: f['modified_date'], reverse=reverse_order)
            elif sort_by == 'size':
                matched_files.sort(key=lambda f: f['size'], reverse=reverse_order)
            else:
                matched_files.sort(key=lambda f: f['name'].lower(), reverse=reverse_order)
            
            return matched_files
            
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            raise

# 创建全局实例，并注入依赖
file_manager = FileManagerService(file_info_service_instance=file_info_service)
