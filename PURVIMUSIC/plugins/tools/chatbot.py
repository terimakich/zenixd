import random
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction, ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from deep_translator import GoogleTranslator
from config import MONGO_DB_URI as MONGO_URL
from PURVIMUSIC import app

# Database Connections
MONGO_URL = config.MONGO_DB_URI
WORD_MONGO_URL = "mongodb+srv://AbhiModszYT:AbhiModszYT@abhimodszyt.flmdtda.mongodb.net/?retryWrites=true&w=majority"

chatdb = MongoClient(MONGO_URL)
worddb = MongoClient(WORD_MONGO_URL)

status_db = chatdb["ChatBotStatusDb"]["StatusCollection"]
chatai = worddb["Word"]["WordDb"]
lang_db = chatdb["ChatLangDb"]["LangCollection"]

translator = GoogleTranslator()

# Language Setup
languages = {
    "english": "en",
    "hindi": "hi",
    "russian": "ru",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "arabic": "ar",
    "turkish": "tr",
    "portuguese": "pt",
    "bengali": "bn",
    "urdu": "ur",
    "tamil": "ta",
    "telugu": "te",
    "marathi": "mr",
    "punjabi": "pa",
}

# Chatbot Enable/Disable Buttons
CHATBOT_ON = [
    [
        InlineKeyboardButton(text="Enable ✅", callback_data="enable_chatbot"),
        InlineKeyboardButton(text="Disable ❌", callback_data="disable_chatbot"),
    ],
]


def generate_language_buttons():
    buttons = []
    row = []
    for lang, code in languages.items():
        row.append(InlineKeyboardButton(lang.capitalize(), callback_data=f"setlang_{code}"))
        if len(row) == 3:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(buttons)


def get_chat_language(chat_id):
    chat_lang = lang_db.find_one({"chat_id": chat_id})
    return chat_lang["language"] if chat_lang else "en"


@app.on_message(filters.command("chatbot"))
async def chatbot_settings(client: Client, message: Message):
    await message.reply_text(
        f"Chat: {message.chat.title}\n**Choose an option to enable/disable chatbot.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )


@app.on_message(filters.command(["chatbotlang", "setchatbotlang"]))
async def set_language(client: Client, message: Message):
    await message.reply_text("Please select your chat language:", reply_markup=generate_language_buttons())


@app.on_callback_query(filters.regex(r"setlang_"))
async def language_selection_callback(client: Client, query: CallbackQuery):
    lang_code = query.data.split("_")[1]
    chat_id = query.message.chat.id

    if lang_code in languages.values():
        lang_db.update_one({"chat_id": chat_id}, {"$set": {"language": lang_code}}, upsert=True)
        await query.answer(f"Chat language set to {lang_code.title()}.", show_alert=True)
        await query.message.edit_text(f"Chat language set to {lang_code.title()}.", reply_markup=generate_language_buttons())
    else:
        await query.answer("Invalid language selection.", show_alert=True)


@app.on_callback_query(filters.regex("enable_chatbot"))
async def enable_chatbot(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "enabled"}}, upsert=True)
    await query.answer("Chatbot Enabled ✅", show_alert=True)
    await query.edit_message_text(f"Chatbot has been enabled in {query.message.chat.title}.")


@app.on_callback_query(filters.regex("disable_chatbot"))
async def disable_chatbot(client: Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True)
    await query.answer("Chatbot Disabled ❌", show_alert=True)
    await query.edit_message_text(f"Chatbot has been disabled in {query.message.chat.title}.")


@app.on_message(filters.text & ~filters.command(["chatbot", "setchatbotlang"]))
async def chatbot_response(client: Client, message: Message):
    chat_id = message.chat.id
    chat_status = status_db.find_one({"chat_id": chat_id})

    if chat_status and chat_status.get("status") == "disabled":
        return

    if message.reply_to_message and message.reply_to_message.from_user.id == client.me.id:
        await client.send_chat_action(chat_id, ChatAction.TYPING)
        reply_data = await get_reply(message.text if message.text else "")

        if reply_data:
            response_text = reply_data["text"]
            chat_lang = get_chat_language(chat_id)

            translated_text = (
                response_text if chat_lang == "en" else GoogleTranslator(source="auto", target=chat_lang).translate(response_text)
            )

            await message.reply_text(translated_text)
        else:
            await message.reply_text("**I don't understand.**")


async def get_reply(word: str):
    replies = list(chatai.find({"word": word}))
    if not replies:
        replies = list(chatai.find())

    if replies:
        return random.choice(replies)
    return None


@app.on_message(filters.reply & filters.text)
async def save_reply(client: Client, message: Message):
    original_message = message.reply_to_message
    reply_text = message.text

    is_chat = chatai.find_one({"word": original_message.text, "text": reply_text})

    if not is_chat:
        chatai.insert_one({"word": original_message.text, "text": reply_text})


    
