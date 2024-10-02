import os
from typing import Union
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

tree = bot.tree

"""

@tree.command(name="echo", description="Echoes a message.")
async def echo(interaction: discord.Interaction, message: str) -> None:
    await interaction.response.send_message(message)

"""


@tree.command(name="volunteer", description="Log volunter hours")
async def volunteer(interaction: discord.Interaction, hours: float, reason: str, proof: Union[str, None]):
    await interaction.response.send_message(f"Logged {hours} hours")


@bot.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=int(os.getenv("DISCORD_GUILD_ID"))))

bot.run(TOKEN)