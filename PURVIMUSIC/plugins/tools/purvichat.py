from pyrogram import Client, filters, enums
from pyrogram.types import Message
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
import random
import os
from PURVIMUSIC import app as bot
from pyrogram import idle

# MongoDB connection
MONGO_URL = os.environ.get("MONGO_URL", "mongodb+srv://bikash:bikash@bikash.3jkvhp7.mongodb.net/?retryWrites=true&w=majority")
mongo_client = MongoClient(MONGO_URL)
vdb = mongo_client["vDb"]["v"]
chatai_db = mongo_client["Word"]["WordDb"]

# Helper function to check if user is an admin
async def is_admins(chat_id: int):
    admins = [member.user.id for member in await bot.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS)]
    return admins

# Command to turn chatbot off
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def chatbot_off(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("**Are you sure you're an admin?**")

    is_v = await vdb.find_one({"chat_id": chat_id})
    if not is_v:
        await vdb.insert_one({"chat_id": chat_id})
        await message.reply_text("**Chatbot disabled successfully! 💔**")
    else:
        await message.reply_text("**Chatbot is already disabled.**")

# Command to turn chatbot on
@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def chatbot_on(client, message: Message):
    user = message.from_user.id
    chat_id = message.chat.id

    if user not in await is_admins(chat_id):
        return await message.reply_text("**Are you sure you're an admin?**")

    is_v = await vdb.find_one({"chat_id": chat_id})
    if is_v:
        await vdb.delete_one({"chat_id": chat_id})
        await message.reply_text("**Chatbot enabled successfully! 🥳**")
    else:
        await message.reply_text("**Chatbot is already enabled.**")

# Command to display usage information
@bot.on_message(filters.command("chatbot", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def chatbot_usage(client, message: Message):
    await message.reply_text("**Usage: /chatbot [on/off] only for groups.**")

# Fix in the handle_group_messages function where you iterate over the AsyncIOMotorCursor
@bot.on_message((filters.text | filters.sticker) & ~filters.private & ~filters.bot)
async def handle_group_messages(client, message: Message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        is_v = await vdb.find_one({"chat_id": chat_id})
        if not is_v:
            await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)
            K = []
            is_chat = chatai_db.find({"word": message.text})  # Returns an AsyncIOMotorCursor
            k = await chatai_db.find_one({"word": message.text})
            if k:
                async for x in is_chat:  # Use async for to iterate over the cursor
                    K.append(x['text'])
                response = random.choice(K)
                is_text = await chatai_db.find_one({"text": response})
                if is_text['check'] == "sticker":
                    await message.reply_sticker(response)
                else:
                    await message.reply_text(response)
    else:
        is_v = await vdb.find_one({"chat_id": chat_id})
        bot_id = (await bot.get_me()).id
        if message.reply_to_message.from_user.id == bot_id:
            if not is_v:
                await bot.send_chat_action(chat_id, enums.ChatAction.TYPING)
                K = []
                is_chat = chatai_db.find({"word": message.text})  # Returns an AsyncIOMotorCursor
                k = await chatai_db.find_one({"word": message.text})
                if k:
                    async for x in is_chat:  # Use async for to iterate over the cursor
                        K.append(x['text'])
                    response = random.choice(K)
                    is_text = await chatai_db.find_one({"text": response})
                    if is_text['check'] == "sticker":
                        await message.reply_sticker(response)
                    else:
                        await message.reply_text(response)
        elif message.reply_to_message.from_user.id != bot_id:
            if message.sticker:
                is_chat = await chatai_db.find_one({"word": message.reply_to_message.text, "id": message.sticker.file_unique_id})
                if not is_chat:
                    await chatai_db.insert_one({
                        "word": message.reply_to_message.text,
                        "text": message.sticker.file_id,
                        "check": "sticker",
                        "id": message.sticker.file_unique_id
                    })
            elif message.text:
                is_chat = await chatai_db.find_one({"word": message.reply_to_message.text, "text": message.text})
                if not is_chat:
                    await chatai_db.insert_one({"word": message.reply_to_message.text, "text": message.text, "check": "none"})
# Start the bot
idle()
