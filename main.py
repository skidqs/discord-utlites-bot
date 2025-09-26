import discord
from discord import InteractionContextType, IntegrationType
import os
import asyncio
import logging
		
logger = logging.getLogger("skidqs")	
logger.setLevel(logging.INFO)

status = discord.Status.idle

bot = discord.Bot(
    default_command_contexts={
                  InteractionContextType.guild,
                  InteractionContextType.bot_dm,
                  InteractionContextType.private_channel
    },
    default_command_integration_types={IntegrationType.user_install},
    status=status,
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, is now online")

async def load_cogs():
    for filename in os.listdir("cogs"):

        if not filename.endswith(".py") or filename == "__init__.py":
            continue

        cog_path = f"cogs.{filename[:-3]}"
        try:
            bot.load_extension(cog_path)
            logger.info(f"Loaded cog {cog_path}")
        except Exception as e:
            logger.exception(f"Failed to load cog {cog_path} {e}")



async def run_bot():
    await load_cogs()
    while True:
        try:
            await bot.start("YOUR_BOT_TOKEN")
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print("rate limit exceeded, retrying in 30 seconds")
                await asyncio.sleep(30)
            else:
                raise

if __name__ == "__main__":
    asyncio.run(run_bot())
