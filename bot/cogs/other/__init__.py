from .group import Group


async def setup(bot):
    """ロード"""
    await bot.add_cog(Group(bot))
