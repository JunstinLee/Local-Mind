"""
文件信息识别服务
用于识别文件的详细信息并记录到SQLite数据库中。
"""
import os, hashlib, json, mimetypes, logging, shutil
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime
from .config import DB_PATH, BASE_DIRECTORIES
from .secure_db import get_db_connection, sqlite3

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileInfoService:
    def __init__(self, db_path: str):
        """
        初始化文件信息识别服务
        
        Args:
            db_path: SQLite数据库文件路径
        """
        self.db_path = db_path
        self.json_info_dir = Path(db_path).parent
        self._init_db()

    def _init_db(self):
        """初始化数据库，创建表并执行一次性数据迁移"""
        try:
            # 确保数据库目录存在
            db_dir = Path(self.db_path).parent
            db_dir.mkdir(parents=True, exist_ok=True)
            
            with get_db_connection(self.db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    CREATE TABLE IF NOT EXISTS file_metadata (
                        md5_hash TEXT PRIMARY KEY,
                        file_name TEXT,
                        file_path TEXT,
                        file_extension TEXT,
                        file_size_bytes INTEGER,
                        file_size_readable TEXT,
                        mime_type TEXT,
                        encoding TEXT,
                        created_time TEXT,
                        modified_time TEXT,
                        accessed_time TEXT,
                        is_directory BOOLEAN,
                        is_file BOOLEAN,
                        permissions TEXT,
                        scan_time TEXT
                    )
                """)
                # 数据库表创建完成
                conn.commit()
        except sqlite3.Error as e:
            pass  # [自动清理] 已移除输出语句
            raise

    def get_file_info(self, file_path: str) -> Dict[str, Any]:
        """
        获取文件的详细信息 (此方法逻辑不变)
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            stat = file_path_obj.stat()
            mime_type, encoding = mimetypes.guess_type(str(file_path_obj))
            md5_hash = self._calculate_md5(file_path_obj)
            
            file_info = {
                "file_name": file_path_obj.name,
                "file_path": str(file_path_obj.absolute()),
                "file_extension": file_path_obj.suffix.lower(),
                "file_size_bytes": stat.st_size,
                "file_size_readable": self._format_file_size(stat.st_size),
                "mime_type": mime_type,
                "encoding": encoding,
                "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "accessed_time": datetime.fromtimestamp(stat.st_atime).isoformat(),
                "md5_hash": md5_hash,
                "is_directory": file_path_obj.is_dir(),
                "is_file": file_path_obj.is_file(),
                "permissions": oct(stat.st_mode)[-3:],
                "scan_time": datetime.now().isoformat()
            }
            return file_info
        except (OSError, IOError) as e:
            pass  # [自动清理] 已移除输出语句
            raise

    def save_file_info_to_db(self, file_path: str) -> bool:
        """
        获取文件信息并保存到SQLite数据库中。
        
        Args:
            file_path: 要分析的文件路径
            
        Returns:
            bool: 如果成功保存则返回True
        """
        try:
            file_info = self.get_file_info(file_path)
            
            columns = list(file_info.keys())
            placeholders = ', '.join(['?'] * len(columns))
            values = [file_info.get(col) for col in columns]

            with get_db_connection(self.db_path) as conn:
                c = conn.cursor()
                c.execute(f"""
                    INSERT OR REPLACE INTO file_metadata ({', '.join(columns)})
                    VALUES ({placeholders})
                """, values)
                conn.commit()
            
            pass  # [自动清理] 已移除输出语句
            return True
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            raise

    def batch_save_files_info(self, file_paths: List[str]) -> Dict[str, bool]:
        """
        批量保存多个文件的信息到数据库
        
        Args:
            file_paths: 文件路径列表
            
        Returns:
            Dict[str, bool]: 文件路径到成功状态的映射
        """
        results = {}
        try:
            with get_db_connection(self.db_path) as conn:
                c = conn.cursor()
                for file_path in file_paths:
                    try:
                        file_info = self.get_file_info(file_path)
                        columns = list(file_info.keys())
                        placeholders = ', '.join(['?'] * len(columns))
                        values = [file_info.get(col) for col in columns]
                        
                        c.execute(f"""
                            INSERT OR REPLACE INTO file_metadata ({', '.join(columns)})
                            VALUES ({placeholders})
                        """, values)
                        
                        results[file_path] = True
                    except Exception as e:
                        pass  # [自动清理] 已移除输出语句
                        results[file_path] = False
                conn.commit()
        except sqlite3.Error as e:
            pass  # [自动清理] 已移除输出语句
        return results

    def get_files_by_extension(self, extension: str) -> List[Dict[str, Any]]:
        """
        根据文件扩展名从数据库获取已记录的文件信息
        
        Args:
            extension: 文件扩展名（如 ".txt", ".py"）
            
        Returns:
            List[Dict[str, Any]]: 该扩展名的所有文件信息列表
        """
        try:
            with get_db_connection(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM file_metadata WHERE file_extension = ?", (extension,))
                rows = c.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            return []

    def _calculate_md5(self, file_path: Path) -> str:
        """
        计算文件的MD5哈希值 (此方法逻辑不变)
        """
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except IOError:
            return "无法计算MD5"

    def _format_file_size(self, size_bytes: int) -> str:
        """
        将字节大小格式化为可读格式 (此方法逻辑不变)
        """
        if size_bytes == 0:
            return "0 B"
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        size = float(size_bytes)
        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1
        return f"{size:.2f} {units[unit_index]}"

# --- 全局实例 ---
# 从配置中获取数据库路径并创建服务实例
# 这确保了整个应用使用同一个数据库文件
file_info_service = FileInfoService(db_path=DB_PATH)
