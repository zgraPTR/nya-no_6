"""権限確認"""

import discord

from .config import Config
from .file_manager import FileManager


def is_owner(interaction: discord.Interaction) -> bool:
    """管理者確認
    Args:
        interaction (discord.Interaction)
    """
    FileManager().read_config()
    return str(interaction.user.id) in Config.data.get("owner_id", "555729675213602816")


async def is_join(interaction: discord.Interaction) -> bool:
    """VC 参加確認"""
    user = interaction.user
    guild = interaction.guild
    if not user.voice:
        await interaction.response.send_message(":question: VCに未接続です。")
        return False
    guild.voice_client or await user.voice.channel.connect()
    return True
