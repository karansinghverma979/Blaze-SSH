#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📋 Blaze Unified Clipboard Bridge & Synchronization Hub
Author: Antigravity Assistant & Karan Singh Verma
Project: Blaze (Motobook ⇄ Lava Blaze 5G Node)
Dual Mode: Fast-Path CLI switches & Rich Interactive Terminal Menu
"""

import sys
import os
import json
import subprocess
import argparse

# UTF-8 Console Safety
if sys.platform == "win32":
    os.system("")
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# ANSI Color Palette
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def run_ssh(cmd, timeout=5):
    """Executes command on Blaze over SSH with safe timeout."""
    try:
        res = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "StrictHostKeyChecking=no", "blaze", cmd],
            capture_output=True, text=True, timeout=timeout + 2, encoding="utf-8", errors="replace"
        )
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "", "Connection timed out.", 255
    except Exception as e:
        return "", str(e), 1

def get_pc_clipboard():
    """Gets Windows clipboard content."""
    try:
        res = subprocess.run(["powershell", "-Command", "Get-Clipboard"], capture_output=True, text=True, encoding="utf-8")
        return res.stdout.rstrip("\r\n")
    except Exception:
        return ""

def set_pc_clipboard(text):
    """Sets Windows clipboard content."""
    try:
        subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value @'\n{text}\n'@"], check=True)
        return True
    except Exception:
        return False

def get_phone_clipboard():
    """Gets phone clipboard content over SSH."""
    out, err, code = run_ssh("termux-clipboard-get")
    return out if code == 0 else ""

def set_phone_clipboard(text):
    """Sets phone clipboard content over SSH."""
    safe_text = text.replace("'", "'\\''")
    out, err, code = run_ssh(f"termux-clipboard-set '{safe_text}' && termux-toast '📋 Copied from Motobook'")
    return code == 0

# --- Fast Actions ---

def pull_clipboard(json_mode=False, raw_mode=False):
    """Pulls phone clipboard to PC."""
    phone_text = get_phone_clipboard()
    if phone_text:
        set_pc_clipboard(phone_text)
        if json_mode:
            print(json.dumps({"status": "success", "content": phone_text, "source": "phone", "target": "pc"}))
        elif raw_mode:
            print(phone_text)
        else:
            print(f"\n{GREEN}{BOLD}✅ PULLED FROM BLAZE ➔ PC CLIPBOARD{RESET}")
            print(f"┌────────────────────────────────────────────────────────┐")
            preview = phone_text[:120] + ("..." if len(phone_text) > 120 else "")
            print(f"│ {CYAN}{preview}{RESET}")
            print(f"└────────────────────────────────────────────────────────┘")
            print(f"{DIM}📋 Ready to paste (Ctrl+V) on Motobook.{RESET}\n")
    else:
        if json_mode:
            print(json.dumps({"status": "empty", "error": "Phone clipboard empty or unreachable"}))
        elif not raw_mode:
            print(f"{YELLOW}⚠️ Phone clipboard is empty or unreachable.{RESET}")

def push_clipboard(custom_text=None, json_mode=False):
    """Pushes PC clipboard (or custom text) to phone."""
    text_to_push = custom_text if custom_text is not None else get_pc_clipboard()
    if not text_to_push:
        if json_mode:
            print(json.dumps({"status": "error", "error": "Clipboard/text is empty"}))
        else:
            print(f"{YELLOW}⚠️ Nothing to push (clipboard is empty).{RESET}")
        return

    success = set_phone_clipboard(text_to_push)
    if success:
        if json_mode:
            print(json.dumps({"status": "success", "content": text_to_push, "source": "pc", "target": "phone"}))
        else:
            print(f"\n{GREEN}{BOLD}✅ PUSHED TO BLAZE CLIPBOARD ➔ PHONE{RESET}")
            print(f"┌────────────────────────────────────────────────────────┐")
            preview = text_to_push[:120] + ("..." if len(text_to_push) > 120 else "")
            print(f"│ {CYAN}{preview}{RESET}")
            print(f"└────────────────────────────────────────────────────────┘")
            print(f"{DIM}📱 Phone received toast and clipboard updated.{RESET}\n")
    else:
        if json_mode:
            print(json.dumps({"status": "error", "error": "Failed to set clipboard on phone"}))
        else:
            print(f"{RED}❌ Failed to push clipboard to phone.{RESET}")

def sync_clipboards():
    """Shows side-by-side visual diff and offers sync choice."""
    pc_text = get_pc_clipboard()
    phone_text = get_phone_clipboard()

    print(f"\n{BOLD}{CYAN}📋 SIDE-BY-SIDE CLIPBOARD RADAR{RESET}")
    print("┌────────────────────────────┬────────────────────────────┐")
    print(f"│ {BOLD}💻 MOTOBOOK (PC){RESET}           │ {BOLD}📱 BLAZE (Phone){RESET}           │")
    print("├────────────────────────────┼────────────────────────────┤")
    pc_p = (pc_text[:24] + "..") if len(pc_text) > 26 else pc_text.ljust(26)
    ph_p = (phone_text[:24] + "..") if len(phone_text) > 26 else phone_text.ljust(26)
    print(f"│ {pc_p} │ {ph_p} │")
    print("└────────────────────────────┴────────────────────────────┘")

    print(f"\n{BOLD}Sync Action:{RESET}")
    print(f"  {CYAN}1{RESET} ➔ Push PC to Phone  (PC ➔ Phone)")
    print(f"  {CYAN}2{RESET} ➔ Pull Phone to PC  (Phone ➔ PC)")
    print(f"  {CYAN}0{RESET} ➔ Cancel")

    try:
        ch = input(f"{BOLD}Sync ❯ {RESET}").strip()
        if ch == "1":
            push_clipboard(pc_text)
        elif ch == "2":
            pull_clipboard()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Cancelled.{RESET}")

# --- Interactive Menu ---

def interactive_menu():
    """Interactive terminal menu."""
    while True:
        print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│         📋 BLAZE UNIFIED CLIPBOARD COMMAND HUB         │
├────────────────────────────────────────────────────────┤
│  {BOLD}1{RESET} 📥 Pull Phone Clipboard ➔ PC Clipboard              │
│  {BOLD}2{RESET} 📤 Push PC Clipboard ➔ Phone Clipboard              │
│  {BOLD}3{RESET} 🔄 Side-by-Side Visual Diff & Bidirectional Sync    │
│  {BOLD}4{RESET} ✍️ Send Custom Text Straight to Phone Clipboard     │
│  {BOLD}0{RESET} 🚪 Exit                                             │
└────────────────────────────────────────────────────────┘{RESET}""")
        try:
            choice = input(f"{BOLD}Blaze-Clip ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            pull_clipboard()
        elif choice == "2":
            push_clipboard()
        elif choice == "3":
            sync_clipboards()
        elif choice == "4":
            text = input("Enter text to send to phone: ").strip()
            if text:
                push_clipboard(custom_text=text)
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Select 0-4.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Unified Clipboard Bridge & Synchronization Hub",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--pull", action="store_true", help="Pull phone clipboard to PC")
    parser.add_argument("--push", action="store_true", help="Push PC clipboard to phone")
    parser.add_argument("--sync", action="store_true", help="Side-by-side diff and sync")
    parser.add_argument("--send", metavar="TEXT", help="Send custom text to phone clipboard")
    parser.add_argument("--get", action="store_true", help="Fetch phone clipboard and print to stdout")
    parser.add_argument("--raw", action="store_true", help="Raw output mode")
    parser.add_argument("--json", action="store_true", help="JSON output mode")
    parser.add_argument("text", nargs="?", help="Direct text to push to phone clipboard")

    args = parser.parse_args()

    if args.pull or args.get:
        pull_clipboard(json_mode=args.json, raw_mode=args.raw)
    elif args.push:
        push_clipboard(json_mode=args.json)
    elif args.send:
        push_clipboard(custom_text=args.send, json_mode=args.json)
    elif args.text:
        push_clipboard(custom_text=args.text, json_mode=args.json)
    elif args.sync:
        sync_clipboards()
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
