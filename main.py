# import os
# import asyncio
# import nest_asyncio
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import (
#     ApplicationBuilder,
#     CommandHandler,
#     CallbackQueryHandler,
#     ContextTypes,
# )
# from yt_dlp import YoutubeDL

# # ========== Configuration ==========
# BOT_TOKEN = "8113456977:AAEW3iHgZmREkgeBZCfmp86YOG-OV97viCE"
# BOT_NAME = "⚡️ Shivaay Music Downloader Pro ⚡️"
# COPYRIGHT = "© 2025 @Shivaay20005 - All Rights Reserved"

# LOADING_ANIMATIONS = [
#     "⬇️ Downloading: ⏳ [□□□□□□□□□□] 0%",
#     "⬇️ Downloading: ⏳ [■□□□□□□□□□] 10%",
#     "⬇️ Downloading: ⏳ [■■□□□□□□□□] 20%",
#     "⬇️ Downloading: ⏳ [■■■□□□□□□□] 30%",
#     "⬇️ Downloading: ⏳ [■■■■□□□□□□] 40%",
#     "⬇️ Downloading: ⏳ [■■■■■□□□□□] 50%",
#     "⬇️ Downloading: ⏳ [■■■■■■□□□□] 60%",
#     "⬇️ Downloading: ⏳ [■■■■■■■□□□] 70%",
#     "⬇️ Downloading: ⏳ [■■■■■■■■□□] 80%",
#     "⬇️ Downloading: ⏳ [■■■■■■■■■□] 90%",
#     "⬇️ Downloaded: ✅ [■■■■■■■■■■] 100%",
# ]

# # YDL options: audio only
# YDL_OPTS_BASE = {
#     'format': 'bestaudio/best',
#     'outtmpl': 'downloads/%(id)s.%(ext)s',
#     'quiet': True,
#     'no_warnings': True,
#     'nocheckcertificate': True,
#     'ignoreerrors': True,
#     'postprocessors': [{
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'mp3',
#         'preferredquality': '192',
#     }],
# }

# AUDIO_QUALITY_OPTIONS = {
#     'High': '320',
#     'Medium': '192',
#     'Low': '128',
# }

# # Ensure downloads folder exists
# os.makedirs('downloads', exist_ok=True)

# # ========== Bot Handlers ==========

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await update.message.reply_text(
#         f"Hello! I am *{BOT_NAME}*\n"
#         "Send me `/song <song name>` to search and download music.\n"
#         f"{COPYRIGHT}",
#         parse_mode="Markdown"
#     )

# async def search_song(song_name: str):
#     """Search YouTube videos using yt-dlp."""
#     ydl_opts = {
#         'quiet': True,
#         'skip_download': True,
#         'default_search': 'ytsearch5',
#     }
#     with YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(song_name, download=False)
#         return info['entries'] if 'entries' in info else []

# async def song_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     if len(context.args) == 0:
#         await update.message.reply_text("Please provide a song name after /song command.")
#         return

#     query = " ".join(context.args)
#     message = await update.message.reply_text(f"🔍 Searching for \"{query}\"...\n{COPYRIGHT}")

#     try:
#         results = await search_song(query)
#     except Exception as e:
#         await message.edit_text(f"❌ Error during search: {e}")
#         return

#     if not results:
#         await message.edit_text(f"No results found for \"{query}\".\nTry a different query.\n{COPYRIGHT}")
#         return

#     buttons = []
#     for video in results[:5]:
#         title = video['title'][:40]
#         video_id = video['id']
#         buttons.append([InlineKeyboardButton(title, callback_data=f"select_{video_id}")])

#     await message.edit_text(
#         "🎶 Select the song you want to download:",
#         reply_markup=InlineKeyboardMarkup(buttons)
#     )

# async def select_song_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     video_id = query.data.split('_')[1]
#     video_url = f"https://www.youtube.com/watch?v={video_id}"

#     buttons = [
#         [InlineKeyboardButton("High (320 kbps)", callback_data=f"download_{video_id}_High")],
#         [InlineKeyboardButton("Medium (192 kbps)", callback_data=f"download_{video_id}_Medium")],
#         [InlineKeyboardButton("Low (128 kbps)", callback_data=f"download_{video_id}_Low")],
#         [InlineKeyboardButton("Cancel", callback_data="cancel")],
#     ]
#     await query.edit_message_text(
#         "Select audio quality:",
#         reply_markup=InlineKeyboardMarkup(buttons)
#     )
#     await query.answer()

# async def download_song_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     data = query.data

#     await query.answer()  # Important to prevent timeout

#     if data == "cancel":
#         await query.edit_message_text("❌ Download cancelled.\n" + COPYRIGHT)
#         return

#     _, video_id, quality = data.split('_')
#     video_url = f"https://www.youtube.com/watch?v={video_id}"

#     ydl_opts = YDL_OPTS_BASE.copy()
#     ydl_opts['postprocessors'][0]['preferredquality'] = AUDIO_QUALITY_OPTIONS.get(quality, '192')
    
#     progress_message = await query.edit_message_text("Starting download...\n" + COPYRIGHT)

#     try:
#         loop = asyncio.get_event_loop()

#         def run_download():
#             with YoutubeDL(ydl_opts) as ydl:
#                 info_dict = ydl.extract_info(video_url, download=True)
#                 return ydl.prepare_filename(info_dict)

#         filename = await loop.run_in_executor(None, run_download)

#         for frame in LOADING_ANIMATIONS:
#             await asyncio.sleep(1.2)
#             try:
#                 await progress_message.edit_text(f"{frame}\n{COPYRIGHT}")
#             except Exception:
#                 pass

#         if filename and os.path.exists(filename):
#             with open(filename, 'rb') as audio_file:
#                 await context.bot.send_audio(
#                     chat_id=query.message.chat_id,
#                     audio=audio_file,
#                     title=os.path.basename(filename),
#                     caption=f"🎵 Downloaded via {BOT_NAME}\n{COPYRIGHT}",
#                 )
#             os.remove(filename)
#             await progress_message.edit_text("✅ Download completed!\n" + COPYRIGHT)
#         else:
#             await progress_message.edit_text("❌ Failed to find the downloaded file.\n" + COPYRIGHT)
#     except Exception as e:
#         await progress_message.edit_text(f"❌ Error during download:\n{e}\n{COPYRIGHT}")

# async def main():
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("song", song_command))
#     app.add_handler(CallbackQueryHandler(select_song_callback, pattern=r"^select_"))
#     app.add_handler(CallbackQueryHandler(download_song_callback, pattern=r"^download_|cancel$"))

#     print(f"{BOT_NAME} is running...")
#     await app.run_polling()

# if __name__ == "__main__":
#     try:
#         asyncio.get_event_loop().run_until_complete(main())
#     except RuntimeError:
#         nest_asyncio.apply()
#         asyncio.get_event_loop().run_until_complete(main())
























# import os
# import asyncio
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler, CallbackQueryHandler
# import yt_dlp

# BOT_TOKEN = "7837774604:AAFjjYxocztQzuIM4vdLddY2_bKquVFa9kE"

# # Branding Constants
# BOT_NAME = "⚡️ Shivaay Music Downloader Pro ⚡️"
# COPYRIGHT = "© 2025 @Shivaay20005 - All Rights Reserved"
# LOADING_ANIMATIONS = [
#     "⬇️ Downloading: ⏳ [□□□□□□□□□□] 0%", "⬇️ Downloading: ⏳ [■□□□□□□□□□] 10%",
#     "⬇️ Downloading: ⏳ [■■□□□□□□□□] 20%", "⬇️ Downloading: ⏳ [■■■□□□□□□□] 30%",
#     "⬇️ Downloading: ⏳ [■■■■□□□□□□] 40%", "⬇️ Downloading: ⏳ [■■■■■□□□□□] 50%",
#     "⬇️ Downloading: ⏳ [■■■■■■□□□□] 60%", "⬇️ Downloading: ⏳ [■■■■■■■□□□] 70%",
#     "⬇️ Downloading: ⏳ [■■■■■■■■□□] 80%", "⬇️ Downloading: ⏳ [■■■■■■■■■□] 90%",
#     "⬇️ Downloaded: ✅ [■■■■■■■■■■] 100%"
# ]

# # Store user data temporarily
# user_data = {}

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     welcome_message = f"""
# {BOT_NAME}

# 🎵 Welcome to the ultimate music experience!
# Send me any song name and I'll fetch it for you in highest quality!

# ⚙️ Now with multiple quality options!

# {COPYRIGHT}
#     """

#     keyboard = [[
#         InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Shivaay20005")
#     ],
#                 [
#                     InlineKeyboardButton("📢 Updates Channel",
#                                          url="https://t.me/Shivaay20005")
#                 ]]
#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     help_text = f"""
# 🎧 <b>How to Use {BOT_NAME}</b>

# 1️⃣ <b>Send the name</b> of any song, artist, or video you want to download.
# 2️⃣ <b>Select a video</b> from the search results.
# 3️⃣ <b>Choose the desired quality</b> (MP3 128kbps, 192kbps, 320kbps or original).
# 4️⃣ <b>Wait while we process</b> and send you the audio file.

# 💡 Examples:
# • <code>Believer Imagine Dragons</code>
# • <code>Arijit Singh New Song 2024</code>

# 🛠 Available Commands:
# /start – Show welcome message
# /help – Show how to use the bot
# /cancel – Cancel the current operation

# {COPYRIGHT}
#     """
#     await update.message.reply_text(help_text, parse_mode="HTML")

# async def update_progress(message, context: ContextTypes.DEFAULT_TYPE):
#     for animation in LOADING_ANIMATIONS:
#         await message.edit_text(animation)
#         await asyncio.sleep(0.5)

# async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.message.text
#     chat_id = update.message.chat.id

#     # Search for videos
#     status_message = await update.message.reply_text(
#         f"🔍 Searching for: {query}\n\n{COPYRIGHT}")

#     try:
#         ydl_opts = {
#             'format': 'bestaudio/best',
#             'quiet': True,
#             'nocheckcertificate': True,
#             'extract_flat': True
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             info = ydl.extract_info(f"ytsearch5:{query}", download=False)
#             if not info or not info.get('entries'):
#                 await status_message.edit_text(
#                     f"❌ No results found for: {query}\n\n{COPYRIGHT}")
#                 return

#             videos = info['entries']
#             keyboard = []

#             # Store video info for callback
#             user_data[chat_id] = {'videos': videos}

#             # Create buttons for each video found
#             for idx, video in enumerate(videos[:5]):  # Show max 5 results
#                 title = video.get(
#                     'title', 'Unknown Title')[:50] + "..." if len(
#                         video.get('title', '')) > 50 else video.get(
#                             'title', 'Unknown Title')
#                 keyboard.append([
#                     InlineKeyboardButton(f"🎵 {idx+1}. {title}",
#                                          callback_data=f"select_{idx}")
#                 ])

#             keyboard.append(
#                 [InlineKeyboardButton("❌ Cancel", callback_data="cancel")])

#             reply_markup = InlineKeyboardMarkup(keyboard)
#             await status_message.edit_text(
#                 f"🔍 Found {len(videos)} results for: {query}\n\nPlease select a song:\n\n{COPYRIGHT}",
#                 reply_markup=reply_markup)

#     except Exception as e:
#         await status_message.edit_text(f"❌ Error: {str(e)}\n\n{COPYRIGHT}")

# async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     chat_id = query.message.chat.id
#     data = query.data

#     await query.answer()

#     if data == "cancel":
#         await query.message.delete()
#         if chat_id in user_data:
#             del user_data[chat_id]
#         return

#     if data.startswith("select_"):
#         video_idx = int(data.split("_")[1])

#         if chat_id not in user_data or video_idx >= len(
#                 user_data[chat_id]['videos']):
#             await query.message.edit_text(
#                 "❌ Invalid selection. Please try again.")
#             return

#         video = user_data[chat_id]['videos'][video_idx]
#         video_url = video.get('url') or f"https://youtu.be/{video.get('id')}"

#         # Show quality options
#         keyboard = [
#             [
#                 InlineKeyboardButton("🎧 MP3 (128kbps)",
#                                      callback_data=f"dl_{video_idx}_mp3_128")
#             ],
#             [
#                 InlineKeyboardButton("🎧 MP3 (192kbps)",
#                                      callback_data=f"dl_{video_idx}_mp3_192")
#             ],
#             [
#                 InlineKeyboardButton("🎧 MP3 (320kbps)",
#                                      callback_data=f"dl_{video_idx}_mp3_320")
#             ],
#             [
#                 InlineKeyboardButton("🎵 Original Quality",
#                                      callback_data=f"dl_{video_idx}_original")
#             ], [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
#         ]

#         reply_markup = InlineKeyboardMarkup(keyboard)

#         await query.message.edit_text(
#             f"🎵 Selected: {video.get('title', 'Unknown Title')}\n\nSelect quality:\n\n{COPYRIGHT}",
#             reply_markup=reply_markup)

#     elif data.startswith("dl_"):
#         parts = data.split("_")
#         video_idx = int(parts[1])
#         format_type = parts[2]
#         quality = parts[3] if len(parts) > 3 else None

#         if chat_id not in user_data or video_idx >= len(
#                 user_data[chat_id]['videos']):
#             await query.message.edit_text(
#                 "❌ Invalid selection. Please try again.")
#             return

#         video = user_data[chat_id]['videos'][video_idx]
#         video_url = video.get('url') or f"https://youtu.be/{video.get('id')}"

#         await query.message.edit_text(
#             f"⬇️ Preparing download...\n\n{COPYRIGHT}")

#         try:
#             output_path = f"{chat_id}_%(title)s.%(ext)s"

#             ydl_opts = {
#                 'outtmpl': output_path,
#                 'quiet': True,
#                 'nocheckcertificate': True
#             }

#             if format_type == "mp3":
#                 ydl_opts['postprocessors'] = [{
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'mp3',
#                     'preferredquality': quality
#                 }]
#                 ydl_opts['format'] = 'bestaudio/best'
#             else:
#                 ydl_opts['format'] = 'best'

#             await update_progress(query.message, context)

#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(video_url, download=True)
#                 filename = ydl.prepare_filename(info)
#                 ext = 'mp3' if format_type == 'mp3' else info['ext']
#                 final_file = filename.rsplit('.', 1)[0] + f'.{ext}'

#             caption = f"""
# 🎵 Title: {info.get('title', 'N/A')}
# ⏱ Duration: {info.get('duration_string', 'N/A')}
# 👁 Views: {info.get('view_count', 'N/A'):,}
# 💿 Quality: {'MP3 '+quality+'kbps' if format_type == 'mp3' else 'Original'}

# Downloaded by {BOT_NAME}
# {COPYRIGHT}
#             """

#             await context.bot.send_audio(chat_id=chat_id,
#                                          audio=open(final_file, 'rb'),
#                                          caption=caption,
#                                          title=info.get('title'),
#                                          performer=info.get(
#                                              'uploader', 'Unknown Artist'))

#             os.remove(final_file)
#             await query.message.delete()

#         except Exception as e:
#             await query.message.edit_text(
#                 f"❌ Download failed: {str(e)}\n\n{COPYRIGHT}")

#         if chat_id in user_data:
#             del user_data[chat_id]

# if __name__ == "__main__":
#     print(f"🤖 {BOT_NAME} is starting...")
#     app = ApplicationBuilder().token(BOT_TOKEN).build()

#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(CommandHandler("help", help_command))

#     app.add_handler(
#         MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
#     app.add_handler(CallbackQueryHandler(handle_callback))

#     print(f"✅ {BOT_NAME} is running!")
#     app.run_polling()

import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler, CallbackQueryHandler
import yt_dlp

BOT_TOKEN = "8113456977:AAEW3iHgZmREkgeBZCfmp86YOG-OV97viCE"

# Branding Constants
BOT_NAME = "⚡️ Shivaay Music Downloader Pro 🤟 ⚡️"
COPYRIGHT = "© 2025 @Shivaay20005 - All Rights Reserved"
LOADING_ANIMATIONS = [
    "⬇️ Downloading: ⏳ [□□□□□□□□□□] 0%", "⬇️ Downloading: ⏳ [■□□□□□□□□□] 10%",
    "⬇️ Downloading: ⏳ [■■□□□□□□□□] 20%", "⬇️ Downloading: ⏳ [■■■□□□□□□□] 30%",
    "⬇️ Downloading: ⏳ [■■■■□□□□□□] 40%", "⬇️ Downloading: ⏳ [■■■■■□□□□□] 50%",
    "⬇️ Downloading: ⏳ [■■■■■■□□□□] 60%", "⬇️ Downloading: ⏳ [■■■■■■■□□□] 70%",
    "⬇️ Downloading: ⏳ [■■■■■■■■□□] 80%", "⬇️ Downloading: ⏳ [■■■■■■■■■□] 90%",
    "⬇️ Downloaded: ✅ [■■■■■■■■■■] 100%"
]

# Temporary user session data
user_data = {}


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = f"""
{BOT_NAME}

🎵 Welcome to the ultimate music experience! 
I can help you download songs in multiple qualities. 🤟

🔽 Click the button below to begin your music search journey!

{COPYRIGHT}
    """

    keyboard = [[
        InlineKeyboardButton("🎵 Search for a Song",
                             callback_data="start_search")
    ], [
        InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/Shivaay20005")
    ],
                [
                    InlineKeyboardButton("📢 Updates Channel",
                                         url="https://t.me/Shivaay20005")
                ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_message, reply_markup=reply_markup)


# /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
🎧 <b>How to Use {BOT_NAME}</b>

1️⃣ <b>Send the name</b> of any song, artist, or video you want to download.
2️⃣ <b>Select a video</b> from the search results.
3️⃣ <b>Choose the desired quality</b> (MP3 128kbps, 192kbps, 320kbps or original).
4️⃣ <b>Wait while we process</b> and send you the audio file.

💡 Examples:
• <code>Believer Imagine Dragons</code>
• <code>Arijit Singh New Song 2024</code>

🛠 Available Commands:
/start – Show Status Of Bot   
/help – Show how to use the bot  
/cancel – Cancel the current operation

{COPYRIGHT}
    """
    await update.message.reply_text(help_text, parse_mode="HTML")


# Progress animation
async def update_progress(message, context: ContextTypes.DEFAULT_TYPE):
    for animation in LOADING_ANIMATIONS:
        await message.edit_text(animation)
        await asyncio.sleep(0.5)


# Handle search query message
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    chat_id = update.message.chat.id
    status_message = await update.message.reply_text(
        f"🔍 Searching for: {query}\n\n{COPYRIGHT}")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'nocheckcertificate': True,
            'extract_flat': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch5:{query}", download=False)
            if not info or not info.get('entries'):
                await status_message.edit_text(
                    f"❌ No results found for: {query}\n\n{COPYRIGHT}")
                return

            videos = info['entries']
            keyboard = []
            user_data[chat_id] = {'videos': videos}

            for idx, video in enumerate(videos[:5]):
                title = video.get('title', 'Unknown Title')
                if len(title) > 50:
                    title = title[:50] + "..."
                keyboard.append([
                    InlineKeyboardButton(f"🎵 {idx+1}. {title}",
                                         callback_data=f"select_{idx}")
                ])

            keyboard.append(
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel")])
            reply_markup = InlineKeyboardMarkup(keyboard)

            await status_message.edit_text(
                f"🔍 Found {len(videos)} results for: {query}\n\nPlease select a song:\n\n{COPYRIGHT}",
                reply_markup=reply_markup)

    except Exception as e:
        await status_message.edit_text(f"❌ Error: {str(e)}\n\n{COPYRIGHT}")


# Callback handler for buttons
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat.id
    data = query.data
    await query.answer()

    if data == "cancel":
        await query.message.delete()
        if chat_id in user_data:
            del user_data[chat_id]
        return

    # New button: "🎵 Search for a Song"
    if data == "start_search":
        instruction_msg = f"""
<b>🎧 How to Use {BOT_NAME}</b>

📌 Now send me the <b>name of the song, artist, or YouTube video</b> you want.

💡 Examples:
• <code>Believer Imagine Dragons</code>
• <code>Arijit Singh New Song 2024</code>

🎚 I will search the top 5 results and let you pick your preferred audio quality:
• MP3 (128kbps, 192kbps, 320kbps)
• Original YouTube Audio

Send your search query now! 🎶

{COPYRIGHT}
        """
        await query.message.edit_text(instruction_msg, parse_mode="HTML")
        return

    if data.startswith("select_"):
        video_idx = int(data.split("_")[1])

        if chat_id not in user_data or video_idx >= len(
                user_data[chat_id]['videos']):
            await query.message.edit_text(
                "❌ Invalid selection. Please try again.")
            return

        video = user_data[chat_id]['videos'][video_idx]

        keyboard = [
            [
                InlineKeyboardButton("🎧 MP3 (128kbps)",
                                     callback_data=f"dl_{video_idx}_mp3_128")
            ],
            [
                InlineKeyboardButton("🎧 MP3 (192kbps)",
                                     callback_data=f"dl_{video_idx}_mp3_192")
            ],
            [
                InlineKeyboardButton("🎧 MP3 (320kbps)",
                                     callback_data=f"dl_{video_idx}_mp3_320")
            ],
            [
                InlineKeyboardButton("🎵 Original Quality",
                                     callback_data=f"dl_{video_idx}_original")
            ], [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            f"🎵 Selected: {video.get('title', 'Unknown Title')}\n\nSelect quality:\n\n{COPYRIGHT}",
            reply_markup=reply_markup)

    elif data.startswith("dl_"):
        parts = data.split("_")
        video_idx = int(parts[1])
        format_type = parts[2]
        quality = parts[3] if len(parts) > 3 else None

        if chat_id not in user_data or video_idx >= len(
                user_data[chat_id]['videos']):
            await query.message.edit_text(
                "❌ Invalid selection. Please try again.")
            return

        video = user_data[chat_id]['videos'][video_idx]
        video_url = video.get('url') or f"https://youtu.be/{video.get('id')}"

        await query.message.edit_text(
            f"⬇️ Preparing download...\n\n{COPYRIGHT}")

        try:
            output_path = f"{chat_id}_%(title)s.%(ext)s"
            ydl_opts = {
                'outtmpl': output_path,
                'quiet': True,
                'nocheckcertificate': True
            }

            if format_type == "mp3":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality
                }]
                ydl_opts['format'] = 'bestaudio/best'
            else:
                ydl_opts['format'] = 'best'

            await update_progress(query.message, context)

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                ext = 'mp3' if format_type == 'mp3' else info['ext']
                final_file = filename.rsplit('.', 1)[0] + f'.{ext}'

            caption = f"""
🎵 Title: {info.get('title', 'N/A')}
⏱ Duration: {info.get('duration_string', 'N/A')}
👁 Views: {info.get('view_count', 'N/A'):,}
💿 Quality: {'MP3 ' + quality + 'kbps' if format_type == 'mp3' else 'Original'}

Downloaded by {BOT_NAME}
{COPYRIGHT}
            """

            await context.bot.send_audio(chat_id=chat_id,
                                         audio=open(final_file, 'rb'),
                                         caption=caption,
                                         title=info.get('title'),
                                         performer=info.get(
                                             'uploader', 'Unknown Artist'))

            os.remove(final_file)
            await query.message.delete()

        except Exception as e:
            await query.message.edit_text(
                f"❌ Download failed: {str(e)}\n\n{COPYRIGHT}")

        if chat_id in user_data:
            del user_data[chat_id]


# Run the bot
if __name__ == "__main__":
    print(f"🤖 {BOT_NAME} is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print(f"✅ {BOT_NAME} is running!")
    app.run_polling()
