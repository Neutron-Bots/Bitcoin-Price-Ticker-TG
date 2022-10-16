import asyncio
import logging

from pyrogram import Client

from config import API_HASH, API_ID, BOT_TOKEN, REPLIT
from plugins.ticker import BTCTicker
from utils import ping_server

logging.getLogger().setLevel(logging.INFO)


if REPLIT:
    from threading import Thread

    from flask import Flask, jsonify
    app = Flask('')
    @app.route('/')
    def main():
        res = {
            "status":"running",
            "hosted":"replit.com",
        }
        return jsonify(res)

    def run():
        app.run(host="0.0.0.0", port=8000)
    
    async def keep_alive():
        server = Thread(target=run)
        server.start()


class Bot(Client):

    def __init__(self):
        super().__init__(
        "BTCTicker",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        plugins=dict(root="plugins")
        )

    async def start(self):
        
        if REPLIT:
            await keep_alive()
            asyncio.create_task(ping_server())

        await super().start()
        await asyncio.create_task(BTCTicker(self))
        logging.info('Task Created')
        logging.info('Bot started')

    async def stop(self, *args):
        await super().stop()
        logging.info('Bot Stopped Bye')

Bot().run()
