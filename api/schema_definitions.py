"""
API JSON Schema definitions for all endpoints
"""

# POST /api/chat schema
CHAT_RAG_SCHEMA = {
    "name": "chat_rag",
    "description": "执行多轮对话RAG流程，每轮都进行检索并返回来源证明",
    "parameters": {
        "type": "object",
        "properties": {
            "conversation_id": {"type": "string", "description": "对话ID"},
            "user_id": {"type": "string", "description": "用户ID"},
            "message": {"type": "string", "description": "用户消息"},
            "history": {
                "type": "array",
                "items": {"type": "object"},
                "description": "对话历史"
            },
            "options": {
                "type": "object",
                "properties": {
                    "max_docs": {"type": "integer", "default": 5},
                    "use_session_cache": {"type": "boolean", "default": True}
                }
            }
        },
        "required": ["conversation_id", "user_id", "message"]
    }
}

# POST /api/verify_file schema
VERIFY_FILE_SCHEMA = {
    "name": "verify_file",
    "description": "检查文件是否存在",
    "parameters": {
        "type": "object",
        "properties": {
            "file_name": {"type": "string", "description": "要验证的文件名"}
        },
        "required": ["file_name"]
    }
}

# POST /api/cross_check_retrieval schema
CROSS_CHECK_RETRIEVAL_SCHEMA = {
    "name": "cross_check_retrieval",
    "description": "交叉验证检索结果的有效性",
    "parameters": {
        "type": "object",
        "properties": {
            "retrieved_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "file_id": {"type": "string"},
                        "title": {"type": "string"},
                        "path": {"type": "string"},
                        "score": {"type": "number"}
                    }
                }
            },
            "available_files": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["retrieved_items", "available_files"]
    }
}

# POST /api/format_answer schema
FORMAT_ANSWER_SCHEMA = {
    "name": "format_answer",
    "description": "格式化或修复答案的JSON格式",
    "parameters": {
        "type": "object",
        "properties": {
            "raw_answer": {"type": "string", "description": "原始答案文本"},
            "schema": {
                "type": "object",
                "description": "用于验证答案的JSON Schema"
            }
        },
        "required": ["raw_answer"]
    }
}

# GET /api/files schema
LIST_FILES_SCHEMA = {
    "name": "list_files",
    "description": "获取所有已入库文件的列表",
    "parameters": {
        "type": "object",
        "properties": {}
    }
}

# GET /api/files/{file_id} schema
GET_FILE_INFO_SCHEMA = {
    "name": "get_file_info",
    "description": "获取特定文件的详细信息",
    "parameters": {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "文件ID"}
        },
        "required": ["file_id"]
    }
}

# GET /api/files/{file_id}/chunks schema
GET_FILE_CHUNKS_SCHEMA = {
    "name": "get_file_chunks",
    "description": "获取特定文件的所有分块信息",
    "parameters": {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "文件ID"}
        },
        "required": ["file_id"]
    }
}

# GET /api/files/{file_id}/content schema
GET_FILE_CONTENT_SCHEMA = {
    "name": "get_file_content",
    "description": "获取特定文件在向量库中的内容",
    "parameters": {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "文件ID"},
            "collection_name": {"type": "string", "description": "集合名称", "default": "knowledge_base_small"},
            "limit": {"type": "integer", "description": "返回结果数量限制", "default": 100}
        },
        "required": ["file_id"]
    }
}

# GET /api/files/{file_id}/status schema
GET_FILE_STATUS_SCHEMA = {
    "name": "get_file_status",
    "description": "获取文件在双层索引中的状态",
    "parameters": {
        "type": "object",
        "properties": {
            "file_id": {"type": "string", "description": "文件ID"}
        },
        "required": ["file_id"]
    }
}

# 定义所有可用的工具Schema
ALL_TOOL_SCHEMAS = [
    CHAT_RAG_SCHEMA,
    VERIFY_FILE_SCHEMA,
    CROSS_CHECK_RETRIEVAL_SCHEMA,
    FORMAT_ANSWER_SCHEMA,
    LIST_FILES_SCHEMA,
    GET_FILE_INFO_SCHEMA,
    GET_FILE_CHUNKS_SCHEMA,
    GET_FILE_CONTENT_SCHEMA,
    GET_FILE_STATUS_SCHEMA
]