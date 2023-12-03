"""管理者Cog"""

import os
import subprocess

import discord
from discord import app_commands
from discord.ext import commands

from modules import is_owner


def cmd(argv: str) -> str:
    """cmdを実行
    Args:
        argv (str): コマンド
    Returns:
        str: 実行結果
    """
    try:
        cmd_run = subprocess.run(
            argv, shell=True, stdout=-1, stderr=-2, text=True, timeout=20, check=False
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

    def __init__(self, bot):
        """"""
        self.bot: commands.Bot = bot

    @app_commands.command()
    @app_commands.check(is_owner)
    @app_commands.describe(argv="実行するコマンド")
    async def execute_cmd(self, interaction: discord.Interaction, argv: str):
        """A: cmdを実行"""
        await interaction.response.send_message("💻 実行しています...")
        await interaction.channel.send(cmd(argv))

    @app_commands.command()
    @app_commands.check(is_owner)
    async def shutdown(self, interaction: discord.Interaction):
        """A: Botを終了"""
        for vcc in self.bot.voice_clients:
            await vcc.disconnect(force=True)
        await interaction.response.send_message("⚙ 終了中です。", ephemeral=True)
        os._exit(4)

    @app_commands.command()
    async def reload(self, interaction: discord.Interaction):
        """A: 拡張機能のみ再読込"""
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
        """A: Botを再起動"""
        for vcc in self.bot.voice_clients:
            await vcc.disconnect(force=True)
        cmd("clear")
        await interaction.response.send_message("再起動中です。", ephemeral=True)
        os._exit(5)

    @app_commands.command()
    async def test(self, interaction: discord.Interaction):
        """テストコマンド"""
        embed = discord.Embed(title="test", description="テスト用")
        embed.add_field(name="test", value="2")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command()
    @app_commands.check(is_owner)
    async def list_guilds(self, interaction: discord.Interaction):
        """A: ギルド 一覧"""
        guild_str = "\n".join(
            [f"{i.name} ( {i.id} )" for i in self.bot.guilds])
        await interaction.response.send_message(
            f"```\n{len(self.bot.guilds)} つのギルドに参加中です。\n{guild_str}\n```"
        )

    @app_commands.command()
    async def trigger_error(self, interaction: discord.Interaction):
        """A: エラーを発生"""
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
