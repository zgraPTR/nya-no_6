"""VC管理"""

import re

import discord
from gtts import gTTS

from modules import Config, FileManager


class VcConfig:
    """VC値 (デフォ)"""

    singleton = None
    name = None

    def __new__(cls, *args, **kwargs):
        if cls.singleton == None:
            cls.singleton = super().__new__(cls)
        # クラスのインスタンスを返す
        return cls.singleton

    music_loops: dict[int, bool] = {}
    music_queues: dict[int, list[str]] = {}
    music_statuses: dict[int, int] = {}
    tts_queues: dict[int, list[str]] = {}
    tts_statuses: dict[int, int] = {}
    voice_clients: dict[int, discord.voice_client.VoiceClient] = {}


class VoicePlayer:
    """VC再生"""

    def __init__(self, guild_id: int, vc_client: discord.voice_client.VoiceClient):
        """
        Args:
            guild_id (int):
            vc_client (discord.voice_client.VoiceClient):
        """
        self.config = Config()
        self.fm = FileManager()
        self.guild_id = guild_id
        self.vc_client = vc_client

    def edit_message(self, message: discord.Message) -> str:
        """読み上げメッセージを編集"""

        text = f"{message.author.display_name}。 {message.content}"
        text = re.sub(
            "(https?|ftp)(://[-_.!~*'()a-zA-Z0-9;/?:@&=+$,%#]+)", " URL 省略", text
        )
        text = re.sub("<.+>", " 指定 省略。", text)
        if len(text) >= 40:  # 文字数制限
            text = text[:40] + "。 以下 省略。"
        if message.attachments:
            text += "ファイル添付。"
        return text

    async def save_tts(self, text: str) -> str:
        """音声保存
        Args:
            text (str): 読み上げないよう
        Returns:
            str: ファイルパス
        """
        savedir = (
            f"{self.fm.get_assets_path}/{self.config.audio_dir}/{self.guild_id}.mp3"
        )
        speech = gTTS(text, lang="ja")
        speech.save(savedir)
        return savedir

    async def queue(self, message: discord.message.Message | str = None):
        """再生
        Args:
            message (discord.Message | str): 読み上げ内容
        """
        if isinstance(message, discord.message.Message):
            tts_text = self.edit_message(message)
        elif isinstance(message, str):
            tts_text = message
        tts_dir = await self.save_tts(tts_text)
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(tts_dir, options="-loglevel panic"),
            volume=0.15,
        )
        self.vc_client.play(source)
