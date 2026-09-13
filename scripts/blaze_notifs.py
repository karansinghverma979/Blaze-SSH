#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔔 Blaze Notifications, Alerts & Mobile UI Dialogs Hub
Author: Antigravity Assistant & Karan Singh Verma
Project: Blaze (Motobook ⇄ Lava Blaze 5G Node)
Dual Mode: Fast-Path CLI switches & Rich Interactive Terminal Menu
"""

import sys
import os
import json
import subprocess
import argparse
import time
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
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def run_ssh(cmd, timeout=6):
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

def list_notifs(json_mode=False):
    """Fetches active status bar notifications."""
    out, err, code = run_ssh("termux-notification-list")
    if code != 0 or not out:
        if json_mode:
            print(json.dumps({"error": "Failed to fetch notifications", "details": err}))
        else:
            print(f"{RED}❌ Failed to retrieve notifications from Blaze.{RESET} ({err})")
        return []
    try:
        notifs = json.loads(out)
        if json_mode:
            print(json.dumps(notifs, indent=2))
            return notifs

        print(f"\n{BOLD}{CYAN}🔔 ACTIVE STATUS BAR NOTIFICATIONS ({len(notifs)}){RESET}")
        print("─" * 65)
        for i, n in enumerate(notifs, 1):
            pkg = n.get("packageName", "").split(".")[-1].capitalize()
            title = n.get("title", "")
            content = n.get("content", "").replace("\n", " ")
            nid = n.get("id", "")
            print(f"{GREEN}[{i:02d}]{RESET} {BOLD}{pkg}{RESET} | {CYAN}{title}{RESET} {DIM}(ID: {nid}){RESET}")
            print(f"    {content[:90]}{'...' if len(content) > 90 else ''}")
        print("─" * 65 + "\n")
        return notifs
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return []

def extract_notif_otp(json_mode=False, raw_mode=False):
    """Extracts OTP specifically from active notifications and copies to PC clipboard."""
    notifs = list_notifs(json_mode=True)
    if not isinstance(notifs, list):
        return

    otp_pattern = re.compile(r'\b(?:otp|code|pin|secret|is)\b.*?(\d{4,8})\b', re.IGNORECASE)
    generic_pattern = re.compile(r'\b(\d{4,8})\b')

    found_otp = None
    target_notif = None

    for n in notifs:
        full_text = f"{n.get('title', '')} {n.get('content', '')}"
        match = otp_pattern.search(full_text)
        if match:
            found_otp = match.group(1)
            target_notif = n
            break
        fallback = generic_pattern.search(full_text)
        if fallback and not found_otp:
            found_otp = fallback.group(1)
            target_notif = n

    if found_otp:
        try:
            subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value '{found_otp}'"], check=True)
        except Exception:
            pass

        if json_mode:
            print(json.dumps({"otp": found_otp, "source": target_notif, "copied": True}))
        elif raw_mode:
            print(found_otp)
        else:
            print(f"\n{GREEN}┌── ✨ NOTIFICATION OTP DETECTED & COPIED ──────────────────────{RESET}")
            print(f"{GREEN}│{RESET}")
            print(f"│ 🔑 {BOLD}OTP Code:{RESET}        {CYAN}{BOLD}{found_otp}{RESET}")
            print(f"│ 📦 {BOLD}App Source:{RESET}      {target_notif.get('packageName', 'Unknown')}")
            print(f"│ 📝 {BOLD}Message Snippet:{RESET} {target_notif.get('content', '')[:60]}")
            print(f"{GREEN}│{RESET}")
            print(f"{GREEN}└── 📋 Ready to paste (Ctrl+V) on Motobook{RESET}\n")
    else:
        if json_mode:
            print(json.dumps({"error": "No OTP found in notifications"}))
        elif not raw_mode:
            print(f"{YELLOW}⚠️ No OTP found in active notifications.{RESET}")

def send_push_notif(title, body, priority="high"):
    """Dispatches native Android push notification."""
    safe_title = title.replace('"', '\\"')
    safe_body = body.replace('"', '\\"')
    out, err, code = run_ssh(f'termux-notification -t "{safe_title}" -c "{safe_body}" --priority {priority} --sound')
    if code == 0:
        print(f"{GREEN}✅ Notification pushed to Blaze screen.{RESET}")
    else:
        print(f"{RED}❌ Failed to push notification: {err}{RESET}")

def spawn_toast(message, background="gray", text_color="white"):
    """Shows floating screen toast on phone."""
    safe_msg = message.replace('"', '\\"')
    out, err, code = run_ssh(f'termux-toast -b {background} -c {text_color} -g bottom "{safe_msg}"')
    if code == 0:
        print(f"{GREEN}✅ Toast displayed on phone screen: \"{message}\"{RESET}")
    else:
        print(f"{RED}❌ Failed to display toast: {err}{RESET}")

def spawn_dialog(dtype="text", title="Motobook Alert", hint="Enter value"):
    """Spawns interactive mobile dialog and retrieves response."""
    print(f"{CYAN}📱 Spawning mobile {dtype} dialog on Blaze...{RESET}")
    if dtype == "confirm":
        out, err, code = run_ssh(f'termux-dialog confirm -t "{title}"')
    elif dtype == "date":
        out, err, code = run_ssh(f'termux-dialog date -t "{title}"')
    elif dtype == "time":
        out, err, code = run_ssh(f'termux-dialog time -t "{title}"')
    else: # text
        out, err, code = run_ssh(f'termux-dialog text -t "{title}" -i "{hint}"')

    if code == 0 and out:
        try:
            res = json.loads(out)
            print(f"\n{GREEN}{BOLD}📱 Mobile Dialog Response:{RESET}")
            print(json.dumps(res, indent=2))
            return res
        except Exception:
            print(out)
    else:
        print(f"{RED}❌ Dialog dismissed or cancelled.{RESET}")

def dismiss_notif(nid):
    """Dismisses notification by ID."""
    out, err, code = run_ssh(f"termux-notification-remove {nid}")
    if code == 0:
        print(f"{GREEN}✅ Notification {nid} dismissed.{RESET}")
    else:
        print(f"{RED}❌ Failed to dismiss notification: {err}{RESET}")

def watch_notifs(interval=3):
    """Continuously monitors and prints new notifications."""
    print(f"{CYAN}👀 Starting Live Notification Watcher (Polling every {interval}s)... [Ctrl+C to stop]{RESET}\n")
    seen_ids = set()
    try:
        while True:
            out, err, code = run_ssh("termux-notification-list", timeout=3)
            if code == 0 and out:
                try:
                    notifs = json.loads(out)
                    for n in notifs:
                        nid = n.get("id")
                        if nid not in seen_ids:
                            seen_ids.add(nid)
                            pkg = n.get("packageName", "").split(".")[-1].capitalize()
                            title = n.get("title", "")
                            content = n.get("content", "")
                            now = datetime.now().strftime("%H:%M:%S")
                            print(f"{GREEN}[{now}]{RESET} {BOLD}{pkg}{RESET}: {CYAN}{title}{RESET} ──► {content}")
                except Exception:
                    pass
            time.sleep(interval)
    except KeyboardInterrupt:
        print(f"\n{DIM}👋 Watcher stopped.{RESET}")

# --- Interactive Menu ---

def interactive_menu():
    """Interactive terminal menu."""
    while True:
        print()
        print(f"{CYAN}┌── 🔔 BLAZE NOTIFICATIONS & MOBILE UI HUB ─────────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│  {BOLD}1{RESET}  📋 View Active Status Bar Notifications")
        print(f"│  {BOLD}2{RESET}  🔑 1-Click Notification OTP Extractor")
        print(f"│  {BOLD}3{RESET}  📤 Send Native Android Push Notification")
        print(f"│  {BOLD}4{RESET}  🍞 Spawn Floating Screen Toast")
        print(f"│  {BOLD}5{RESET}  📱 Spawn Interactive Mobile Dialog Prompt")
        print(f"│  {BOLD}6{RESET}  🗑️ Dismiss Notification by ID")
        print(f"│  {BOLD}7{RESET}  👀 Live Notification Watcher Stream")
        print(f"│  {BOLD}0{RESET}  🚪 Exit")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└── ⚡ Select Option [0-7]{RESET}")
        print()
        try:
            choice = input(f"{BOLD}Blaze-Notifs ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            list_notifs()
        elif choice == "2":
            extract_notif_otp()
        elif choice == "3":
            t = input("Notification Title: ").strip()
            b = input("Notification Body: ").strip()
            if t and b:
                send_push_notif(t, b)
        elif choice == "4":
            msg = input("Toast Message: ").strip()
            if msg:
                spawn_toast(msg)
        elif choice == "5":
            print("Dialog Types: 1) Text  2) Confirm  3) Date  4) Time")
            dt = input("Choice [1-4]: ").strip()
            mapping = {"1": "text", "2": "confirm", "3": "date", "4": "time"}
            spawn_dialog(dtype=mapping.get(dt, "text"))
        elif choice == "6":
            nid = input("Notification ID to remove: ").strip()
            if nid:
                dismiss_notif(nid)
        elif choice == "7":
            watch_notifs()
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Select 0-7.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Notifications, Alerts & Mobile UI Dialogs Hub",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--list", action="store_true", help="List active status bar notifications")
    parser.add_argument("--otp", action="store_true", help="Extract OTP from notifications and copy to clipboard")
    parser.add_argument("--title", help="Push notification title")
    parser.add_argument("--body", help="Push notification body")
    parser.add_argument("--toast", metavar="MESSAGE", help="Display floating toast on phone screen")
    parser.add_argument("--dialog", choices=["text", "confirm", "date", "time"], help="Spawn interactive mobile dialog")
    parser.add_argument("--dismiss", metavar="ID", help="Dismiss notification by ID")
    parser.add_argument("--watch", type=int, nargs="?", const=3, help="Watch notifications live (seconds interval)")
    parser.add_argument("--json", action="store_true", help="JSON output mode")
    parser.add_argument("--raw", action="store_true", help="Raw output mode")

    args = parser.parse_args()

    if args.list:
        list_notifs(json_mode=args.json)
    elif args.otp:
        extract_notif_otp(json_mode=args.json, raw_mode=args.raw)
    elif args.title and args.body:
        send_push_notif(args.title, args.body)
    elif args.toast:
        spawn_toast(args.toast)
    elif args.dialog:
        spawn_dialog(dtype=args.dialog)
    elif args.dismiss:
        dismiss_notif(args.dismiss)
    elif args.watch is not None:
        watch_notifs(interval=args.watch)
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
