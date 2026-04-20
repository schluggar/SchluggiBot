# SchluggiBot 📺

SchluggiBot is a modular Python-based Discord bot designed to handle community tasks: automatically announcing new YouTube uploads, notifying about new Spotify releases, and greeting new members with an automatic role.

## Features 🚀

* **YouTube Monitoring:** Periodically checks a YouTube channel for new content and posts notifications to a designated Discord channel.
* **Spotify Monitoring:** Tracks a specific Spotify artist for new releases (albums/singles) and posts notifications.
* **Auto-Role:** Automatically assigns a specific role to new members the moment they join the server.
* **Automatic Publishing:** If notifications are sent to a Discord News (Announcement) channel, the bot will automatically publish the message.
* **Modular Architecture:** Built with Discord.py "Cogs," allowing features to be separated into clean, manageable modules.
* **Localization Support:** Supports multiple languages via JSON files located in the `locales/` folder.
* **Persistent Storage:** Uses `resources/` to track the most recent IDs and prevent duplicate notifications.

## Prerequisites 🛠️

To run this bot, you will need:

* **Python 3.8** or higher.
* A **Discord Bot Token** with the **Server Members Intent** and **Message Content Intent** enabled in the [Discord Developer Portal](https://discord.com/developers/applications).
* A YouTube Channel ID and/or Spotify Client credentials + Artist ID.
* Target Discord Channel and Role IDs.

## Installation 📦

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/schluggar/SchluggiBot.git
    cd SchluggiBot
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment. Install the necessary libraries using:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration:**
    Rename `.env_example` to `.env` and fill in your credentials:
    ```env
    DISCORD_TOKEN=your_discord_bot_token
    DISCORD_CHANNEL_ID=the_target_discord_channel_id
    WELCOME_ROLE_ID=the_role_id_to_assign_on_join

    YOUTUBE_CHANNEL_ID=the_youtube_channel_id

    SPOTIFY_CLIENT_ID=your_spotify_client_id
    SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
    SPOTIFY_ARTIST_ID=the_spotify_artist_id

    LANGUAGE=de
    ```

## Usage 🚀

Run the bot using Python:

```bash
python schluggibot.py
```

## Project Structure 📂
- `schluggibot.py`: The main entry point that initializes the bot and loads all modules (Cogs).
- `cogs/`:
    - `youtube_cog.py`: Logic for YouTube feed monitoring and notifications.
    - `spotify_cog.py`: Logic for Spotify release monitoring.
    - `welcome_role_cog.py`: Logic for automatic role assignment on member join.
- `locales/`: JSON files for multi-language support (e.g., `de.json`, `en.json`).
- `resources/`: Stores state persistence files (automatically created):
    - `video_id.json`: Tracks the latest YouTube video.
    - `release_id.json`: Tracks the latest Spotify release.
- `.env_example`: Sensitive configuration template.

## Contributing 🤝
Contributions, issues, and feature requests are welcome! Feel free to:
- Add a new language file to `locales/`.
- Propose new features by adding a new Cog to the `cogs/` directory.
- Open an issue for any bugs you encounter.
