"""設定ファイル管理、パス管理など
"""


import os
import pickle

from .config import Config


class FileManager:
    """"""

    def __init__(self) -> None:
        """初期化"""
        self.config = Config()

    @property
    def get_assets_path(self) -> str:
        """アセットのパス取得"""
        assets_dir = self.config.assets_dir

        if not os.path.exists(assets_dir):
            assets_dir = assets_dir.replace("..", ".")
        return assets_dir

    @property
    def get_config_path(self) -> str:
        """アセットのパス取得"""
        return self.config.config_dir

    def read_data(self, filename: str):
        """pklファイル読み込み
        Args:
            filename (str): ファイル名
        Returns:
            obj : 内容
        """
        filedir: str = self.get_config_path + filename

        if not os.path.exists(filedir):
            return {}

        with open(filedir, "rb") as load_data:
            objdata = pickle.load(load_data)

        return objdata

    def read_config(self):
        """設定読み込み"""

        Config.data = self.read_data("config.bin")

    def write_data(self, filename: str, objdata) -> None:
        """pklファイル書き込み
        Args:
            filename (str): ファイル名
            objdata : 書き込み内容
        """
        filedir: str = self.get_config_path + filename

        with open(filedir, mode="wb") as f:
            pickle.dump(objdata, f)
