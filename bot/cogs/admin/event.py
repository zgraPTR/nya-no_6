import asyncio

import discord
from discord.ext import commands

from modules import Logger, VoiceManager, VoicePlayer


class Event(commands.Cog):
    """イベントCog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.logger = Logger("message.log")
        self.vcm = VoiceManager()

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        """メッセージ 編集時"""

        if (before.author.bot) or (before.content == after.content):
            return

        await self.logger.message_log(before, after, event_type="編集")

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        """メッセージ 削除時"""

        if message.author.bot:
            return

        await self.logger.message_log(message, None, event_type="削除")

    @commands.Cog.listener()
    async def on_ready(self):
        """ロード時"""

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
        """VC イベント"""

        guild_id = member.guild.id
        vc_data = self.vcm.data

        voice_state: discord.VoiceProtocol | None = member.guild.voice_client

        if not isinstance(voice_state, discord.VoiceClient):
            return

        if len(voice_state.channel.members) == 1:
            await asyncio.sleep(1.5)
            await voice_state.disconnect(force=True)
            self.vcm.delete_vc_data(member.guild.id, "all")
        else:
            # 入退出確認 Trueならreturn
            if (
                not vc_data.tts_statuses.get(guild_id, None)
                # or not self.gd.guild_dict.get(guild_id, {}).get("notice", False)
                or before.channel == after.channel
            ):
                return

            tts_queues = vc_data.tts_queues
            read_text = ""

            if after.channel is None:
                read_text = f"{member.display_name}。 がVCから退出しました。"
            else:
                read_text = f"{member.display_name}。 がVCに参加しました。"

            if not tts_queues.get(guild_id, []):
                tts_queues.setdefault(guild_id, []).append(read_text)
                await VoicePlayer(guild_id).queue(read_text)
            else:
                tts_queues.setdefault(guild_id, []).append(read_text)

            self.vcm.write()
