#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 Blaze System Telemetry, Battery, Wi-Fi & Storage Status Radar
Author: Antigravity Assistant & Karan Singh Verma
Project: Blaze (Motobook ⇄ Lava Blaze 5G Node)
Dual Mode: Clean Left-Anchored Terminal HUD (1 datum per line, symmetrical spacing) & Fast-Path JSON
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
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

def run_ssh_multi(timeout=5):
    """Runs multiple telemetry queries in a single bundled SSH call for sub-second execution."""
    bundled_cmd = (
        "echo '===BATTERY==='; timeout 1.5 termux-battery-status 2>/dev/null || echo '{}'; "
        "echo '===WIFI==='; timeout 1.5 termux-wifi-connectioninfo 2>/dev/null || echo '{}'; "
        "echo '===STORAGE==='; df -h /sdcard 2>/dev/null | tail -n 1; "
        "echo '===UPTIME==='; uptime -p 2>/dev/null || uptime 2>/dev/null"
    )
    try:
        res = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "StrictHostKeyChecking=no", "blaze", bundled_cmd],
            capture_output=True, text=True, timeout=timeout + 2, encoding="utf-8", errors="replace"
        )
        return res.stdout, res.returncode
    except Exception:
        return "", 255

def parse_telemetry(raw_output):
    """Parses bundled output sections."""
    sections = {}
    current_key = None
    lines = []
    
    for line in raw_output.splitlines():
        if line.startswith("===") and line.endswith("==="):
            if current_key:
                sections[current_key] = "\n".join(lines).strip()
            current_key = line.strip("=").strip()
            lines = []
        else:
            lines.append(line)
    if current_key:
        sections[current_key] = "\n".join(lines).strip()
    return sections

def format_battery_bar(percentage):
    pct = max(0, min(100, percentage))
    filled = int(pct / 10)
    bar = "█" * filled + "░" * (10 - filled)
    col = GREEN if pct > 40 else (YELLOW if pct > 20 else RED)
    return f"{col}[{bar}] {pct}%{RESET}"

def format_signal_bar(rssi):
    if rssi == 0 or rssi < -95:
        return f"{RED}[░░░░░] No Signal{RESET}"
    bars = "█████" if rssi > -55 else ("████░" if rssi > -67 else ("███░░" if rssi > -75 else ("██░░░" if rssi > -85 else "█░░░░")))
    col = GREEN if rssi > -65 else (YELLOW if rssi > -78 else RED)
    return f"{col}[{bars}] {rssi} dBm{RESET}"

def display_dashboard(sections, json_mode=False, battery_only=False, wifi_only=False, storage_only=False, raw_mode=False):
    # Parse Battery
    battery_data = {}
    try:
        battery_data = json.loads(sections.get("BATTERY", "{}"))
    except Exception:
        pass

    # Parse Wi-Fi
    wifi_data = {}
    try:
        wifi_data = json.loads(sections.get("WIFI", "{}"))
    except Exception:
        pass

    # Parse Storage
    storage_raw = sections.get("STORAGE", "").split()
    storage_info = {"total": "Unknown", "used": "Unknown", "free": "Unknown", "pct": "Unknown"}
    if len(storage_raw) >= 5:
        storage_info = {
            "total": storage_raw[1],
            "used": storage_raw[2],
            "free": storage_raw[3],
            "pct": storage_raw[4]
        }

    uptime_str = sections.get("UPTIME", "Unknown").replace("up ", "")

    if json_mode:
        payload = {
            "device": "Lava Blaze 5G (Android 14)",
            "battery": battery_data,
            "wifi": wifi_data,
            "storage": storage_info,
            "uptime": uptime_str
        }
        print(json.dumps(payload, indent=2))
        return

    if raw_mode:
        print(battery_data.get("percentage", 0))
        return

    # Extract clean fields
    pct = battery_data.get("percentage", 0)
    status = battery_data.get("status", "Unknown").upper()
    plugged = battery_data.get("plugged", "UNPLUGGED").upper()
    temp = battery_data.get("temperature", 0)
    health = battery_data.get("health", "GOOD").upper()

    charge_icon = "⚡" if status == "CHARGING" else "🔋"
    charge_str = f"{GREEN}Charging ({plugged}){RESET}" if status == "CHARGING" else f"{YELLOW}Discharging{RESET}"

    ssid = wifi_data.get("ssid", "<Unknown>").strip('"')
    rssi = wifi_data.get("rssi", 0)
    speed = wifi_data.get("link_speed_mbps", 0)
    ip = wifi_data.get("ip", "Unknown")
    freq = wifi_data.get("frequency_mhz", 0)
    band = "5 GHz" if freq > 4000 else ("2.4 GHz" if freq > 2000 else "Wi-Fi")

    # Filter: Battery Only
    if battery_only:
        print(f"\n{CYAN}┌── 🔋 BLAZE BATTERY & POWER TELEMETRY ────────────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│ {charge_icon}  {BOLD}Charge Level:{RESET}       {format_battery_bar(pct)}")
        print(f"│ 🔌 {BOLD}Power State:{RESET}        {charge_str}")
        print(f"│ 🌡️  {BOLD}Temperature:{RESET}        {temp}°C")
        print(f"│ 🩺 {BOLD}Battery Health:{RESET}     {health}")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└──{RESET}\n")
        return

    # Filter: Wi-Fi Only
    if wifi_only:
        print(f"\n{CYAN}┌── 📶 BLAZE NETWORK & WIRELESS RADAR ─────────────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│ 🌐 {BOLD}Access Point:{RESET}       {CYAN}{BOLD}{ssid}{RESET}")
        print(f"│ 📻 {BOLD}Frequency Band:{RESET}     {band} ({freq} MHz)")
        print(f"│ 📡 {BOLD}Signal Strength:{RESET}    {format_signal_bar(rssi)}")
        print(f"│ ⚡ {BOLD}Link Throughput:{RESET}    {speed} Mbps")
        print(f"│ 💻 {BOLD}Local IP Address:{RESET}   {GREEN}{ip}{RESET} (Port 8022/SSH)")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└──{RESET}\n")
        return

    # Filter: Storage Only
    if storage_only:
        print(f"\n{CYAN}┌── 💾 BLAZE STORAGE TELEMETRY (/sdcard) ──────────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│ 📁 {BOLD}Used Space:{RESET}         {storage_info['used']} / {storage_info['total']} ({storage_info['pct']})")
        print(f"│ 🟢 {BOLD}Available Space:{RESET}    {GREEN}{storage_info['free']}{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└──{RESET}\n")
        return

    # Full Visual HUD (Single-Column, Left-Anchored, Symmetrical Spacing)
    print()
    print(f"{CYAN}┌── 📱 BLAZE HARDWARE & TELEMETRY RADAR ────────────────────────{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"│ 📱 {BOLD}Device Model:{RESET}       Lava Blaze 5G (Android 14)")
    print(f"│ ⏱️  {BOLD}System Uptime:{RESET}      {uptime_str}")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}├── 🔋 Battery & Power ─────────────────────────────────────────{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"│ {charge_icon}  {BOLD}Charge Level:{RESET}       {format_battery_bar(pct)}")
    print(f"│ 🔌 {BOLD}Power State:{RESET}        {charge_str}")
    print(f"│ 🌡️  {BOLD}Temperature:{RESET}        {temp}°C")
    print(f"│ 🩺 {BOLD}Battery Health:{RESET}     {health}")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}├── 📶 Network & Wireless Connectivity ─────────────────────────{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"│ 🌐 {BOLD}Access Point:{RESET}       {CYAN}{BOLD}{ssid}{RESET}")
    print(f"│ 📻 {BOLD}Frequency Band:{RESET}     {band} ({freq} MHz)")
    print(f"│ 📡 {BOLD}Signal Strength:{RESET}    {format_signal_bar(rssi)}")
    print(f"│ ⚡ {BOLD}Link Throughput:{RESET}    {speed} Mbps")
    print(f"│ 💻 {BOLD}Local IP Address:{RESET}   {GREEN}{ip}{RESET} (Port 8022/SSH)")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}├── 💾 Storage & Filesystem (/sdcard) ──────────────────────────{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"│ 📁 {BOLD}Storage Usage:{RESET}      {storage_info['used']} / {storage_info['total']} ({storage_info['pct']})")
    print(f"│ 🟢 {BOLD}Available Space:{RESET}    {GREEN}{storage_info['free']}{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}└── 🚀 Node Live & Operational{RESET}")
    print()

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Hardware Telemetry, Battery, Wi-Fi & Storage Status Radar",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--battery", action="store_true", help="Display only battery metrics")
    parser.add_argument("--wifi", action="store_true", help="Display only Wi-Fi metrics")
    parser.add_argument("--storage", action="store_true", help="Display only storage metrics")
    parser.add_argument("--json", action="store_true", help="Output complete telemetry in JSON format")
    parser.add_argument("--raw", action="store_true", help="Output bare battery percentage value")

    args = parser.parse_args()

    raw_out, code = run_ssh_multi(timeout=4)
    if code != 0 or not raw_out:
        if args.json:
            print(json.dumps({"error": "Failed to reach Blaze over SSH :8022"}))
        else:
            print()
            print(f"{RED}┌── ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022 ─────────────────────{RESET}")
            print(f"{RED}│{RESET}")
            print(f"│ • Root Cause: Phone offline or SSH daemon (sshd) not running.")
            print(f"│ • Action:     1. Ensure Termux is active on Blaze.")
            print(f"│               2. Run 'sshd' in Termux.")
            print(f"│               3. Ensure phone is connected to same Wi-Fi / Hotspot.")
            print(f"{RED}│{RESET}")
            print(f"{RED}└── ⏱️ Connection Timeout (4s){RESET}")
            print()
        return

    sections = parse_telemetry(raw_out)
    display_dashboard(
        sections,
        json_mode=args.json,
        battery_only=args.battery,
        wifi_only=args.wifi,
        storage_only=args.storage,
        raw_mode=args.raw
    )

if __name__ == "__main__":
    main()
