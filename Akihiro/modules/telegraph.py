import os

from pyrogram import filters
from telegraph import upload_file
from requests import get
from config import PREFIX
from Akihiro import CMD_HELP, app

CMD_HELP.update(
    {
        "telegraph": f"""
『 **Telegraph** 』
  `{PREFIX}tm` atau `{PREFIX}tgm` -> Upload media ke Telegraph.
"""
    }
)

@app.on_message(filters.command(["tm", "tgm"], PREFIX) & filters.me)
async def telegraph(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.edit_text("reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (replied.animation and replied.animation.file_size <= 5242880)
        or (
            replied.video
            and replied.video.file_name.endswith(".mp4")
            and replied.video.file_size <= 5242880
        )
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png", ".gif", ".mp4")
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.edit_text("not supported!")
        return
    download_location = await app.download_media(
        message=message.reply_to_message, file_name="./downloads/"
    )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await app.send_message(message.chat.id, document)
    else:
        await message.edit_text(
            f"**Document passed to: [Telegra.ph](https://telegra.ph{response[0]})**",
        )
    finally:
        os.remove(download_location)

@app.on_message(filters.command("qrd", PREFIX) & filters.me)
async def qrdecode(client, message):
    uh = await message.edit("Prosses membaca barcode")
    replied = message.reply_to_message
    if not replied:
        await message.edit_text("reply to a supported media file")
        return
    if not (
        (replied.photo and replied.photo.file_size <= 5242880)
        or (
            replied.document
            and replied.document.file_name.endswith(
                (".jpg", ".jpeg", ".png")
            )
            and replied.document.file_size <= 5242880
        )
    ):
        await message.edit_text("not supported!")
        return
    download_location = await app.download_media(
        message=message.reply_to_message, file_name="./downloads/"
        )
    try:
        response = upload_file(download_location)
    except Exception as document:
        await app.send_message(message.chat.id, document)
    else:
        ppk = f"https://telegra.ph{response[0]}"
        tai = get(f"http://api.qrserver.com/v1/read-qr-code/?fileurl={ppk}").json()
        memek = (tai[0]["symbol"][0]["data"])
        await uh.edit(memek)
    finally:
        os.remove(download_location)
