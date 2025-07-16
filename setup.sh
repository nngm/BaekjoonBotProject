#!/bin/bash
#
# This script interactively sets up the .env file for the BaekjoonBot.
# It prompts the user for their Discord bot token and creates the .env file.

if [ -f .env ]; then
  echo ".env file already exists. Overwrite? (y/n)"
  read -r answer
  if [ "$answer" != "y" ]; then
    echo "Aborting. No changes were made."
    exit 0
  fi
fi

echo "Please enter your Discord bot token:"
read -r DISCORD_TOKEN

if [ -z "$DISCORD_TOKEN" ]; then
  echo "No token provided. Aborting."
  exit 1
fi

echo "DISCORD_TOKEN=\"$DISCORD_TOKEN\"" > .env

echo
echo ".env file created successfully."
echo "You can now start the bot using 'python main.py'"
