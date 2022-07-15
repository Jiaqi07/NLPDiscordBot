import time

import discord
import datetime
import asyncio
import keyboard
import openai as ai
from emotionDetection import detect

TOKEN = "OTk2NTU3ODAwMjk5ODIzMTU0.GohnVo.iltgmiTLhz-I8SNza1OkvDLWrNhELc7fXguWv0"
client = discord.Client()
ai.api_key = "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"
completion = ai.Completion()


@client.event
async def on_message(message):
    if message.content.startswith(".help"):
        await message.channel.send(".detect, .train, .chat")

    if message.content.startswith(".chat"):
        with open('chat-log.txt') as f:
            chat_log = f.read()

        def check(mesg):
            return message.author == mesg.author and message.channel == mesg.channel

        await message.channel.send("Enter questions to talk to me! :) (Type + to quit!)")
        while True:
            time.sleep(2)

            await message.channel.send("----------------------")
            await message.channel.send("Question: ")

            try:
                question = await client.wait_for('message', check=check, timeout=30)
            except:
                await message.channel.send("30 seconds is up! Session Terminated!")
                break

            if question.content == "+":
                await message.channel.send("Session Terminated!")
                break

            await message.channel.send(chat(question.content, chat_log))

    if message.content.startswith(".detect"):
        emotion = detect(str(message.content)[7:])
        await message.channel.send(emotion)
        #
        # if len(str(dj.to_discord(emotion, put_colons=True))) <= 2:
        #     await message.channel.send(emotion)
        # else:
        #     await message.channel.send(dj.to_discord(emotion, put_colons=True))

    if message.content.startswith(".train"):
        def modify_message(s, question, answer) -> str:
            s += f"Human: {question}\nAI: {answer}\n"
            return s

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        with open('chat-log.txt') as f:
            chat_log = f.read()

        await message.channel.send("Would you like to train the bot? (T/F)")

        try:
            train = await client.wait_for('message', check=check, timeout=30)
        except:
            await message.channel.send("30 seconds is up! Session Terminated!")
            train = "F"

        if train.content == "T":
            await train.channel.send("(Type + To Finish)")

            while True:
                await message.channel.send("Question: ")
                try:
                    question = await client.wait_for('message', check=check, timeout=30)
                except:
                    await message.channel.send("30 seconds is up! Session Terminated!")
                    break

                if question.content == "+":
                    await message.channel.send("Training Stopped!!!")
                    break
                await message.channel.send("Answer: ")
                try:
                    answer = await client.wait_for('message', check=check, timeout=30)
                except:
                    await message.channel.send("30 seconds is up! Session Terminated!")
                    break

                chat_log = modify_message(chat_log, question.content, answer.content)

                with open('chat-log.txt', 'w') as f:
                    f.write(chat_log)
        else:
            await train.channel.send("Seeya next time!")


@client.event
async def on_ready():
    print("RUNNING")


def chat(msg, s) -> str:
    prompt = f"{s}Human: {msg}\nAI:"
    response = completion.create(prompt=prompt, engine="davinci", temperature=0.85, top_p=1,
                                 frequency_penalty=0,
                                 presence_penalty=0.7, best_of=2, max_tokens=50, stop="\nHuman: ")
    return response.choices[0].text


client.run(TOKEN)
