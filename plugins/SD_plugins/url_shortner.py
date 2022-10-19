#!/usr/bin/env python3
import os
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.handlers import MessageHandler
from pyshorteners import Shortener

SHORTURLLINK_API = os.environ.get("SHORTURLLINK_API", "6acb58912cdc0c550d65653ddd83fa1462ad643d")

reply_markup = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text='join channel', url='https://t.me/NKBACKUPCHANNEL')
        ]]
    )

@Client.on_message(filters.command(["short"]) & filters.regex(r'https?://[^\s]+'))
async def reply_shortens(bot, update):
    message = await update.reply_text(
        text="`Analysing your link...`",
        disable_web_page_preview=False,
        quote=False 
    )
    link = update.matches[0].group(0)
    shorten_urls = await short(link)
    await message.edit_text(
        text=shorten_urls,
        reply_markup=reply_markup,
        disable_web_page_preview=False 
    )

@Client.on_inline_query(filters.regex(r'https?://[^\s]+'))
async def inline_short(bot, update):
    link = update.matches[0].group(0),
    shorten_urls = await short(link)
    answers = [
        InlineQueryResultArticle(
            title="Short Links",
            description=update.query,
            input_message_content=InputTextMessageContent(
                message_text=shorten_urls,
                disable_web_page_preview=False 
            ),
            reply_markup=reply_markup
        )
    ]
    await bot.answer_inline_query(
        inline_query_id=update.id,
        results=answers
    )

async def short(link):
    shorten_urls = "**--Shorted URLs--**\n"
    
    # SHORTURLLINK shorten
    if SHORTURLLINK_API:
        try:
            s = Shortener(api_key=SHORTURLLINK_API)
            url = s.SHORTURLLINK.short(link)
            shorten_urls += f"\n**SHORTURLLINK :-** {url}"
        except Exception as error:
            print(f"SHORTURLLINK error :- {error}")
    # Send the text
    try:
        shorten_urls += "\n\nThere are shortened links of various providers.🔥"
        return shorten_urls
    except Exception as error:
        return error
