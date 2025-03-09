import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    """配置管理类，负责读写校园网登录配置"""

    def __init__(self, config_file="campus_config.json"):
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件，如果不存在则创建默认配置"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                from console_ui import ConsoleUI
                ConsoleUI.print_error(f"配置文件 {self.config_file} 格式错误，将使用默认配置")

        # 默认配置
        default_config = {
            "username": "",
            "password": "",
            "operator": "@cmcc",
            "phone": ""
        }

        self._save_config(default_config)
        return default_config

    def _save_config(self, config=None):
        """保存配置到文件"""
        if config is None:
            config = self.config

        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def get(self, key: str, default=None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """设置配置项并保存"""
        self.config[key] = value
        self._save_config()

    def is_config_complete(self) -> bool:
        """检查配置是否完整"""
        return bool(self.config.get("username")) and bool(self.config.get("password"))


if __name__ == "__main__":
    config_manager = ConfigManager()