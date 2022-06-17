# Copyright (C) 2020-2021 by Toni880@Github, < https://github.com/Toni880 >.
#
# This file is part of < https://github.com/Toni880/Prime-Userbot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/Toni880/Prime-Userbot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
import os
import re
from asyncio import gather
from base64 import b64decode
from io import BytesIO

import aiofiles
import aiohttp
import requests
from pyrogram import filters
from pyrogram.types import Message

from config import PREFIX
from Akihiro import CMD_HELP, app

CMD_HELP.update(
    {
        "misc": f"""
『 **Misc** 』
  `{PREFIX}paste` -> Tempelkan konten yang dibalas ke pastebin.
  `{PREFIX}neko` -> Tempelkan konten yang dibalas ke Nekobin
  `{PREFIX}pasty` -> Tempelkan konten yang dibalas ke pasty
  `{PREFIX}ss` -> Screenshot web.
  `{PREFIX}whois` [user handle] -> Memberikan informasi tentang user.
  `{PREFIX}id` [user handle] -> Menampilkan user id atau chat id.
"""
    }
)

BASE = "https://batbin.me/"


async def post(url: str, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception:
                data = await resp.text()
        return data


async def Primebin(content: str):
    resp = await post(f"{BASE}api/v2/paste", data=content)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link


pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


async def take_screenshot(url: str, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    payload = {
        "url": url,
        "width": 1920,
        "height": 1080,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True
    data = await post(
        "https://webscreenshot.vercel.app/api",
        data=payload,
    )
    if "image" not in data:
        return None
    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(b64decode(b))
    file.name = "webss.jpg"
    return file


@app.on_message(filters.command(["pasty"], PREFIX) & filters.me)
async def paste(_, message: Message):
    text = message.reply_to_message.text
    try:
        params = {"content": text}
        headers = {"content-type": "application/json"}
        url = "https://pasty.lus.pm/api/v2/pastes/"
        paste = requests.post(url, json=params, headers=headers)
        key = paste.json()["id"]
    except Exception:
        await message.edit_text("`API is down try again later`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f"https://pasty.lus.pm/{key}"
        reply_text = f"**Pasted to: [Pasty]({url})\nRaw link: [Raw]({url}/raw)**"
        delete = (
            True
            if len(message.command) > 1
            and message.command[1] in ["d", "del"]
            and message.reply_to_message.from_user.is_self
            else False
        )
        if delete:
            await asyncio.gather(
                app.send_message(
                    message.chat.id, reply_text, disable_web_page_preview=True
                ),
                message.reply_to_message.delete(),
                message.delete(),
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )


@app.on_message(filters.command("neko", PREFIX) & filters.me)
async def neko(_, message: Message):
    text = message.reply_to_message.text
    try:
        params = {"content": text}
        headers = {"content-type": "application/json"}
        url = "https://nekobin.com/api/documents"
        neko = requests.post(url, json=params, headers=headers)
        key = neko.json()["result"]["key"]
    except Exception:
        await message.edit_text("`API is down try again later`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f"https://nekobin.com/{key}"
        reply_text = f"**Pasted to: [Nekobin]({url})**"
        delete = (
            True
            if len(message.command) > 1
            and message.command[1] in ["d", "del"]
            and message.reply_to_message.from_user.is_self
            else False
        )
        if delete:
            await asyncio.gather(
                app.send_message(
                    message.chat.id, reply_text, disable_web_page_preview=True
                ),
                message.reply_to_message.delete(),
                message.delete(),
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )


@app.on_message(filters.command("paste", PREFIX) & filters.me)
async def patebin(client, message):
    if not message.reply_to_message:
        return await message.edit_text(f"Reply To A Message With {PREFIX}paste")
    r = message.reply_to_message
    if not r.text and not r.document:
        return await message.edit_text("Hanya untuk text dan documents.")
    m = await message.edit_text("Pasting...")
    if r.text:
        content = str(r.text)
    elif r.document:
        if r.document.file_size > 40000:
            return await m.edit_text("Anda hanya dapat paste file yang lebih kecil dari 40KB.")
        if not pattern.search(r.document.mime_type):
            return await m.edit_text("Hanya untuk text dan documents.")
        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            content = await f.read()

        os.remove(doc)

    link = await Primebin(content)
    try:
        await message.reply_photo(
            photo=link,
            quote=False,
            caption=f"**Paste Link:** [Here]({link})",
        )
        await m.delete()
    except Exception:
        await m.edit_text("Here's your paste")


@app.on_message(filters.command("ss", PREFIX) & filters.me)
async def screenshot(client, message):
    if len(message.command) < 2:
        return await message.edit_text("Tolong masukan url")
    if len(message.command) == 2:
        url = message.text.split(None, 1)[1]
        full = False
    elif len(message.command) == 3:
        url = message.text.split(None, 2)[1]
        full = message.text.split(None, 2)[2].lower().strip() in [
            "yes",
            "y",
            "1",
            "true",
        ]
    else:
        return await message.edit_text("Invalid Command.")
    m = await message.edit_text("Mengambil tangkapan layar...")
    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("Gagal Mengambil Tangkapan Layar")
        m = await m.edit("Mengunggah...")
        if not full:
            await gather(*[message.reply_document(photo), message.reply_photo(photo)])
        else:
            await message.reply_document(photo)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))
