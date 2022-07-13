import discord
import datetime
import asyncio
import keyboard
from emotionDetection import detect
import discord_emoji as dj

TOKEN = "---"

client = discord.Client()


@client.event
async def on_message(message):
    if message.content.startswith(".detect"):
        emotion = detect(str(message.content)[7:])
        await message.channel.send(emotion)
        #
        # if len(str(dj.to_discord(emotion, put_colons=True))) <= 2:
        #     await message.channel.send(emotion)
        # else:
        #     await message.channel.send(dj.to_discord(emotion, put_colons=True))


@client.event
async def on_ready():
    print("RUNNING")


client.run(TOKEN)