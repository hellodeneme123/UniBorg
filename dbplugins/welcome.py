"""Greetings
Commands:
.clearwelcome
.savewelcome <Welcome Message>"""

import logging

from telethon import events

from sample_config import Config
from sql_helpers.welcome_sql import (add_welcome_setting,
                                     get_current_welcome_settings,
                                     rm_welcome_setting,
                                     update_previous_welcome)
from uniborg.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

@borg.on(events.ChatAction())   
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined or event.user_added:
            if cws.should_clean_welcome:
                try:
                    await event.client.delete_messages(
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))   
            a_user = await event.get_user()
            msg_o = await event.client.get_messages(
                entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
                ids=int(cws.f_mesg_id)
            )
            current_saved_welcome_message = msg_o.message
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            file_media = msg_o.media
            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention),
                file=file_media
            )
            update_previous_welcome(event.chat_id, current_message.id)


@borg.on(admin_cmd(pattern="savewelcome"))   
async def _(event):
    if event.fwd_from:
        return
    msg = await event.get_reply_message()
    if msg:
        msg_o = await event.client.forward_messages(
            entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
            messages=msg,
            from_peer=event.chat_id,
            silent=True
        )
        add_welcome_setting(event.chat_id, True, 0, msg_o.id)
        await event.edit("Welcome note saved. ")


@borg.on(admin_cmd(pattern="clearwelcome"))   
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit(
        "Welcome note cleared. " + \
        "[This](https://t.me/c/{}/{}) was your previous welcome message.".format(
            str(Config.PRIVATE_CHANNEL_BOT_API_ID)[4:],
            cws.f_mesg_id
        )
    )
