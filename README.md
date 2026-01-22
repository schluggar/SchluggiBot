# SchluggiBot 📺

SchluggiBot is a Python-based Discord bot designed to automatically announce new uploads from a specific YouTube channel directly into a your Discord server.

## Features 🚀

* **YouTube Monitoring:** Periodically checks a YouTube channel for new content.
* **Instant Notifications:** Posts a formatted message to a Discord channel as soon as a new video is detected.
* **Localization Support:** Supports multiple languages via locale files (located in the `locales` folder).
* **State Persistence:** Tracks the most recent video in `last_video_id.txt` to prevent duplicate notifications after a restart.

## Prerequisites 🛠️

To run this bot, you will need:

* Python 3.8 or higher
* A Discord Bot with it's Token ([Discord Developer Portal](https://discord.com/developers/applications))
* The Channel ID of the YouTube channel you wish to monitor.

## Installation 📦

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/schluggar/SchluggiBot.git](https://github.com/schluggar/SchluggiBot.git)
    cd SchluggiBot
    ```

2.  **Install dependencies:**
    Ensure you have the necessary libraries installed:
    ```bash
    pip install discord.py feedparser python-dotenv 
    ```

3.  **Configuration:**
    Copy the `.env_example` file and rename it to `.env`. Fill in your credentials:
    ```env
    DISCORD_TOKEN=your_discord_bot_token
    YOUTUBE_CHANNEL_ID=the_youtube_channel_id
    DISCORD_CHANNEL_ID=the_target_discord_channel_id
    LANGUAGE=your_preferred_language
    ```

## Usage 🚀

Run the bot using Python:

```bash
python schluggibot.py
```

## Project Structure 📂
- `schluggibot.py`: The main application script.
- `locales/`: Contains translation files for multi-language support.
- `last_video_id.txt`: A local database file storing the ID of the last announced video.
- `.env_example`: Template for environment variables.

## Contributing 🤝
Contributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to contribute. Feel free to add your language to the `locales/` folder, to make the Bot more accessable.
