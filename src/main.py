# coding=utf-8

import os
os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'linrol'

import asyncio
from server import puppetware_start_server

from wechaty import (
    Contact,
    FileBox,
    Message,
    Wechaty,
    ScanStatus,
)

async def on_scan(
    qrcode: str,
    status: ScanStatus,
    _data,
):
    """
    Scan Handler for the Bot
    """
    print('Status: ' + str(status))
    print('View QR Code Online: https://wechaty.js.org/qrcode/' + qrcode)



async def main():
    """
    Async Main Entry
    """

    bot = Wechaty()

    bot.on('scan',      on_scan)

    # await bot.start()

    await asyncio.gather(
        puppetware_start_server(bot),
        bot.start()
    )

    print('[Python Wechaty] Ding Dong Bot started.')


asyncio.run(main())
