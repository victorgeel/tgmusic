import os
from pyrogram import Client, filters
from yt_dlp import YoutubeDL
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
vc = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 **Telegram Group Voice Chat Music Bot**\nUse /play <song> to start playing.")

@app.on_message(filters.command("play"))
async def play(client, message):
    chat_id = message.chat.id
    args = message.text.split(" ", 1)
    
    if len(args) < 2:
        await message.reply("သီချင်းခေါင်းစဉ် (သို့) YouTube Link ထည့်ပါ။")
        return

    query = args[1]
    
    if "youtube.com" in query or "youtu.be" in query:
        video_url = query
    else:
        video_url = await search_youtube(query)

    if not video_url:
        return

    audio_file = await download_audio(video_url)
    await vc.join_group_call(chat_id, AudioPiped(audio_file, stream_type=StreamType().local_stream))
    await message.reply(f"🎵 **Now Playing:** {video_url}")

async def search_youtube(query):
    opts = {"format": "bestaudio", "noplaylist": True, "quiet": True}
    with YoutubeDL(opts) as ydl:
        search_results = ydl.extract_info(f"ytsearch:{query}", download=False)
        return search_results["entries"][0]["url"] if search_results["entries"] else None

async def download_audio(video_url):
    opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        return f"downloads/{info['title']}.mp3"

app.run()
