"""グループ系Cog"""

import re

import discord
from discord import app_commands
from discord.ext import commands


class Group(commands.Cog):
    """グループCog"""

    def __init__(self, bot: commands.Bot) -> None:
        """グループ用"""

        self.bot = bot

    @app_commands.command()
    @app_commands.describe(user="ユーザー")
    async def boop(self, interaction: discord.Interaction, user: discord.User):
        """Boop!"""

        from_user = interaction.user.name
        channel = await user.create_dm()
        await channel.send(f"From {from_user}: Boop!")
        await interaction.response.send_message(
            f"To {user.name}: Boop!", ephemeral=True
        )

    @app_commands.command()
    @app_commands.describe(content="内容")
    async def contact(self, interaction: discord.Interaction, content: str):
        """お問い合わせ"""

        user = await self.bot.fetch_user(555729675213602816)
        await user.send(
            f"--------------------\n名前: {interaction.user.name} ({interaction.user.id})\n内容: {content}"
        )
        await interaction.response.send_message("💬 送信しました。", ephemeral=True)

    @app_commands.command()
    @app_commands.describe(formula="式")
    async def eval(self, interaction: discord.Interaction, formula: str):
        """式計算"""
        safe_pattern = re.compile(r"^[\d+\-*/.() ]+$")
        if not safe_pattern.match(formula):
            await interaction.response.send_message("⛔ 計算不可能 : 不正な文字列です。")
        else:
            await interaction.response.send_message(f"{formula} = {eval(formula)}")

    @app_commands.command()
    @app_commands.describe(userid="ユーザー固有ID")
    async def profile(self, interaction: discord.Interaction, userid: str):
        """ユーザーIDからプロフィール取得"""

        user = await self.bot.fetch_user(int(userid))
        embed = discord.Embed(title=userid)
        embed.set_thumbnail(url=user.avatar)
        embed.add_field(name="名前", value=f"{user.name}", inline=True)
        embed.add_field(name="作成日", value=user.created_at, inline=True)
        embed.add_field(name="Bot", value=user.bot, inline=True)
        embed.add_field(name="アイコン", value=user.display_avatar, inline=True)
        embed.add_field(name="バナー", value=user.banner, inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command()
    async def ping(self, interaction: discord.Interaction):
        """Ping!"""

        await interaction.response.send_message(
            f"💻 Ping: {round(self.bot.latency*1000, 1)}ms", ephemeral=True
        )
