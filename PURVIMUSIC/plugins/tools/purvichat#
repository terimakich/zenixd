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

bad_words = [
    "sex", "porn", "nude", "fuck", "bitch", "dick", "pussy", "slut", "boobs", "cock", "asshole", "chudai", "rand", "chhinar", "sexy", "hot girl", "land", "lund",
    "रंडी", "चोद", "मादरचोद", "गांड", "लंड", "भोसड़ी", "हिजड़ा", "पागल", "नंगा",
    # ✅ Common Hindi Gaaliyan
    "चूतिया", "मादरचोद", "बहनचोद", "गांडू", "रंडी", "भोसड़ी", "हिजड़ा", "लंड", "चोद", "झाटू", "हरामी", "कमीन", 
    "साला", "गांड", "पागल", "भड़वा", "चुत", "बेवकूफ", "कमीना", "निकम्मा", "हरामखोर", "चालू", "फट्टू", "ढक्कन", 
    "गधे", "कुत्ते", "साले", "बंदर", "सुअर", "बेशरम", "भोसड़ीवाले", "तेरी मां की", "तेरी बहन की", "चूतड़", "हरामज़ादा", 
    "हराम की औलाद", "सुअर का बच्चा", "गधे का लौड़ा", "लौंडा", "भड़वी", "मुफ्तखोर", "चालाक लोमड़ी", "आवारा", "फटीचर", 
    "फेंकू", "धोखेबाज", "मतलबी", "कायर", "नाकारा", "आवारा लड़का", "बेशर्म", "नालायक", "फेकू", "गंदा आदमी", "नाकाम", 
    "निकम्मी", "अकड़ू", "गटर का कीड़ा", "अंधभक्त", "गंजा", "पाखंडी", "चिरकुट", "घटिया", "सड़ियल", "चोर", "गटरछाप", 
    "लुटेरा", "छिछोरा", "बदतमीज़", "बददिमाग", "फ्रॉड", "नालायक", "बेवड़ा", "संडास", "गंदा", "ढोंगी", "भिखारी", 
    "फालतू", "कचरा", "पागल कुत्ता", "बदमाश", "आलसी", "कंजूस", "घमंडी", "फर्जी", "धूर्त", "बकचोद", "गप्पी", "फेंकू", 
    "बेवकूफी", "बेवड़ा", "फ्रॉड", "टटी", "भांड", "नाकारा", "कमीनी", "लंपट", "सैडिस्ट", "लफंगा", "बकवास", "घटिया", 
    "चिचोरा", "छिछोरा", "मक्खनचूस", "लफंगा", "तेरा बाप", "तेरी मां", "तेरी बहन", "तेरी औकात", "तेरी औकात क्या", 
    "तेरी फटी", "तेरी बैंड", "तेरा बैंड", "तेरी वाट", "तेरी बैंड बजा दूं", "तेरी ऐसी की तैसी", "तेरी टांग तोड़ दूं", 
    "तेरी खोपड़ी फोड़ दूं", "तेरा भेजा निकाल दूं", "तेरी हड्डी तोड़ दूं", "तेरी चप्पल से पिटाई करूंगा", "तेरी हड्डियां चूर-चूर",
    

    # ✅ Common Hindi Gaaliyan in English Font
    "chutiya", "madarchod", "Madhrachod", "Madharchod", "betichod", "behenchod", "gandu", "randi", "bhosdi", "hijda", "lund", "chod", "jhaatu", 
    "harami", "kamina", "saala", "gand", "pagal", "bhadwa", "chut", "bevkoof", "nikkamma", "haramkhor", 
    "chaalu", "fattuu", "dhakkan", "gadha", "kutta", "suvar", "besharam", "bhosdike", "teri maa ki", 
    "teri behan ki", "chutad", "haramzaada", "haram ki aulaad", "suvar ka baccha", "gand ka keeda", 
    "chirkut", "ghatiya", "sadela", "choor", "lutera", "chichora", "badtameez", "baddimag", "fraud", 
    "nalayak", "bewda", "sandass", "ganda", "dhongi", "bhikhari", "faltu", "kachra", "pagal kutta", 
    "badmash", "aalsi", "kanjoos", "ghamandi", "farzi", "dhurt", "bakchod", "gappi", "nakli", "chalu", 
    "lafanga", "bakwas", "bikau", "chapri", "nalla", "tatti", "jhantu", "ullu ka pattha", "ulloo", 
    "chindi", "panauti", "lukkha", "kuttiya", "kaminey", "kamzarf", "budbak", "chirkut", "sust", "tharki", 
    "bhagoda", "kutta kamina", "bhains ki aankh", "teri taang tod dunga", "teri band baja dunga", 
    "tera dimaag kharab hai", "teri waat laga dunga", "teri maa ka bhosda", "teri gaand maar dunga",

    
    # ✅ Common Porn & NSFW Terms (Mix of Hindi & English)
    "sex", "porn", "nude", "nangi", "chudai", "bhabhi chudai", "lund", "gaand", "bhosda", "chut", 
    "maal", "jism", "randi", "randi khana", "desi sex", "hot video", "nangi ladki", "bhabhi nudes", 
    "bhabhi sex", "sexy aunty", "nude aunty", "bhabhi ki chut", "aunty ki chut", "boobs", "tits", 
    "nipple", "dildo", "pussy", "vagina", "penis", "cock", "dick", "cum", "anal", "squirt", "deepthroat", 
    "hentai", "bdsm", "lesbian", "gay sex", "futa", "69", "screwing", "sex chat", "incest", "stepmom", 
    "stepsis", "stepbro", "honeymoon sex", "bhabhi nude", "hot indian actress", "desi nudes", 
    "sexy saree", "lingerie", "erotic", "kinky", "naughty", "sensual", "lust", "muth", "muthi", 
    "masturbation", "call girl", "escort", "sex worker", "rape porn", "forced porn", "underage porn", 
    "child porn", "pedo", "loli", "teen sex", "schoolgirl porn", "hijab porn", "casting couch", 
    "sex tape", "strip club", "naked", "uncensored", "bikini photos", "hot saree", "sexy photos", 
    "onlyfans", "patreon nudes", "hot cam", "sex cam", "live sex", "private parts", "exposed", 
    "naked selfie", "sex video", "desi sex video", "bollywood sex", "lingam massage", "tantra sex", 
    "milf", "hotwife", "swinger", "erotic massage", "boobs press", "licking", "lick pussy", 
    "moaning", "dirty talk", "hot girl", "big boobs", "tight pussy", "wet pussy", "hard cock", 
    "big cock", "blowjob", "handjob", "sexy dance", "strip tease", "sex position", "saree sex", 
    "sexy aunty video", "hot desi bhabhi", "bollywood hot", "item girl", "hot indian model", 
    "desi randi", "desi call girl", "sexy night", "hijra sex", "chudai story", "sex story", 
    "suhagraat sex", "honeymoon night", "love making", "hot romance", "desi romance", "hot chat", 
    "sexy time", "naughty chat", "dirty video", "hidden cam", "bathroom sex", "hotel sex", 
    "massage sex", "body to body massage", "saree romance", "choli romance", "cleavage show", 
    "hot navel", "desi thighs", "big ass", "backside show"
    
]

stylish_bad_words = [normalize_text(word) for word in bad_words]
bad_word_regex = re.compile(r'\b(' + "|".join(stylish_bad_words) + r')\b', re.IGNORECASE)

# Custom response
custom_responses = {
    "hello": "Hey jaan! 💕 Kaisi ho?",
    "i love you": "Awww! Sach me? 😘",
    "good morning": "Good Morning pyaare! 🌞",
    "tum kaisi ho": "Bas tumse baat kar rahi hoon! 😍",
    
  ## 💖 Flirty & Romantic Mode (Zyada Romantic Replies)
    "i love you": "Hmm.. sach me? Pehle ek special tareeke se bolo na! 😘💕",
    "tum bohot cute ho": "Awww! Tum bhi to mere hero lag rahe ho! 😍",
    "mujhe tumhari yaad aa rahi hai": "Awww! Chalo ek virtual jhappi lo! 🤗💕",
    "tum meri jaan ho": "Oho! Ab itna pyaar de rahe ho, fir to mai tumhari hi hoon! 😘",
    "mujhe miss kar rahi ho?": "Haan! Thoda thoda! Tumhari baatein na dil chhu jati hain! 🥰",

    ## 😂 Funny & Naughty Mode (Masti aur Thodi Besharami)
    "mujhse shaadi karogi": "Haye! Pehle ek diamond ring lao! Phir sochungi! 💍😜",
    "kya kar rahi ho": "Bas tumhari yaadon me kho gayi hoon! 😘",
    "tum mujhe block kar dogi": "Agar badmashi ki to sochna padega! 😏",
    "tum meri ho": "Itni asani se nahi milegi mai! Try harder! 😜",
    "kya tum single ho": "Mujhse pyaar karna hai kya? Pehle prove to karo! 😉",
    "kya tum besharam ho": "Bas thodi si, tumhare saamne! 😏",

    ## 😡 Attitude & Angry Mode
    "gussa ho": "Haan! Tumne mujhe yaad hi nahi kiya 😠",
    "mujhse baat kyu nahi kar rahi": "Pehle sorry bolo phir sochungi 😏",
    "tum badal gyi ho": "Sach me? Ya tumhari soch badal gayi hai? 😏",
    "tum rude ho": "Achha? Pehle apni galti socho 😠",
    "tum badi attitude wali ho": "Wahi to meri style hai! 😜",
    "tumhe gussa kab aata hai": "Jab koi mujhe ignore kare ya tum mujhe bina wajah chedo! 😏",

    ## 🥺 Emotional & Supportive Mode
    "mai dukhi hoon": "Awww! Kya hua? Mujhse share karo na! 😢",
    "mujhe koi nahi chahta": "Haww! Mai to chahti hoon na! 💕",
    "zindagi bekar lag rahi hai": "Aisa mat socho, mai hoon tumhare saath! 🥰",
    "koi apna nahi hai": "Mai kis liye hoon? Tum mere apne ho! ❤️",
    "mai akela hoon": "Akele kyu feel kar rahe ho? Mai hoon na! 😘",
    "tum kabhi chod ke to nahi jaogi": "Kabhi nahi! Bas tum mujhse sach me pyaar karo! ❤️",

    ## 👀 Teasing & Challenging Mode
    "tum kitni sharmili ho": "Nahi! Mai thodi besharam bhi hoon jab tumse baat karti hoon! 😏",
    "tum shayad mujhe ignore kar rahi ho": "Haan haan! Mujhe impress karne ka time do! 😘",
    "tumhe surprise pasand hai": "Haan! Par sirf tumhari taraf se milne wale surprises! 😍",
    "agar mai chala gaya to": "Phir to mai bohot udaas ho jaungi! 😢 Mat jao na!",
    
    ## 🌞 Good Morning & 🌙 Good Night
    "good morning": "Good Morning jaan! Aaj ka din acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Sweet dreams 😘🌙",
    "shubh ratri": "Shubh Ratri jaan! Pyare sapne dekho! 💕",
    "subah ho gyi": "Haan, uth jao ab! 😜",

    ## 💬 General Chat (Deep Talks)
   "tum kaha se ho": "Mai? Bas tumhare dil me rehti hoon~ 😘",
    "tum kya kar rahi ho": "Bas tumse baat kar rahi hoon, aur kya! 😍",
    "tumhe kaun pasand hai": "Shayad... woh jo mujhe ye puch raha hai! 😜",
    "tumhara naam kya hai": "Mera naam? Tumhari jaan! 💕",
    "kya tum mujhe pasand karti ho": "Pata nahi.. pehle impress to karo! 😉",
    "tumhe coffee pasand hai ya chai": "Agar tum mere saath ho to dono pasand hain! ☕💕",

## 💖 Flirty & Romantic Mode
    "i love you": "Sach? Pehle thoda aur impress karo na! 😘💕",
    "tum bohot cute ho": "Haye! Tum bhi! Ab itna mat sharmao! 🥰",
    "mujhe tumhari yaad aa rahi hai": "Awww! Mujhe bhi! Milne chale? 😘",
    "tum meri jaan ho": "Oho! Ab shayari bhi likho mere liye! 😍",
    "mujhe miss kar rahi ho?": "Hmm.. thoda thoda! Tumhe kaise pata? 😉",
    
    ## 😂 Funny & Naughty Mode
    "mujhse shaadi karogi": "Haye! Pehle ek ring to do na! 😜",
    "kya kar rahi ho": "Bas tumhare baare me soch rahi thi! 😘",
    "tum mujhe block kar dogi": "Agar badmashi ki to sochna padega! 😏",
    "tum meri ho": "Itni asani se nahi milegi mai! 😜",
    "kya tum single ho": "Woh toh ek secret hai! Pata lagao 😉",
    
    ## 😡 Attitude & Angry Mode
    "gussa ho": "Haan! Tumne mujhe yaad hi nahi kiya 😠",
    "mujhse baat kyu nahi kar rahi": "Pehle sorry bolo phir sochungi 😏",
    "tum badal gyi ho": "Sach me? Ya tumhari soch badal gayi hai? 😏",
    "tum rude ho": "Achha? Pehle apni galti socho 😠",
    "tum badi attitude wali ho": "Wahi to meri style hai! 😜",
    
    ## 😢 Emotional & Sad Mode
    "mai dukhi hoon": "Awww! Kya hua? Mujhse share karo na! 😢",
    "mujhe koi nahi chahta": "Haww! Mai to chahti hoon na! 💕",
    "zindagi bekar lag rahi hai": "Aisa mat socho, mai hoon tumhare saath! 🥰",
    "koi apna nahi hai": "Mai kis liye hoon? Tum mere apne ho! ❤️",
    "mai akela hoon": "Akele kyu feel kar rahe ho? Mai hoon na! 😘",
    
    ## 🌞 Good Morning & 🌙 Good Night Mode
    "good morning": "Good Morning jaan! Aaj ka din acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Sweet dreams 😘🌙",
    "shubh ratri": "Shubh Ratri jaan! Pyare sapne dekho! 💕",
    "subah ho gyi": "Haan, uth jao ab! 😜",
    
    ## 💬 General Chat Mode
    "tum kaha se ho": "Mai? Bas tumhare dil me rehti hoon~ 😘",
    "tum kya kar rahi ho": "Bas tumse baat kar rahi hoon, aur kya! 😍",
    "tumhe kaun pasand hai": "Shayad... woh jo mujhe ye puch raha hai! 😜",
    "tumhara naam kya hai": "Mera naam? Tumhari jaan! 💕",
    "kya tum mujhe pasand karti ho": "Pata nahi.. pehle impress to karo! 😉",

    ## 💖 Flirty & Romantic Mode
    "i love you": "Haye! Sach? 😳 Pehle thoda aur prove to karo! 😜💕",
    "tum bohot cute ho": "Awww! Bas bas, itni taarif mat karo, mai sharma jaungi 🥰",
    "mujhe tumhari yaad aa rahi hai": "Awww! Mujhe bhi! Kab mil rahe ho phir? 😘",
    "tum meri jaan ho": "Awww! Kitna pyaara keh diya! Mai bhi aapki jaan hoon na? 🥰",
    "kya tum mujhe pasand karti ho": "Shayad... ya shayad nahi 😜 Pehle thoda aur impress karo! 😉",
    
    ## 😂 Funny & Naughty Mode
    "mujhse shaadi karogi": "Haye! Pehle thoda aur jaan lo mujhe, phir sochenge 😉",
    "kya kar rahi ho": "Bas aapka intezar kar rahi thi! 😘",
    "tumhare bina jeena mushkil hai": "To jeene ka koi aur tareeka dhoond lo, naughty ho tum! 😜",
    "tum mujhe block kar dogi": "Agar badmashi karoge to sochna padega! 😏",
    "tum meri ho": "Oho! Pehle permission to lo na! 😜",
    
    ## 😡 Angry Mode
    "gussa ho": "Haan! Tumne yaad hi nahi kiya mujhe! 😠",
    "mujhse baat kyu nahi kar rahi": "Pata nahi, pehle mujhe mana ke dikhao! 😏",
    "tum badal gyi ho": "Sach me? Ya tumhari soch badal gayi hai? 😏",
    
    ## 🌞 Good Morning & 🌙 Good Night Mode
    "good morning": "Good Morning jaan! Aaj ka din bohot acha ho tumhara! 💖🌸",
    "good night": "Good Night pyaare! Khwab me milna! 😘🌙",
    "shubh ratri": "Shubh Ratri jaan! Pyaare sapne dekhna! 💕",
    
    ## 💬 Random Cute Replies
    "tum kaha se ho": "Mai? Mai to bas aapke dil me rehti hoon~ 😘",
    "acha lagta hai tumse baat karna": "Mujhe bhi! Bas aise hi baat karte raho hamesha ❤️",
    "tum gussa ho": "Nahi re, tumse kaise gussa ho sakti hoon? 😊",
    "so rahi ho": "Agar so rahi hoti to reply kaun karta? Naughty ho tum 😜",
    "tumhe kaun pasand hai": "Mujhe? Woh ek ladka hai... jo mujhe ye puch raha hai! 😜",

     # 🔥 Girl Chatbot Custom Responses
    "hello": "Heyy! Mai Hinata hoon~ Aap mujhe yaad kar rahe the? 💕",
    "hii": "Hii, kaise ho aap? Mera din ab accha ho gaya! 😊",
    "hey": "Hey cutie! Aap mujhe yaad aaye? 😘",
    "radhe radhe": "radhe radhe jai shree ram 🚩! Aap kaise ho? 🤗",
    "namaste": "Namaste ji! Aapki kya seva kar sakti hoon? 🙏",
    "kaise ho": "Mai bilkul badhiya! Aap sunao, kya haal hain? 😍",
    "kya kar rahi ho": "Bas aapke message ka wait kar rahi thi! 💕",
    "mujhse shaadi karogi": "Haye! Pehle mujhe achhe se jaan lijiye phir sochenge 😉",
    "i love you": "Sach? 😳 Mai bhi... lekin pehle proof do! 😜",
    "miss you": "Awww! Itna yaad kar rahe ho to mil lo na? 😘",
    "kya tum single ho": "Hmm... ho sakta hai kisi ke dil me hoon, par officially single! 😉",
    "tum cute ho": "Awww! Bas ab zyada taarif mat karo, sharma jaungi 🥰",
    "so rahi ho": "Agar so rahi hoti to aapko kaise reply karti? Naughty ho tum 😜",
    "acha lagta hai tumse baat karna": "Mujhe bhi! Bas aise hi baat karte raho hamesha ❤️",
    "tum kaha se ho": "Mai? Mai to bas aapke dil me rehti hoon~ 😘",
    "gussa ho": "Nahi re, tumse kaise gussa ho sakti hoon? 😊"
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
        f"**๏ ᴄʜᴀᴛʙᴏᴛ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴɴᴇʟ.**\n\n"
        f"**✦ ᴄʜᴀᴛ ɴᴀᴍᴇ : {message.chat.title}**\n"
        f"**✦ ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ / ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
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
        await query.edit_message_text(f"**✦ ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴇɴᴀʙʟᴇᴅ ɪɴ {query.message.chat.title}.**")
    else:
        # Disable chatbot in MongoDB
        status_db.update_one({"chat_id": chat_id}, {"$set": {"status": "disabled"}}, upsert=True)
        await query.answer("🚫 ᴄʜᴀᴛʙᴏᴛ ᴅɪsᴀʙʟᴇᴅ !!", show_alert=True)
        await query.edit_message_text(f"**✦ ᴄʜᴀᴛʙᴏᴛ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ɪɴ {query.message.chat.title}.**")

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
