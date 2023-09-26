"""イベントCog"""

import asyncio

import discord
from discord.ext import commands

from modules import Logger, VcConfig


class Event(commands.Cog):
    """イベントCog"""

    def __init__(self, bot: commands.Bot):
        """"""
        self.bot = bot
        self.logger = Logger("message.log")
        self.vcc = VcConfig()

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
        vc_data = self.vcc
        voice_state: discord.VoiceProtocol | None = member.guild.voice_client
        if not isinstance(voice_state, discord.VoiceClient):
            return
        if before.channel.id == after.channel.id:
            return
        if len(voice_state.channel.members) == 1:
            await asyncio.sleep(1.5)
            await voice_state.disconnect(force=True)
            self.vcc.voice_clients.pop(member.guild.id, None)
        else:
            if not vc_data.tts_statuses.get(guild_id, None):
                return
            tts_queues = vc_data.tts_queues
            read_text = "この文章が再生されたらどこかがおかしいよ!"
            if after.channel is None:
                read_text = f"{member.display_name}。 が退出しました。"
            else:
                read_text = f"{member.display_name}。 が参加しました。"
            tts_queues.setdefault(guild_id, []).append(read_text)
