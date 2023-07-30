"""Botを実行する
"""

import asyncio
import os

import discord
from discord.ext import commands

from modules import FileManager, Config, Xor

intents = discord.Intents.default()
intents.message_content = True


class ErrorTree(discord.app_commands.CommandTree):
    """ツリークラス
    Args:
        discord (_type_): _description_
    """

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ):
        try:
            await interaction.response.send_message(":no_entry: エラーが発生しました。")
            raise error
        except Exception as exeption:
            await interaction.channel.send(f":no_entry: エラー : {exeption}")


bot = commands.Bot(
    command_prefix="/", help_command=None, intents=intents, tree_cls=ErrorTree
)


async def start():
    """bot起動"""

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    for i in os.listdir("./cogs"):
        await bot.load_extension(f"cogs.{i}")

    fm = FileManager()
    config = Config()
    token = fm.read_data(config.token_path)

    if not token:
        token = input("Discord Bot Token : ")
    else:
        token_key = input("Token Key : ")
        token = Xor().decrypto_hex_to_text(token, token_key)

    await bot.start(token)


if __name__:
    asyncio.run(start())
