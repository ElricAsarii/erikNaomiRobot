# ©AKBOTZ

import re
import aiohttp

from os import environ
from pyrogram import Client, filters
from pyrogram.types import *
from Naomi import pbot as akbotz

API_KEY = environ.get('API_KEY')
API_URL = environ.get('API_URL')


@akbotz.on_message(filters.command('lshelp') & filters.private)
async def start(bot, message):
    await message.reply(
        "Link Shortener Module for https://atglinks.com.\n\n**Developer:** @cant_think_1")


@akbotz.on_message(filters.private & filters.text & filters.incoming)
async def link_handler(bot, message):
    link_pattern = re.compile('https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}', re.DOTALL)
    links = re.findall(link_pattern, message.text)
    if len(links) <1:
        await message.reply("No links Found in this text",quote=True)
        return
    for link in links:
        try:
            short_link = await get_shortlink(link)
            await message.reply(f"𝐇𝐞𝐫𝐞 𝐢𝐬 𝐘𝐨𝐮𝐫 𝐒𝐡𝐨𝐫𝐭𝐞𝐧𝐞𝐝 𝐋𝐢𝐧𝐤\n\n𝐎𝐫𝐢𝐠𝐢𝐧𝐚𝐥 𝐋𝐢𝐧𝐤: {link}\n\n𝐒𝐡𝐨𝐫𝐭𝐞𝐧𝐞𝐝 𝐋𝐢𝐧𝐤: `{short_link}`",quote=True,disable_web_page_preview=True)
        except Exception as e:
            await message.reply(f'𝐄𝐫𝐫𝐨𝐫: `{e}`', quote=True)


async def get_shortlink(link):
    url = API_URL
    params = {'api': API_KEY, 'url': link}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            data = await response.json()
            return data["shortenedUrl"]
