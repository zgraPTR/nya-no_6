"""Pickle管理する モジュール
"""

import json
import os

# ディレクトリ
config_path = "assets/config/"


class JsonManager:
    """設定ファイル"""

    def __init__(self, filepath="config.json"):
        """初期化
        Args:
            filepath (str): ファイル名
        """
        self.filepath = config_path + filepath

    def read(self) -> dict:
        """読み込む"""
        if not os.path.exists(self.filepath):
            return None
        with open(self.filepath, mode="r") as f:
            return json.load(f)

    def write(self, objdata):
        """書き込む
        Args:
            objdata (_type_): 保存するオブジェクト
        """
        with open(self.filepath, mode="w") as f:
            json.dump(objdata, f, indent=4, ensure_ascii=False)
