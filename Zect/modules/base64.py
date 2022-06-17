from pyrogram import filters
from Akihiro import CMD_HELP, app
from config import PREFIX
from Akihiro.helpers.pyrohelper import get_arg
import base64

CMD_HELP.update(
    {
        "base64": f"""
『 **Base64** 』
  `{PREFIX}en` -> Mengkodekan textbase64.
  `{PREFIX}de` - > Membuka kode text base64.
"""
    }
)


@app.on_message(filters.command("en", PREFIX) & filters.me)
async def encode(client, message):
    ppk = get_arg(message)
    chat = message.chat.id
    if not ppk:
        return await message.edit_text("`Give me Something to Encode..`")
    byt = ppk.encode("ascii")
    et = base64.b64encode(byt)
    atc = et.decode("ascii")
    await message.edit_text(
        f"**=>> Encoded Text :** `{ppk}`\n\n**=>> OUTPUT :**\n`{atc}`"
    )


@app.on_message(filters.command("de", PREFIX) & filters.me)
async def decode(client, message):
    ppk = get_arg(message)
    chat = message.chat.id
    if not ppk:
        return await message.edit_text("`Give me Something to Decode..`")
    byt = ppk.encode("ascii")
    try:
        et = base64.b64decode(byt)
        atc = et.decode("ascii")
        await message.edit_text(
            f"**=>> Decoded Text :** `{ppk}`\n\n**=>> OUTPUT :**\n`{atc}`"
        )
    except Exception as p:
        await message.edit_text("**ERROR :** " + str(p))
