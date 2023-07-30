import random

import discord
from discord import app_commands
from discord.ext import commands

from modules import VoiceManager, VoicePlayer, is_owner, is_join


class Tts(commands.Cog):
    """読み上げ関係Cog"""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.vcm = VoiceManager()
        self.vcp = VoicePlayer

    @app_commands.command()
    @app_commands.describe(guild_id="ギルドID", content="読み上げ内容")
    @app_commands.check(is_owner)
    async def add_tts(
        self, interaction: discord.Interaction, guild_id: str, content: str
    ):
        """A: 読み上げ内容追加"""

        tts_queues = self.vcm.data.tts_queues
        guild_id = int(guild_id)

        if not tts_queues.get(guild_id, []):
            tts_queues.setdefault(guild_id, []).append(content)
            await VoicePlayer(guild_id).queue(content)
        else:
            tts_queues.setdefault(guild_id, []).append(content)

        self.vcm.write()
        await interaction.response.send_message("💬 読み上げを追加しました。", ephemeral=True)

    @app_commands.command()
    @app_commands.describe(vcid="VC CH ID")
    @app_commands.check(is_owner)
    async def admin_tts(self, interaction: discord.Interaction, vcid: str):
        """A: VC参加 読み上げ"""

        voice_channel: discord.VoiceChannel = self.bot.get_channel(int(vcid))
        if not voice_channel.guild.voice_client in self.bot.voice_clients:
            await voice_channel.connect()
            await interaction.response.send_message(
                f"🧾 **{voice_channel.guild.name}** の読み上げを開始しました｡", ephemeral=True
            )
        self.vcm.data.tts_statuses[voice_channel.guild.id] = 1
        self.vcm.data.voice_clients[
            voice_channel.guild.id
        ] = voice_channel.guild.voice_client

        self.vcm.write()

    @app_commands.command()
    async def leave(self, interaction: discord.Interaction):
        """通話から退出"""

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect(force=True)
            self.vcm.delete_vc_data(interaction.guild_id, "all")
        await interaction.response.send_message(":telephone: 退出しました。")

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        """メッセージ受信"""
        if message.author.bot:
            return

        tts_flag = self.vcm.data.tts_statuses.get(message.guild.id, None)
        tts_queues = self.vcm.data.tts_queues

        # 全体読み上げ or 指定部屋読み上げ
        if (tts_flag == 1) or (tts_flag == message.channel.id):
            if not tts_queues.get(message.guild.id, []):
                tts_queues.setdefault(message.guild.id, []).append(message)
                await VoicePlayer(message.guild.id).queue(message)
            else:
                tts_queues.setdefault(message.guild.id, []).append(message)
            self.vcm.write()

    @app_commands.command()
    @app_commands.check(is_join)
    async def stop(self, interaction: discord.Interaction):
        """再生停止"""

        vc_client: discord.VoiceClient = interaction.guild.voice_client
        if vc_client:
            vc_client.stop()
        await interaction.response.send_message("⏹ 再生を停止しました。")

    @app_commands.command()
    @app_commands.check(is_join)
    @app_commands.describe(headcount="チーム人数")
    async def team(self, interaction: discord.Interaction, headcount: int):
        """通話メンバー ランダムチーム分け"""

        mes1 = f"```\n通話メンバーを {headcount}人 でチーム分けしました。\n\n"

        # VCメンバー
        usersa = [
            member.display_name for member in interaction.user.voice.channel.members
        ]
        usersa.remove("にゃーの")

        # チーム編成
        random.shuffle(usersa)
        for i in range(0, len(usersa), headcount):
            members = "\n".join(usersa[i : i + headcount])
            mes1 += f"チーム {i}\n{members}\n\n"

        await interaction.response.send_message(f"{mes1}\n```")

    @app_commands.command()
    @app_commands.check(is_join)
    @app_commands.choices(
        room=[
            app_commands.Choice(name="グループ全体", value=1),
            app_commands.Choice(name="このチャンネルのみ", value=0),
        ]
    )
    async def tts(self, interaction: discord.Interaction, room: int = 1):
        """通話 読み上げ開始"""

        self.vcm.delete_vc_data(interaction.guild_id, "music")

        status = room
        if room == 0:
            await interaction.response.send_message(
                f"🧾 **<#{interaction.channel.id}>** の読み上げを開始しました。"
            )
            status = interaction.channel.id
        self.vcm.data.tts_statuses[interaction.guild_id] = status
        await interaction.response.send_message(
            f"🧾 **{interaction.guild.name}** の読み上げを開始しました。"
        )

        self.vcm.write()

    @app_commands.command()
    async def vc_value(self, interaction: discord.Interaction):
        """読み上げない時のデバック用"""

        send_text = f"""```py
tts_queue = {self.vcm.data.tts_queues}
tts_statuses = {self.vcm.data.tts_statuses}
voice_clients = {self.vcm.data.voice_clients}
```"""
        await interaction.response.send_message(send_text)
