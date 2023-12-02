"""イベントCog"""

import asyncio

import discord
from discord.ext import commands

from modules import Logger, VcManager


class Event(commands.Cog):
    """イベントCog"""

    def __init__(self, bot: commands.Bot):
        """"""
        self.bot = bot
        self.logger = Logger("message.log")
        self.vcm = VcManager()

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """メッセージ 編集"""
        if (before.author.bot) or (before.content == after.content):
            return
        await self.logger.message_log(before, after, event_type="編集")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """メッセージ 削除"""
        if message.author.bot:
            return
        await self.logger.message_log(message, None, event_type="削除")

    @commands.Cog.listener()
    async def on_ready(self):
        """読み込み完了"""
        await self.bot.tree.sync()
        await self.bot.change_presence(activity=discord.Game(name="にゃーの6代目"))
        self.logger.write("WARNING", f"Event > {self.bot.user.display_name} ログインしました。")

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        """VC状態変化"""
        guild_id = member.guild.id
        vc_data = self.vcm
        voice_state: discord.VoiceProtocol | None = member.guild.voice_client

        if not isinstance(voice_state, discord.VoiceClient):
            return
        if len(voice_state.channel.members) == 1:
                await asyncio.sleep(1.5)
                await voice_state.disconnect(force=True)
                self.vcm.vc_remove(voice_state)
                return
        if before.channel != after.channel:
            if not vc_data.tts_statuses.get(guild_id, None):
                return
            read_text = ""
            if after.channel is None:
                read_text = f"{member.display_name}。 が退出しました。"
            else:
                read_text = f"{member.display_name}。 が参加しました。"
            self.vcm.add_queue(guild_id, read_text)
