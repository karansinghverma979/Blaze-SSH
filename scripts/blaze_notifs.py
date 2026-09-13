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
import shutil
from datetime import datetime

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

def run_fzf(options, prompt="Blaze Notifs > ", header=None):
    """Runs inline interactive FZF fuzzy picker directly beneath the cursor in the active terminal."""
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

def set_clipboard(text):
    """Sets text to Windows clipboard."""
    try:
        subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value @'\n{text}\n'@"], check=True)
        return True
    except Exception:
        return False

def list_notifs(json_mode=False):
    """Fetches and displays active status bar notifications strictly sorted newest first."""
    out, err, code = run_ssh("termux-notification-list")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        elif json_mode:
            print(json.dumps({"error": "Failed to fetch notifications", "details": err}))
        else:
            print(f"{RED}❌ Failed to retrieve notifications from Blaze.{RESET} ({err})")
        return []
    try:
        raw_notifs = json.loads(out)
        notifs = sorted(raw_notifs, key=lambda x: str(x.get("when", "")), reverse=True)
        if json_mode:
            print(json.dumps(notifs, indent=2))
            return notifs

        print(f"\n{BOLD}{CYAN}🔔 ACTIVE STATUS BAR NOTIFICATIONS ({len(notifs)} - Newest First){RESET}")
        print("─" * 65)
        for i, n in enumerate(notifs, 1):
            pkg = n.get("packageName", "").split(".")[-1].capitalize()
            title = n.get("title", "")
            content = n.get("content", "").replace("\n", " ").strip()
            tag = n.get("tag", "").strip() if n.get("tag") else ""
            raw_id = str(n.get("id", "")).strip()
            nid = tag if tag else raw_id
            when = n.get("when", "")
            print(f"{GREEN}[{i:02d}]{RESET} {BOLD}{pkg}{RESET} | {CYAN}{title}{RESET} {DIM}(ID: {nid} | {when}){RESET}")
            print(f"    {content[:90]}{'...' if len(content) > 90 else ''}\n")
        print("─" * 65 + "\n")
        return notifs
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return []

def notifs_fzf_interactive():
    """Interactive FZF Notification Browser with 1-click Copy, Inspect, OTP Extract, and Dismiss."""
    print(f"{CYAN}🔔 Fetching active notifications from Blaze...{RESET}")
    out, err, code = run_ssh("termux-notification-list")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to fetch notifications: {err}{RESET}")
        return

    try:
        raw_notifs = json.loads(out)
        notifs = sorted(raw_notifs, key=lambda x: str(x.get("when", "")), reverse=True)
    except Exception:
        print(f"{RED}❌ Could not parse notifications.{RESET}")
        return

    if not notifs:
        print(f"{YELLOW}⚠️ No active status bar notifications on Blaze.{RESET}\n")
        return

    fzf_lines = []
    for idx, n in enumerate(notifs):
        pkg = n.get("packageName", "").split(".")[-1].capitalize()
        title = n.get("title", "No Title")
        content = n.get("content", "").replace("\n", " ").strip()
        fzf_lines.append(f"{idx+1:02d}. {pkg:<12} │ {title:<20} │ {content}")

    chosen = run_fzf(fzf_lines, prompt="Select Notification > ", header="🔔 ACTIVE NOTIFICATIONS (Newest First | Enter to inspect | Esc to back)")
    if not chosen:
        return

    match = re.match(r'^(\d+)\.', chosen)
    if not match:
        return

    idx = int(match.group(1)) - 1
    n = notifs[idx]
    pkg = n.get("packageName", "Unknown")
    title = n.get("title", "")
    content = n.get("content", "")
    tag = n.get("tag", "").strip() if n.get("tag") else ""
    raw_id = str(n.get("id", "")).strip()
    nid = tag if tag else raw_id
    when = n.get("when", "")

    otp_match = re.search(r'\b(\d{4,8})\b', f"{title} {content}")
    otp_str = otp_match.group(1) if otp_match else None

    print(f"\n{BOLD}{CYAN}🔔 NOTIFICATION #{idx+1}{RESET}")
    print("┌────────────────────────────────────────────────────────┐")
    print(f"│ 📦 {BOLD}App:{RESET}     {pkg}")
    print(f"│ 🏷️ {BOLD}Title:{RESET}   {title}")
    print(f"│ 🕒 {BOLD}Time:{RESET}    {when}")
    print(f"│ 🆔 {BOLD}ID/Tag:{RESET}  {nid}")
    if otp_str:
        print(f"│ 🔑 {BOLD}OTP:{RESET}     {GREEN}{BOLD}{otp_str}{RESET}")
    print("├────────────────────────────────────────────────────────┤")
    print(f"│ {BOLD}Content:{RESET}")
    for bl in content.splitlines():
        if bl.strip():
            print(f"│   {bl.strip()}")
    print("└────────────────────────────────────────────────────────┘")

    actions = [
        "1. 📋 Copy Notification Text     ──► Copy title & body to PC clipboard",
        f"2. 🗑️ Dismiss Notification ({nid}) ──► Clear notification from status bar",
        "0. 🔙 Back to Notifications       ──► Return to notification list"
    ]
    if otp_str:
        actions.insert(0, f"🔑 1. Copy OTP ({otp_str})       ──► Copy detected 2FA code to PC")

    chosen_action = run_fzf(actions, prompt=f"Action on {pkg} > ", header=f"Notification from {pkg}")
    if not chosen_action or "0. 🔙" in chosen_action:
        return

    if "Copy OTP" in chosen_action and otp_str:
        set_clipboard(otp_str)
        print(f"{GREEN}✅ OTP '{otp_str}' copied to Windows clipboard!{RESET}\n")
    elif "Copy Notification Text" in chosen_action:
        set_clipboard(f"{title}\n{content}")
        print(f"{GREEN}✅ Notification text copied to Windows clipboard!{RESET}\n")
    elif "Dismiss" in chosen_action:
        dismiss_notif(nid)

def extract_notif_otp(json_mode=False, raw_mode=False):
    """Extracts OTP specifically from active notifications and copies to PC clipboard."""
    out, err, code = run_ssh("termux-notification-list")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        return None

    try:
        raw_notifs = json.loads(out)
        notifs = sorted(raw_notifs, key=lambda x: str(x.get("when", "")), reverse=True)
    except Exception:
        return None

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
        set_clipboard(found_otp)
        if json_mode:
            print(json.dumps({"otp": found_otp, "source": target_notif, "copied": True}))
        elif raw_mode:
            print(found_otp)
        else:
            print(f"\n{GREEN}{BOLD}✨ NOTIFICATION OTP DETECTED & COPIED!{RESET}")
            print(f"┌────────────────────────────────────────────────────────┐")
            print(f"│ 🔑 {BOLD}OTP Code:{RESET}   {CYAN}{BOLD}{found_otp}{RESET}")
            print(f"│ 📦 {BOLD}App:{RESET}        {target_notif.get('packageName', 'Unknown')}")
            print(f"│ 📝 {BOLD}Message:{RESET}    {target_notif.get('content', '')[:60]}")
            print(f"└────────────────────────────────────────────────────────┘\n")
        return found_otp
    else:
        if json_mode:
            print(json.dumps({"error": "No OTP found in notifications"}))
        elif not raw_mode:
            print(f"{YELLOW}⚠️ No OTP found in active notifications.{RESET}\n")
        return None

def send_push_notif(title, body, priority="high"):
    """Dispatches native Android push notification."""
    safe_title = title.replace('"', '\\"')
    safe_body = body.replace('"', '\\"')
    out, err, code = run_ssh(f'termux-notification -t "{safe_title}" -c "{safe_body}" --priority {priority} --sound')
    if code == 0:
        print(f"{GREEN}✅ Notification pushed to Blaze screen.{RESET}\n")
    else:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to push notification: {err}{RESET}\n")

def spawn_toast(message, background="gray", text_color="white", gravity="middle"):
    """Shows floating screen toast on phone centered on screen by default."""
    safe_msg = message.replace('"', '\\"')
    safe_bg = background.replace('"', '\\"')
    safe_fg = text_color.replace('"', '\\"')
    safe_g = gravity.replace('"', '\\"')
    out, err, code = run_ssh(f'termux-toast -b "{safe_bg}" -c "{safe_fg}" -g "{safe_g}" "{safe_msg}"')
    if code == 0:
        print(f"\n{GREEN}{BOLD}✅ Toast displayed in screen ({gravity}):{RESET} \"{message}\"\n")
    else:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to display toast: {err}{RESET}\n")

def spawn_dialog(dtype="text", title="Motobook Alert", hint=None, values=None, range_vals=None, multiline=False, numeric=False, password=False):
    """Spawns rich interactive mobile dialog and retrieves response with auto-copy to PC clipboard."""
    print(f"\n{CYAN}📱 Spawning mobile {dtype.upper()} dialog on Blaze screen... (Waiting for input on phone){RESET}")
    safe_title = title.replace('"', '\\"') if title else "Motobook Alert"
    
    cmd = f'termux-dialog {dtype} -t "{safe_title}"'
    if hint:
        safe_hint = hint.replace('"', '\\"')
        cmd += f' -i "{safe_hint}"'
    if values:
        safe_vals = values.replace('"', '\\"')
        cmd += f' -v "{safe_vals}"'
    if range_vals:
        cmd += f' -r "{range_vals}"'
    if multiline and not numeric:
        cmd += ' -m'
    if numeric and not multiline:
        cmd += ' -n'
    if password:
        cmd += ' -p'

    out, err, code = run_ssh(cmd, timeout=120)

    if code == 0 and out:
        try:
            res = json.loads(out)
            code_ret = res.get("code")
            text_val = res.get("text", "")
            selected_vals = res.get("values", [])
            index_val = res.get("index")

            # Android Dialog return codes:
            # -1: Positive button (OK, Set, Yes, Submit) -> SUCCESS
            # -2: Negative button (Cancel, No) -> CANCELLED
            # -3: Neutral button
            # 0: Dismissed or back pressed without button

            if code_ret == -2 or (code_ret == 0 and not text_val and not selected_vals and index_val is None):
                print(f"{YELLOW}⚠️ Dialog cancelled or closed by user on phone.{RESET}\n")
                return res

            print(f"\n{GREEN}{BOLD}📱 MOBILE DIALOG RESPONSE RECEIVED:{RESET}")
            print("┌────────────────────────────────────────────────────────┐")
            print(f"│ 🏷️ {BOLD}Dialog Type:{RESET}  {dtype.upper():<39}│")
            print(f"│ 📌 {BOLD}Title:{RESET}        {safe_title[:38]:<39}│")
            
            result_to_copy = None
            if dtype == "confirm":
                is_yes = (str(text_val).lower() == "yes") or (code_ret == -1)
                status_str = f"{GREEN}YES (Confirmed){RESET}" if is_yes else f"{RED}NO (Cancelled){RESET}"
                print(f"│ ❓ {BOLD}Decision:{RESET}    {status_str:<48}│")
                result_to_copy = "YES" if is_yes else "NO"
            elif text_val:
                print(f"│ 💬 {BOLD}Input Text:{RESET}   {CYAN}{BOLD}{text_val[:38]:<39}{RESET}│")
                result_to_copy = text_val
            elif selected_vals:
                sel_strs = [v.get("text", str(v)) for v in selected_vals]
                combined = ", ".join(sel_strs)
                print(f"│ ☑️ {BOLD}Selected:{RESET}     {CYAN}{BOLD}{combined[:38]:<39}{RESET}│")
                result_to_copy = combined
            elif index_val is not None:
                print(f"│ 🔢 {BOLD}Index / Choice:{RESET} {CYAN}{BOLD}{str(index_val):<37}{RESET}│")
                result_to_copy = str(index_val)

            print("└────────────────────────────────────────────────────────┘")
            if result_to_copy:
                set_clipboard(str(result_to_copy))
                print(f"{DIM}📋 '{result_to_copy}' automatically copied to Windows clipboard!{RESET}\n")
            return res
        except Exception as e:
            print(f"\n{GREEN}📱 Raw Output:{RESET} {out}\n")
            set_clipboard(out)
            return {"raw": out}
    else:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Dialog timed out or cancelled.{RESET}\n")
        return None

def dismiss_notif(nid):
    """Dismisses notification by tag or ID."""
    clean_id = str(nid).strip()
    out, err, code = run_ssh(f'termux-notification-remove "{clean_id}"')
    if code == 0:
        print(f"\n{GREEN}✅ Notification '{clean_id}' dismiss request dispatched.{RESET}\n")
    else:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to dismiss notification '{clean_id}': {err}{RESET}\n")

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
                        nid = str(n.get("tag") or n.get("id") or n.get("key"))
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
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Watcher stopped.{RESET}\n")

def show_help_manual(pause=True):
    """Displays formatted command reference."""
    print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-NOTIFS COMMAND & CLI REFERENCE                │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-notifs                      │
│ • List Notifications:blaze-notifs --list               │
│ • Extract OTP:       blaze-notifs --otp                │
│ • Push Notification: blaze-notifs --title <t> --body <b>│
│ • Centered Toast:    blaze-notifs --toast "<message>"  │
│ • Rich Mobile Dialog:blaze-notifs --dialog <widget>    │
│   (text, password, multiline, confirm, radio, sheet,   │
│    checkbox, spinner, counter, speech, date, time)     │
│ • Dismiss by ID/Tag: blaze-notifs --dismiss <id|tag>   │
│ • Live Watcher:      blaze-notifs --watch [seconds]    │
│ • JSON Machine Mode: blaze-notifs --json               │
└────────────────────────────────────────────────────────┘{RESET}
""")
    if pause:
        try:
            input("Press Enter to return...")
        except (KeyboardInterrupt, EOFError):
            pass

# --- Interactive Menu ---

def interactive_dialog_studio():
    """Interactive Mobile Dialog Designer & Runner Studio."""
    widgets = [
        "1. 📝 Text Input          ──► Standard keyboard prompt",
        "2. 🔒 Password / Secret    ──► Masked text entry (PIN/Password)",
        "3. 📄 Multiline Text Area  ──► Large paragraph / note editor",
        "4. 🔢 Number Input         ──► Numeric keypad input",
        "5. ❓ Confirmation Prompt  ──► Yes / No (OK / Cancel) modal",
        "6. 🔘 Radio Buttons        ──► Single choice from options list",
        "7. ☑️ Checkbox Selector    ──► Multiple choices from list",
        "8. 📜 Sliding Bottom Sheet ──► Native Android slide-up picker",
        "9. 🎯 Dropdown Spinner     ──► Compact dropdown select menu",
        "10. 🔢 Numeric Counter     ──► Stepper / Range counter",
        "11. 🎤 Voice / Mic Input   ──► Speech-to-text via phone microphone",
        "12. 📅 Date Picker         ──► Interactive calendar selector",
        "13. 🕒 Time Picker         ──► Interactive clock selector",
        "0. 🔙 Return to Main Menu ──► Cancel"
    ]

    while True:
        try:
            chosen = run_fzf(widgets, prompt="Dialog Type > ", header="📱 MOBILE DIALOG STUDIO (Design & Dispatch)")
            if not chosen or "0. 🔙" in chosen:
                break

            title = input(f"{CYAN}Enter Dialog Title [default: Motobook]: {RESET}").strip() or "Motobook"

            if "1. 📝 Text Input" in chosen:
                hint = input("Enter Input Hint / Placeholder: ").strip() or "Enter text here..."
                spawn_dialog(dtype="text", title=title, hint=hint)
            elif "2. 🔒 Password" in chosen:
                hint = input("Enter Password Hint: ").strip() or "Enter secret..."
                spawn_dialog(dtype="text", title=title, hint=hint, password=True)
            elif "3. 📄 Multiline" in chosen:
                hint = input("Enter Editor Hint: ").strip() or "Type multiline notes..."
                spawn_dialog(dtype="text", title=title, hint=hint, multiline=True)
            elif "4. 🔢 Number" in chosen:
                hint = input("Enter Number Hint: ").strip() or "Enter digits..."
                spawn_dialog(dtype="text", title=title, hint=hint, numeric=True)
            elif "5. ❓ Confirmation" in chosen:
                hint = input("Enter Confirmation Question / Hint: ").strip() or "Do you want to proceed?"
                spawn_dialog(dtype="confirm", title=title, hint=hint)
            elif "6. 🔘 Radio" in chosen:
                raw_v = input("Enter choices (comma-separated, e.g. Low,Medium,High): ").strip()
                if raw_v:
                    spawn_dialog(dtype="radio", title=title, values=raw_v)
            elif "7. ☑️ Checkbox" in chosen:
                raw_v = input("Enter options (comma-separated, e.g. Wi-Fi,Bluetooth,GPS): ").strip()
                if raw_v:
                    spawn_dialog(dtype="checkbox", title=title, values=raw_v)
            elif "8. 📜 Sliding Bottom" in chosen:
                raw_v = input("Enter sheet items (comma-separated): ").strip()
                if raw_v:
                    spawn_dialog(dtype="sheet", title=title, values=raw_v)
            elif "9. 🎯 Dropdown Spinner" in chosen:
                raw_v = input("Enter spinner options (comma-separated): ").strip()
                if raw_v:
                    spawn_dialog(dtype="spinner", title=title, values=raw_v)
            elif "10. 🔢 Numeric Counter" in chosen:
                raw_r = input("Enter range 'min,max,start' [default: 0,100,50]: ").strip() or "0,100,50"
                spawn_dialog(dtype="counter", title=title, range_vals=raw_r)
            elif "11. 🎤 Voice" in chosen:
                hint = input("Enter Speech Prompt Hint: ").strip() or "Speak now..."
                spawn_dialog(dtype="speech", title=title, hint=hint)
            elif "12. 📅 Date" in chosen:
                spawn_dialog(dtype="date", title=title)
            elif "13. 🕒 Time" in chosen:
                spawn_dialog(dtype="time", title=title)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Dialog studio exited.{RESET}\n")
            break

def interactive_toast_menu():
    """Interactive Toast Customizer with rich color themes and positions."""
    presets = [
        "1. 💬 Standard Slate      ──► Screen Center | Slate Gray (#37474F)",
        "2. 🟢 Emerald Green (OK)   ──► Screen Center | Forest Green (#1B5E20)",
        "3. 🔴 Crimson Alert (War) ──► Screen Center | Ruby Red (#B71C1C)",
        "4. 🔵 Neon Cyber Cyan     ──► Screen Center | Deep Cyan (#006064)",
        "5. 🟡 Amber Gold (Warning) ──► Screen Center | Warm Amber (#FF6F00)",
        "6. 🟣 Deep Purple Matrix   ──► Screen Center | Regal Purple (#4A148C)",
        "7. 🌑 Midnight Stealth     ──► Screen Center | Jet Black (#121212)",
        "8. ☀️ Solar Sunshine       ──► Screen Center | Bright Yellow (#FFD600)",
        "9. 🌊 Sapphire Blue        ──► Screen Center | Royal Blue (#0D47A1)",
        "10. 🎨 Custom Palette & Pos ──► Choose Custom Colors (Hex/Name) & Gravity",
        "0. 🔙 Return to Menu"
    ]
    while True:
        try:
            chosen = run_fzf(presets, prompt="Toast Theme > ", header="🍞 TOAST DESIGNER (Screen Center)")
            if not chosen or "0. 🔙" in chosen:
                break
            msg = input(f"{CYAN}Enter Toast Message: {RESET}").strip()
            if not msg:
                continue

            if "1. 💬" in chosen:
                spawn_toast(msg, background="#37474F", text_color="white", gravity="middle")
            elif "2. 🟢" in chosen:
                spawn_toast(msg, background="#1B5E20", text_color="white", gravity="middle")
            elif "3. 🔴" in chosen:
                spawn_toast(msg, background="#B71C1C", text_color="white", gravity="middle")
            elif "4. 🔵" in chosen:
                spawn_toast(msg, background="#006064", text_color="white", gravity="middle")
            elif "5. 🟡" in chosen:
                spawn_toast(msg, background="#FF6F00", text_color="black", gravity="middle")
            elif "6. 🟣" in chosen:
                spawn_toast(msg, background="#4A148C", text_color="#E1BEE7", gravity="middle")
            elif "7. 🌑" in chosen:
                spawn_toast(msg, background="#121212", text_color="#EEEEEE", gravity="middle")
            elif "8. ☀️" in chosen:
                spawn_toast(msg, background="#FFD600", text_color="black", gravity="middle")
            elif "9. 🌊" in chosen:
                spawn_toast(msg, background="#0D47A1", text_color="#E0F7FA", gravity="middle")
            elif "10. 🎨" in chosen:
                grav_opts = ["1. 🎯 Middle (Center)", "2. ⬆️ Top", "3. ⬇️ Bottom"]
                g_sel = run_fzf(grav_opts, prompt="Gravity > ")
                g_val = "middle"
                if g_sel:
                    if "Top" in g_sel: g_val = "top"
                    elif "Bottom" in g_sel: g_val = "bottom"
                bg = input("Background Color [hex code or name, e.g. #FF0055 / red / black]: ").strip() or "gray"
                fg = input("Text Color [hex code or name, e.g. white / black / yellow]: ").strip() or "white"
                spawn_toast(msg, background=bg, text_color=fg, gravity=g_val)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Toast menu exited.{RESET}\n")
            break

def interactive_menu():
    """Interactive FZF terminal menu matching blaze standard."""
    menu_items = [
        "📋 1. Browse Active Notifications  ──► Fuzzy search & 1-click inspect / dismiss (FZF)",
        "🔑 2. Extract Notification OTP    ──► Scan active status bar alerts for 2FA code",
        "📤 3. Send Push Notification      ──► Dispatch native Android alert to phone screen",
        "🍞 4. Screen Center Toast         ──► Display centered floating overlay toast",
        "📱 5. Mobile Dialog Studio        ──► Rich interactive dialogs (text, confirm, voice, pickers)",
        "🗑️ 6. Dismiss Notification by ID  ──► Remove target notification from status bar",
        "👀 7. Live Notification Watcher   ──► Real-time live streaming notification radar",
        "📖 8. Help & CLI Reference        ──► Flags, command switches & examples",
        "🚪 0. Exit                        ──► Return to PowerShell terminal"
    ]

    while True:
        try:
            chosen = run_fzf(menu_items, prompt="Blaze Notifs > ", header="🔔 BLAZE NOTIFICATIONS & MOBILE UI HUB")
            if not chosen or "0. Exit" in chosen:
                print(f"{DIM}👋 Exited.{RESET}\n")
                break

            if "1. Browse Active" in chosen:
                notifs_fzf_interactive()
            elif "2. Extract" in chosen:
                extract_notif_otp()
            elif "3. Send Push" in chosen:
                try:
                    t = input("Notification Title: ").strip()
                    b = input("Notification Body: ").strip()
                    if t and b:
                        nid = str(int(time.time()))[-4:]
                        safe_t = t.replace('"', '\\"')
                        safe_b = b.replace('"', '\\"')
                        out, err, code = run_ssh(f'termux-notification --id {nid} -t "{safe_t}" -c "{safe_b}" --priority high --sound')
                        if code == 0:
                            print(f"{GREEN}✅ Notification pushed with ID: {nid}{RESET}\n")
                        else:
                            print(f"{RED}❌ Failed: {err}{RESET}\n")
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
            elif "4. Screen Center Toast" in chosen:
                interactive_toast_menu()
            elif "5. Mobile Dialog Studio" in chosen:
                interactive_dialog_studio()
            elif "6. Dismiss" in chosen:
                try:
                    nid = input("Notification ID or Tag to remove: ").strip()
                    if nid:
                        dismiss_notif(nid)
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
            elif "7. Live Notification" in chosen:
                watch_notifs()
            elif "8. Help" in chosen:
                show_help_manual(pause=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}\n")
            break

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blaze Notifications, Alerts & Mobile UI Dialogs Hub",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("--list", action="store_true", help="List active status bar notifications")
        parser.add_argument("--otp", action="store_true", help="Extract OTP from notifications and copy to clipboard")
        parser.add_argument("--title", help="Push notification title")
        parser.add_argument("--body", help="Push notification body")
        parser.add_argument("--id", help="Push notification custom ID")
        parser.add_argument("--toast", metavar="MESSAGE", help="Display centered toast on phone screen")
        parser.add_argument("--dialog", choices=["text", "confirm", "date", "time", "radio", "checkbox", "sheet", "spinner", "counter", "speech"], help="Spawn interactive mobile dialog")
        parser.add_argument("--dismiss", metavar="ID", help="Dismiss notification by ID or tag")
        parser.add_argument("--watch", type=int, nargs="?", const=3, help="Watch notifications live (seconds interval)")
        parser.add_argument("--json", action="store_true", help="JSON output mode")
        parser.add_argument("--raw", action="store_true", help="Raw output mode")

        args = parser.parse_args()

        if args.list:
            list_notifs(json_mode=args.json)
        elif args.otp:
            extract_notif_otp(json_mode=args.json, raw_mode=args.raw)
        elif args.title and args.body:
            nid = args.id or str(int(time.time()))[-4:]
            safe_t = args.title.replace('"', '\\"')
            safe_b = args.body.replace('"', '\\"')
            run_ssh(f'termux-notification --id {nid} -t "{safe_t}" -c "{safe_b}" --priority high --sound')
            print(f"{GREEN}✅ Notification pushed (ID: {nid}).{RESET}")
        elif args.toast:
            spawn_toast(args.toast, gravity="middle")
        elif args.dialog:
            spawn_dialog(dtype=args.dialog)
        elif args.dismiss:
            dismiss_notif(args.dismiss)
        elif args.watch is not None:
            watch_notifs(interval=args.watch)
        else:
            interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Exited gracefully.{RESET}")

if __name__ == "__main__":
    main()
