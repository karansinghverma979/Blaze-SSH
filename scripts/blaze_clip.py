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
import shutil
import re

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

def render_unreachable_card():
    """Renders standardized offline diagnostic card when Blaze SSH is unreachable."""
    print(f"\n{RED}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{RED}│ ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022                 │{RESET}")
    print(f"{RED}├────────────────────────────────────────────────────────┤{RESET}")
    print(f"│ • Root Cause: Phone offline or SSH daemon not running. │")
    print(f"│ • Action:     1. Ensure Termux is active on Blaze.     │")
    print(f"│               2. Run 'sshd' in Termux.                 │")
    print(f"│               3. Confirm same Wi-Fi / Hotspot.         │")
    print(f"{RED}└────────────────────────────────────────────────────────┘{RESET}\n")

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

def run_fzf(options, prompt="Blaze Clip > ", header=None):
    """Runs inline interactive FZF fuzzy picker directly beneath the cursor."""
    if not shutil.which("fzf") or not options:
        return None
    cmd = ["fzf", "--prompt", prompt, "--height=40%", "--reverse", "--cycle"]
    if header:
        cmd.extend(["--header", header])
    input_str = "\n".join(options)
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            encoding="utf-8"
        )
        stdout, _ = proc.communicate(input=input_str)
        if proc.returncode == 0 and stdout and stdout.strip():
            return stdout.strip()
    except (KeyboardInterrupt, Exception):
        pass
    return None

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
    """Gets phone clipboard content over SSH using Termux API v2 protocol."""
    cmd = "/data/data/com.termux/files/usr/libexec/termux-api Clipboard -e api_version 2 --ez set false"
    out, err, code = run_ssh(cmd)
    if code != 0 or not out:
        # Fallback to standard termux-clipboard-get
        out, err, code = run_ssh("termux-clipboard-get")
    return out if code == 0 else ""

def set_phone_clipboard(text):
    """Sets phone clipboard content over SSH with safe payload piping."""
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
            print("┌────────────────────────────────────────────────────────┐")
            lines = phone_text.splitlines()
            if not lines:
                lines = [phone_text]
            for line in lines[:8]:
                clean_l = line.replace('\t', '    ')
                print(f"│ {CYAN}{clean_l[:52]:<52}{RESET} │")
            if len(lines) > 8 or len(phone_text) > 300:
                print(f"│ {DIM}... ({len(phone_text)} total characters){'':<27}{RESET} │")
            print("└────────────────────────────────────────────────────────┘")
            print(f"{DIM}📋 Ready to paste (Ctrl+V) on Motobook.{RESET}\n")
    else:
        if json_mode:
            print(json.dumps({"status": "empty", "error": "Phone clipboard empty or unreachable"}))
        elif not raw_mode:
            print(f"\n{YELLOW}⚠️ Phone clipboard is empty or Android clipboard service is idle.{RESET}")
            print(f"{DIM}💡 Copy any text on Blaze screen first, then run pull again.{RESET}\n")

def push_clipboard(custom_text=None, json_mode=False):
    """Pushes PC clipboard (or custom text) to phone."""
    text_to_push = custom_text if custom_text is not None else get_pc_clipboard()
    if not text_to_push:
        if json_mode:
            print(json.dumps({"status": "error", "error": "Clipboard/text is empty"}))
        else:
            print(f"{YELLOW}⚠️ Nothing to push (Windows clipboard is empty).{RESET}\n")
        return

    success = set_phone_clipboard(text_to_push)
    if success:
        if json_mode:
            print(json.dumps({"status": "success", "content": text_to_push, "source": "pc", "target": "phone"}))
        else:
            print(f"\n{GREEN}{BOLD}✅ PUSHED TO BLAZE CLIPBOARD ➔ PHONE{RESET}")
            print("┌────────────────────────────────────────────────────────┐")
            lines = text_to_push.splitlines()
            if not lines:
                lines = [text_to_push]
            for line in lines[:8]:
                clean_l = line.replace('\t', '    ')
                print(f"│ {CYAN}{clean_l[:52]:<52}{RESET} │")
            if len(lines) > 8 or len(text_to_push) > 300:
                print(f"│ {DIM}... ({len(text_to_push)} total characters){'':<27}{RESET} │")
            print("└────────────────────────────────────────────────────────┘")
            print(f"{DIM}📱 Phone received toast and clipboard updated.{RESET}\n")
    else:
        if json_mode:
            print(json.dumps({"status": "error", "error": "Failed to set clipboard on phone"}))
        else:
            print(f"{RED}❌ Failed to push clipboard to phone.{RESET}\n")

def sync_clipboards():
    """Shows side-by-side visual diff and offers sync choice in FZF."""
    pc_text = get_pc_clipboard()
    phone_text = get_phone_clipboard()

    print(f"\n{BOLD}{CYAN}📋 SIDE-BY-SIDE CLIPBOARD RADAR{RESET}")
    print("┌────────────────────────────┬────────────────────────────┐")
    print(f"│ {BOLD}💻 MOTOBOOK (PC){RESET}           │ {BOLD}📱 BLAZE (Phone){RESET}           │")
    print("├────────────────────────────┼────────────────────────────┤")
    pc_p = (pc_text[:24] + "..") if len(pc_text) > 26 else pc_text.ljust(26)
    ph_p = (phone_text[:24] + "..") if len(phone_text) > 26 else (phone_text if phone_text else "[Empty]").ljust(26)
    print(f"│ {pc_p} │ {ph_p} │")
    print("└────────────────────────────┴────────────────────────────┘\n")

    actions = [
        "1. 📤 Push PC to Phone  ──► Overwrite Blaze clipboard with PC text",
        "2. 📥 Pull Phone to PC  ──► Overwrite Motobook clipboard with Phone text",
        "0. 🔙 Cancel            ──► Return to menu"
    ]
    chosen = run_fzf(actions, prompt="Sync Action > ", header="Select Clipboard Direction")
    if not chosen or "0. 🔙" in chosen:
        return
    if "1. 📤" in chosen:
        push_clipboard(pc_text)
    elif "2. 📥" in chosen:
        pull_clipboard()

def show_help_manual(pause=True):
    """Displays formatted command reference."""
    print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-CLIP COMMAND & CLI REFERENCE                  │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-clip                        │
│ • Pull Phone to PC:  blaze-clip --pull                 │
│ • Push PC to Phone:  blaze-clip --push                 │
│ • Send Direct Text:  blaze-clip --send "<text>"        │
│ • Side-by-Side Sync: blaze-clip --sync                 │
│ • Raw Output Mode:   blaze-clip --raw                  │
│ • JSON Machine Mode: blaze-clip --json                 │
└────────────────────────────────────────────────────────┘{RESET}
""")
    if pause:
        try:
            input("Press Enter to return...")
        except (KeyboardInterrupt, EOFError):
            pass

# --- Interactive Menu ---

def interactive_menu():
    """Interactive FZF terminal menu matching blaze-phone standard."""
    menu_items = [
        "📥 1. Pull Phone Clipboard ➔ PC    ──► Copy Blaze text into Windows clipboard",
        "📤 2. Push PC Clipboard ➔ Phone    ──► Send Windows clipboard to Blaze phone",
        "🔄 3. Side-by-Side Visual Diff     ──► Compare Motobook vs Blaze and sync",
        "✍️ 4. Send Custom Text to Phone    ──► Type arbitrary text straight to Blaze",
        "📖 5. Help & CLI Reference         ──► Flags, command switches & examples",
        "🚪 0. Exit                         ──► Return to PowerShell terminal"
    ]

    while True:
        try:
            chosen = run_fzf(menu_items, prompt="Blaze Clip > ", header="📋 BLAZE UNIFIED CLIPBOARD COMMAND HUB")
            if not chosen or "0. Exit" in chosen:
                print(f"{DIM}👋 Exited.{RESET}\n")
                break

            if "1. Pull Phone" in chosen:
                pull_clipboard()
            elif "2. Push PC" in chosen:
                push_clipboard()
            elif "3. Side-by-Side" in chosen:
                sync_clipboards()
            elif "4. Send Custom" in chosen:
                try:
                    text = input("Enter text to send to phone: ").strip()
                    if text:
                        push_clipboard(custom_text=text)
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
            elif "5. Help" in chosen:
                show_help_manual(pause=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}\n")
            break

def main():
    try:
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
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Exited gracefully.{RESET}")

if __name__ == "__main__":
    main()
