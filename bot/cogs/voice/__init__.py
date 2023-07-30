from .tts import Tts


async def setup(bot):
    """ロード"""
    await bot.add_cog(Tts(bot))
