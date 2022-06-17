# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from google_trans_new import google_translator
from pyrogram import filters
from inspect import getfullargspec
from pyrogram.types import Message
from Akihiro import app
from config import PREFIX

trl = google_translator()


async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_message(filters.command("tr", PREFIX) & filters.me)
async def translate(_client, message):
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await edrep(message, text="Usage: Reply to a message, then `tr <lang>`")
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, lang_tgt=target)
        except ValueError as err:
            await edrep(message, text=f"Error: `{str(err)}`")
            return
    else:
        if len(message.text.split()) <= 2:
            await edrep(message, text="Usage: `tr <lang> <text>`")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, lang_tgt=target)
        except ValueError as err:
            await edrep(message, text="Error: `{}`".format(str(err)))
            return

    await edrep(
        message,
        text=f"Translated from `{detectlang[0]}` to `{target}`:\n```{tekstr}```",
    )
