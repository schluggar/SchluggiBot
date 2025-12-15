from discord.ext import tasks
from dotenv import load_dotenv

import discord
import feedparser
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
YOUTUBE_CHANNEL_ID = os.getenv('YOUTUBE_CHANNEL_ID')
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID'))

FEED_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={YOUTUBE_CHANNEL_ID}"
DATA_FILE = "last_video_id.txt"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

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
    print(f'Eingeloggt als {client.user}')

    current_saved = get_video_id()
    if current_saved:
        print(f"Letztes bekanntes Video ID: {current_saved}")
    else:
        print("Noch kein Video gespeichert.")

    check_for_videos.start()

@tasks.loop(minutes=10)
async def check_for_videos():
    print('Ich komme hier an')

    feed = feedparser.parse(FEED_URL)
    
    if not feed.entries:
        return

    latest_video = feed.entries[0]
    current_video_id = latest_video.yt_videoid
    video_link = latest_video.link
    video_title = latest_video.title

    last_known_id = get_video_id()
    
    if last_known_id is None:
        set_video_id(current_video_id)
        print(f"Erster Lauf: Aktuelles Video '{video_title}' wurde als Startpunkt gespeichert.")
        return

    if current_video_id != last_known_id:
        set_video_id(current_video_id)
        
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            message = f"🚨 **Neues Video online!** 🚨\n\n**{video_title}**\nSchau es dir hier an: {video_link}"
            await channel.send(message)
            print(f"Benachrichtigung gesendet: {video_title}")
    else:
        print(f"Kein neues Video gefunden. Letztes war: {video_title}")

client.run(TOKEN)