import asyncio
import re
from config import bot_token, owner_id, bot_id, ARQ_API_BASE_URL as ARQ_API
from pyrogram import Client, filters
from Python_ARQ import ARQ

luna = Client(
    ":memory:",
    bot_token=1582636407:AAGuKzkSdzblLiJKqfPbJ9tFeGQKPi7h_PM,
    api_id=2443183,
    api_hash="66b6799e1b784aff78bad680cd8362db",
)

arq = ARQ(ARQ_API)

blacklisted = []
mode = None


async def getresp(query):
    luna = await arq.luna(query)
    response = luna.response
    return response


@luna.on_message(filters.command("repo") & ~filters.edited)
async def repo(_, message):
    await message.reply_text(
        "[Github](https://github.com/thehamkercat/LunaChatBot)"
        + " | [Group](t.me/PatheticProgrammers)", disable_web_page_preview=True)


@luna.on_message(filters.command("help") & ~filters.edited)
async def start(_, message):
    user_id = message.from_user.id
    if user_id in blacklisted:
        return
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text(
        "**Only For Owners**\n/shutdown - `Shutdown Luna.`\n/blacklist - `Blacklist A User.`\n/whitelist - `Whitelist A User.`"
    )


@luna.on_message(filters.command("shutdown") & filters.user(owner_id) & ~filters.edited)
async def shutdown(_, message):
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text("**Shutted Down!**")
    print("Exited!")
    exit()


@luna.on_message(filters.command("blacklist") & filters.user(owner_id) & ~filters.edited)
async def blacklist(_, message):
    global blacklisted
    if not message.reply_to_message:
        await luna.send_chat_action(message.chat.id, "typing")
        await message.reply_text("Reply To A User's Message To Blacklist.")
        return
    victim = message.reply_to_message.from_user.id
    if victim in blacklisted:
        await luna.send_chat_action(message.chat.id, "typing")
        await message.reply_text("Already Blacklisted Lol.")
        return
    blacklisted.append(victim)
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text("Blacklisted.")


@luna.on_message(filters.command("whitelist") & filters.user(owner_id) & ~filters.edited)
async def whitelist(_, message):
    global blacklisted
    if not message.reply_to_message:
        await luna.send_chat_action(message.chat.id, "typing")
        await message.reply_text("Reply To A User's Message To Whitelist.")
        return
    victim = message.reply_to_message.from_user.id
    if victim not in blacklisted:
        await luna.send_chat_action(message.chat.id, "typing")
        await message.reply_text("Already Whitelisted Lol.")
        return
    blacklisted.remove(victim)
    await luna.send_chat_action(message.chat.id, "typing")
    await message.reply_text("Whitelisted.")


@luna.on_message(
    ~filters.private &
    ~filters.command("blacklist")
    & ~filters.command("shutdown")
    & ~filters.command("help")
    & ~filters.edited
)
async def chat(_, message):
    if message.from_user.id in blacklisted:
        return
    if message.reply_to_message:
        if not message.reply_to_message.from_user.id == bot_id:
            return
        await luna.send_chat_action(message.chat.id, "typing")
        if not message.text:
            query = "Hello"
        else:
            query = message.text
        if len(query) > 50:
            return
        try:
            res = await getresp(query)
            await asyncio.sleep(1)
        except Exception as e:
            res = str(e)
        await message.reply_text(res)
        await luna.send_chat_action(message.chat.id, "cancel")
    else:
        if message.text:
            query = message.text
            if len(query) > 50:
                return
            if re.search("[.|\n]{0,}[l|L][u|U][n|N][a|A][.|\n]{0,}", query):
                await luna.send_chat_action(message.chat.id, "typing")
                try:
                    res = await getresp(query)
                    await asyncio.sleep(1)
                except Exception as e:
                    res = str(e)
                await message.reply_text(res)
                await luna.send_chat_action(message.chat.id, "cancel")


@luna.on_message(
    filters.private
    & ~filters.command("blacklist")
    & ~filters.command("shutdown")
    & ~filters.command("help")
    & ~filters.edited
)
async def chatpm(_, message):
    if message.from_user.id in blacklisted:
        return
    if not message.text:
        return
    await luna.send_chat_action(message.chat.id, "typing")
    query = message.text
    if len(query) > 50:
        return
    try:
        res = await getresp(query)
        await asyncio.sleep(1)
    except Exception as e:
        res = str(e)
    await message.reply_text(res)
    await luna.send_chat_action(message.chat.id, "cancel")


print(
    """
-----------------
| Luna Started! |
-----------------

"""
)


luna.run()
