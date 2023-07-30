"""VC管理"""

import asyncio
import re

import discord
from gtts import gTTS

from modules import Config, FileManager, Logger


class VcConfig:
    """Vc設定"""

    music_loops: dict[int, bool] = {}
    music_queues: dict[int, list[str]] = {}
    music_statuses: dict[int, int] = {}

    tts_queues: dict[int, list[str]] = {}
    tts_statuses: dict[int, int] = {}
    voice_clients: dict[int, discord.voice_client.VoiceClient] = {}


class VoiceManager:
    """VCデータ管理"""

    def __init__(self) -> None:
        """初期化"""

        self.vcc = VcConfig()
        self.fm = FileManager()
        self.config = Config()
        self.vcc: VcConfig | None
        self.read()

    def delete_vc_data(self, guild_id: int, data_type: str = "all") -> None:
        """VCデータ削除
        Args:
            guild_id (int): ギルドID
            data_type (str): music->音楽系削除, tts->読み上げ系削除, all->全削除
        """

        if data_type == "music":
            self.vcc.music_queues.pop(guild_id, None)
            self.vcc.music_loops.pop(guild_id, None)
        elif data_type == "tts":
            self.vcc.tts_queues.pop(guild_id, None)
            self.vcc.tts_statuses.pop(guild_id, None)
        elif data_type == "all":
            self.vcc.music_queues.pop(guild_id, None)
            self.vcc.music_loops.pop(guild_id, None)
            self.vcc.tts_queues.pop(guild_id, None)
            self.vcc.tts_statuses.pop(guild_id, None)
            self.vcc.voice_clients.pop(guild_id, None)

        self.write()

    def write(self):
        """VCデータ書き込み"""

        self.fm.write_data(self.config.voice_path, self.vcc)

    def read(self):
        """VCデータ読み込み"""

        self.vcc = self.fm.read_data(self.config.voice_path)
        if not self.vcc:
            self.vcc = VcConfig()
            self.write()

    @property
    def data(self):
        return self.vcc


class VoicePlayer:
    """VC再生"""

    def __init__(self, guild_id: int):
        """初期化
        Args:
            guild_id (int): ギルドID
        """

        self.config = Config()
        self.fm = FileManager()
        self.vcm = VoiceManager()

        self.guild_id = guild_id
        self.vc_client: discord.VoiceClient = self.vcm.data.voice_clients.get(
            guild_id, None
        )
        self.loop1 = asyncio.get_event_loop()

    async def done(self):
        """再生終了後"""

        if not self.vc_client.is_connected():
            return

        tts_queues = self.vcm.data.tts_queues

        if tts_queues.get(self.guild_id, []):
            tts_queues.get(self.guild_id, []).pop(0)
        if tts_queues.get(self.guild_id, []):
            await VoicePlayer(self.guild_id).queue(
                message=tts_queues.get(self.guild_id, [])[0]
            )

    def edit_message(self, message: discord.Message) -> str:
        """読み上げ用のメッセージを作成する"""

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
        """tts保存"""

        savedir = (
            f"{self.fm.get_assets_path}/{self.config.audio_dir}/{self.guild_id}.mp3"
        )
        speech = gTTS(text, lang="ja")
        speech.save(savedir)
        return savedir

    async def queue(self, message: discord.Message | str = None):
        """再生
        Args:
            message (discord.Message | str): 読み上げないよう(もしくはメッセージ本体)
        """

        # メッセージ判定
        if isinstance(message, discord.message.Message):
            tts_text = self.edit_message(message)
        elif isinstance(message, str):
            tts_text = message

        # 音声ファイル保存
        tts_dir = await self.save_tts(tts_text)

        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(tts_dir, options="-loglevel panic"),
            volume=0.15,
        )

        # 読み上げ
        try:
            self.vc_client.play(
                source, after=lambda a: self.loop1.create_task(self.done())
            )
        except discord.errors.ClientException as clientex:
            Logger.write("ERROR", f"VoicePlayer.queue() > エラー : {clientex}")
            if isinstance(message, discord.message.Message):
                await message.channel.send("> :x: 読み上げエラーが発生しました。\n再接続しています...")
            await self.vc_client.connect(force=True)
