import os
import instaloader
import yt_dlp
from pyrogram import Client, filters

# Bot Credentials
API_ID = 28795512
API_HASH = "c17e4eb6d994c9892b8a8b6bfea4042a"
BOT_TOKEN = "7589052839:AAGPMVeZpb63GEG_xXzQEua1q9ewfNzTg50"

# Initialize the bot
bot = Client("insta_reel_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Function to download Instagram Reel
def download_instagram_reel(url):
    loader = instaloader.Instaloader()
    try:
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        filename = f"{post.shortcode}.mp4"

        # yt-dlp से वीडियो डाउनलोड करें
        ydl_opts = {
            'outtmpl': filename,
            'quiet': True,
            'noplaylist': True,
            'merge_output_format': 'mp4'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([post.video_url])

        return filename if os.path.exists(filename) else None
    except Exception as e:
        return None

# Command Handler to Download Instagram Reels
@bot.on_message(filters.command("reel") & filters.private)
def reel_handler(client, message):
    if len(message.command) < 2:
        message.reply_text("Usage: /reel <Instagram Reel URL>")
        return
    
    url = message.command[1]
    message.reply_text("Downloading Reel... Please wait!")
    
    filename = download_instagram_reel(url)
    
    if filename and os.path.exists(filename):
        message.reply_video(video=filename, caption="Here is your downloaded Reel!")
        os.remove(filename)
    else:
        message.reply_text("Failed to download Reel. Please check the URL and try again.")

# Start the bot
print("Bot is running...")
bot.run()
