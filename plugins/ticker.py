import asyncio
import datetime
import logging
from pyrogram import Client, types
from pycoingecko import CoinGeckoAPI
from config import CHANNEL_ID, DETAIL_TEMPLATE, OWNER_ID, SLEEP_TIME, INFO_TEMPLATE
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
cg = CoinGeckoAPI()
from os.path import exists


logging.getLogger().setLevel(logging.INFO)

async def BTCTicker(client: Client):
    if file_exists := exists("log.txt"):
        with open("log.txt", "r") as f:
            detail_message_id, info_message_id = f.read().split(",")
            del_msg = await client.get_messages(CHANNEL_ID, [int(detail_message_id), int(info_message_id)])
            for msg in del_msg:
                await msg.delete()

    while 1:
        info_message = ""
        detail_message = ""
        try:
            data = (cg.get_coins_markets(ids="bitcoin", vs_currency="usd"))[0]

            symbol = "🔻" if data['price_change_percentage_24h'].__str__().startswith("-") else "📈"
            market_cap_symbol = "🔻" if data['market_cap_change_percentage_24h'].__str__().startswith("-") else "📈"
            ath_symbol = "🔻" if data['ath_change_percentage'].__str__().startswith("-") else "📈"
            atl_symbol = "🔻" if data['atl_change_percentage'].__str__().startswith("-") else "📈"

            reply_text = DETAIL_TEMPLATE.format(
                market_cap=data["market_cap"],
                market_cap_change_24h=int(data["market_cap_change_24h"]),
                market_cap_change_percentage_24h=data["market_cap_change_percentage_24h"],
                market_cap_symbol=market_cap_symbol,
                market_cap_rank=data["market_cap_rank"],
                fully_diluted_valuation=data["fully_diluted_valuation"],
                total_volume=data["total_volume"],
                ath=data["ath"],
                ath_change_percentage=data["ath_change_percentage"],
                atl=data["atl"],
                atl_change_percentage=data["atl_change_percentage"],
                ath_symbol=ath_symbol,
                atl_symbol=atl_symbol,
                last_updated=f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S%z}',
            )
            detail_message = await client.send_message(CHANNEL_ID, reply_text)

            reply_text = INFO_TEMPLATE.format(
                current_price=data['current_price'],
                price_change_percentage_24h="%.2f" % data['price_change_percentage_24h'],
                symbol=symbol,
                price_change_24h="%.2f" % data["price_change_24h"],
                low_24h=data["low_24h"],
                high_24h=data["high_24h"],
                last_updated=f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S%z}',
            )
            info_message = await client.send_photo(CHANNEL_ID, data['image'] ,reply_text)

            with open("log.txt", "w") as f:
                f.write(f"{detail_message.id},{info_message.id}")
                f.close()

        except MessageNotModified as error:
            pass
        except Exception as e:
            await client.send_message(OWNER_ID, e.with_traceback)
        finally:
            await asyncio.sleep(SLEEP_TIME)
            if info_message and detail_message:
                await info_message.delete()
                await detail_message.delete()