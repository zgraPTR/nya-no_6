"""ファイルパス"""

import os

ASSETS_DIR = "../assets/"


class Config:
    """設定値"""

    def __init__(self):
        """"""
        pass

    data = {}

    @property
    def assets_dir(self):
        assets_dir_ = ASSETS_DIR
        if not os.path.exists(assets_dir_):
            assets_dir_ = assets_dir_.replace("..", ".")
        return assets_dir_

    @property
    def audio_dir(self):
        return self.assets_dir+self.dir_dict["audio"]

    @property
    def config_dir(self):
        return self.assets_dir + self.dir_dict["config"]

    @property
    def dir_dict(self):
        dir_dict = {"audio": "mp3/", "config": "config/", "log": "log/"}
        return dir_dict

    @property
    def log_dir(self):
        return self.assets_dir + self.dir_dict["log"]

    @property
    def token_path(self):
        return "token.json"

    @property
    def voice_path(self):
        return "voice.json"
