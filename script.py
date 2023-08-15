import discord
from discord.ext import commands
import asyncio

TOKEN = 'YOUR_BOT_TOKEN'
GUILD_ID = 123456789012345678
CHANNEL_ID = 123456789012345678
USER_ID = 123456789012345678
DELETE_INTERVAL_SECONDS = 3600

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    bot.loop.create_task(delete_messages())  # Start the periodic delete task

async def delete_messages():
    await bot.wait_until_ready()

    while not bot.is_closed():
        await delete_user_messages()

        await asyncio.sleep(DELETE_INTERVAL_SECONDS)

async def delete_user_messages():
    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    if channel:
        try:
            user = await bot.fetch_user(USER_ID)
        except discord.NotFound:
            print("Invalid user ID.")
            return

        async for message in channel.history(limit=None):
            if message.author == user:
                await message.delete()
                print(f"Deleted message from {user.name} in {channel.name}: {message.content}")

await bot.start(TOKEN)
