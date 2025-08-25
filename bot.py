import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# ------------------------
# Discord Bot Setup
# ------------------------
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("❌ Error: DISCORD_TOKEN environment variable not found!")
    exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------------
# Trigger phrases and GIFs
# ------------------------
TRIGGER_SENTENCE_DANCE = "oguri cap, do that dance i like"
DANCE_GIF_URL = "https://tenor.com/view/oguri-cap-oguri-cap-dancing-umamusume-chibi-gif-10169214246627292150"

TRIGGER_SENTENCE_RUN = "oguri cap, run away"
RUN_GIF_URL = "https://tenor.com/view/oguri-cap-oguri-cap-umamusume-uma-gif-5585391520653559663"

TRIGGER_SENTENCE_AGREE = "oguri cap, do you agree?"
AGREE_GIF_URL = "https://tenor.com/view/oguri-cap-oguri-cap-umamusume-uma-gif-15407094230313995300"

# ------------------------
# Events
# ------------------------
@bot.event
async def on_ready():
    print(f"✅ {bot.user} has connected to Discord!")
    print("🤖 Bot is ready and listening for:")
    print(f"   • '{TRIGGER_SENTENCE_DANCE}' -> Dance GIF")
    print(f"   • '{TRIGGER_SENTENCE_RUN}' -> Run GIF")
    print(f"   • '{TRIGGER_SENTENCE_AGREE}' -> Agree GIF")
    print(f"📊 Connected to {len(bot.guilds)} server(s)")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_lower = message.content.lower()

    if message_lower == TRIGGER_SENTENCE_DANCE.lower():
        await message.channel.send(DANCE_GIF_URL)
    elif message_lower == TRIGGER_SENTENCE_RUN.lower():
        await message.channel.send(RUN_GIF_URL)
    elif message_lower == TRIGGER_SENTENCE_AGREE.lower():
        await message.channel.send(AGREE_GIF_URL)

    await bot.process_commands(message)

# ------------------------
# Keep-alive web server for Render
# ------------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_web_server():
    port = int(os.environ.get("PORT", 8080))  # Render sets PORT automatically
    app.run(host='0.0.0.0', port=port)

Thread(target=run_web_server).start()

# ------------------------
# Run the bot
# ------------------------
bot.run(TOKEN)
