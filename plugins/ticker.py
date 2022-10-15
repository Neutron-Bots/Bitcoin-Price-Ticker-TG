import asyncio
import datetime
from pyrogram import Client, types
from pycoingecko import CoinGeckoAPI
from config import CHANNEL_ID, DETAIL_MESSAGE_ID, DETAIL_TEMPLATE, MESSAGE_ID, OWNER_ID, SLEEP_TIME, INFO_TEMPLATE
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
cg = CoinGeckoAPI()

async def BTCTicker(client: Client):
    while 1:
        try:
            data = (cg.get_coins_markets(ids="bitcoin", vs_currency="usd"))[0]

            info_message: types.Message = await client.get_messages(chat_id=CHANNEL_ID, message_ids=MESSAGE_ID)
            detail_message: types.Message = await client.get_messages(chat_id=CHANNEL_ID, message_ids=DETAIL_MESSAGE_ID)

            symbol = "🔻" if data['price_change_percentage_24h'].__str__().startswith("-") else "📈"
            market_cap_symbol = "🔻" if data['market_cap_change_percentage_24h'].__str__().startswith("-") else "📈"
            ath_symbol = "🔻" if data['ath_change_percentage'].__str__().startswith("-") else "📈"
            atl_symbol = "🔻" if data['atl_change_percentage'].__str__().startswith("-") else "📈"

            reply_text = INFO_TEMPLATE.format(
                current_price=data['current_price'],
                price_change_percentage_24h="%.2f" % data['price_change_percentage_24h'],
                symbol=symbol,
                price_change_24h="%.2f" % data["price_change_24h"],
                low_24h=data["low_24h"],
                high_24h=data["high_24h"],
                last_updated=f'{datetime.datetime.now():%Y-%m-%d %H:%M:%S%z}',
                detail_message_link=detail_message.link
            )
            await info_message.edit_caption(reply_text)

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
            await detail_message.edit_text(reply_text)

        except MessageNotModified as error:
            pass
        except Exception as e:
            await client.send_message(OWNER_ID, e)
        await asyncio.sleep(SLEEP_TIME)