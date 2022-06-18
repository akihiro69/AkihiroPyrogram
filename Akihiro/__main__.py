# Copyright (C) 2020-2021 by okay-retard@Github, < https://github.com/okay-retard >.
#
# This file is part of < https://github.com/okay-retard/ZectUserBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/okay-retard/ZectUserBot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram import Client
from pyrogram import idle
from config import LOG_CHAT, PREFIX
from Akihiro import app, LOGGER
from pyrogram.errors import BadRequest
import logging
from Akihiro.modules import *

app.start()
me = app.get_me()
print(f"Akihiro UserBot started for user {me.id}. Type {PREFIX}help in any telegram chat.")
try:
    app.send_message(
        LOG_CHAT,
        f"✨ **AKIHIRO-USERBOT is Activated Successfully.** ✨\n",
    )
    app.join_chat("akihirosupport")
    app.join_chat("akihiroupdate")
    idle()
except BadRequest:
    pass
