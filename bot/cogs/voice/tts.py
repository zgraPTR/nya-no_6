"""読み上げCog"""

import random

import discord
from discord import app_commands
from discord.ext import commands

from modules import VcManager, is_owner, is_join


class Tts(commands.Cog):
    """読み上げCog"""

    def __init__(self, bot: commands.Bot):
        """"""
        self.bot = bot
        self.vcm = VcManager()

    @app_commands.command()
    @app_commands.describe(guild_id="ギルドID", content="読み上げ内容")
    @app_commands.check(is_owner)
    async def add_tts(
        self, interaction: discord.Interaction, guild_id: str, content: str
    ):
        """A: 読み上げ内容追加"""
        self.vcm.add_queue(guild_id, content)
        await interaction.response.send_message("💬 読み上げを追加しました。", ephemeral=True)

    @app_commands.command()
    @app_commands.describe(vcid="VC CH ID")
    @app_commands.check(is_owner)
    async def admin_tts(self, interaction: discord.Interaction, vcid: str):
        """A: テキスト読み上げ開始"""
        voice_channel: discord.VoiceChannel = self.bot.get_channel(int(vcid))
        if voice_channel.guild.voice_client not in self.bot.voice_clients:
            await voice_channel.connect()
            await interaction.response.send_message(
                f"🧾 **{voice_channel.guild.name}** の読み上げを開始しました｡", ephemeral=True
            )
        self.vcm.vc_add(interaction.guild.voice_client, "tts", status= 1)

    @app_commands.command()
    async def leave(self, interaction: discord.Interaction):
        """通話から退出"""
        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect(force=True)
        await interaction.response.send_message(":telephone: 退出しました。")

    @commands.Cog.listener()
    async def on_message(self, message: discord.message.Message):
        """メッセージ受信"""
        if message.author.bot:
            return
        self.vcm.on_message(message)

    @app_commands.command()
    @app_commands.check(is_join)
    async def stop(self, interaction: discord.Interaction):
        """通話の再生を停止する"""
        vc_client: discord.VoiceClient = interaction.guild.voice_client
        if vc_client:
            vc_client.stop()
        await interaction.response.send_message("⏹ 再生を停止しました。")

    @app_commands.command()
    @app_commands.check(is_join)
    @app_commands.describe(headcount="チーム人数")
    async def team(self, interaction: discord.Interaction, headcount: int):
        """通話メンバーをランダムにチーム分け"""
        mes1 = f"```\n通話メンバーを {headcount}人 でチーム分けしました。\n\n"
        # VCメンバー
        usersa = [
            member.display_name for member in interaction.user.voice.channel.members
        ]
        usersa.remove(self.bot.user.display_name)
        random.shuffle(usersa)
        for i in range(0, len(usersa), headcount):
            members = "\n".join(usersa[i + headcount])
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
        """通話でテキスト読み上げ開始"""
        status = room
        if room == 0:
            await interaction.response.send_message(
                f"🧾 **<#{interaction.channel.id}>** の読み上げを開始しました。"
            )
            status = interaction.channel.id
        self.vcm.vc_add(interaction.guild.voice_client, "tts", status)
        await interaction.response.send_message(
            f"🧾 **{interaction.guild.name}** の読み上げを開始しました。"
        )