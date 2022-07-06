import discord
from discord.ext import commands, timers
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
intents = discord.Intents.all()
client = commands.Bot(intents=intents)
client.time_manager = timers.TimerManager(client)


@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")


cog_files = [
    f"cogs.{filename[:-3]}"
    for filename in os.listdir("./cogs/")
    if filename.endswith(".py")
]

if __name__ == "__main__":
    for cog in cog_files:
        try:
            client.load_extension(cog)
        except Exception as err:
            print(err)

client.run(TOKEN)
