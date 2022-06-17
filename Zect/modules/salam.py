import asyncio
from asyncio import sleep
from pyrogram import filters
from config import PREFIX
from Akihiro import CMD_HELP, app

CMD_HELP.update(
    {
        "salam": f"""
『 **salam** 』
  `{PREFIX}pr` -> Assalamualaikum Dulu Biar Sopan.
  `{PREFIX}pe` -> salam.
  `{PREFIX}p` -> salam.
  `{PREFIX}l` -> salam.
  `{PREFIX}j` -> salam.
  `{PREFIX}k` -> salam.
  `{PREFIX}ass` -> salam.
  `{PREFIX}was` -> salam.
  """
    }
)

@app.on_message(filters.command("pr", PREFIX) & filters.me)
async def pr(client, message):
    await message.edit("**Assalamualaikum Dulu Biar Sopan**")


@app.on_message(filters.command("pe", PREFIX) & filters.me)
async def pe(client, message):
    await message.edit("**Assalamualaikum Warahmatullahi Wabarakatuh**")


@app.on_message(filters.command("P", PREFIX) & filters.me)
async def p(client, message):
    owner = message.from_user.first_name
    xx = await message.edit(f"**Haii Salken Saya {owner}**")
    await sleep(2)
    await xx.edit("**Assalamualaikum...**")


@app.on_message(filters.command("l", PREFIX) & filters.me)
async def l(client, message):
    await message.edit("**Wa'alaikumsalam**")

@app.on_message(filters.command("j", PREFIX) & filters.me)
async def j(client, message):
    xx = await message.edit("**JAKA SEMBUNG BAWA GOLOK**")
    await sleep(3)
    await xx.edit("**NIMBRUNG GOBLOKK!!!🔥**")


@app.on_message(filters.command("k", PREFIX) & filters.me)
async def k(client, message):
    owner = message.from_user.first_name
    xx = await message.edit(f"**Hallo KIMAAKK SAYA {owner}**")
    await sleep(2)
    await xx.edit("**LU SEMUA NGENTOT 🔥**")


@app.on_message(filters.command("ass", PREFIX) & filters.me)
async def ass(client, message):
    xx = await message.edit("**Salam Dulu Biar Sopan**")
    await sleep(2)
    await xx.edit("**السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ**")
@app.on_message(filters.command("was", PREFIX) & filters.me)
async def was(client, message):
    xx = await message.edit("**Salam Dulu Biar Sopan**")
    await sleep(2)
    await xx.edit("**وَعَلَيْكُمْ السَّلاَمُ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ**")
