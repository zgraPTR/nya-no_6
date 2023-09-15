"""Pickle管理する モジュール
"""

import os
import pickle

# ディレクトリ
config_path = "assets/config/"


class Pick:
    """設定ファイル"""

    def __init__(self, filepath="config.bin"):
        """初期化
        Args:
            filepath (str): ファイル名. Defaults to "Config.pick".
        """
        self.filepath = config_path + filepath

    def read(self):
        """読み込む"""

        if not os.path.exists(self.filepath):
            return None
        with open(self.filepath, mode="rb") as f:
            return pickle.load(f)

    def write(self, objdata):
        """書き込む
        Args:
            objdata (_type_): 保存するオブジェクト
        """

        with open(self.filepath, mode="wb") as f:
            pickle.dump(objdata, f)
