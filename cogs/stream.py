import discord
from discord.ext import commands, tasks
import itertools

STREAM_STATUSES = [
    {"name": " ", "url": "https://twitch.tv/0day"},
]

ROTATION_INTERVAL = 60

class Stream(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_cycle = itertools.cycle(STREAM_STATUSES)
        self.rotate_status.start()

    def cog_unload(self):
        self.rotate_status.cancel()

    @tasks.loop(seconds=ROTATION_INTERVAL)
    async def rotate_status(self):
        await self.bot.wait_until_ready()
        next_status = next(self.status_cycle)
        activity = discord.Streaming(name=next_status["name"], url=next_status["url"])
        await self.bot.change_presence(status=discord.Status.online, activity=activity)

def setup(bot):
    bot.add_cog(Stream(bot))
