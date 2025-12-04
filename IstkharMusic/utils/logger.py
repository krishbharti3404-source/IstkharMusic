from pyrogram import enums
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    User
)
from pyrogram.enums import ParseMode, ChatMemberStatus, ChatMembersFilter

from IstkharMusic import app
from IstkharMusic.utils.database import is_on_off
from config import LOGGER_ID as LOG_GROUP_ID

import asyncio

async def play_logs(message: Message, streamtype: str):
    """
    Logs play actions to the log group if logging is enabled.
    """

    # Check if logging (mode 2) is enabled via DB
    if not await is_on_off(2):
        return

    try:
        # Total chat members
        chat_members = await app.get_chat_members_count(message.chat.id)

        # Find the group owner
        owner_name = "Hidden / Deleted"
        owner_id = "Hidden / Deleted"

        async for admin in app.get_chat_members(
            message.chat.id,
            filter=ChatMembersFilter.ADMINISTRATORS
        ):
            if admin.status == ChatMemberStatus.OWNER:
                if admin.user:
                    owner_name = getattr(admin.user, "mention", owner_name)
                    owner_id = getattr(admin.user, "id", owner_id)

    except Exception:
        chat_members = "N/A"

    # Extract searched query
    try:
        query = message.text.split(None, 1)[1]
    except:
        query = "Unknown"

    # Build log text
    logger_text = f"""
<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>
╔════❰𝐏𝐋𝐀𝐘𝐈𝐍𝐆❱═══❍⊱❁۪۪
<b>◈ 𝐂𝐡𝐚𝐭 ➪ </b> {message.chat.title}
<b>◈ 𝐂𝐡𝐚𝐭 𝐈𝐝 ➪ </b> <code>{message.chat.id}</code>
<b>◈ 𝐔𝐬𝐞𝐫 ➪ </b> {message.from_user.mention}
<b>◈ 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 ➪ </b> @{message.from_user.username}
<b>◈ 𝐈𝐝 ➪ </b> <code>{message.from_user.id}</code>
<b>◈ 𝐂𝐡𝐚𝐭 𝐋𝐢𝐧𝐤 ➪ </b> @{message.chat.username}
<b>◈ 𝐂𝗵𝗮𝘁 𝗠𝗲𝗺𝗯𝗲𝗿𝘀 ➪ </b> <code>{chat_members}</code>
<b>◈ 𝐒𝐞𝐚𝐫𝐜𝐡𝐞𝐝 ➪ </b> <code>{query}</code>
<b>◈ 𝐁𝐲 ➪ </b> {streamtype}
╚═══❰ #𝐍𝐞𝐰𝐒𝐨𝐧𝐠 ❱══❍⊱❁۪۪
"""

    # Send to log group if not same chat
    if message.chat.id != LOG_GROUP_ID:
        try:
            await app.send_message(
                chat_id=LOG_GROUP_ID,
                text=logger_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception:
            pass

    return
