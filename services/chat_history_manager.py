from typing import List, Dict
from services.history_services import HistoryService
from services.config import HISTORY_CONFIG

class ChatHistoryManager:
    """
    Manages the business logic of recording chat dialogue turns.
    This service ensures that history is prepared and saved in a consistent manner.
    """
    def __init__(self):
        # Instantiate the low-level history service
        self.history_service = HistoryService(history_dir=HISTORY_CONFIG["history_directory"])

    def record_dialogue_turn(
                self,
                conversation_id: str,
                user_message: str,
                ai_response: str,
                thinking_data: list = None
            ):
                """
                Prepares and saves a single turn of a dialogue.

                Args:
                    conversation_id: The ID of the conversation.
                    user_message: The new user message in this turn.
                    ai_response: The new AI response in this turn.
                    thinking_data: The thinking chain data associated with the AI response (optional).
                """
                try:
                    # First, load the existing history from disk.
                    messages_to_save = self.history_service.load_history_session(conversation_id)
                    pass  # [自动清理] 已移除输出语句

                    # Then, append the new turn.
                    user_message_obj = {"role": "user", "content": user_message}
                    messages_to_save.append(user_message_obj)
                    pass  # [自动清理] 已移除输出语句

                    # Create the AI response object with thinking data if provided
                    ai_message = {"role": "assistant", "content": ai_response}
                    if thinking_data is not None:
                        ai_message["thinkingData"] = thinking_data
                        pass  # [自动清理] 已移除输出语句
                    else:
                        pass  # [自动清理] 已移除输出语句

                    messages_to_save.append(ai_message)

                    # Finally, save the complete, updated list.
                    pass  # [自动清理] 已移除输出语句
                    self.history_service.save_history(messages_to_save, conversation_id)
                except Exception as e:
                    # It's better to log the error here and not let it crash the chat flow.
                    pass  # [自动清理] 已移除输出语句
