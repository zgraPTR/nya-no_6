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


class TreeClass(discord.app_commands.CommandTree):
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
    command_prefix="/", help_command=None, intents=intents, tree_cls=TreeClass
)


async def start():
    """bot起動"""
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    config = Config()
    fm = FileManager()

    for folder in config.dir_dict.values():
        print(config.assets_dir, folder)
        os.makedirs(config.assets_dir+folder, exist_ok=True)
    for i in os.listdir("./cogs"):
        await bot.load_extension(f"cogs.{i}")

    token_dict = fm.read_data(config.token_path)
    token = token_dict.get("token", False)
    is_crypto = token_dict.get("is_crypto", 0)

    if not token:
        logger.write(
            "ERROR", "Token が見つかりません。\n/script/set_token.py でtokenを設定してください。"
        )
        os._exit(0)

    if is_crypto:
        if __name__ == "__main__" and len(sys.argv) < 2:
            token_key = input("Token Key : ")
        elif len(sys.argv) < 2:
            logger.write("ERROR", "Token Keyが見つかりません。")
            os._exit(0)
        token_key = sys.argv[1]
        token = Xor().decrypto_hex_to_text(token, token_key)

    await bot.start(token)

asyncio.run(start())
