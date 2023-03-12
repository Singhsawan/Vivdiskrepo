from pyrogram import Client
from config import *
import asyncio


import logging
import aiohttp
import traceback

API_ID = API_ID
API_HASH = API_HASH
BOT_TOKEN = BOT_TOKEN
ADMIN = ADMINS

async def ping_server():
    sleep_time = PING_INTERVAL
    while True:
        await asyncio.sleep(sleep_time)
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(REPLIT) as resp:
                    logging.info("Pinged server with response: {}".format(resp.status))
        except TimeoutError:
            logging.warning("Couldn't connect to the site URL..!")
        except Exception:
            traceback.print_exc()
            
if REPLIT:
    from flask import Flask, jsonify
    from threading import Thread
    
    app = Flask('')
    
    @app.route('/')
    def main():
        
        res = {
            "status":"running",
            "hosted":"replit.com",
            "repl":REPLIT,
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
        "shortener",
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
        me = await self.get_me()
        self.username = '@' + me.username

        print('Bot started')


    async def stop(self, *args):

        await super().stop()
        print('Bot Stopped Bye')

Bot().run()