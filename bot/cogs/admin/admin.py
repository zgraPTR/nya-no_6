"""管理者用Cog"""

import os
import subprocess

import discord
from discord import app_commands
from discord.ext import commands

from modules import is_owner


def cmd(args1: str) -> str:
    """cmd 実行"""

    try:
        cmd_run = subprocess.run(
            args1, shell=True, stdout=-1, stderr=-2, text=True, timeout=10, check=False
        )
        cmd_res = cmd_run.stdout
        print("\n", cmd_res)

        if len(cmd_res) < 1900:
            return f"```\n実行結果\n\n{cmd_res}\n```"
        else:
            return f"```\n実行結果 (略)\n\n{cmd_res[:1900]}\n```"
    except subprocess.TimeoutExpired:
        return "⏰ タイムアウトしました。"


class Admin(commands.Cog):
    """管理者Cog"""

    def __init__(self, bot) -> None:
        """管理者用"""

        self.bot: commands.Bot = bot

    @app_commands.command()
    @app_commands.check(is_owner)
    @app_commands.describe(args1="コマンド")
    async def cmd(self, interaction: discord.Interaction, args1: str):
        """A: cmd実行"""

        await interaction.response.send_message("💻 実行しています...")
        await interaction.channel.send(cmd(args1), ephemeral=True)

    @app_commands.command()
    @app_commands.check(is_owner)
    async def exit(self, interaction: discord.Interaction):
        """A: 終了"""

        for vcc in self.bot.voice_clients:
            await vcc.disconnect(force=True)

        cmd("clear")
        await interaction.response.send_message("⚙ 終了中です。", ephemeral=True)
        os._exit(4)

    @app_commands.command()
    async def reload(self, interaction: discord.Interaction):
        """A: リロード"""

        bot = self.bot

        for i in os.listdir("./cogs"):
            cog_path = f"cogs.{i}"
            if cog_path in bot.extensions:
                await bot.unload_extension(cog_path)
            await bot.load_extension(cog_path)

        await interaction.response.send_message("リロードしました。", ephemeral=True)

    @app_commands.command()
    @app_commands.check(is_owner)
    async def restart(self, interaction: discord.Interaction):
        """A: 再起動"""

        for vcc in self.bot.voice_clients:
            await vcc.disconnect(force=True)

        cmd("clear")

        await interaction.response.send_message("再起動中です。", ephemeral=True)
        os._exit(5)

    @app_commands.command()
    async def test(self, interaction: discord.Interaction):
        """テスト"""

        embed = discord.Embed(title="test", description="テスト用")
        embed.add_field(name="test", value=f"2")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command()
    @app_commands.check(is_owner)
    async def guild_dict(self, interaction: discord.Interaction):
        """A: ギルド 一覧"""

        guild_str = "\n".join([f"{i.name} ( {i.id} )" for i in self.bot.guilds])
        await interaction.response.send_message(
            f"```\n{len(self.bot.guilds)} つのギルドに参加中です。\n{guild_str}\n```"
        )

    @app_commands.command()
    async def test_error(self, interaction: discord.Interaction):
        """A: テストエラー"""
        raise Exception("エラー!")

    @app_commands.command()
    @app_commands.describe(content="内容")
    @app_commands.check(is_owner)
    async def send_dm(
        self, interaction: discord.Interaction, user: discord.User, content: str
    ):
        """A: DM送信"""

        channel = await user.create_dm()
        await channel.send(content)
        await interaction.response.send_message("💬 送信完了", ephemeral=True)
