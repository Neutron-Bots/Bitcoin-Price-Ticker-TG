from config import CHANNEL_ID, WELCOME_IMAGE
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(filters.command('start') & filters.private & filters.incoming)
async def start(c:Client, m:Message):
    channel = await c.get_chat(CHANNEL_ID)

    REPLY_MARKUP = [
                [
                    InlineKeyboardButton('Join', url=channel.invite_link),
                ]
            ]
    txt = "Nothing Here\n\n**Check out my channel to know the bitcoin prices and details 24/7**"
    await m.reply_photo(WELCOME_IMAGE, caption=txt, reply_markup=InlineKeyboardMarkup(REPLY_MARKUP))
