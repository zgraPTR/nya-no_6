"""せ"""

import os

ASSETS_DIR = "../assets/"


class Config:
    """設定値 (デフォルト)"""

    def __init__(self) -> None:
        """初期化"""
        pass

    data = {}

    @property
    def assets_dir(self):
        return ASSETS_DIR

    @property
    def audio_dir(self):
        return ASSETS_DIR + "mp3/"

    @property
    def config_dir(self):
        return ASSETS_DIR + "config/"

    @property
    def log_dir(self):
        return ASSETS_DIR + "log/"

    @property
    def token_path(self):
        return "token.bin"

    @property
    def voice_path(self):
        return "voice.bin"
