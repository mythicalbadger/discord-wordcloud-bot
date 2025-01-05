import os
import discord

from dotenv import load_dotenv
from discord.ext import commands

from helpers import generate_wordcloud, is_valid_message

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.all()

bot = commands.Bot(command_prefix="?", intents=intents)

async def get_all_messages_from_user(ctx, user, channels = None) -> tuple[list, int]:
    messages = []
    message_cnt = 0

    if not channels:
        channels = bot.get_all_channels()

    # Get all channels
    for channel in channels:
        if not isinstance(channel, discord.TextChannel):
            continue

        print(f"Checking channel {channel.name}")

        async for message in channel.history(limit=None):
            message_cnt += 1

            if message_cnt % 1000 == 0:
                await ctx.send(f"Checked {message_cnt} messages", delete_after=5, silent=True)

            if message.author == user and is_valid_message(message):
                messages.append(message.content)

    return messages, message_cnt

@bot.command(name="wordcloud")
async def wordcloud(ctx):
    user = ctx.message.mentions[0]
    channels = ctx.message.channel_mentions

    messages, cnt = await get_all_messages_from_user(ctx, user, channels)
    raw_text = " ".join(messages)

    await ctx.send(f"*{user.name}*")
    await ctx.send(f"Processed {cnt} messages. {len(messages)} from {user.name} in {len(channels)} channels [{', '.join([channel.name for channel in channels])}]")

    # Create wordcloud
    FILENAME = "wordcloud.png"
    wordcloud = generate_wordcloud(raw_text)
    wordcloud.to_file(FILENAME)

    with open(FILENAME, "rb") as image:
        await ctx.send(file=discord.File(image))


bot.run(TOKEN)