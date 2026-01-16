# File: api/tree_generator.py

import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Set, Union
from pathlib import Path
import logging

# 导入配置
from services.config import BASE_DIRECTORIES, get_safe_path

# 配置日志
logger = logging.getLogger(__name__)

# --- 1. 创建一个 APIRouter 实例 ---
router = APIRouter(
    prefix="/tree",
    tags=["Directory Tree"],
)

# --- 2. 路径映射组件 ---
class PathMapper:
    """
    前端到后端路径映射逻辑处理类
    """
    
    @staticmethod
    def map_frontend_path(frontend_path: str) -> Path:
        """
        将前端路径映射到后端实际路径
        
        Args:
            frontend_path: 前端传入的路径
            
        Returns:
            Path: 映射后的安全路径
            
        Raises:
            ValueError: 当路径映射失败时抛出异常
        """
        try:
            # 处理前端 'forRubbables' 路径映射
            if frontend_path == "forRubbables" or frontend_path.startswith("forRubbables/"):
                # 移除前端的 'forRubbables' 前缀，映射到实际的 forRubbables/forRubbables/ 目录
                if frontend_path == "forRubbables":
                    relative_path = ""
                else:
                    relative_path = frontend_path[len("forRubbables/"):]
                
                # 使用配置化的安全路径处理
                mapped_path = get_safe_path(relative_path)
                pass  # [自动清理] 已移除输出语句
                return mapped_path
            
            # 处理其他路径，直接使用安全路径处理
            mapped_path = get_safe_path(frontend_path)
            pass  # [自动清理] 已移除输出语句
            return mapped_path
            
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            raise ValueError(f"路径映射失败: {str(e)}") from e
    
    @staticmethod
    def validate_and_create_path(path: Path) -> Path:
        """
        验证路径并在需要时创建目录
        
        Args:
            path: 要验证和创建的路径
            
        Returns:
            Path: 验证后的路径
            
        Raises:
            OSError: 当目录创建失败时抛出异常
        """
        try:
            # 如果目录不存在，创建它
            if not path.exists():
                path.mkdir(parents=True, exist_ok=True)
                pass  # [自动清理] 已移除输出语句
            
            # 验证路径是否为目录
            if not path.is_dir():
                raise ValueError(f"路径不是目录: {path}")
            
            return path
            
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            raise OSError(f"路径验证和创建失败: {str(e)}") from e

# --- 3. 安全性：使用配置化的根目录 ---
SAFE_BASE_DIR = BASE_DIRECTORIES

# --- 3. Pydantic 响应模型 ---
class FileNode(BaseModel):
    id: str
    name: str
    type: str = "file"
    path: str

class FolderNode(BaseModel):
    id: str
    name: str
    type: str = "folder"
    path: str
    children: List[Union['FolderNode', FileNode]] = []
    file_count: int = 0 # 新增字段，默认值为0

# 使用JSON格式的树结构
class TreeResponse(BaseModel):
    requested_path: str
    full_path: str
    tree: List[Union[FolderNode, FileNode]]

# --- 4. JSON树生成函数 ---
def generate_tree_json(dir_path: str, parent_path: str = '') -> List[Union[FolderNode, FileNode]]:
    """递归生成目录树的JSON结构，并计算每个文件夹的文件总数"""
    items = []
    if not os.path.isdir(dir_path):
        return items

    try:
        for item_name in sorted(os.listdir(dir_path)):
            item_path = os.path.join(dir_path, item_name)
            relative_path = os.path.join(parent_path, item_name)
            item_id = f"{parent_path}-{item_name}" if parent_path else item_name

            if os.path.isdir(item_path):
                # 1. 先递归获取子节点
                children_nodes = generate_tree_json(item_path, relative_path)
                
                # 2. 计算当前文件夹的递归文件总数
                recursive_file_count = 0
                for child in children_nodes:
                    if child.type == 'file':
                        recursive_file_count += 1
                    elif child.type == 'folder':
                        recursive_file_count += child.file_count
                
                # 3. 创建包含文件总数的 FolderNode
                folder_node = FolderNode(
                    id=item_id,
                    name=item_name,
                    path=relative_path,
                    children=children_nodes,
                    file_count=recursive_file_count # 传入计算出的总数
                )
                items.append(folder_node)
            else:
                file_node = FileNode(
                    id=item_id,
                    name=item_name,
                    path=relative_path
                )
                items.append(file_node)
    except PermissionError:
        # 处理权限错误
        pass
    except Exception:
        # 处理其他可能的错误
        pass
            
    return items

# --- 5. API 请求模型 ---
class TreeRequest(BaseModel):
    path: str = Field(default=".", description="The relative path from the safe base directory.")
    ignore_dirs: Optional[List[str]] = Field(default_factory=list, description="List of directory names to ignore.")
    ignore_files: Optional[List[str]] = Field(default_factory=list, description="List of file names to ignore.")
    timestamp: Optional[int] = Field(default=None, description="Timestamp for cache busting.")

# --- 6. API 端点 ---
@router.post("/generate", response_model=TreeResponse)
async def create_directory_tree(request: TreeRequest):
    """
    生成并返回给定路径的目录树结构的JSON表示.
    使用新的路径映射逻辑和配置化路径处理.
    """
    try:
        # 记录请求信息，包括时间戳
        pass  # [自动清理] 已移除输出语句
        
        # 使用新的路径映射逻辑
        mapped_path = PathMapper.map_frontend_path(request.path)
        
        # 验证路径并在需要时创建目录
        target_path = PathMapper.validate_and_create_path(mapped_path)
        
        # 生成JSON树结构
        # If the request is for the virtual root, the parent path for node generation should be empty.
        # Otherwise, it's the requested path itself.
        base_parent_path = "" if request.path == "forRubbables" else request.path
        tree_content = generate_tree_json(str(target_path), base_parent_path)
        
        pass  # [自动清理] 已移除输出语句
        
        return TreeResponse(
            requested_path=request.path,
            full_path=str(target_path),
            tree=tree_content,
        )
        
    except ValueError as e:
        # 路径映射或验证错误
        pass  # [自动清理] 已移除输出语句
        raise HTTPException(status_code=400, detail=f"路径处理错误: {str(e)}")
        
    except OSError as e:
        # 目录创建或访问错误
        pass  # [自动清理] 已移除输出语句
        raise HTTPException(status_code=500, detail=f"目录操作失败: {str(e)}")
        
    except Exception as e:
        # 其他未预期的错误
        pass  # [自动清理] 已移除输出语句
        raise HTTPException(status_code=500, detail="生成目录树时发生内部错误")
