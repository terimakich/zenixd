from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    ABUTTON = [[InlineKeyboardButton("˹ sᴜᴘᴘᴏꝛᴛ ˼", url="https://t.me/The_Incricible")],[InlineKeyboardButton("˹ ᴜᴘᴅᴧᴛᴇ ˼", url="https://t.me/The_Incricible"),
    InlineKeyboardButton("˹ ᴧʟʟ ʙᴏᴛ ˼", url="https://t.me/The_Incricible")],[InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data=f"settingsback_helper"),
    ]]

    UBUTTON = [[InlineKeyboardButton("˹ ᴍᴜsɪᴄ ˼", callback_data="help_callback"),InlineKeyboardButton("˹ ᴛᴏᴏʟs ˼", callback_data=f"tbot_cb")],[InlineKeyboardButton("˹ ᴄʀᴇᴀᴛᴇ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ˼", callback_data="dplus HELP_host")],[InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data=f"settingsback_helper"),
    ]]

    TBUTTON = [[InlineKeyboardButton("˹ ᴀᴄᴛɪᴠᴇ ˼", callback_data="cplus HELP_active"),InlineKeyboardButton("˹ ᴀᴜᴛʜ ˼", callback_data="cplus HELP_auth")],[InlineKeyboardButton("˹ ʙʟᴏᴄᴋ ˼", callback_data="cplus HELP_block")],[InlineKeyboardButton("˹ ᴅᴇᴠ ˼", callback_data="cplus HELP_dev"),
    InlineKeyboardButton("˹ ɢ-ᴄᴀsᴛ ˼", callback_data="cplus HELP_gcast")],[InlineKeyboardButton("↺ ʙᴧᴄᴋ ↻", callback_data=f"ubot_cb"),
    ]]
