#!/bin/bash
#
# This script initializes the .env file for the BaekjoonBot.
# It copies the .env.example file to .env if it doesn't already exist.

if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env file created successfully."
  echo "Please open the .env file and add your Discord bot token."
else
  echo ".env file already exists. No changes were made."
fi
