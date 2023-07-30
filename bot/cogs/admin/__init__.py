from .admin import Admin
from .event import Event


async def setup(bot):
    """ロード"""
    await bot.add_cog(Admin(bot))
    await bot.add_cog(Event(bot))
