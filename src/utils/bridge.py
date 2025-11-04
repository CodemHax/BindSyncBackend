from telegram.constants import ParseMode
TG_TAG = "[TG]"
DC_TAG = "[DC]"
from src.utils.misc import escape_tag_and_username


def istg(text):
    return text.startswith(TG_TAG)

def isdd(text):
    return text.startswith(DC_TAG)

def tgformat(username, text):
    return f"{TG_TAG} {username}: {text}"


def ddformat(display_name, text):
    return f"{DC_TAG} {display_name}: {text}"


def telegram_formatting(text, entities):
    if not entities:
        return text

    sorted_entities = sorted(entities, key=lambda e: e.offset, reverse=True)

    for entity in sorted_entities:
        start = entity.offset
        end = entity.offset + entity.length
        entity_text = text[start:end]

        if entity.type == "bold":
            formatted = f"**{entity_text}**"
        elif entity.type == "italic":
            formatted = f"*{entity_text}*"
        elif entity.type == "code":
            formatted = f"`{entity_text}`"
        elif entity.type == "pre":
            formatted = f"```\n{entity_text}\n```"
        elif entity.type == "strikethrough":
            formatted = f"~~{entity_text}~~"
        elif entity.type == "underline":
            formatted = f"__{entity_text}__"
        elif entity.type == "spoiler":
            formatted = f"||{entity_text}||"
        elif entity.type == "url":
            formatted = entity_text
        elif entity.type == "text_link":
            formatted = f"[{entity_text}]({entity.url})"
        elif entity.type == "text_mention":
            formatted = f"@{entity.user.username if entity.user else entity_text}"
        else:
            formatted = entity_text

        text = text[:start] + formatted + text[end:]

    return text


async def fwd_to_dd(dbot, channel_id, message):
    channel = dbot.get_channel(channel_id)
    if not channel:
        print(f"Discord channel not found: {channel_id}")
        return

    sent = await channel.send(message)
    return getattr(sent, "id", None)



async def fwd_tg(tbot, chat_id, message):
    message = escape_tag_and_username(message)
    await tbot.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.MARKDOWN_V2)


async def fwd_dd_with_reply(dbot, channel_id, message, message_id=None):
    channel = dbot.get_channel(channel_id)
    if not channel:
        print(f"Discord channel not found: {channel_id}")
        return None

    if message_id:
        try:
            ref_msg = await channel.fetch_message(message_id)
            sent = await ref_msg.reply(message)
        except:
            sent = await channel.send(message)
    else:
        sent = await channel.send(message)
    return getattr(sent, "id", None)


async def fwd_to_tg_rply(tbot, chat_id, message, msg_id=None):
    message = escape_tag_and_username(message)
    sent = await tbot.bot.send_message(
        chat_id=chat_id,
        text=message,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_to_message_id=msg_id,
    )
    return getattr(sent, "message_id", None)
