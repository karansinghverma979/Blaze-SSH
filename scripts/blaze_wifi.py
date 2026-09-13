#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 Blaze Wireless, Network Radar, Scrcpy Streaming & ADB Hub
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
        return "", "Connection timed out. Blaze may be offline.", 255
    except Exception as e:
        return "", str(e), 1

def run_fzf(options, prompt="Blaze Wi-Fi > ", header=None):
    """Runs inline interactive FZF fuzzy picker directly beneath the cursor in active terminal."""
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

def get_blaze_ip():
    """Detects active IP address of Blaze across Wi-Fi, Hotspot, and Cellular interfaces."""
    out, err, code = run_ssh("termux-wifi-connectioninfo")
    if code == 0 and out:
        try:
            data = json.loads(out)
            wifi_ip = data.get("ip")
            if wifi_ip and wifi_ip != "0.0.0.0":
                return wifi_ip
        except Exception:
            pass

    out_if, _, code_if = run_ssh("ifconfig")
    if code_if == 0 and out_if:
        ap_match = re.search(r'ap0.*?inet\s+([0-9.]+)', out_if, re.DOTALL)
        if ap_match:
            return ap_match.group(1)
        wlan_match = re.search(r'wlan0.*?inet\s+([0-9.]+)', out_if, re.DOTALL)
        if wlan_match:
            return wlan_match.group(1)

    return "10.154.149.220" # fallback to typical hotspot gateway

# --- Wi-Fi & Hotspot Radar ---

def get_wifi_info(json_mode=False):
    """Displays active Wi-Fi connection info, Hotspot state, and signal metrics."""
    out, err, code = run_ssh("termux-wifi-connectioninfo")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        elif json_mode:
            print(json.dumps({"error": "Failed to get Wi-Fi info", "details": err}))
        else:
            print(f"{RED}❌ Failed to fetch Wi-Fi connection info.{RESET} ({err})")
        return None

    try:
        data = json.loads(out)
        ssid = data.get("ssid", "<Unknown>").strip('"')
        bssid = data.get("bssid", "Unknown")
        rssi = data.get("rssi", 0)
        speed = data.get("link_speed_mbps", 0)
        wifi_ip = data.get("ip", "0.0.0.0")
        freq = data.get("frequency_mhz", 0)
        supplicant = data.get("supplicant_state", "UNKNOWN")

        # Check interface details if Wi-Fi client is uninitialized (Hotspot mode)
        is_hotspot = False
        active_ip = wifi_ip
        if wifi_ip == "0.0.0.0" or ssid == "<unknown ssid>" or supplicant == "UNINITIALIZED":
            out_if, _, _ = run_ssh("ifconfig")
            if "ap0:" in out_if:
                is_hotspot = True
                ap_m = re.search(r'ap0.*?inet\s+([0-9.]+)', out_if, re.DOTALL)
                if ap_m:
                    active_ip = ap_m.group(1)

        if json_mode:
            res_dict = {
                "mode": "Mobile Hotspot AP" if is_hotspot else "Wi-Fi Client",
                "ssid": "Mobile Hotspot (Active)" if is_hotspot else ssid,
                "bssid": bssid,
                "rssi": rssi,
                "link_speed_mbps": speed,
                "frequency_mhz": freq,
                "ip": active_ip
            }
            print(json.dumps(res_dict, indent=2))
            return res_dict

        band = "5 GHz" if freq > 4000 else ("2.4 GHz" if freq > 2000 else "Auto")
        bars = "█████" if rssi > -55 else ("████░" if rssi > -67 else ("███░░" if rssi > -75 else ("██░░░" if rssi > -85 else "█░░░░")))
        sig_color = GREEN if rssi > -65 else (YELLOW if rssi > -78 else RED)

        print(f"\n{BOLD}{CYAN}📶 BLAZE WIRELESS & NETWORK RADAR{RESET}")
        print("┌────────────────────────────────────────────────────────┐")
        if is_hotspot:
            print(f"│ 📡 {BOLD}Mode:{RESET}         {GREEN}{BOLD}🔥 Mobile Hotspot (AP Active){RESET}       │")
            print(f"│ 💻 {BOLD}Hotspot IP:{RESET}   {CYAN}{BOLD}{active_ip:<38}{RESET}│")
            print(f"│ 🔗 {BOLD}Uplink:{RESET}       {MAGENTA}5G / LTE Mobile Cellular Uplink{RESET}       │")
        else:
            print(f"│ 📡 {BOLD}Mode:{RESET}         {GREEN}Wi-Fi Client Connected{RESET}                 │")
            print(f"│ 🌐 {BOLD}SSID:{RESET}         {CYAN}{BOLD}{ssid[:38]:<39}{RESET}│")
            print(f"│ 📻 {BOLD}BSSID:{RESET}        {bssid[:38]:<39}│")
            print(f"│ 📶 {BOLD}Signal:{RESET}       {sig_color}{rssi} dBm [{bars}]{RESET}{'':<20}│")
            print(f"│ ⚡ {BOLD}Throughput:{RESET}   {speed} Mbps{'':<33}│")
            print(f"│ 📻 {BOLD}Band:{RESET}         {freq} MHz ({band}){'':<26}│")
            print(f"│ 💻 {BOLD}Local IP:{RESET}     {GREEN}{active_ip:<38}{RESET}│")
        print("└────────────────────────────────────────────────────────┘\n")
        return data
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return None

def scan_wifi(json_mode=False):
    """Scans visible Wi-Fi spectrum and presents in FZF or table."""
    print(f"{CYAN}🔍 Scanning visible Wi-Fi spectrum on Blaze...{RESET}")
    out, err, code = run_ssh("termux-wifi-scaninfo")
    if code != 0 or not out:
        if code == 255:
            render_unreachable_card()
        elif json_mode:
            print(json.dumps({"error": "Wi-Fi scan failed", "details": err}))
        else:
            print(f"{RED}❌ Wi-Fi scan failed: {err}{RESET}")
            print(f"{DIM}💡 Note: If Hotspot is active, Android pauses Wi-Fi client scanning.{RESET}\n")
        return []

    try:
        networks = json.loads(out)
        if not networks:
            if json_mode:
                print(json.dumps([]))
            else:
                print(f"{YELLOW}⚠️ No visible Wi-Fi networks found (Wi-Fi client radio may be idle).{RESET}\n")
            return []

        sorted_nets = sorted(networks, key=lambda x: x.get("rssi", -100), reverse=True)
        if json_mode:
            print(json.dumps(sorted_nets, indent=2))
            return sorted_nets

        fzf_lines = []
        for i, net in enumerate(sorted_nets, 1):
            ssid = net.get("ssid", "<Hidden>") or "<Hidden>"
            bssid = net.get("bssid", "")
            rssi = net.get("rssi", 0)
            freq = net.get("frequency_mhz", 0)
            band = "5G" if freq > 4000 else "2.4G"
            fzf_lines.append(f"{i:02d}. {ssid:<24} │ {rssi:>4} dBm │ {band} │ {bssid}")

        chosen = run_fzf(fzf_lines, prompt="Wi-Fi AP > ", header="📡 VISIBLE WI-FI NETWORKS (Sorted by Signal Strength)")
        if chosen:
            match = re.match(r'^(\d+)\.', chosen)
            if match:
                idx = int(match.group(1)) - 1
                net = sorted_nets[idx]
                print(f"\n{BOLD}{CYAN}📡 ACCESS POINT DETAILS:{RESET}")
                print("┌────────────────────────────────────────────────────────┐")
                print(f"│ 🌐 {BOLD}SSID:{RESET}         {CYAN}{BOLD}{net.get('ssid', '<Hidden>'):<38}{RESET}│")
                print(f"│ 📻 {BOLD}BSSID:{RESET}        {net.get('bssid', ''):<38}│")
                print(f"│ 📶 {BOLD}Signal:{RESET}       {net.get('rssi', 0)} dBm{'':<30}│")
                print(f"│ ⚡ {BOLD}Frequency:{RESET}    {net.get('frequency_mhz', 0)} MHz{'':<28}│")
                print(f"│ 🔒 {BOLD}Capabilities:{RESET} {net.get('capabilities', 'Unknown')[:35]:<36}│")
                print("└────────────────────────────────────────────────────────┘\n")
        return sorted_nets
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")
        return []

def toggle_wifi(state):
    """Toggles Wi-Fi power state (true/false/bounce)."""
    if state == "bounce":
        print(f"\n{YELLOW}🔄 Bouncing Wi-Fi radio (Power OFF ➔ 3s wait ➔ Power ON)...{RESET}")
        run_ssh("termux-wifi-enable false")
        time.sleep(3)
        run_ssh("termux-wifi-enable true")
        print(f"{GREEN}✅ Wi-Fi radio bounced and re-initialized.{RESET}\n")
    elif state in ["on", "true"]:
        print(f"\n{CYAN}⚡ Enabling Wi-Fi radio on Blaze...{RESET}")
        run_ssh("termux-wifi-enable true")
        print(f"{GREEN}✅ Wi-Fi radio enabled.{RESET}\n")
    elif state in ["off", "false"]:
        print(f"\n{YELLOW}⚡ Disabling Wi-Fi radio on Blaze...{RESET}")
        run_ssh("termux-wifi-enable false")
        print(f"{GREEN}✅ Wi-Fi radio disabled.{RESET}\n")

# --- Wireless ADB Transport Suite ---

def is_adb_ready():
    """Checks if at least one authorized ADB device is connected."""
    try:
        res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=12)
        lines = [l.strip() for l in res.stdout.splitlines() if l.strip() and not l.startswith("List of")]
        for l in lines:
            if "\tdevice" in l or " device " in l:
                return True, l.split()[0]
            elif "unauthorized" in l:
                return False, "unauthorized"
        return False, "no_device"
    except subprocess.TimeoutExpired:
        # If ADB hung on daemon start, clean up zombie process
        subprocess.run(["taskkill", "/F", "/IM", "adb.exe"], capture_output=True)
        return False, "timeout"
    except Exception:
        return False, "adb_not_found"

def check_and_ensure_adb():
    """Validates ADB connection and provides interactive zero-crash fallback recovery."""
    ready, status = is_adb_ready()
    if ready:
        return True

    b_ip = get_blaze_ip()
    if status == "unauthorized":
        print(f"\n{YELLOW}┌────────────────────────────────────────────────────────┐{RESET}")
        print(f"{YELLOW}│ ⚠️ ADB DEVICE UNAUTHORIZED ON PHONE SCREEN             │{RESET}")
        print(f"{YELLOW}├────────────────────────────────────────────────────────┤{RESET}")
        print(f"│ • Action: Check your Blaze phone screen now.          │")
        print(f"│ • Prompt: Tap 'Always allow from this computer' ➔ OK.  │")
        print(f"{YELLOW}└────────────────────────────────────────────────────────┘{RESET}\n")
        safe_pause("Press Enter after granting permission on phone...")
        ready_retry, _ = is_adb_ready()
        return ready_retry

    # Try auto-connecting to Blaze on default port 5555
    print(f"{CYAN}🔌 Checking Wireless ADB connection to Blaze ({b_ip}:5555)...{RESET}")
    success = connect_wireless_adb(b_ip, 5555, quiet=True)
    if success:
        return True

    print(f"\n{YELLOW}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{YELLOW}│ ⚠️ WIRELESS ADB NOT CONNECTED                          │{RESET}")
    print(f"{YELLOW}├────────────────────────────────────────────────────────┤{RESET}")
    print(f"│ • Target Node: Blaze ({b_ip}:5555)                     │")
    print(f"│ • Root Cause:  Wireless debugging disabled or port off.│")
    print(f"│ • Fix Steps:   1. On Blaze: Open Developer Options.    │")
    print(f"│                2. Enable 'Wireless Debugging'.         │")
    print(f"│                3. Or plug USB once via option 2 below. │")
    print(f"{YELLOW}└────────────────────────────────────────────────────────┘{RESET}\n")

    recovery_opts = [
        "1. 🔄 Retry Connection (5555)      ──► Try default wireless port again",
        "2. ⚡ USB ➔ Wireless Setup Wizard  ──► Plug USB once to switch ADB to wireless mode",
        "3. 🔢 Enter Custom Port             ──► Connect with dynamic port (from phone)",
        "4. 🔑 Pair Device (Pairing Code)   ──► Android 11+ Wi-Fi Pairing assistant",
        "5. 🔄 Restart ADB Server           ──► Kill and restart local adb daemon",
        "0. 🔙 Return to Menu               ──► Cancel and go back"
    ]
    chosen = run_fzf(recovery_opts, prompt="Recovery Option > ", header="⚠️ ADB NOT CONNECTED - CHOOSE FIX")
    if not chosen or "0. 🔙" in chosen:
        return False

    if "1. 🔄 Retry" in chosen:
        return connect_wireless_adb(b_ip, 5555)
    elif "2. ⚡ USB" in chosen:
        return setup_usb_to_wireless_adb()
    elif "3. 🔢 Enter Custom" in chosen:
        try:
            port_str = input(f"{CYAN}Enter Port from Wireless Debugging screen: {RESET}").strip()
            if port_str and port_str.isdigit():
                return connect_wireless_adb(b_ip, int(port_str))
        except (KeyboardInterrupt, EOFError):
            pass
    elif "4. 🔑 Pair" in chosen:
        pair_wireless_adb()
        ready_after, _ = is_adb_ready()
        return ready_after
    elif "5. 🔄 Restart" in chosen:
        restart_adb_server()
        return connect_wireless_adb(b_ip, 5555)

    return False

def setup_usb_to_wireless_adb():
    """One-click wizard to switch ADB from USB to TCP/IP Wireless Mode."""
    print(f"\n{BOLD}{CYAN}⚡ 1-CLICK USB ➔ WIRELESS ADB SWITCH WIZARD{RESET}")
    print("┌────────────────────────────────────────────────────────┐")
    print("│ 1. Connect your Blaze phone to PC via USB cable.       │")
    print("│ 2. Ensure USB Debugging is enabled on phone.          │")
    print("└────────────────────────────────────────────────────────┘")
    safe_pause("Press Enter once USB is connected...")

    try:
        res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=12)
        lines = [l.strip() for l in res.stdout.splitlines() if l.strip() and not l.startswith("List of")]
        usb_devices = [l for l in lines if not l.startswith("10.") and not l.startswith("192.") and "\tdevice" in l]

        if not usb_devices:
            unauth = [l for l in lines if "unauthorized" in l]
            if unauth:
                print(f"\n{YELLOW}⚠️ USB Device detected but UNAUTHORIZED on phone screen.{RESET}")
                print(f"{DIM}💡 Check your Blaze screen and tap 'Always allow from this computer' ➔ OK.{RESET}\n")
                safe_pause("Press Enter after allowing...")
            else:
                print(f"\n{RED}❌ No USB-connected Android device detected by ADB.{RESET}")
                print(f"{DIM}💡 Check USB cable / USB mode (File Transfer) on Blaze.{RESET}\n")
                safe_pause()
                return False

        print(f"\n{CYAN}⚡ Switching ADB daemon on phone to TCP/IP mode on port 5555...{RESET}")
        tcp_res = subprocess.run(["adb", "tcpip", "5555"], capture_output=True, text=True, timeout=15)
        out_t = tcp_res.stdout.strip()
        print(f"{GREEN}{out_t}{RESET}")

        b_ip = get_blaze_ip()
        print(f"\n{GREEN}{BOLD}🎉 TCP Mode Enabled on Phone!{RESET}")
        print(f"┌────────────────────────────────────────────────────────┐")
        print(f"│ 🔌 You can now UNPLUG the USB cable from your PC.      │")
        print(f"│ 🌐 Attempting wireless connection to {b_ip}:5555...    │")
        print("└────────────────────────────────────────────────────────┘\n")
        time.sleep(1)

        return connect_wireless_adb(b_ip, 5555)
    except subprocess.TimeoutExpired:
        print(f"{RED}❌ ADB timed out while communicating with USB device.{RESET}")
        subprocess.run(["taskkill", "/F", "/IM", "adb.exe"], capture_output=True)
        safe_pause()
        return False
    except Exception as e:
        print(f"{RED}❌ Error during USB-to-Wireless setup: {e}{RESET}\n")
        safe_pause()
        return False

def get_adb_devices(json_mode=False):
    """Lists connected ADB transport devices with status card."""
    try:
        res = subprocess.run(["adb", "devices", "-l"], capture_output=True, text=True, timeout=12)
        out = res.stdout.strip()
        if json_mode:
            print(json.dumps({"adb_output": out}))
            return out

        print(f"\n{BOLD}{CYAN}🔌 CONNECTED ADB TRANSPORT DEVICES{RESET}")
        print("┌────────────────────────────────────────────────────────┐")
        lines = [l for l in out.splitlines() if l.strip() and not l.startswith("List of")]
        if not lines:
            print(f"│ {YELLOW}⚠️ No ADB devices currently attached.{RESET}                │")
            print(f"│ {DIM}💡 Use 'Connect Wireless ADB' or USB setup wizard.{RESET}     │")
        else:
            for l in lines:
                print(f"│ 📱 {GREEN}{l[:52]:<52}{RESET}│")
        print("└────────────────────────────────────────────────────────┘\n")
        return out
    except FileNotFoundError:
        print(f"{RED}❌ ADB executable not found in PATH.{RESET}\n")
        return None
    except subprocess.TimeoutExpired:
        print(f"{RED}❌ ADB daemon query timed out. Resetting ADB server...{RESET}\n")
        subprocess.run(["taskkill", "/F", "/IM", "adb.exe"], capture_output=True)
        return None
    except Exception as e:
        print(f"{RED}❌ Failed to query ADB: {e}{RESET}\n")
        return None

def connect_wireless_adb(ip=None, port=5555, quiet=False):
    """Connects to Blaze over wireless ADB with safe feedback."""
    target_ip = ip or get_blaze_ip()
    target_addr = f"{target_ip}:{port}"
    if not quiet:
        print(f"\n{CYAN}🔌 Connecting to Wireless ADB at {target_addr}...{RESET}")
    try:
        res = subprocess.run(["adb", "connect", target_addr], capture_output=True, text=True, timeout=15)
        out = res.stdout.strip()
        if "connected" in out.lower() and "cannot" not in out.lower() and "failed" not in out.lower():
            if not quiet:
                print(f"{GREEN}{BOLD}✅ Successfully connected to Wireless ADB ({target_addr})!{RESET}\n")
            return True
        else:
            if not quiet:
                print(f"{YELLOW}⚠️ ADB response: {out}{RESET}")
                print(f"{DIM}💡 Ensure 'Wireless Debugging' is enabled on Blaze Developer Options.{RESET}\n")
            return False
    except subprocess.TimeoutExpired:
        if not quiet:
            print(f"{RED}❌ Connection to {target_addr} timed out.{RESET}\n")
        return False
    except Exception as e:
        if not quiet:
            print(f"{RED}❌ Failed to connect wireless ADB: {e}{RESET}\n")
        return False

def pair_wireless_adb():
    """Android 11+ Wireless Debugging Pairing Assistant."""
    print(f"\n{BOLD}{CYAN}🔑 ANDROID 11+ WIRELESS DEBUGGING PAIRING ASSISTANT{RESET}")
    print("─" * 60)
    print("1. On Blaze: Open Developer Options ➔ Wireless Debugging.")
    print("2. Tap 'Pair device with pairing code'.")
    print("─" * 60)
    try:
        ip_port = input(f"{CYAN}Enter IP:Port shown on phone (e.g. 10.154.149.220:41235): {RESET}").strip()
        code = input(f"{CYAN}Enter 6-digit Pairing Code: {RESET}").strip()
        if ip_port and code:
            res = subprocess.run(["adb", "pair", ip_port, code], capture_output=True, text=True, timeout=20)
            out_res = res.stdout.strip()
            if "success" in out_res.lower():
                print(f"\n{GREEN}{BOLD}✅ {out_res}{RESET}\n")
                # Extract IP and prompt for connect port
                base_ip = ip_port.split(":")[0]
                conn_port = input(f"{CYAN}Enter main Wireless Debugging Port on phone [from main screen]: {RESET}").strip()
                if conn_port and conn_port.isdigit():
                    connect_wireless_adb(base_ip, int(conn_port))
            else:
                print(f"\n{YELLOW}{out_res}{RESET}\n")
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Pairing cancelled.{RESET}\n")

def restart_adb_server():
    """Restarts PC ADB daemon."""
    print(f"\n{CYAN}🔄 Restarting ADB Daemon...{RESET}")
    try:
        subprocess.run(["adb", "kill-server"], timeout=8)
        time.sleep(1)
        subprocess.run(["adb", "start-server"], timeout=12)
        print(f"{GREEN}✅ ADB Server restarted cleanly.{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Failed to restart ADB: {e}{RESET}\n")

def interactive_adb_hub():
    """Interactive Wireless ADB Transport Hub."""
    options = [
        "1. 🔌 Connect Wireless ADB (Auto-IP: 5555)  ──► Connect to Blaze on port 5555",
        "2. ⚡ USB ➔ Wireless Setup Wizard (tcpip)   ──► Plug USB once to enable wireless ADB",
        "3. 🔢 Connect Custom IP:Port (Dynamic Port) ──► Connect to specific port on phone",
        "4. 🔑 Pair Wireless ADB (Pairing Code)      ──► Android 11+ Wi-Fi Debugging Pair",
        "5. 📱 List Connected ADB Devices             ──► Check transport status & IDs",
        "6. 🔄 Restart ADB Server                     ──► Kill and restart local adb daemon",
        "7. ❌ Disconnect All Devices                 ──► Disconnect all active wireless sessions",
        "0. 🔙 Return to Main Menu                   ──► Cancel"
    ]
    while True:
        try:
            chosen = run_fzf(options, prompt="ADB Hub > ", header="🔌 WIRELESS ADB TRANSPORT HUB")
            if not chosen or "0. 🔙" in chosen:
                break
            if "1. 🔌 Connect" in chosen:
                b_ip = get_blaze_ip()
                connect_wireless_adb(ip=b_ip, port=5555)
            elif "2. ⚡ USB" in chosen:
                setup_usb_to_wireless_adb()
            elif "3. 🔢 Connect Custom" in chosen:
                b_ip = get_blaze_ip()
                port = input(f"Enter Port from phone screen: ").strip()
                if port.isdigit():
                    connect_wireless_adb(ip=b_ip, port=int(port))
            elif "4. 🔑 Pair" in chosen:
                pair_wireless_adb()
            elif "5. 📱 List" in chosen:
                get_adb_devices()
            elif "6. 🔄 Restart" in chosen:
                restart_adb_server()
            elif "7. ❌ Disconnect" in chosen:
                subprocess.run(["adb", "disconnect"], timeout=5)
                print(f"{YELLOW}⚡ Disconnected all ADB sessions.{RESET}\n")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 ADB Hub exited.{RESET}\n")
            break

# --- Scrcpy Streaming Studio ---

def safe_pause(msg="Press Enter to continue..."):
    """Safely prompts user to press Enter with signal protection."""
    try:
        input(f"{DIM}{msg}{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

def launch_scrcpy(mode="stealth", camera_facing="back", custom_flags=None):
    """Launches high-performance wireless Scrcpy display session with full pre-flight error protection."""
    if not shutil.which("scrcpy"):
        print(f"\n{RED}❌ Scrcpy executable not found in PATH.{RESET}")
        print(f"{DIM}💡 Install via Scoop: 'scoop install scrcpy'{RESET}\n")
        safe_pause()
        return

    # Pre-flight ADB connection validation & auto-healing
    adb_ok = check_and_ensure_adb()
    if not adb_ok:
        print(f"{YELLOW}⚠️ Scrcpy launch aborted: No authorized ADB connection.{RESET}\n")
        safe_pause("Press Enter to return...")
        return

    cmd = ["scrcpy"]
    if mode == "stealth":
        print(f"\n{CYAN}📺 Launching Scrcpy in Stealth Mode (Screen Off, 60 FPS, H.265)...{RESET}")
        cmd += ["--turn-screen-off", "--stay-awake", "--video-codec=h265", "--max-fps=60"]
    elif mode == "live":
        print(f"\n{CYAN}🖥️ Launching Scrcpy in Live Display Mode (Screen On, 60 FPS)...{RESET}")
        cmd += ["--stay-awake", "--max-fps=60"]
    elif mode == "gaming":
        print(f"\n{CYAN}⚡ Launching Scrcpy in Ultra-Low Latency Mode (1080p, 8M, 0 Buffer)...{RESET}")
        cmd += ["--max-size=1080", "--video-bit-rate=8M", "--max-fps=60", "--display-buffer=0", "--stay-awake"]
    elif mode == "audio":
        print(f"\n{CYAN}🔊 Launching Audio-Only Stream to PC Speakers (Opus Codec)...{RESET}")
        cmd += ["--no-video", "--audio-codec=opus"]
    elif mode == "camera":
        facing = "back" if camera_facing != "front" else "front"
        print(f"\n{CYAN}📷 Launching Wireless HD PC Webcam ({facing.upper()} Camera, 60 FPS)...{RESET}")
        cmd += ["--video-source=camera", f"--camera-facing={facing}", "--max-fps=60"]
    elif mode == "record":
        rec_dir = os.path.expanduser("~/Videos/Blaze_Recordings")
        os.makedirs(rec_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        rec_file = os.path.join(rec_dir, f"Blaze_Screen_{ts}.mp4")
        print(f"\n{CYAN}🎥 Launching Screen & Audio Recorder ➔ {rec_file}...{RESET}")
        cmd += ["--record", rec_file]
    elif mode == "otg":
        print(f"\n{CYAN}🎮 Launching Physical Keyboard & Mouse Pass-Through (Screen Off)...{RESET}")
        cmd += ["--turn-screen-off", "--keyboard=aoa", "--mouse=aoa"]

    if custom_flags:
        cmd.extend(custom_flags)

    try:
        proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        # Brief health check on process initialization
        time.sleep(1.0)
        if proc.poll() is not None and proc.returncode != 0:
            err_out = proc.stderr.read()
            print(f"\n{RED}┌────────────────────────────────────────────────────────┐{RESET}")
            print(f"{RED}│ ❌ SCRCPY LAUNCH FAILED                                │{RESET}")
            print(f"{RED}├────────────────────────────────────────────────────────┤{RESET}")
            for l in err_out.splitlines()[:5]:
                print(f"│ {l[:54]:<54} │")
            print(f"{RED}└────────────────────────────────────────────────────────┘{RESET}\n")
            safe_pause()
        else:
            print(f"{GREEN}✅ Scrcpy stream launched successfully in background.{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Failed to start Scrcpy: {e}{RESET}\n")
        safe_pause()

def interactive_scrcpy_studio():
    """Interactive Scrcpy Preset Selector Studio."""
    presets = [
        "1. 📺 Stealth Mirror (Screen OFF)  ──► Control phone quietly (H.265, 60fps)",
        "2. 🖥️ Live Display (Screen ON)     ──► Mirror with phone screen visible",
        "3. ⚡ Ultra-Low Latency Mode       ──► 1080p, 8 Mbps bitrate, 0 display buffer",
        "4. 🔊 Audio-Only Stream to PC      ──► Play phone audio through PC speakers (Opus)",
        "5. 📷 Wireless HD PC Webcam        ──► Stream rear or selfie camera as webcam",
        "6. 🎥 Screen & Audio Recorder      ──► Record session directly to MP4 in Videos",
        "7. 🎮 OTG Keyboard/Mouse Pass      ──► Direct hardware input pass-through",
        "0. 🔙 Return to Main Menu          ──► Cancel"
    ]
    while True:
        try:
            chosen = run_fzf(presets, prompt="Scrcpy Preset > ", header="📺 SCRCPY WIRELESS STREAMING STUDIO")
            if not chosen or "0. 🔙" in chosen:
                break
            if "1. 📺 Stealth" in chosen:
                launch_scrcpy("stealth")
            elif "2. 🖥️ Live" in chosen:
                launch_scrcpy("live")
            elif "3. ⚡ Ultra-Low" in chosen:
                launch_scrcpy("gaming")
            elif "4. 🔊 Audio-Only" in chosen:
                launch_scrcpy("audio")
            elif "5. 📷 Wireless" in chosen:
                cam_opts = ["1. 📷 Rear / Main Camera", "2. 🤳 Front / Selfie Camera", "0. 🔙 Cancel"]
                c_sel = run_fzf(cam_opts, prompt="Camera Lens > ")
                if c_sel and "0. 🔙" not in c_sel:
                    facing = "front" if "Front" in c_sel else "back"
                    launch_scrcpy("camera", camera_facing=facing)
            elif "6. 🎥 Screen" in chosen:
                launch_scrcpy("record")
            elif "7. 🎮 OTG" in chosen:
                launch_scrcpy("otg")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Scrcpy Studio exited.{RESET}\n")
            break

def show_help_manual(pause=True):
    """Displays formatted command reference."""
    print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-WIFI COMMAND & CLI REFERENCE                  │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-wifi                        │
│ • Wi-Fi Radar:       blaze-wifi --info                 │
│ • Spectrum Scanner:  blaze-wifi --scan                 │
│ • Power ON / OFF:    blaze-wifi --on / --off           │
│ • Bounce Radio:      blaze-wifi --bounce               │
│ • Scrcpy Stealth:    blaze-wifi --stealth              │
│ • Scrcpy Live:       blaze-wifi --live                 │
│ • Audio Stream:      blaze-wifi --audio-only           │
│ • HD PC Webcam:      blaze-wifi --camera [back|front]  │
│ • Screen Record:     blaze-wifi --record               │
│ • ADB Devices:       blaze-wifi --adb-devices          │
│ • ADB Connect:       blaze-wifi --adb-connect [ip:port]│
│ • JSON Machine Mode: blaze-wifi --json                 │
└────────────────────────────────────────────────────────┘{RESET}
""")
    if pause:
        try:
            input("Press Enter to return...")
        except (KeyboardInterrupt, EOFError):
            pass

# --- Interactive Main Menu ---

def interactive_menu():
    """Interactive FZF terminal menu matching blaze standard."""
    menu_items = [
        "📶 1. Wi-Fi & Hotspot Network Radar   ──► Active SSID, BSSID, RSSI bars, and throughput",
        "🔍 2. Spectrum Scanner (Visible APs)  ──► Scan nearby Wi-Fi networks with signal rating",
        "📺 3. Scrcpy Wireless Streaming Suite ──► Stealth display, 60fps mirror, webcam & recorder",
        "🔌 4. Wireless ADB Transport Hub       ──► Connect, pair, restart and inspect ADB sessions",
        "🔄 5. Bounce Wi-Fi Radio (Power Reset) ──► Power cycle Wi-Fi hardware on Blaze",
        "⚡ 6. Toggle Wi-Fi Power (ON / OFF)    ──► Enable or disable Wi-Fi client radio",
        "📖 7. Help & CLI Reference             ──► Flags, command switches & examples",
        "🚪 0. Exit                             ──► Return to PowerShell terminal"
    ]

    while True:
        try:
            chosen = run_fzf(menu_items, prompt="Blaze Wi-Fi > ", header="🌐 BLAZE WIRELESS, NETWORK RADAR & STREAMING HUB")
            if not chosen or "0. Exit" in chosen:
                print(f"{DIM}👋 Exited.{RESET}\n")
                break

            if "1. Wi-Fi & Hotspot" in chosen:
                get_wifi_info()
            elif "2. Spectrum Scanner" in chosen:
                scan_wifi()
            elif "3. Scrcpy Wireless" in chosen:
                interactive_scrcpy_studio()
            elif "4. Wireless ADB" in chosen:
                interactive_adb_hub()
            elif "5. Bounce Wi-Fi" in chosen:
                toggle_wifi("bounce")
            elif "6. Toggle Wi-Fi" in chosen:
                p_opts = ["1. ⚡ Power ON Wi-Fi", "2. 🛑 Power OFF Wi-Fi", "0. 🔙 Cancel"]
                p_sel = run_fzf(p_opts, prompt="Power State > ")
                if p_sel:
                    if "Power ON" in p_sel: toggle_wifi("on")
                    elif "Power OFF" in p_sel: toggle_wifi("off")
            elif "7. Help" in chosen:
                show_help_manual(pause=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}\n")
            break

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blaze Wireless, Network Radar, Scrcpy Streaming & ADB Hub",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("--info", action="store_true", help="Display active Wi-Fi / Hotspot connection metrics")
        parser.add_argument("--scan", action="store_true", help="Scan nearby visible Wi-Fi spectrum")
        parser.add_argument("--on", action="store_true", help="Turn Wi-Fi radio ON")
        parser.add_argument("--off", action="store_true", help="Turn Wi-Fi radio OFF")
        parser.add_argument("--bounce", action="store_true", help="Bounce Wi-Fi radio (reboot cycle)")
        parser.add_argument("--stealth", action="store_true", help="Launch Scrcpy in stealth mode (screen off)")
        parser.add_argument("--live", action="store_true", help="Launch Scrcpy with display screen on")
        parser.add_argument("--audio-only", action="store_true", help="Stream phone audio to PC speakers")
        parser.add_argument("--camera", choices=["back", "front"], nargs="?", const="back", help="Stream camera as PC webcam")
        parser.add_argument("--record", action="store_true", help="Record wireless screen session to MP4")
        parser.add_argument("--adb-devices", action="store_true", help="List connected ADB devices")
        parser.add_argument("--adb-connect", metavar="IP[:PORT]", nargs="?", const="auto", help="Connect to wireless ADB")
        parser.add_argument("--json", action="store_true", help="JSON output mode")

        args = parser.parse_args()

        if args.info:
            get_wifi_info(json_mode=args.json)
        elif args.scan:
            scan_wifi(json_mode=args.json)
        elif args.on:
            toggle_wifi("on")
        elif args.off:
            toggle_wifi("off")
        elif args.bounce:
            toggle_wifi("bounce")
        elif args.stealth:
            launch_scrcpy("stealth")
        elif args.live:
            launch_scrcpy("live")
        elif args.audio_only:
            launch_scrcpy("audio")
        elif args.camera:
            launch_scrcpy("camera", camera_facing=args.camera)
        elif args.record:
            launch_scrcpy("record")
        elif args.adb_devices:
            get_adb_devices(json_mode=args.json)
        elif args.adb_connect:
            if args.adb_connect == "auto":
                connect_wireless_adb()
            else:
                parts = args.adb_connect.split(":")
                ip = parts[0]
                port = int(parts[1]) if len(parts) > 1 else 5555
                connect_wireless_adb(ip, port)
        else:
            interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Exited gracefully.{RESET}")

if __name__ == "__main__":
    main()
