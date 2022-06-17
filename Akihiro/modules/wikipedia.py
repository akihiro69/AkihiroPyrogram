import wikipedia

from pyrogram import filters
from Akihiro import app, CMD_HELP
from config import PREFIX

@app.on_message(filters.command("wiki", PREFIX) & filters.me)
async def wiki(client, message):
    lang = message.command[1]
    user_request = " ".join(message.command[2:])
    await message.edit("**Telusuri info**")
    if user_request == "":
        wikipedia.set_lang("id")
        user_request = " ".join(message.command[1:])
    try:
        if lang == "id":
            wikipedia.set_lang("id")

        result = wikipedia.summary(user_request)
        await message.edit(
            f"""**Kata:**
`{user_request}`
**Info:**
`{result}`"""
        )
    except Exception as exc:
        await message.edit(
            f"""**Request:**
`{user_request}`
**Result:**
`{exc}`"""
        )
        
CMD_HELP.update(
  {
    "wikipedia": f"""
『 **Wikipedia** 』
`{PREFIX}wiki [Kata] -> Mencari kata di wikipedia
"""
  }
)
