# SchluggiBot 📺

SchluggiBot is a modular Python-based Discord bot designed to handle community tasks: automatically announcing new YouTube uploads and greeting new members with an automatic role.

## Features 🚀

* **YouTube Monitoring:** Periodically checks a YouTube channel for new content and posts notifications to a designated Discord channel.
* **Auto-Role:** Automatically assigns a specific role to new members the moment they join the server.
* **Modular Architecture:** Built with Discord.py "Cogs," allowing features to be separated into clean, manageable modules.
* **Localization Support:** Supports multiple languages via JSON files located in the `locales/` folder.
* **Persistent Storage:** Uses `resources/video_id.json` to track the most recent video and prevent duplicate notifications.

## Prerequisites 🛠️

To run this bot, you will need:

* **Python 3.8** or higher.
* A **Discord Bot Token** with the **Server Members Intent** enabled in the [Discord Developer Portal](https://discord.com/developers/applications).
* A YouTube Channel ID and the corresponding Discord Channel/Role IDs.

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
    Rename .env_example to .env and fill in your credentials:
    ```env
    DISCORD_TOKEN=your_discord_bot_token
    YOUTUBE_CHANNEL_ID=the_youtube_channel_id
    DISCORD_CHANNEL_ID=the_target_discord_channel_id
    WELCOME_ROLE_ID=the_role_id_to_assign_on_join
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
    - `welcome_cog.py`: Logic for automatic role assignment on member join.
- `locales/`: JSON files for multi-language support.
- `resources/`: Stores `video_id.json` for state persistence (automatically created).
- `.env_example`: Sensitive configuration (Tokens and IDs). Do not share this file!

## Contributing 🤝
Contributions, issues, and feature requests are welcome! Feel free to:
- Add a new language file to locales/.
- Propose new features by adding a new Cog to the cogs/ directory.
- Open an issue for any bugs you encounter.
