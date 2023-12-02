"""VC管理"""

import re

import discord
from discord.ext import tasks
from gtts import gTTS

from modules import Config, FileManager


class VcManager:
    """VC値 管理"""
    # 曲再生なら使用
    music_loops: dict[int, bool] = {}
    music_queues: dict[int, list[str]] = {}
    music_statuses: dict[int, int] = {}
    # ttsなら使用
    tts_queues: dict[int, list[discord.message.Message | str]] = {}
    tts_statuses: dict[int, int] = {}
    # 再生用
    voice_clients: dict[int, discord.voice_client.VoiceClient] = {}

    def __init__(self) -> None:
        """"""
        self.vcp = VoicePlayer()
    
    def add_queue(self, guild_id: int, read_text: discord.message.Message | str):
        """tts 読み上げ追加
        Args:
            guild_id (int): 
            read_text (str): 
        """
        if not self.vcm_loop.is_running():
            self.vcm_loop.start()
        self.tts_queues.setdefault(guild_id, []).append(read_text)

    @tasks.loop(seconds=1)
    async def vcm_loop(self):
        """読み上げチェック"""
        for i in self.tts_queues:
            queues = self.tts_queues.get(i, [])
            if len(queues) == 0:
                return
            vc = self.voice_clients.get(i, None)
            
            if not vc.is_playing():
                await self.vcp.read_text(vc, self.tts_queues[i][0])
                self.tts_queues[i].pop(0, None)
    
    def on_message(self, message: discord.message.Message):
        """受信時処理
        Args:
            message (discord.message.Message):
        """
        tts_statuses = self.tts_statuses.get(message.guild.id, 0)
        
        if not self.vcm_loop.is_running():
            self.vcm_loop.start()
        if tts_statuses == 1 or tts_statuses == message.channel.id:
            self.add_queue(message.guild.id, message)
        
    def vc_add(self, voice_client: discord.voice_client.VoiceClient, vc_type = "tts", status = 1):
        """vcリスト追加
        Args:
            voice_client (discord.voice_client.VoiceClient):
            vc_type (str, optional): tts
            status : 1 -> ギルド全体, chid
        """
        guild_id = voice_client.guild.id
        self.voice_clients[guild_id] = voice_client

        if vc_type == "tts":
            self.tts_statuses[guild_id] = status

    def vc_remove(self, voice_client: discord.voice_client.VoiceClient, vc_type="tts"):
        """vcリスト削除
        Args:
            voice_client (discord.voice_client.VoiceClient): 
            vc_type (str, optional): tts
        """
        guild_id = voice_client.guild.id
        self.voice_clients.pop(guild_id, None)

        if vc_type == "tts":
            self.tts_statuses.pop(guild_id, None)
            
        if self.vcm_loop.is_running():
            self.vcm_loop.stop()


class VoicePlayer:
    """VC再生"""

    def __init__(self):
        """"""
        self.config = Config()
        self.fm = FileManager()

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
            f"{self.config.audio_dir}{self.guild_id}.mp3"
        )
        speech = gTTS(text, lang="ja")
        speech.save(savedir)
        return savedir

    async def read_text(self, vc_client: discord.voice_client.VoiceClient, message: discord.message.Message | str):
        """再生
        Args:
            message (discord.Message | str): 読み上げ内容
        """
        self.guild_id = vc_client.guild.id
        if isinstance(message, discord.message.Message):
            tts_text = self.edit_message(message)
        elif isinstance(message, str):
            tts_text = message
        tts_dir = await self.save_tts(tts_text)
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(tts_dir),
            volume=0.15,
        )
        vc_client.play(source)
