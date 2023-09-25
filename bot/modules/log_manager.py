"""ログの保存"""

import logging
import os
import time

import discord

from .config import Config


class Logger:
    """ログ保存"""

    def __init__(self, filepath: str):
        """
        Args:
            filepath (str): ファイル名
        """
        self.config = Config()

        self.logger = logging.getLogger(filepath)
        self.logger.setLevel(logging.WARNING)
        self.formatter = logging.Formatter("----------\n%(asctime)s \n%(message)s")
        self.handler = logging.StreamHandler()
        self.handler.setLevel(logging.WARNING)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        self.fh = logging.FileHandler(self.config.log_dir + filepath, encoding="utf-8")
        self.fh.setLevel(logging.WARNING)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

    async def message_log(
        self, message: discord.Message, edited_message: discord.Message, event_type: str
    ):
        """メッセージの ログ保存
        Args:
            message (discord.Message): 削除されたメッセージ or 編集前メッセージ
            edited_message (discord.Message): 編集済みメッセージ or None
            event_type (str): 削除 or 変更
        """
        content = f"イベント: {event_type}\nチャンネル: {message.guild.name} / {message.channel.name}\nユーザー: {message.author.name}\n\n"
        if edited_message:
            content += f"変更前: {message.content}\n\n変更後: {edited_message.content}"
        else:
            content += f"内容 : {message.content}"
        file_names = []
        if message.attachments:
            for attachment in message.attachments:
                file_names.append(await self.save_attachment(attachment))
        if file_names:
            content += f"\nファイル : {', '.join(file_names)}"
        self.write("WARNING", content)

    async def save_attachment(self, attachment: discord.Attachment) -> str:
        """ファイル保存
        Args:
            attachment (discord.Attachment)
        Returns:
            str: ファイル名
        """
        timestamp = int(time.time())
        file_name = f"{timestamp}_{attachment.filename}"
        await attachment.save(os.path.join(self.config.assets_dir, "file", file_name))
        return file_name

    def write(self, level="WARNING", message=""):
        """ログ出力
        Args:
            level (str): WARNING, ERROR.
            message (str): 内容
        """
        if level == "ERROR":
            self.logger.error(message)
        else:
            self.logger.warning(message)
