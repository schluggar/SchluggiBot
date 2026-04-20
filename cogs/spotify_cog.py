import discord
from discord.ext import tasks, commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import logging
import json

logger = logging.getLogger('schluggibot')

class SpotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv('DISCORD_CHANNEL_ID'))
        self.spotify_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.spotify_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.artist_id = os.getenv('SPOTIFY_ARTIST_ID')
        self.data_file = "resources/release_id.json"
        self.language = os.getenv('LANGUAGE', 'en')
        self.texts = self.load_translations(self.language)
        
        if self.spotify_id and self.spotify_secret:
            auth_manager = SpotifyClientCredentials(client_id=self.spotify_id, client_secret=self.spotify_secret)
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            self.check_for_releases.start()
        else:
            logger.warning("Spotify credentials not set. SpotifyCog will not start.")

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
                return data.get("last_release_id")
        except (json.JSONDecodeError, KeyError):
            return None

    def set_last_id(self, release_id):
        dir_name = os.path.dirname(self.data_file)
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logger.info(f"Created directory: {dir_name}")

        data = {}
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding='utf-8') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        data["last_release_id"] = release_id
        
        with open(self.data_file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @tasks.loop(minutes=30)
    async def check_for_releases(self):
        try:
            if not self.artist_id:
                logger.warning("SPOTIFY_ARTIST_ID not set.")
                return

            results = self.sp.artist_albums(self.artist_id, album_type='album,single', limit=1)
            if not results['items']: return

            latest_release = results['items'][0]
            current_id = latest_release['id']
            
            last_known = self.get_last_id()
            if last_known is None:
                self.set_last_id(current_id)
                logger.info(f"Current release ‘{latest_release['name']}’ has been saved as the starting point.")
                return

            if current_id != last_known:
                await self.bot.wait_until_ready()

                self.set_last_id(current_id)
                channel = self.bot.get_channel(self.channel_id)
                if channel:
                    artist_name = latest_release['artists'][0]['name']
                    release_title = latest_release['name']
                    release_link = latest_release['external_urls']['spotify']
                    
                    message = self.texts['new_release_msg'].format(artist=artist_name, title=release_title, link=release_link)
                    try:
                        sent_message = await channel.send(message)
                        logger.info(f"Spotify notification sent: {artist_name} - {release_title}")
                        if channel.type == discord.ChannelType.news:
                            try:
                                await sent_message.publish()
                                logger.info("Spotify message successfully published.")
                            except discord.Forbidden:
                                logger.warning("Could not publish Spotify message: Missing 'Manage Messages' permission.")  
                    except Exception as e:
                        logger.error(f"Error while sending Spotify release: {e}")
                else:
                    logger.error(f"Could not send Spotify message: Channel {self.channel_id} not found.")
        except Exception as e:
            logger.error(f"Error in Spotify loop: {e}")

async def setup(bot):
    await bot.add_cog(SpotifyCog(bot))
