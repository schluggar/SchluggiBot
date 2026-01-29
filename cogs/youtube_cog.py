import discord
from discord.ext import tasks, commands
import feedparser
import os
import logging
import json

logger = logging.getLogger('schluggibot')

class YoutubeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
        self.youtube_id = os.getenv('YOUTUBE_CHANNEL_ID')
        self.feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={self.youtube_id}"
        self.data_file = "resources/video_id.json"
        self.language = os.getenv('LANGUAGE', 'en')
        self.texts = self.load_translations(self.language)
        self.check_for_videos.start()

    def load_translations(self, lang):
        path = f"locales/{lang}.json"
        if not os.path.exists(path):
            path = "locales/en.json"
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_last_id(self):
        if not os.path.exists(self.data_file):
            return None
        try:
            with open(self.data_file, "r", encoding='utf-8') as f:
                data = json.load(f)
                return data.get("last_video_id")
        except (json.JSONDecodeError, KeyError):
            return None

    def set_last_id(self, video_id):
        data = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        data["last_video_id"] = video_id
        
        with open(self.data_file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @tasks.loop(minutes=10)
    async def check_for_videos(self):
        try:
            feed = feedparser.parse(self.feed_url)
            if not feed.entries: return

            latest_video = feed.entries[0]
            current_id = latest_video.get('yt_videoid') or latest_video.id.split(':')[-1]
            
            last_known = self.get_last_id()
            if last_known is None:
                self.set_last_id(current_id)
                logger.info(f"Current video ‘{latest_video.title}’ has been saved as the starting point.")
                return

            if current_id != last_known:
                await self.bot.wait_until_ready()

                self.set_last_id(current_id)
                channel = self.bot.get_channel(self.channel_id)
                if channel:
                    message = self.texts['new_video_msg'].format(title=latest_video.title, link=latest_video.link)
                    try:
                        sent_message = await channel.send(message)
                        logger.info(f"Notification sent: {latest_video.title}")
                        
                        await sent_message.publish()
                        logger.info("Message successfully published.")
                        
                    except discord.HTTPException as e:
                        logger.warning(f"Message sent, but publish failed (no announcement channel?): {e}")
                    except Exception as e:
                        logger.error(f"Error while sending/publishing: {e}")
                else:
                    logger.error(f"Could not send message: Channel {self.channel_id} not found. {self.bot.get_channel(self.channel_id)}")
        except Exception as e:
            logger.error(f"Error in loop: {e}")

async def setup(bot):
    await bot.add_cog(YoutubeCog(bot))