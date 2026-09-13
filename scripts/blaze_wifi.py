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

def get_wifi_info(json_mode=False):
    """Displays active Wi-Fi connection info and signal metrics."""
    out, err, code = run_ssh("termux-wifi-connectioninfo")
    if code != 0 or not out:
        if json_mode:
            print(json.dumps({"error": "Failed to get Wi-Fi info", "details": err}))
        else:
            print(f"{RED}❌ Failed to fetch Wi-Fi connection info.{RESET} ({err})")
        return
    try:
        data = json.loads(out)
        if json_mode:
            print(json.dumps(data, indent=2))
            return

        ssid = data.get("ssid", "<Unknown>").strip('"')
        bssid = data.get("bssid", "Unknown")
        rssi = data.get("rssi", 0)
        speed = data.get("link_speed_mbps", 0)
        ip = data.get("ip", "Unknown")
        freq = data.get("frequency_mhz", 0)
        band = "5 GHz" if freq > 4000 else ("2.4 GHz" if freq > 2000 else "Unknown")

        # Signal Quality Bar
        bars = "█████" if rssi > -55 else ("████░" if rssi > -67 else ("███░░" if rssi > -75 else ("██░░░" if rssi > -85 else "█░░░░")))
        sig_color = GREEN if rssi > -65 else (YELLOW if rssi > -78 else RED)

        print(f"\n{CYAN}┌── 📶 ACTIVE WI-FI CONNECTION RADAR ───────────────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│ 🌐 {BOLD}Access Point (SSID):{RESET}  {CYAN}{BOLD}{ssid}{RESET}")
        print(f"│ 📡 {BOLD}Hardware BSSID:{RESET}       {bssid}")
        print(f"│ 📶 {BOLD}Signal Strength:{RESET}      {format_signal_bar(rssi)}")
        print(f"│ ⚡ {BOLD}Link Throughput:{RESET}      {speed} Mbps")
        print(f"│ 📻 {BOLD}Frequency Band:{RESET}       {freq} MHz ({band})")
        print(f"│ 💻 {BOLD}Local IP Address:{RESET}     {GREEN}{ip}{RESET} (Port 8022/SSH)")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└── ⚡ Network Active{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")

def scan_wifi(json_mode=False):
    """Scans visible Wi-Fi access points."""
    print(f"{CYAN}🔍 Scanning visible Wi-Fi spectrum on Blaze...{RESET}")
    out, err, code = run_ssh("termux-wifi-scaninfo")
    if code != 0 or not out:
        if json_mode:
            print(json.dumps({"error": "Wi-Fi scan failed", "details": err}))
        else:
            print(f"{RED}❌ Wi-Fi scan failed.{RESET} ({err})")
        return
    try:
        networks = json.loads(out)
        if json_mode:
            print(json.dumps(networks, indent=2))
            return

        sorted_nets = sorted(networks, key=lambda x: x.get("rssi", -100), reverse=True)
        print(f"\n{BOLD}{CYAN}📡 VISIBLE WI-FI NETWORKS ({len(sorted_nets)} Found){RESET}")
        print("─" * 65)
        for i, net in enumerate(sorted_nets, 1):
            ssid = net.get("ssid", "<Hidden>")
            bssid = net.get("bssid", "")
            rssi = net.get("rssi", 0)
            freq = net.get("frequency_mhz", 0)
            band = "5G" if freq > 4000 else "2.4G"
            sig_col = GREEN if rssi > -65 else (YELLOW if rssi > -78 else RED)
            print(f"{GREEN}[{i:02d}]{RESET} {BOLD}{ssid:<24}{RESET} {sig_col}{rssi:>4} dBm{RESET} | {band:<4} | {DIM}{bssid}{RESET}")
        print("─" * 65 + "\n")
    except Exception as e:
        print(f"{RED}❌ Parsing error: {e}{RESET}")

def toggle_wifi(state):
    """Toggles Wi-Fi power state (true/false/bounce)."""
    if state == "bounce":
        print(f"{YELLOW}🔄 Bouncing Wi-Fi radio (Power OFF ➔ 3s wait ➔ Power ON)...{RESET}")
        run_ssh("termux-wifi-enable false")
        time.sleep(3)
        run_ssh("termux-wifi-enable true")
        print(f"{GREEN}✅ Wi-Fi radio bounced successfully.{RESET}")
    elif state in ["on", "true"]:
        print(f"{CYAN}⚡ Enabling Wi-Fi radio...{RESET}")
        run_ssh("termux-wifi-enable true")
        print(f"{GREEN}✅ Wi-Fi radio enabled.{RESET}")
    elif state in ["off", "false"]:
        print(f"{YELLOW}⚡ Disabling Wi-Fi radio...{RESET}")
        run_ssh("termux-wifi-enable false")
        print(f"{GREEN}✅ Wi-Fi radio disabled.{RESET}")

# --- Scrcpy & Wireless Streaming Suite ---

def launch_scrcpy(mode="stealth", camera_facing="back"):
    """Launches wireless Scrcpy display session."""
    target_ip = "10.242.186.1" # default hotspot gateway fallback
    # Check if adb device connected or try wireless port 5555
    cmd = ["scrcpy"]
    if mode == "stealth":
        print(f"{CYAN}📺 Launching Scrcpy in Stealth Mode (Screen Off, 60fps, H.265)...{RESET}")
        cmd += ["--turn-screen-off", "--stay-awake", "--video-codec=h265", "--max-fps=60"]
    elif mode == "live":
        print(f"{CYAN}📺 Launching Scrcpy in Live Display Mode...{RESET}")
        cmd += ["--stay-awake", "--max-fps=60"]
    elif mode == "audio":
        print(f"{CYAN}🔊 Launching Audio-Only Stream to PC Speakers (Opus Codec)...{RESET}")
        cmd += ["--no-video", "--audio-codec=opus"]
    elif mode == "camera":
        facing = "back" if camera_facing != "front" else "front"
        print(f"{CYAN}📷 Launching Wireless HD PC Webcam ({facing.upper()} Camera)...{RESET}")
        cmd += ["--video-source=camera", f"--camera-facing={facing}", "--max-fps=60"]
    elif mode == "record":
        rec_dir = os.path.expanduser("~/Videos/Blaze_Recordings")
        os.makedirs(rec_dir, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        rec_file = os.path.join(rec_dir, f"Blaze_Screen_{ts}.mp4")
        print(f"{CYAN}🎥 Launching Screen & Audio Recorder ➔ {rec_file}...{RESET}")
        cmd += ["--record", rec_file]

    try:
        subprocess.Popen(cmd)
        print(f"{GREEN}✅ Scrcpy session started.{RESET}")
    except FileNotFoundError:
        print(f"{RED}❌ Scrcpy not found in PATH. Install via Scoop: 'scoop install scrcpy'{RESET}")
    except Exception as e:
        print(f"{RED}❌ Failed to start Scrcpy: {e}{RESET}")

# --- ADB Tools ---

def get_adb_devices(json_mode=False):
    """Lists ADB connected devices."""
    try:
        res = subprocess.run(["adb", "devices", "-l"], capture_output=True, text=True)
        if json_mode:
            print(json.dumps({"adb_output": res.stdout.strip()}))
        else:
            print(f"\n{BOLD}{CYAN}🔌 CONNECTED ADB TRANSPORT DEVICES{RESET}")
            print("─" * 60)
            print(res.stdout.strip())
            print("─" * 60 + "\n")
    except FileNotFoundError:
        print(f"{RED}❌ ADB not found in PATH.{RESET}")

# --- Interactive Menu ---

def interactive_menu():
    """Interactive terminal menu."""
    while True:
        print()
        print(f"{CYAN}┌── 🌐 BLAZE WIRELESS, SCRCPY & ADB COMMAND HUB ────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│  {BOLD}1{RESET}  📶 Active Wi-Fi Connection Radar")
        print(f"│  {BOLD}2{RESET}  🔍 Scan Visible Wi-Fi Networks (Spectrum Radar)")
        print(f"│  {BOLD}3{RESET}  📺 Scrcpy Wireless Stream (Stealth - Screen Off)")
        print(f"│  {BOLD}4{RESET}  🖥️ Scrcpy Live Display Stream (Screen On)")
        print(f"│  {BOLD}5{RESET}  🔊 Audio-Only Wireless Stream (PC Speakers)")
        print(f"│  {BOLD}6{RESET}  📷 Wireless HD PC Webcam (Rear / Front Camera)")
        print(f"│  {BOLD}7{RESET}  🎥 Screen & Audio Recording Studio")
        print(f"│  {BOLD}8{RESET}  🔄 Bounce Wi-Fi Radio (Power Reset)")
        print(f"│  {BOLD}9{RESET}  🔌 Wireless ADB Transport Diagnostics")
        print(f"│  {BOLD}0{RESET}  🚪 Exit")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└── ⚡ Select Option [0-9]{RESET}")
        print()
        try:
            choice = input(f"{BOLD}Blaze-WiFi ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            get_wifi_info()
        elif choice == "2":
            scan_wifi()
        elif choice == "3":
            launch_scrcpy("stealth")
        elif choice == "4":
            launch_scrcpy("live")
        elif choice == "5":
            launch_scrcpy("audio")
        elif choice == "6":
            cam = input(f"Select Camera [rear/front] (default rear): ").strip().lower()
            launch_scrcpy("camera", camera_facing=cam)
        elif choice == "7":
            launch_scrcpy("record")
        elif choice == "8":
            toggle_wifi("bounce")
        elif choice == "9":
            get_adb_devices()
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Select 0-9.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Wireless, Network Radar, Scrcpy Streaming & ADB Hub",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--info", action="store_true", help="Display active Wi-Fi connection metrics")
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
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")

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
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
