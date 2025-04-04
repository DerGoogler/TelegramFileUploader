#!/usr/bin/env python3

import os
import subprocess
import sys
import json
from argparse import ArgumentParser

def process_files_arg(files):
    processed_files = []
    for file_arg in files:
        processed_files.extend(
            [arg.lstrip() for arg in file_arg.splitlines() if arg.strip()]
        )
    return processed_files

def process_buttons_arg(buttons):
    if not buttons:
        return None
    inline_keyboard = []
    for button in buttons:
        if "|" in button:
            text, url = button.split("|", 1)
            inline_keyboard.append({"text": text.strip(), "url": url.strip()})
    return json.dumps({"inline_keyboard": [[btn] for btn in inline_keyboard]})

parser = ArgumentParser(prog="TelegramFileUploader", epilog="@GitHub:xz-dev")
parser.add_argument("--to", help="Chat ID or username")
parser.add_argument("--message", help="Message")
parser.add_argument("--files", help="Files", nargs="+")
parser.add_argument("--buttons", help="Inline buttons in 'Text|URL' format", nargs="*")
args = parser.parse_args()

if args.files:
    args.files = process_files_arg(args.files)

def build_command_args():
    cmd_args = []
    if args.to:
        cmd_args.extend(["--to", args.to])
    if args.message:
        cmd_args.extend(["--message", args.message])
    if args.files:
        cmd_args.append("--files")
        for file_path in args.files:
            cmd_args.append(file_path)
    if args.buttons:
        keyboard_json = process_buttons_arg(args.buttons)
        if keyboard_json:
            cmd_args.extend(["--buttons", keyboard_json])
    return cmd_args

current_script_dir = os.path.dirname(os.path.abspath(__file__))
main_py_path = os.path.join(current_script_dir, "main.py")
new_command_args = build_command_args()

print(f"exec: python3 {main_py_path} {' '.join(new_command_args)}")
result = subprocess.run(["python3", main_py_path] + new_command_args)
sys.exit(result.returncode)
