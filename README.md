# BaekjoonBot

[![Discord.py](https://img.shields.io/badge/discord.py-v1.7.3-blue.svg)](https://github.com/Rapptz/discord.py)

BaekjoonBot is a Discord bot designed to help competitive programming enthusiasts by providing quick access to problem information from [Baekjoon Online Judge](https://www.acmicpc.net/) and user profiles from [solved.ac](https://solved.ac/).

This project has been refactored to follow modern Python best practices, including dependency management with Conda, centralized data models, and robust error handling.

## Features

- **Problem Lookup:** Fetch and display details for any Baekjoon problem by its number.
- **User Profile:** Display a user's solved.ac profile and tier information.
- **Random Problem:** Get a random problem suggestion within a specified tier range.
- **Problem Search:** Search for problems by title.
- **Server-Specific Prefixes:** Customize the bot's command prefix for each Discord server.
- **And more:** Includes various utility and convenience commands.

## Getting Started

Follow these instructions to get a local copy of the bot up and running.

### Prerequisites

- **Conda:** You must have Conda installed. You can get it by installing [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution).

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone -b feat/modernize-project https://github.com/nngm/BaekjoonBotProject.git
    cd BaekjoonBotProject
    ```

2.  **Create and activate the Conda environment:**
    This command creates a new environment named `baekjoonbot` and installs all necessary dependencies from the `environment.yml` file.
    ```bash
    conda env create -f environment.yml
    conda activate baekjoonbot
    ```

3.  **Configure the Bot Token:**
    Run the interactive setup script. This will prompt you for your Discord bot token and create the necessary `.env` file.
    ```bash
    ./setup.sh
    ```

### Running the Bot

Once the environment is activated and the token is configured, you can start the bot with:

```bash
python main.py
```

## Usage

Here are some of the main commands. The default prefix is `/`.

-   **Get problem #1000:**
    `/1000`
-   **Get user profile for `solvedac`:**
    `/user solvedac`
-   **Get a random Gold-tier problem:**
    `/random gold`
-   **Search for a problem titled "A+B":**
    `/search A+B`
-   **Change the server's prefix to `!`:**
    `/prefix !`

For a full list of commands, you can mention the bot or use the `/help` command.
