import discord
from discord.ext import commands
import os
import logging

logger = logging.getLogger('schluggibot')

class WelcomeRoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        role_id = os.getenv('WELCOME_ROLE_ID')
        self.welcome_role_id = int(role_id) if role_id else None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.bot.wait_until_ready()

        if not self.welcome_role_id:
            logger.warning("WELCOME_ROLE_ID is not configured.")
            return

        role = member.guild.get_role(self.welcome_role_id)
        if role:
            try:
                await member.add_roles(role)
                logger.info(f"Role '{role.name}' given to {member.name}.")
            except discord.Forbidden:
                logger.error("Error: Bot doesn't have the right to assign roles to users.")
            except Exception as e:
                logger.error(f"Error assigning role: {e}")
        else:
            logger.error(f"Role with ID {self.welcome_role_id} not found.")

async def setup(bot):
    await bot.add_cog(WelcomeRoleCog(bot))