from discord.ext import tasks
from dotenv import load_dotenv
import discord
import feedparser
import os
import logging

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
DATA_FILE = "last_video_id.txt"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

logger = logging.getLogger('schluggibot')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename='schluggibot.log', encoding='utf-8', mode='a')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

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
    logger.info(f'Eingeloggt als {client.user}')

    current_saved = get_video_id()
    if current_saved:
        logger.info(f"Letztes bekannte Video-ID: {current_saved}")
    else:
        logger.info("Noch keine Video-ID gespeichert.")

    check_for_videos.start()

@tasks.loop(minutes=10)
async def check_for_videos():
    try:
        feed = feedparser.parse(FEED_URL)
        
        if not feed.entries:
            logger.warning("Feed abgerufen, aber keine Einträge gefunden.")
            return

        latest_video = feed.entries[0]
        current_video_id = latest_video.yt_videoid
        video_link = latest_video.link
        video_title = latest_video.title

        last_known_id = get_video_id()
        
        if last_known_id is None:
            set_video_id(current_video_id)
            logger.info(f"Aktuelles Video '{video_title}' wurde als Startpunkt gespeichert.")
            return

        if current_video_id != last_known_id:
            set_video_id(current_video_id)
            
            channel = client.get_channel(DISCORD_CHANNEL_ID)
            if channel:
                message = f"🚨 **Neues Video online!** 🚨\n\n**{video_title}**\nSchau es dir hier an: {video_link}"
                
                try:
                    sent_message = await channel.send(message)
                    logger.info(f"Benachrichtigung gesendet: {video_title}")
                    
                    await sent_message.publish()
                    logger.info("Nachricht erfolgreich veröffentlicht.")
                    
                except discord.HTTPException as e:
                    logger.warning(f"Nachricht gesendet, aber Publish fehlgeschlagen (Kein Announcement Channel?): {e}")
                except Exception as e:
                    logger.error(f"Fehler beim Senden/Publishen: {e}")
            else:
                logger.error(f"Konnte Nachricht nicht senden: Kanal {DISCORD_CHANNEL_ID} nicht gefunden.")
            
    except Exception as e:
        logger.error(f"Fehler im Loop: {e}")

client.run(DISCORD_TOKEN)