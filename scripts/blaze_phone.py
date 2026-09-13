#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 Blaze Telephony, SMS, Contacts, Call Logs & 5G Cellular Command Hub
Author: Antigravity Assistant & Karan Singh Verma
Project: Blaze (Motobook ⇄ Lava Blaze 5G Node)
Interactive FZF Fuzzy Control Center & Fast-Path CLI Triggers
"""

import sys
import os
import json
import subprocess
import re
import argparse
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
            capture_output=True, text=True, timeout=timeout + 3, encoding="utf-8", errors="replace"
        )
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "", "Connection timed out. Blaze may be offline.", 255
    except Exception as e:
        return "", str(e), 1

def set_clipboard(text):
    """Sets text to Windows clipboard."""
    try:
        subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value @'\n{text}\n'@"], check=True)
        return True
    except Exception:
        return False

def run_fzf(options, prompt="Blaze Phone > ", header=None):
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

# ==============================================================================
# 🔑 1. OTP 1-Click Extraction Engine
# ==============================================================================

def get_otp(json_mode=False, raw_mode=False):
    """Scans SMS inbox (latest first), extracts latest 4-8 digit OTP, and copies to PC clipboard."""
    out, err, code = run_ssh("termux-sms-list -l 20 -t inbox")
    if code != 0 or not out:
        if json_mode:
            print(json.dumps({"error": "Failed to retrieve SMS", "details": err}))
        else:
            if code == 255:
                render_unreachable_card()
            else:
                print(f"{RED}❌ Failed to fetch SMS inbox from Blaze.{RESET} ({err})")
        return None

    try:
        raw_msgs = json.loads(out)
        # Explicit descending sort by received timestamp
        messages = sorted(raw_msgs, key=lambda x: str(x.get("received", "")), reverse=True)
    except Exception:
        if json_mode:
            print(json.dumps({"error": "Invalid SMS JSON response"}))
        else:
            print(f"{RED}❌ Could not parse SMS data.{RESET}")
        return None

    otp_pattern = re.compile(r'\b(?:otp|code|verification|passcode|secret|pin|is)\b.*?(\d{4,8})\b', re.IGNORECASE)
    generic_num_pattern = re.compile(r'\b(\d{4,8})\b')

    found_otp = None
    source_msg = None

    for msg in messages:
        body = msg.get("body", "")
        match = otp_pattern.search(body)
        if match:
            found_otp = match.group(1)
            source_msg = msg
            break
        fallback = generic_num_pattern.search(body)
        if fallback and not found_otp:
            found_otp = fallback.group(1)
            source_msg = msg

    if found_otp:
        set_clipboard(found_otp)
        sender = source_msg.get("number", "Unknown") if source_msg else "Unknown"
        received = source_msg.get("received", "") if source_msg else ""
        if json_mode:
            print(json.dumps({"otp": found_otp, "sender": sender, "received": received, "copied": True}))
        elif raw_mode:
            print(found_otp)
        else:
            print(f"\n{GREEN}{BOLD}✨ OTP DETECTED & COPIED TO CLIPBOARD!{RESET}")
            print(f"┌────────────────────────────────────────────────────────┐")
            print(f"│ 🔑 {BOLD}OTP Code:{RESET}   {CYAN}{BOLD}{found_otp}{RESET}")
            print(f"│ 👤 {BOLD}Sender:{RESET}     {sender}")
            print(f"│ 🕒 {BOLD}Received:{RESET}   {received}")
            print(f"└────────────────────────────────────────────────────────┘")
            print(f"{DIM}📋 Ready to paste (Ctrl+V) anywhere on Motobook.{RESET}\n")
        return found_otp
    else:
        if json_mode:
            print(json.dumps({"error": "No recent OTP found in SMS inbox"}))
        elif raw_mode:
            print("")
        else:
            print(f"{YELLOW}⚠️ No recent OTP found in the latest messages.{RESET}")
        return None

# ==============================================================================
# 📬 2. SMS Inbox & Actions (Latest First + FZF)
# ==============================================================================

def list_sms(limit=15, json_mode=False):
    """Displays formatted SMS messages strictly sorted latest first."""
    out, err, code = run_ssh(f"termux-sms-list -l {limit} -t inbox")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to fetch SMS inbox.{RESET}")
        return []
    try:
        raw_msgs = json.loads(out)
        messages = sorted(raw_msgs, key=lambda x: str(x.get("received", "")), reverse=True)
        if json_mode:
            print(json.dumps(messages, indent=2))
            return messages
        print(f"\n{BOLD}{CYAN}📬 BLAZE SMS INBOX (Latest {len(messages)} - Newest First){RESET}")
        print("─" * 65)
        for i, m in enumerate(messages, 1):
            sender = m.get("number", "Unknown")
            body = m.get("body", "").replace("\n", " ").strip()
            received = m.get("received", "")
            read_status = f"{GREEN}Read{RESET}" if m.get("read", True) else f"{YELLOW}{BOLD}UNREAD ✉️{RESET}"
            print(f"{GREEN}[{i:02d}]{RESET} {BOLD}{sender}{RESET} {DIM}({received}){RESET} - {read_status}")
            print(f"    {body[:95]}{'...' if len(body) > 95 else ''}\n")
        print("─" * 65 + "\n")
        return messages
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return []

def sms_fzf_interactive():
    """Interactive FZF SMS Browser with 1-click Inspect, Reply, Call, or Copy OTP."""
    print(f"{CYAN}📬 Fetching SMS inbox from Blaze...{RESET}")
    out, err, code = run_ssh("termux-sms-list -l 40 -t inbox")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to fetch SMS: {err}{RESET}")
        return

    try:
        raw_msgs = json.loads(out)
        messages = sorted(raw_msgs, key=lambda x: str(x.get("received", "")), reverse=True)
    except Exception:
        print(f"{RED}❌ Could not parse SMS data.{RESET}")
        return

    if not messages:
        print(f"{YELLOW}⚠️ SMS inbox is empty.{RESET}")
        return

    fzf_lines = []
    for idx, m in enumerate(messages):
        sender = m.get("number") or m.get("address", "Unknown")
        date_str = m.get("received", "")
        body = m.get("body", "").replace("\n", " ").strip()
        fzf_lines.append(f"{idx+1:02d}. {sender:<16} │ {date_str} │ {body}")

    chosen = run_fzf(fzf_lines, prompt="Select SMS > ", header="📬 SMS INBOX (Newest First | Type to filter | Enter to inspect | Esc to back)")
    if not chosen:
        return

    match = re.match(r'^(\d+)\.', chosen)
    if not match:
        return

    idx = int(match.group(1)) - 1
    msg = messages[idx]
    sender = msg.get("number") or msg.get("address", "Unknown")
    received = msg.get("received", "")
    body = msg.get("body", "")

    otp_match = re.search(r'\b(\d{4,8})\b', body)
    otp_str = otp_match.group(1) if otp_match else None

    print(f"\n{BOLD}{CYAN}📨 SMS MESSAGE #{idx+1}{RESET}")
    print("┌────────────────────────────────────────────────────────┐")
    print(f"│ 👤 {BOLD}Sender:{RESET}   {sender}")
    print(f"│ 🕒 {BOLD}Date:{RESET}     {received}")
    if otp_str:
        print(f"│ 🔑 {BOLD}OTP:{RESET}      {GREEN}{BOLD}{otp_str}{RESET}")
    print("├────────────────────────────────────────────────────────┤")
    print(f"│ {BOLD}Message Content:{RESET}")
    for bl in body.splitlines():
        if bl.strip():
            print(f"│   {bl.strip()}")
    print("└────────────────────────────────────────────────────────┘")

    action_items = [
        "1. 📨 Reply via SMS              ──► Type text response to sender",
        f"2. 📞 Call Sender ({sender})   ──► Dial sender phone number",
        "3. 📋 Copy Full Message Body     ──► Copy entire text to PC clipboard",
        "0. 🔙 Back to Inbox              ──► Return to message list"
    ]
    if otp_str:
        action_items.insert(0, f"🔑 1. Copy OTP ({otp_str})       ──► Copy 2FA code to PC clipboard")

    chosen_action = run_fzf(action_items, prompt=f"Action on {sender} > ", header=f"Message from {sender}")
    if not chosen_action or "0. 🔙" in chosen_action:
        return

    if "Copy OTP" in chosen_action and otp_str:
        set_clipboard(otp_str)
        print(f"{GREEN}✅ OTP '{otp_str}' copied to Windows clipboard!{RESET}\n")
    elif "Reply" in chosen_action:
        try:
            reply_txt = input(f"Reply to {sender}: ").strip()
            if reply_txt:
                send_sms(sender, reply_txt)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
    elif "Call" in chosen_action:
        clean_num = re.sub(r'[^0-9+]', '', sender)
        if clean_num:
            call_number(clean_num)
        else:
            print(f"{YELLOW}⚠️ '{sender}' is an alphanumeric business ID and cannot be dialed directly.{RESET}\n")
    elif "Copy Full Message" in chosen_action:
        set_clipboard(body)
        print(f"{GREEN}✅ Full message copied to Windows clipboard!{RESET}\n")

# ==============================================================================
# 📨 3. SMS Dispatch Engine
# ==============================================================================

def send_sms(number, message):
    """Sends SMS to target number."""
    if not number or not message:
        print(f"{RED}❌ Number and message are required.{RESET}")
        return
    safe_msg = message.replace('"', '\\"')
    print(f"{CYAN}📨 Sending SMS to {number}...{RESET}")
    out, err, code = run_ssh(f'termux-sms-send -n {number} "{safe_msg}"')
    if code == 0:
        print(f"{GREEN}✅ SMS dispatched successfully to {number}.{RESET}\n")
    else:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to send SMS: {err}{RESET}\n")

# ==============================================================================
# 📞 4. Phone Dialer & Call Engine (Dual Method)
# ==============================================================================

def call_number(number, speaker=False):
    """Initiates phone call reliably on Android hardware with double-quoted number parameter."""
    if not number:
        print(f"{RED}❌ Phone number required.{RESET}")
        return
    clean_num = re.sub(r'[^0-9+]', '', number)
    mode_tag = f"{YELLOW}[SPEAKER MODE 🔊]{RESET}" if speaker else f"{CYAN}[EARPIECE / NORMAL 📱]{RESET}"
    print(f"{CYAN}📞 Initiating call to \"{clean_num}\" on Blaze {mode_tag}...{RESET}")

    # Method 1: Official Termux API telephony call with strict double-quoted parameter
    out, err, code = run_ssh(f'termux-telephony-call "{clean_num}"')
    
    # Method 2: Termux URL Intent (Launches Android Dialer with number ready)
    if code != 0:
        out, err, code = run_ssh(f'termux-open-url "tel:{clean_num}"')

    if code == 0:
        if speaker:
            # Boost and trigger speaker routing if device permits
            run_ssh("termux-volume stream call 15 2>/dev/null; termux-volume stream music 15 2>/dev/null &")
        print(f"{GREEN}✅ Phone call dispatched on Blaze for \"{clean_num}\".{RESET}")
        print(f"{DIM}💡 Check your phone screen if Android requires manual SIM slot confirmation.{RESET}\n")
    else:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to trigger phone call: {err}{RESET}\n")

# ==============================================================================
# 📇 5. Contacts & Address Book (FZF & Direct CLI)
# ==============================================================================

def search_contacts(query="", json_mode=False):
    """Searches phone contacts."""
    out, err, code = run_ssh("termux-contact-list")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to fetch contacts.{RESET}")
        return []
    try:
        contacts = json.loads(out)
        if query:
            q = query.lower()
            filtered = [c for c in contacts if q in (c.get("name") or "").lower() or q in (c.get("number") or "")]
        else:
            filtered = contacts

        if json_mode:
            print(json.dumps(filtered, indent=2))
            return filtered

        print(f"\n{BOLD}{CYAN}📇 CONTACTS ({len(filtered)} Found){RESET}")
        print("─" * 60)
        for i, c in enumerate(filtered[:25], 1):
            print(f"{GREEN}[{i:02d}]{RESET} {BOLD}{c.get('name')}{RESET} ──► {c.get('number')}")
        if len(filtered) > 25:
            print(f"{DIM}... and {len(filtered)-25} more (use query to filter).{RESET}")
        print("─" * 60 + "\n")
        return filtered
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return []

def contacts_fzf_interactive():
    """FZF Address Book Search with instant Call, SMS, or Copy Number."""
    print(f"{CYAN}📇 Loading contacts from Blaze...{RESET}")
    out, err, code = run_ssh("termux-contact-list")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to load contacts.{RESET}")
        return

    try:
        contacts = json.loads(out)
    except Exception:
        print(f"{RED}❌ Could not parse contacts.{RESET}")
        return

    fzf_lines = []
    for idx, c in enumerate(contacts):
        name = c.get("name") or "Unknown"
        num = c.get("number") or "No Number"
        fzf_lines.append(f"{idx+1:03d}. {name:<26} │ {num}")

    chosen = run_fzf(fzf_lines, prompt="Search Contacts > ", header="📇 ADDRESS BOOK (Type to filter | Enter to select | Esc to back)")
    if not chosen:
        return

    match = re.match(r'^(\d+)\.', chosen)
    if not match:
        return

    idx = int(match.group(1)) - 1
    c = contacts[idx]
    name = c.get("name", "Unknown")
    num = c.get("number", "")

    action_items = [
        f"1. 📞 Call {name} (Normal)      ──► Cellular call via earpiece",
        f"2. 🔊 Call {name} (Speaker)     ──► Cellular call on Speakerphone",
        f"3. 📨 Send SMS to {name}        ──► Compose and dispatch text",
        f"4. 📋 Copy Number ({num})       ──► Copy to PC clipboard",
        "0. 🔙 Back                       ──► Return to address book"
    ]
    chosen_action = run_fzf(action_items, prompt=f"Action on {name} > ", header=f"Contact: {name} ({num})")
    if not chosen_action or "0. 🔙" in chosen_action:
        return

    if "1. 📞 Call" in chosen_action:
        call_number(num, speaker=False)
    elif "2. 🔊 Call" in chosen_action:
        call_number(num, speaker=True)
    elif "Send SMS" in chosen_action:
        try:
            msg = input(f"Message for {name}: ").strip()
            if msg:
                send_sms(num, msg)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
    elif "Copy Number" in chosen_action:
        set_clipboard(num)
        print(f"{GREEN}✅ Phone number '{num}' copied to Windows clipboard!{RESET}\n")

# ==============================================================================
# 📜 6. Call History & Logs (Latest First + FZF)
# ==============================================================================

def view_call_logs(limit=15, json_mode=False):
    """Displays call logs strictly sorted latest first."""
    out, err, code = run_ssh(f"termux-call-log -l {limit}")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to fetch call logs.{RESET}")
        return []
    try:
        raw_logs = json.loads(out)
        logs = sorted(raw_logs, key=lambda x: str(x.get("date", "")), reverse=True)
        if json_mode:
            print(json.dumps(logs, indent=2))
            return logs
        print(f"\n{BOLD}{CYAN}📞 BLAZE CALL HISTORY (Latest {len(logs)} - Newest First){RESET}")
        print("─" * 65)
        for i, c in enumerate(logs, 1):
            name = c.get("name") or c.get("phone_number", "Unknown")
            num = c.get("phone_number", "")
            ctype = c.get("type", "").upper()
            date = c.get("date", "")
            duration = c.get("duration", "0")
            
            icon = "🟢" if "INCOMING" in ctype else ("🔵" if "OUTGOING" in ctype else "🔴")
            print(f"{icon} {GREEN}[{i:02d}]{RESET} {BOLD}{name}{RESET} ({num}) | {ctype} | {duration}s | {DIM}{date}{RESET}")
        print("─" * 65 + "\n")
        return logs
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return []

def call_logs_fzf_interactive():
    """FZF Call Log Browser strictly sorted latest first with 1-click Call Back or SMS."""
    print(f"{CYAN}📜 Fetching call history from Blaze...{RESET}")
    out, err, code = run_ssh("termux-call-log -l 40")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to load call logs.{RESET}")
        return

    try:
        raw_logs = json.loads(out)
        logs = sorted(raw_logs, key=lambda x: str(x.get("date", "")), reverse=True)
    except Exception:
        print(f"{RED}❌ Could not parse call logs.{RESET}")
        return

    fzf_lines = []
    for idx, c in enumerate(logs):
        name = c.get("name") or c.get("phone_number", "Unknown")
        num = c.get("phone_number", "")
        ctype = c.get("type", "").upper()
        date = c.get("date", "")
        duration = c.get("duration", "0")
        fzf_lines.append(f"{idx+1:02d}. {name:<22} │ {num:<14} │ {ctype:<9} │ {duration} │ {date}")

    chosen = run_fzf(fzf_lines, prompt="Select Call Log > ", header="📜 CALL HISTORY (Newest First | Type to search | Enter to select | Esc to back)")
    if not chosen:
        return

    match = re.match(r'^(\d+)\.', chosen)
    if not match:
        return

    idx = int(match.group(1)) - 1
    c = logs[idx]
    name = c.get("name") or c.get("phone_number", "Unknown")
    num = c.get("phone_number", "")

    action_items = [
        f"1. 📞 Call Back (Normal)        ──► Redial number via earpiece",
        f"2. 🔊 Call Back (Speaker)       ──► Redial number on Speakerphone",
        f"3. 📨 Send SMS to {name}        ──► Dispatch SMS message",
        f"4. 📋 Copy Number ({num})       ──► Copy to PC clipboard",
        "0. 🔙 Back                       ──► Return to call history"
    ]
    chosen_action = run_fzf(action_items, prompt=f"Action on {name} > ", header=f"Call Log: {name} ({num})")
    if not chosen_action or "0. 🔙" in chosen_action:
        return

    if "1. 📞 Call" in chosen_action:
        call_number(num, speaker=False)
    elif "2. 🔊 Call" in chosen_action:
        call_number(num, speaker=True)
    elif "Send SMS" in chosen_action:
        try:
            msg = input(f"Message for {name}: ").strip()
            if msg:
                send_sms(num, msg)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
    elif "Copy Number" in chosen_action:
        set_clipboard(num)
        print(f"{GREEN}✅ Phone number '{num}' copied to Windows clipboard!{RESET}\n")

# ==============================================================================
# 📡 7. 5G NR / LTE Cell Tower Telemetry
# ==============================================================================

def get_cell_info(json_mode=False):
    """Displays 5G NR / LTE cell tower diagnostics."""
    out, err, code = run_ssh("termux-telephony-cellinfo")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to retrieve cell tower telemetry.{RESET}")
        return
    try:
        data = json.loads(out)
        if json_mode:
            print(json.dumps(data, indent=2))
            return
        print(f"\n{BOLD}{CYAN}📡 5G / CELLULAR TELEMETRY RADAR{RESET}")
        print("─" * 60)
        for cell in data:
            ctype = cell.get("type", "Unknown")
            registered = cell.get("registered", False)
            reg_badge = f"{GREEN}[REGISTERED / ACTIVE]{RESET}" if registered else f"{DIM}[NEIGHBOR]{RESET}"
            print(f"• {BOLD}Radio Type:{RESET} {CYAN}{ctype.upper()}{RESET} {reg_badge}")
            for k, v in cell.items():
                if k not in ["type", "registered"]:
                    print(f"  └─ {k}: {v}")
        print("─" * 60 + "\n")
    except Exception:
        print(out)

# ==============================================================================
# 📱 8. SIM & Telephony Hardware Specs
# ==============================================================================

def get_device_info(json_mode=False):
    """Displays SIM and telephony hardware info."""
    out, err, code = run_ssh("termux-telephony-deviceinfo")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        else:
            print(f"{RED}❌ Failed to retrieve device info.{RESET}")
        return
    try:
        data = json.loads(out)
        if json_mode:
            print(json.dumps(data, indent=2))
            return
        print(f"\n{BOLD}{CYAN}📱 HARDWARE & SIM TELEPHONY SPECS{RESET}")
        print("─" * 60)
        for k, v in data.items():
            print(f"• {BOLD}{k.replace('_', ' ').title()}:{RESET} {v}")
        print("─" * 60 + "\n")
    except Exception:
        print(out)

# ==============================================================================
# 📖 Help Manual
# ==============================================================================

def show_help_manual(pause=True):
    """Displays formatted command reference."""
    print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-PHONE COMMAND & CLI REFERENCE                 │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-phone (Runs FZF control hub)│
│ • Extract OTP:       blaze-phone --otp                 │
│ • View SMS Inbox:    blaze-phone --sms                 │
│ • Send SMS:          blaze-phone --send-sms <num> <msg>│
│ • Dial Normal Call:  blaze-phone --call <number>       │
│ • Dial Speaker Call: blaze-phone --speaker <number>    │
│ • Search Contacts:   blaze-phone --contacts [query]    │
│ • Call Logs:         blaze-phone --logs                │
│ • 5G Cell Towers:    blaze-phone --cell                │
│ • SIM Hardware:      blaze-phone --device              │
│ • JSON Machine Mode: blaze-phone --json                │
└────────────────────────────────────────────────────────┘{RESET}
""")
    if pause:
        try:
            input("Press Enter to return...")
        except (KeyboardInterrupt, EOFError):
            pass

# ==============================================================================
# 🌟 Interactive Main Command Hub
# ==============================================================================

def make_call_interactive():
    """Interactive Call starter with Normal and Speakerphone choices."""
    options = [
        "1. 📇 Select Contact from Address Book  ──► Search & choose call mode",
        "2. 📜 Select from Recent Call Logs      ──► Redial & choose call mode",
        "3. 📱 Type Number (Normal Earpiece)     ──► Manual dial prompt",
        "4. 🔊 Type Number (Speakerphone Mode)   ──► Manual dial on Speaker",
        "0. 🔙 Cancel                            ──► Return to main menu"
    ]
    chosen = run_fzf(options, prompt="Call Method > ", header="📞 INITIATE CALL")
    if not chosen or "0. 🔙" in chosen:
        return

    if "1. 📇" in chosen:
        contacts_fzf_interactive()
    elif "2. 📜" in chosen:
        call_logs_fzf_interactive()
    elif "3. 📱" in chosen:
        try:
            num = input("Phone Number to Dial (Normal): ").strip()
            if num:
                call_number(num, speaker=False)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Action cancelled.{RESET}\n")
    elif "4. 🔊" in chosen:
        try:
            num = input("Phone Number to Dial (Speaker): ").strip()
            if num:
                call_number(num, speaker=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Action cancelled.{RESET}\n")

def send_sms_interactive():
    """Interactive SMS starter."""
    options = [
        "1. 📇 Select Recipient from Address Book──► Search and compose",
        "2. ⌨️ Type Recipient Number Directly    ──► Manual number prompt",
        "0. 🔙 Cancel                            ──► Return to main menu"
    ]
    chosen = run_fzf(options, prompt="SMS Recipient > ", header="📨 COMPOSE SMS")
    if not chosen or "0. 🔙" in chosen:
        return

    if "1. 📇" in chosen:
        contacts_fzf_interactive()
    else:
        try:
            num = input("Target Number: ").strip()
            msg = input("Message Body: ").strip()
            if num and msg:
                send_sms(num, msg)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Action cancelled.{RESET}\n")

def interactive_menu():
    """Displays interactive FZF menu."""
    menu_items = [
        "🔑 1. 1-Click OTP Extractor       ──► Auto-extract & copy latest OTP to PC",
        "📬 2. Interactive SMS Inbox       ──► Browse & search SMS messages (FZF)",
        "📨 3. Send SMS Message           ──► Pick contact or type number & message",
        "📇 4. Search Address Book         ──► Instant fuzzy search & dial / SMS (FZF)",
        "📞 5. Dial Phone / Make Call      ──► Initiate native cellular call on Blaze",
        "📜 6. View Call History           ──► Browse call logs & 1-click callback (FZF)",
        "📡 7. 5G NR & Cell Telemetry      ──► View live carrier & tower radio signals",
        "📱 8. SIM & Telephony Specs       ──► Inspect baseband hardware & operator",
        "📖 9. Help & CLI Reference        ──► Command switches, options & examples",
        "🚪 0. Exit                       ──► Return to PowerShell terminal"
    ]

    while True:
        try:
            chosen = run_fzf(menu_items, prompt="Blaze Phone > ", header="📱 BLAZE TELEPHONY & CELLULAR COMMAND HUB")
            if not chosen or "0. Exit" in chosen:
                print(f"{DIM}👋 Exited.{RESET}\n")
                break

            if "1. 1-Click OTP" in chosen:
                get_otp()
            elif "2. Interactive SMS" in chosen:
                sms_fzf_interactive()
            elif "3. Send SMS" in chosen:
                send_sms_interactive()
            elif "4. Search Address" in chosen:
                contacts_fzf_interactive()
            elif "5. Dial Phone" in chosen:
                make_call_interactive()
            elif "6. View Call" in chosen:
                call_logs_fzf_interactive()
            elif "7. 5G NR" in chosen:
                get_cell_info()
            elif "8. SIM & Telephony" in chosen:
                get_device_info()
            elif "9. Help" in chosen:
                show_help_manual(pause=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}\n")
            break

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blaze Telephony, SMS, Contacts & Cellular Command Center",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("--otp", action="store_true", help="Extract latest SMS OTP and copy to PC clipboard")
        parser.add_argument("--sms", action="store_true", help="View SMS inbox")
        parser.add_argument("--send-sms", nargs=2, metavar=("NUMBER", "MESSAGE"), help="Send SMS to recipient")
        parser.add_argument("--call", metavar="NUMBER", help="Dial a phone number on Blaze (Normal Earpiece)")
        parser.add_argument("--speaker", metavar="NUMBER", help="Dial a phone number on Blaze (Speakerphone Mode)")
        parser.add_argument("--contacts", nargs="?", const="", metavar="QUERY", help="Search address book contacts")
        parser.add_argument("--logs", action="store_true", help="View recent incoming/outgoing/missed call logs")
        parser.add_argument("--cell", action="store_true", help="Dump 5G NR and LTE cell tower telemetry")
        parser.add_argument("--device", action="store_true", help="Dump SIM and telephony hardware specs")
        parser.add_argument("--json", action="store_true", help="Output results in clean JSON for automation")
        parser.add_argument("--raw", action="store_true", help="Output raw value (e.g. bare OTP code)")

        args = parser.parse_args()

        if args.otp:
            get_otp(json_mode=args.json, raw_mode=args.raw)
        elif args.sms:
            list_sms(json_mode=args.json)
        elif args.send_sms:
            send_sms(args.send_sms[0], args.send_sms[1])
        elif args.call:
            call_number(args.call, speaker=False)
        elif args.speaker:
            call_number(args.speaker, speaker=True)
        elif args.contacts is not None:
            search_contacts(args.contacts, json_mode=args.json)
        elif args.logs:
            view_call_logs(json_mode=args.json)
        elif args.cell:
            get_cell_info(json_mode=args.json)
        elif args.device:
            get_device_info(json_mode=args.json)
        else:
            interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Exited gracefully.{RESET}")

if __name__ == "__main__":
    main()
