#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📱 Blaze Telephony, SMS, Contacts & 5G Cellular Command Hub
Author: Antigravity Assistant & Karan Singh Verma
Project: Blaze (Motobook ⇄ Lava Blaze 5G Node)
Dual Mode: Fast-Path CLI switches & Rich Interactive Terminal Menu
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

def run_ssh(cmd, timeout=6):
    """Executes command on Blaze over SSH with safe timeout."""
    try:
        res = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "StrictHostKeyChecking=no", "blaze", cmd],
            capture_output=True, text=True, timeout=timeout + 2, encoding="utf-8", errors="replace"
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

# --- Telephony Features ---

def get_otp(json_mode=False, raw_mode=False):
    """Scans SMS inbox, extracts latest 4-8 digit OTP code, and copies to PC clipboard."""
    out, err, code = run_ssh("termux-sms-list -l 10 -t inbox")
    if code != 0 or not out:
        if json_mode:
            print(json.dumps({"error": "Failed to retrieve SMS", "details": err}))
        else:
            print(f"{RED}❌ Failed to fetch SMS inbox from Blaze.{RESET} ({err})")
        return None

    try:
        messages = json.loads(out)
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
            print(f"{YELLOW}⚠️ No recent OTP found in the latest 10 messages.{RESET}")
        return None

def list_sms(limit=10, json_mode=False):
    """Displays formatted SMS messages."""
    out, err, code = run_ssh(f"termux-sms-list -l {limit} -t inbox")
    if code != 0 or not out:
        print(f"{RED}❌ Failed to fetch SMS inbox.{RESET}")
        return
    try:
        messages = json.loads(out)
        if json_mode:
            print(json.dumps(messages, indent=2))
            return
        print(f"\n{BOLD}{CYAN}📬 BLAZE SMS INBOX (Latest {len(messages)}){RESET}")
        print("─" * 60)
        for i, m in enumerate(messages, 1):
            sender = m.get("number", "Unknown")
            body = m.get("body", "").replace("\n", " ")
            received = m.get("received", "")
            print(f"{GREEN}[{i:02d}]{RESET} {BOLD}{sender}{RESET} {DIM}({received}){RESET}")
            print(f"    {body[:100]}{'...' if len(body) > 100 else ''}")
        print("─" * 60 + "\n")
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")

def send_sms(number, message):
    """Sends SMS to target number."""
    if not number or not message:
        print(f"{RED}❌ Number and message are required.{RESET}")
        return
    # Escape quotes
    safe_msg = message.replace('"', '\\"')
    print(f"{CYAN}📨 Sending SMS to {number}...{RESET}")
    out, err, code = run_ssh(f'termux-sms-send -n {number} "{safe_msg}"')
    if code == 0:
        print(f"{GREEN}✅ SMS dispatched successfully to {number}.{RESET}")
    else:
        print(f"{RED}❌ Failed to send SMS: {err}{RESET}")

def call_number(number):
    """Initiates phone call."""
    if not number:
        print(f"{RED}❌ Phone number required.{RESET}")
        return
    print(f"{CYAN}📞 Dialing {number} on Blaze...{RESET}")
    out, err, code = run_ssh(f"termux-telephony-call {number}")
    if code == 0:
        print(f"{GREEN}✅ Call initiated on Blaze.{RESET}")
    else:
        print(f"{RED}❌ Failed to dial: {err}{RESET}")

def view_call_logs(limit=10, json_mode=False):
    """Displays call logs."""
    out, err, code = run_ssh(f"termux-call-log -l {limit}")
    if code != 0 or not out:
        print(f"{RED}❌ Failed to fetch call logs.{RESET}")
        return
    try:
        logs = json.loads(out)
        if json_mode:
            print(json.dumps(logs, indent=2))
            return
        print(f"\n{BOLD}{CYAN}📞 BLAZE CALL HISTORY (Latest {len(logs)}){RESET}")
        print("─" * 60)
        for i, c in enumerate(logs, 1):
            name = c.get("name") or c.get("phone_number", "Unknown")
            num = c.get("phone_number", "")
            ctype = c.get("type", "").upper()
            date = c.get("date", "")
            duration = c.get("duration", "0")
            
            icon = "🟢" if "INCOMING" in ctype else ("🔵" if "OUTGOING" in ctype else "🔴")
            print(f"{icon} {BOLD}{name}{RESET} ({num}) | {ctype} | {duration}s | {DIM}{date}{RESET}")
        print("─" * 60 + "\n")
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")

def search_contacts(query="", json_mode=False):
    """Searches phone contacts."""
    out, err, code = run_ssh("termux-contact-list")
    if code != 0 or not out:
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

def get_cell_info(json_mode=False):
    """Displays 5G NR / LTE cell tower diagnostics."""
    out, err, code = run_ssh("termux-telephony-cellinfo")
    if code != 0 or not out:
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

def get_device_info(json_mode=False):
    """Displays SIM and telephony hardware info."""
    out, err, code = run_ssh("termux-telephony-deviceinfo")
    if code != 0 or not out:
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

# --- Interactive Menu ---

def interactive_menu():
    """Displays interactive ASCII menu for terminal users."""
    while True:
        print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│         📱 BLAZE TELEPHONY & CELLULAR COMMAND HUB      │
├────────────────────────────────────────────────────────┤
│  {BOLD}1{RESET} 🔑 1-Click OTP Extractor (Copies to PC Clipboard)  │
│  {BOLD}2{RESET} 📬 View Recent SMS Inbox                            │
│  {BOLD}3{RESET} 📨 Send SMS Message                                 │
│  {BOLD}4{RESET} 📇 Search Contacts & Address Book                   │
│  {BOLD}5{RESET} 📞 Dial Phone Number                                │
│  {BOLD}6{RESET} 📜 View Call History & Callback                     │
│  {BOLD}7{RESET} 📡 5G NR / LTE Cell Tower Telemetry                 │
│  {BOLD}8{RESET} 📱 SIM & Baseband Hardware Specs                    │
│  {BOLD}0{RESET} 🚪 Exit                                             │
└────────────────────────────────────────────────────────┘{RESET}""")
        try:
            choice = input(f"{BOLD}Blaze-Phone ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            get_otp()
        elif choice == "2":
            list_sms()
        elif choice == "3":
            num = input(f"Target Number: ").strip()
            msg = input(f"Message Body: ").strip()
            if num and msg:
                send_sms(num, msg)
        elif choice == "4":
            q = input(f"Search Query (blank for all): ").strip()
            contacts = search_contacts(q)
        elif choice == "5":
            num = input(f"Phone Number to Dial: ").strip()
            if num:
                call_number(num)
        elif choice == "6":
            view_call_logs()
        elif choice == "7":
            get_cell_info()
        elif choice == "8":
            get_device_info()
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid option. Select 0-8.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Telephony, SMS, Contacts & Cellular Command Center",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--otp", action="store_true", help="Extract latest SMS OTP and copy to PC clipboard")
    parser.add_argument("--sms", action="store_true", help="View SMS inbox")
    parser.add_argument("--send-sms", nargs=2, metavar=("NUMBER", "MESSAGE"), help="Send SMS to recipient")
    parser.add_argument("--call", metavar="NUMBER", help="Dial a phone number on Blaze")
    parser.add_argument("--contacts", nargs="?", const="", metavar="QUERY", help="Search address book contacts")
    parser.add_argument("--logs", action="store_true", help="View recent incoming/outgoing/missed call logs")
    parser.add_argument("--cell", action="store_true", help="Dump 5G NR and LTE cell tower telemetry")
    parser.add_argument("--device", action="store_true", help="Dump SIM and telephony hardware specs")
    parser.add_argument("--json", action="store_true", help="Output results in clean JSON for automation")
    parser.add_argument("--raw", action="store_true", help="Output raw value (e.g. bare OTP code)")

    args = parser.parse_args()

    # Fast-Path Flag Execution
    if args.otp:
        get_otp(json_mode=args.json, raw_mode=args.raw)
    elif args.sms:
        list_sms(json_mode=args.json)
    elif args.send_sms:
        send_sms(args.send_sms[0], args.send_sms[1])
    elif args.call:
        call_number(args.call)
    elif args.contacts is not None:
        search_contacts(args.contacts, json_mode=args.json)
    elif args.logs:
        view_call_logs(json_mode=args.json)
    elif args.cell:
        get_cell_info(json_mode=args.json)
    elif args.device:
        get_device_info(json_mode=args.json)
    else:
        # Default: Interactive Mode
        interactive_menu()

if __name__ == "__main__":
    main()
