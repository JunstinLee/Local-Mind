import os, json, uuid
from datetime import datetime, timedelta, date
import logging
from logging import StreamHandler, Formatter
from services.config import HISTORY_CONFIG

def configure_logging():
    """
    配置日志记录器。
    该函数设置一个名为 'history_service' 的日志记录器，确保它只被配置一次，
    并将其日志级别设置为 INFO。日志消息将被格式化并输出到控制台。
    """
    logger = logging.getLogger('history_service')
    if not logger.handlers:  # 避免重复添加处理程序
        logger.setLevel(logging.INFO)
        # 创建控制台处理程序
        handler = StreamHandler()
        # 定义日志消息的格式
        formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

class HistoryService:
    """
    历史记录服务类，用于管理聊天历史的保存、加载和清除。
    聊天历史以 JSON 文件的形式存储在指定目录下。
    """
    def __init__(self, history_dir=None):
        """
        初始化 HistoryService 实例。
        
        Args:
            history_dir (str, optional): 存储历史记录的目录名称，默认使用配置文件中的路径。
        """
        # 如果没有提供历史记录目录，则使用配置文件中的默认路径
        if history_dir is None:
            history_dir = HISTORY_CONFIG["history_directory"]
        
        self.logger = configure_logging() # 获取配置好的日志记录器
        pass  # [自动清理] 已移除输出语句
        self.history_dir = history_dir
        # 如果历史记录目录不存在，则创建它
        os.makedirs(self.history_dir, exist_ok=True)
    
    def save_history(self, messages: list, session_id: str = None):
        """
        保存历史记录，支持更新现有会话或创建新会话。
        
        Args:
            messages (list): 要保存的消息列表。列表中的每个元素预期是
                             一个具有 'role' 和 'content' 属性的对象，或者是一个字典。
            session_id (str, optional): 会话的唯一标识符。如果为 None，则会生成一个新的。
                                        默认为 None。
        
        Returns:
            str: 保存的会话的唯一标识符。
        
        Raises:
            Exception: 如果保存历史记录失败。
        """
        try:
            pass  # [自动清理] 已移除输出语句
            
            # 生成或复用会话ID
            if session_id is None:
                session_id = str(uuid.uuid4()) # 生成一个新的 UUID 作为会话 ID
                pass  # [自动清理] 已移除输出语句
            else:
                pass  # [自动清理] 已移除输出语句
            
            # 加载现有历史记录以检查重复
            existing_messages = self.load_history_session(session_id) if session_id else []
            
            # 去重逻辑：如果现有历史记录不为空，且新消息列表不为空
            if existing_messages and messages:
                # 检查新消息列表的第一项是否与现有历史记录的最后一项重复
                last_existing = existing_messages[-1]
                first_new = messages[0] if isinstance(messages[0], dict) else \
                           {'role': messages[0].role if hasattr(messages[0], 'role') else getattr(messages[0], 'get', lambda key, default=None: default)('role', None),
                            'content': messages[0].content if hasattr(messages[0], 'content') else getattr(messages[0], 'get', lambda key, default=None: default)('content', ''),
                            'thinking_chains': getattr(messages[0], 'thinking_chains', []) if hasattr(messages[0], 'thinking_chains') else getattr(messages[0], 'get', lambda key, default=None: default)('thinking_chains', [])}
                
                # 检查角色和内容是否完全相同
                if (last_existing.get('role') == first_new.get('role') and
                    last_existing.get('content') == first_new.get('content')):
                    # 如果是重复消息，从消息列表中移除第一项
                    pass  # [自动清理] 已移除输出语句
                    messages = messages[1:] if len(messages) > 1 else []

            # 生成标题
            title = "New Chat" # 默认标题
            if messages and len(messages) > 0:
                for msg in messages:
                    # 尝试从第一条用户消息的内容中提取标题
                    if (hasattr(msg, 'role') and msg.role == 'user' and 
                        hasattr(msg, 'content') and msg.content) or \
                       (isinstance(msg, dict) and msg.get('role') == 'user' and msg.get('content')):
                        title = (msg.content if hasattr(msg, 'content') else msg.get('content'))[:50] # 截取前50个字符作为标题
                        break
            
            filename = f"{session_id}.json" # 构造文件名
            filepath = os.path.join(self.history_dir, filename) # 构造文件完整路径

            # 将消息转换为字典格式，以便序列化为 JSON
            messages_as_dicts = []
            for i, message in enumerate(messages):
                if hasattr(message, 'dict'):
                    # 如果消息对象有 'dict' 方法（例如 Pydantic 模型），则调用它
                    message_dict = message.dict()
                else:
                    # 否则，假设它是字典或具有 'role'、'content' 和 'thinkingData' 属性的对象
                    message_dict = {
                        'role': message.role if hasattr(message, 'role') else getattr(message, 'get', lambda key, default=None: default)('role', None),
                        'content': message.content if hasattr(message, 'content') else getattr(message, 'get', lambda key, default=None: default)('content', ''),
                        'thinkingData': getattr(message, 'thinkingData', []) if hasattr(message, 'thinkingData') else getattr(message, 'get', lambda key, default=None: default)('thinkingData', [])
                    }

                # 添加调试输出
                pass  # [自动清理] 已移除输出语句

                messages_as_dicts.append(message_dict)

            # 准备要保存的数据
            data_to_save = {
                "title": title,
                "messages": messages_as_dicts,
                "session_id": session_id,
                "updated_at": datetime.now().isoformat() # 记录更新时间
            }

            # 将数据写入 JSON 文件
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4) # 写入文件，保持非 ASCII 字符，并使用4个空格缩进
            
            pass  # [自动清理] 已移除输出语句
            return session_id # 返回会话 ID
            
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            raise # 重新抛出异常

    def load_history_list(self) -> list:
        """
        加载所有历史记录会话的列表，并按日期（今天、昨天、更早）分类和排序。
        
        Returns:
            list: 包含按日期分类的会话信息（id 和 title）的列表。
                  每个元素是一个字典，类型为 "separator" 或 "session"。
        """
        try:
            today = date.today()
            yesterday = today - timedelta(days=1)

            all_items = os.listdir(self.history_dir) # 获取历史记录目录中的所有文件和文件夹
            files = []
            for item in all_items:
                if item.endswith(".json"): # 过滤出 JSON 文件
                    files.append(item)
            
            if not files:
                pass  # [自动清理] 已移除输出语句
                return []

            # 按文件修改时间降序排序文件列表
            files.sort(key=lambda f: os.path.getmtime(os.path.join(self.history_dir, f)), reverse=True)
            
            date_files = {} # 用于按日期存储文件信息的字典

            for filename in files:
                filepath = os.path.join(self.history_dir, filename)
                try:
                    file_modified_time = os.path.getmtime(filepath) # 获取文件最后修改时间戳
                    file_date = datetime.fromtimestamp(file_modified_time).date() # 将时间戳转换为日期
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f) # 加载 JSON 数据
                        # 获取标题，如果不存在则使用文件名作为默认标题
                        title = data.get("title", os.path.splitext(filename)[0]) 
                except (FileNotFoundError, PermissionError, json.JSONDecodeError) as e:
                    # 捕获文件访问或解析错误
                    pass  # [自动清理] 已移除输出语句
                    continue # 跳过当前文件，处理下一个

                # 根据日期判断是今天、昨天还是更早的日期
                if file_date == today:
                    date_str = "今天"
                elif file_date == yesterday:
                    date_str = "昨天"
                else:
                    date_str = file_date.strftime("%Y-%m-%d") # 格式化为 YYYY-MM-DD 形式
                
                # 将文件信息添加到对应的日期分类中
                if date_str not in date_files:
                    date_files[date_str] = []
                date_files[date_str].append({"id": os.path.splitext(filename)[0], "title": title})
            
            result = []
            # 获取所有日期键
            date_keys = list(date_files.keys())
            
            # 分离"今天"和"昨天"与其他日期
            today_items = [d for d in date_keys if d == "今天"]
            yesterday_items = [d for d in date_keys if d == "昨天"]
            other_dates = [d for d in date_keys if d not in ["今天", "昨天"]]
            
            # 对其他日期进行降序排序（从新到旧）
            other_dates_sorted = sorted(other_dates, reverse=True)
            
            # 组合最终结果：今天、昨天、其他日期（从新到旧）
            sorted_dates = today_items + yesterday_items + other_dates_sorted
            
            # 使用排序后的日期
            for date_str in sorted_dates:
                result.append({"type": "separator", "title": f"-----{date_str}-----"}) # 添加日期分隔符
                result.extend([{"type": "session", **item} for item in date_files[date_str]]) # 添加会话列表
            return result
        
        except FileNotFoundError:
            pass  # [自动清理] 已移除输出语句
            return [] # 目录不存在时返回空列表
        
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            return [] # 发生其他错误时返回空列表

    def load_history_session(self, session_id: str):
        """
        根据会话 ID 加载特定的历史记录会话。
        
        Args:
            session_id (str): 要加载的会话的唯一标识符。
        
        Returns:
            list: 加载的会话中的消息列表。如果会话不存在或加载失败，则返回空列表。
        """
        try: 
            filename = f"{session_id}.json" # 构造文件名
            filepath = os.path.join(self.history_dir, filename) # 构造文件完整路径
            pass  # [自动清理] 已移除输出语句

            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f) # 从文件中加载 JSON 数据
            pass  # [自动清理] 已移除输出语句

            # 确保加载的消息包含thinkingData字段
            messages = data.get("messages", [])
            pass  # [自动清理] 已移除输出语句
            for i, message in enumerate(messages):
                if 'thinkingData' not in message:
                    message['thinkingData'] = []
                    pass  # [自动清理] 已移除输出语句
                else:
                    pass  # [自动清理] 已移除输出语句

            return messages # 返回消息列表，如果不存在则返回空列表
        except FileNotFoundError:
            pass  # [自动清理] 已移除输出语句
            return [] # 文件未找到时返回空列表
        except json.JSONDecodeError:
            pass  # [自动清理] 已移除输出语句
            return [] # JSON 解码错误时返回空列表
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
            return [] # 发生其他错误时返回空列表

    def clear_history(self):
        """
        清除所有历史记录文件。
        """
        try:
            all_items = os.listdir(self.history_dir) # 获取历史记录目录中的所有文件和文件夹
            for item in all_items:
                filepath = os.path.join(self.history_dir, item)
                if os.path.isfile(filepath) and item.endswith(".json"): # 检查是否是 JSON 文件
                    os.remove(filepath) # 删除文件
            pass  # [自动清理] 已移除输出语句
        except Exception as e:
            pass  # [自动清理] 已移除输出语句
