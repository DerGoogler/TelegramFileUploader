#!/usr/bin/env python3

from argparse import ArgumentParser
from os import environ
from telethon import TelegramClient
from telethon.tl.custom import Button
import json

api_id = environ.get("API_ID")
if not api_id:
    print("API_ID is missing")
    exit(1)
api_id = int(api_id)
api_hash = environ.get("API_HASH")
if not api_hash:
    print("API_HASH is missing")
    exit(1)
bot_token = environ.get("BOT_TOKEN")
if not bot_token:
    print("BOT_TOKEN is missing")
    exit(1)

bot = TelegramClient("bot", api_id, api_hash).start(bot_token=bot_token)

async def main(client: TelegramClient, to: str, message: str, files: list[str], buttons: str | None):
    def callback(current, total):
        print(f"Uploaded: {current/total*100}%")

    uploaded_files = []
    if files:
        for file in files:
            print(f"Uploading {file}")
            ufile = await client.upload_file(file, progress_callback=callback)
            print(f"Uploaded {file}")
            uploaded_files.append(ufile)

    keyboard = None
    if buttons:
        try:
            btn_data = json.loads(buttons)
            keyboard = [[Button.url(btn["text"], btn["url"])] for btn in btn_data.get("inline_keyboard", [])]
        except Exception as e:
            print(f"Failed to parse buttons: {e}")

    print(f"Sending message")
    message_list = [None for _ in range(len(uploaded_files) - 1)]
    message_list.append(message)

    await client.send_file(
        entity=to,
        file=uploaded_files or None,
        caption=message_list if uploaded_files else message,
        buttons=keyboard,
        progress_callback=callback if uploaded_files else None,
    )
    print(f"Sent message")

def get_arg_parser():
    parser = ArgumentParser(prog="TelegramFileUploader", epilog="@GitHub:xz-dev")
    parser.add_argument("--to", help="Chat ID or username")
    parser.add_argument("--message", help="Message")
    parser.add_argument("--files", help="Files", nargs="+")
    parser.add_argument("--buttons", help="JSON string for inline buttons")
    return parser

parser = get_arg_parser()
args = parser.parse_args()

with bot:
    bot.loop.run_until_complete(main(bot, args.to, args.message, args.files, args.buttons))
