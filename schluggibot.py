from discord.ext import tasks
from dotenv import load_dotenv
import discord
import feedparser
import os
import logging
import json

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))
AUTO_ROLE_ID = os.getenv('AUTO_ROLE_ID')
if AUTO_ROLE_ID:
    AUTO_ROLE_ID = int(AUTO_ROLE_ID)
LANGUAGE = os.getenv('LANGUAGE', 'en')

FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
DATA_FILE = "last_video_id.txt"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True 
client = discord.Client(intents=intents)

logger = logging.getLogger('schluggibot')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename='schluggibot.log', encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def load_translations(lang):
    path = f"locales/{lang}.json"
    if not os.path.exists(path):
        path = "locales/en.json" 
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

texts = load_translations(LANGUAGE)

def get_video_id():
    if not os.path.exists(DATA_FILE):
        return None
    
    with open(DATA_FILE, "r") as f:
        return f.read().strip()

def set_video_id(video_id):
    with open(DATA_FILE, "w") as f:
        f.write(video_id)

@client.event
async def on_ready():
    logger.info(f'Log in as: {client.user}')

    current_saved = get_video_id()
    if current_saved:
        logger.info(f"Last known Video-ID: {current_saved}")
    else:
        logger.info("No Video-ID saved.")

    check_for_videos.start()

@client.event
async def on_member_join(member):
    if AUTO_ROLE_ID is None:
        logger.warning("AUTO_ROLE_ID is not configured.")
        return

    role = member.guild.get_role(AUTO_ROLE_ID)
    if role:
        try:
            await member.add_roles(role)
            logger.info(f"Role '{role.name}' given to {member.name}.")
        except discord.Forbidden:
            logger.error("Error: Bot doesn't have the right to assign roles to users.")
        except Exception as e:
            logger.error(f"Error assigning role: {e}")
    else:
        logger.error(f"Role with ID {AUTO_ROLE_ID} not found.")

@tasks.loop(minutes=10)
async def check_for_videos():
    try:
        feed = feedparser.parse(FEED_URL)
        
        if not feed.entries:
            logger.warning("Feed retrieved, but no entries found.")
            return

        latest_video = feed.entries[0]
        current_video_id = latest_video.yt_videoid
        video_link = latest_video.link
        video_title = latest_video.title

        last_known_id = get_video_id()
        
        if last_known_id is None:
            set_video_id(current_video_id)
            logger.info(f"Current video ‘{video_title}’ has been saved as the starting point.")
            return

        if current_video_id != last_known_id:
            set_video_id(current_video_id)
            
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            if channel:
                message = texts['new_video_msg'].format(title=video_title, link=video_link)
                
                try:
                    sent_message = await channel.send(message)
                    logger.info(f"Notification sent: {video_title}")
                    
                    await sent_message.publish()
                    logger.info("Message successfully published.")
                    
                except discord.HTTPException as e:
                    logger.warning(f"Message sent, but publish failed (no announcement channel?): {e}")
                except Exception as e:
                    logger.error(f"Error while sending/publishing: {e}")
            else:
                logger.error(f"Could not send message: Channel {DISCORD_CHANNEL_ID} not found.")
            
    except Exception as e:
        logger.error(f"Error in loop: {e}")

client.run(DISCORD_TOKEN)