from config import WELCOME_IMAGE
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c:Client, m:Message):
    REPLY_MARKUP = [
                [
                    InlineKeyboardButton('Join', url=''),
                ]
            ]
    txt = ""
    await m.reply_photo(WELCOME_IMAGE, txt, reply_markup=InlineKeyboardMarkup(REPLY_MARKUP))
