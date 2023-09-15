"""Botを実行する
"""

import asyncio
import os
import sys

import discord
from discord.ext import commands

from modules import FileManager, Config, Xor, Logger

intents = discord.Intents.default()
intents.message_content = True

logger = Logger("error.log")


class ErrorTree(discord.app_commands.CommandTree):
    """ツリークラス"""

    async def on_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError,
    ):
        content = f">>> :no_entry: エラーが発生しました。\n{type(error)} : {error}"
        if interaction.response.is_done():
            await interaction.channel.send(content)
        else:
            await interaction.response.send_message(content)

        logger.write("ERROR", f"{type(error)} : {error}")


bot = commands.Bot(
    command_prefix="/", help_command=None, intents=intents, tree_cls=ErrorTree
)


async def start():
    """bot起動"""

    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    config = Config()

    for folder in config.dir_dict.values():
        os.makedirs(config.assets_dir + folder, exist_ok=True)

    fm = FileManager()

    # token準備
    token = fm.read_data(config.token_path)

    if not token:
        logger.write(
            "ERROR", "tokenファイルが見つかりません。\n/script/set_token.py でtokenを設定してください。"
        )
        os._exit(0)
    if len(sys.argv) < 2:
        logger.write("ERROR", "Token Keyが見つかりません。")
        os._exit(0)

    token_key = sys.argv[1]
    token = Xor().decrypto_hex_to_text(token, token_key)

    for i in os.listdir("./cogs"):
        await bot.load_extension(f"cogs.{i}")

    await bot.start(token)


if __name__:
    asyncio.run(start())
