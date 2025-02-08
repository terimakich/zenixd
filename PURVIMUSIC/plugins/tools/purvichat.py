from pyrogram import Client, filters, enums
from pyrogram.enums import ChatAction
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import os
import re
import requests
import random
import unicodedata

from langdetect import detect

from PURVIMUSIC import app as bot

# ✅ MongoDB Connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://teamdaxx123:teamdaxx123@cluster0.ysbpgcp.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
status_db = mongo_client["ChatbotStatus"]["status"]
chatai_db = mongo_client["Word"]["WordDb"]

# ✅ API Configuration
API_KEY = "abacf43bf0ef13f467283e5bc03c2e1f29dae4228e8c612d785ad428b32db6ce"
BASE_URL = "https://api.together.xyz/v1/chat/completions"

# ✅ Helper Function: Check If User Is Admin
async def is_admin(chat_id: int, user_id: int):
    admins = [member.user.id async for member in bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return user_id in admins

# ✅ Stylish Font Bad Words Detection
def normalize_text(text):
    return unicodedata.normalize("NFKD", text)

bad_words = ["sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole", "chudai", "rand", "chhinar", "sexy", "hot girl", "land", "lund", "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा"]
stylish_bad_words = [normalize_text(word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# Custom response
custom_responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍"
}

# ✅ Inline Buttons for Chatbot Control
CHATBOT_ON = [
    [InlineKeyboardButton(text="ᴇɴᴀʙʟᴇ", callback_data="enable_chatbot"), InlineKeyboardButton(text="ᴅɪsᴀʙʟᴇ", callback_data="disable_chatbot")]
]

# ✅ /chatbot Command with Buttons
@bot.on_message(filters.command("chatbot") & filters.group)
async def chatbot_control(client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if not await is_admin(chat_id, user_id):
        return await message.reply_text("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !!")

    await message.reply_text(
        f"๏ ᴄʜᴀᴛʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴɴᴇʟ\n\n"
        f"✦ ᴄʜᴀᴛ ɴᴀᴍᴇ : {message.chat.title}\n"
        f"✦ ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ / ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

# ✅ Callback for Enable/Disable Buttons
@bot.on_callback_query(filters.regex(r"enable_chatbot|disable_chatbot"))
async def chatbot_callback(client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id

    if not await is_admin(chat_id, user_id):
        return await query.answer("❍ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ !!", show_alert=True)

    action = query.data

    if action == "enable_chatbot":
        # Enable chatbot in MongoDB
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "enabled"}}, upsert=True)
        await query.answer("✅ ᴄʜᴀᴛʙᴏᴛ ᴇɴᴀʙʟᴇᴅ !!", show_alert=True)
        await query.edit_message_text(f"✦ ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ ɪɴ {query.message.chat.title}.")
    else:
        # Disable chatbot in MongoDB
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True)
        await query.answer("🚫 ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ !!", show_alert=True)
        await query.edit_message_text(f"✦ ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ɪɴ {query.message.chat.title}.")

# ✅ Main Chatbot Handler (Text & Stickers)
@bot.on_message(filters.text | filters.sticker)
async def chatbot_reply(client, message: Message):
    chat_id = message.chat.id
    text = message.text.strip() if message.text else ""
    bot_username = (await bot.get_me()).username.lower()

    # First, check if the chatbot is enabled for the current chat
    chat_status = await status_db.find_one({"chat_id": chat_id})
    if chat_status and chat_status.get("status") == "disabled":
        return  # If chatbot is disabled, do not reply to any messages

    # Typing indicator
    await bot.send_chat_action(chat_id, ChatAction.TYPING)

    # Check if bad words exist in the message
    if re.search(bad_word_regex, text):
        await message.delete()
        await message.reply_text("ᴘʟᴇᴀsᴇ : ᴅᴏɴ'ᴛ sᴇɴᴅ ʙᴀᴅ ᴡᴏʀᴅ ᴛʏᴘᴇ ᴍᴇssᴀɢᴇs ᴀᴘɴᴀ ʙᴇʜᴀᴠɪᴏʀ ᴄʜᴀɴɢᴇ ᴋᴀʀᴇ ᴘʟᴇsᴀsᴇ 🙂.")
        return

    # If it's a group message
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        # Check custom responses
        for key in custom_responses:
            if key in text.lower():
                await message.reply_text(custom_responses[key])
                return

        # Fetch response from MongoDB
        K = []
        if message.sticker:
            async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
                K.append(x['text'])
        else:
            async for x in chatai_db.find({"word": text}):
                K.append(x['text'])

        if K:
            response = random.choice(K)
            is_text = await chatai_db.find_one({"text": response})
            if is_text and is_text['check'] == "sticker":
                await message.reply_sticker(response)
            else:
                await message.reply_text(response)
            return

    # If it's a mention or bot's username, use the API
    if f"@{bot_username}" in text.lower() or bot_username in text.lower():
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "messages": [{"role": "user", "content": text}]}

        response = requests.post(BASE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "❍ ᴇʀʀᴏʀ: API response missing!")
            await message.reply_text(result)
        else:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API failed. Status: {response.status_code}")
        return

    # Handle private chat messages (same logic as for groups, but for private)
    elif message.chat.type == enums.ChatType.PRIVATE:
        # Check custom responses
        for key in custom_responses:
            if key in text.lower():
                await message.reply_text(custom_responses[key])
                return

        # Fetch response from MongoDB
        K = []
        if message.sticker:
            async for x in chatai_db.find({"word": message.sticker.file_unique_id}):
                K.append(x['text'])
        else:
            async for x in chatai_db.find({"word": text}):
                K.append(x['text'])

        if K:
            response = random.choice(K)
            is_text = await chatai_db.find_one({"text": response})
            if is_text and is_text['check'] == "sticker":
                await message.reply_sticker(response)
            else:
                await message.reply_text(response)
            return

        # Fallback to API if no responses found
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo", "messages": [{"role": "user", "content": text}]}

        response = requests.post(BASE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json().get("choices", [{}])[0].get("message", {}).get("content", "❍ ᴇʀʀᴏʀ: API response missing!")
            await message.reply_text(result)
        else:
            await message.reply_text(f"❍ ᴇʀʀᴏʀ: API failed. Status: {response.status_code}")
