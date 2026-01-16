import json
from pathlib import Path
from typing import Dict, Any

from schemas.settings import Settings
from .config import SETTINGS_FILE_PATH

class SettingsService:
    def __init__(self, settings_file: Path = SETTINGS_FILE_PATH):
        self.settings_file = settings_file
        # 确保设置文件所在的目录存在
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.settings_file.exists():
            # Provide a default structure if the file doesn't exist
            self.settings_file.write_text(Settings(save_chunked_files=True).model_dump_json(indent=4))

    def get_settings(self) -> Settings:
        """Reads settings from the JSON file and returns a Pydantic model."""
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings_data = json.load(f)
            return Settings(**settings_data)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return default settings if file is missing or corrupt
            return Settings(save_chunked_files=True)

    def update_settings(self, settings_update: Dict[str, Any]) -> Settings:
        """Updates the settings file with new values."""
        current_settings = self.get_settings().model_dump()
        current_settings.update(settings_update)
        
        updated_settings = Settings(**current_settings)
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(updated_settings.model_dump(), f, indent=4)
            
        return updated_settings

# Global instance for easy access
settings_service = SettingsService()
