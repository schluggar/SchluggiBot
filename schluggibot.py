import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger('schluggibot')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename='schluggibot.log', encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class SchluggiBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await self.load_extension(f'cogs.{filename[:-3]}')
                logger.info(f'Loaded extension: {filename}')

    async def on_ready(self):
        logger.info(f'Logged in as: {self.user}')

bot = SchluggiBot()
bot.run(os.getenv('DISCORD_TOKEN'))