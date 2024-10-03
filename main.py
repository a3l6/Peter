import os
from typing import Union
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json
import time

open("hours.json", "r+")
assert os.path.isfile("hours.json")

with open("hours.json", "r") as f:
    data = json.load(f)


def write_data(d):
    with open("hours.json", "w") as f:
        json.dump(d, f)

"""
General Structure of Data

{
    username: {
        total_hours: x,
        time_stamp: { 
            hours: y,
            purpose: z
        }
    }
}

"""



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)

@bot.tree.command(name="volunteer", description="Log volunteer hours")
async def slash_command(interaction: discord.Interaction, hours: float, purpose: str):
    if hours < 0:
        await interaction.response.send_message("Hours cannot be negative!")
        return
    user = str(interaction.user)

    if user in data:
        session = {
            "hours": hours,
            "purpose": purpose
        }
        timestamp = str(time.time_ns())
        print(type(timestamp))
        data[user][timestamp] = session
        data[user]["total_hours"] += hours
        print(data)
        write_data(data)
    else:
        session = {
            "hours": hours,
            "purpose": purpose
        }
        timestamp = str(time.time_ns())
        data[user] = {
            "total_hours": hours,
            timestamp: session
        }
        print(data)
        write_data(data)
    await interaction.response.send_message(f"Logged {hours} hours for {user}!")


@bot.tree.command(name="hours", description="Get volunteer hours given a username")
async def get_hours(interaction: discord.Interaction, username: str):
    if username not in data:
        await interaction.response.send_message("User not found!")
        return
    hours = data[username]["total_hours"]
    await interaction.response.send_message(f"{username} has logged {hours} hours")


@bot.event
async def on_ready():
    print("Syncing")
    await bot.tree.sync()
    print("Synced")

bot.run(TOKEN)