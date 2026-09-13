#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎵 Blaze Hierarchical Audio Browser, Media Player & Sound Engine Hub
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

def play_media(file_path):
    """Plays audio track on phone."""
    print(f"{CYAN}▶️ Playing on Blaze: {file_path}...{RESET}")
    out, err, code = run_ssh(f"termux-media-player play '{file_path}'")
    if code == 0:
        print(f"{GREEN}✅ Playback started.{RESET}")
    else:
        print(f"{RED}❌ Playback failed: {err}{RESET}")

def pause_media():
    """Pauses playback."""
    print(f"{YELLOW}⏸️ Pausing playback on Blaze...{RESET}")
    run_ssh("termux-media-player pause")

def resume_media():
    """Resumes playback."""
    print(f"{GREEN}▶️ Resuming playback on Blaze...{RESET}")
    run_ssh("termux-media-player play")

def stop_media():
    """Stops playback."""
    print(f"{RED}⏹️ Stopping playback on Blaze...{RESET}")
    run_ssh("termux-media-player stop")

def get_media_info(json_mode=False):
    """Gets active playback info."""
    out, err, code = run_ssh("termux-media-player info")
    if code != 0 or not out:
        if json_mode:
            print(json.dumps({"error": "No active playback or query failed"}))
        else:
            print(f"{YELLOW}⚠️ No active media playback.{RESET}")
        return
    try:
        data = json.loads(out)
        if json_mode:
            print(json.dumps(data, indent=2))
            return
        status = data.get("status", "Unknown").upper()
        track = data.get("current_track", "None")
        pos = data.get("current_position", "00:00")
        dur = data.get("duration", "00:00")
        print(f"\n{BOLD}{CYAN}🎵 MEDIA PLAYBACK RADAR{RESET}")
        print("┌────────────────────────────────────────────────────────┐")
        print(f"│ 📻 {BOLD}Status:{RESET}   {GREEN if status == 'PLAYING' else YELLOW}{status}{RESET}")
        print(f"│ 🎶 {BOLD}Track:{RESET}    {CYAN}{track}{RESET}")
        print(f"│ ⏱️ {BOLD}Progress:{RESET} {pos} / {dur}")
        print("└────────────────────────────────────────────────────────┘\n")
    except Exception:
        print(out)

def set_volume(level, stream="music"):
    """Sets Android volume level (0-15)."""
    lvl = max(0, min(15, int(level)))
    print(f"{CYAN}🔊 Setting Blaze volume [{stream}] ➔ {lvl}/15...{RESET}")
    out, err, code = run_ssh(f"termux-volume {stream} {lvl} && termux-toast '🔊 Volume: {lvl}/15'")
    if code == 0:
        bar = "█" * lvl + "░" * (15 - lvl)
        print(f"{GREEN}✅ Volume updated: [{bar}] ({lvl}/15){RESET}")
    else:
        print(f"{RED}❌ Failed to set volume: {err}{RESET}")

def scan_mediastore(target_path="/sdcard/Music"):
    """Triggers Android MediaStore scanner."""
    print(f"{CYAN}🔄 Refreshing Android MediaStore on {target_path}...{RESET}")
    out, err, code = run_ssh(f"termux-media-scan '{target_path}'")
    if code == 0:
        print(f"{GREEN}✅ MediaStore re-indexed. Tracks are visible in all players.{RESET}")
    else:
        print(f"{RED}❌ Failed to scan MediaStore: {err}{RESET}")

def get_audio_diag(json_mode=False):
    """Fetches hardware audio diagnostics."""
    out, err, code = run_ssh("termux-audio-info")
    if code != 0 or not out:
        print(f"{RED}❌ Failed to get audio diagnostics.{RESET}")
        return
    try:
        data = json.loads(out)
        if json_mode:
            print(json.dumps(data, indent=2))
            return
        print(f"\n{BOLD}{CYAN}🔊 HARDWARE AUDIO DIAGNOSTICS{RESET}")
        print("─" * 60)
        print(json.dumps(data, indent=2))
        print("─" * 60 + "\n")
    except Exception:
        print(out)

# --- Hierarchical Remote Audio Browser ---

def browse_and_play():
    """Interactive remote directory audio explorer."""
    current_dir = "/sdcard/Music"
    while True:
        print(f"\n{BOLD}{CYAN}📁 REMOTE AUDIO EXPLORER:{RESET} {current_dir}")
        print("─" * 60)
        # List items
        cmd = f"ls -p -1 '{current_dir}' 2>/dev/null"
        out, err, code = run_ssh(cmd)
        items = [line.strip() for line in out.splitlines() if line.strip()]
        
        print(f"  {YELLOW}[00] 📁 .. (Back to parent directory){RESET}")
        for i, item in enumerate(items[:35], 1):
            icon = "📁" if item.endswith("/") else "🎵"
            print(f"  {GREEN}[{i:02d}]{RESET} {icon} {item}")
        print("─" * 60)
        print(f"{DIM}Enter index number to navigate/play, or 'q' to exit.{RESET}")

        try:
            sel = input(f"{BOLD}Browse ❯ {RESET}").strip()
            if sel in ["q", "exit"]:
                break
            if sel in ["0", "00", ".."]:
                current_dir = os.path.dirname(current_dir.rstrip("/")) or "/sdcard"
                continue
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(items):
                    chosen = items[idx]
                    full_p = f"{current_dir.rstrip('/')}/{chosen.rstrip('/')}"
                    if chosen.endswith("/"):
                        current_dir = full_p
                    else:
                        play_media(full_p)
                else:
                    print(f"{YELLOW}⚠️ Invalid index.{RESET}")
        except (KeyboardInterrupt, EOFError):
            break

# --- Interactive Menu ---

def interactive_menu():
    """Interactive terminal menu."""
    while True:
        print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│         🎵 BLAZE AUDIO BROWSER & MEDIA COMMAND HUB     │
├────────────────────────────────────────────────────────┤
│  {BOLD}1{RESET} 📁 Browse Remote Tracks & Play (Hierarchical Explorer)│
│  {BOLD}2{RESET} 📻 View Active Playback Status & Progress           │
│  {BOLD}3{RESET} ⏸️ Pause Playback                                   │
│  {BOLD}4{RESET} ▶️ Resume Playback                                  │
│  {BOLD}5{RESET} ⏹️ Stop Playback                                    │
│  {BOLD}6{RESET} 🔊 Set Hardware Volume (0-15 Slider)                │
│  {BOLD}7{RESET} 🔄 Refresh Android MediaStore (Gallery/Music Sync)  │
│  {BOLD}8{RESET} 📊 Audio Hardware Diagnostics & Stream Routing      │
│  {BOLD}0{RESET} 🚪 Exit                                             │
└────────────────────────────────────────────────────────┘{RESET}""")
        try:
            choice = input(f"{BOLD}Blaze-Media ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            browse_and_play()
        elif choice == "2":
            get_media_info()
        elif choice == "3":
            pause_media()
        elif choice == "4":
            resume_media()
        elif choice == "5":
            stop_media()
        elif choice == "6":
            lvl = input("Enter Volume Level (0-15): ").strip()
            if lvl.isdigit():
                set_volume(int(lvl))
        elif choice == "7":
            scan_mediastore()
        elif choice == "8":
            get_audio_diag()
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Select 0-8.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Hierarchical Audio Browser, Media Player & Sound Engine Hub",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--play", metavar="PATH", help="Play audio file on Blaze")
    parser.add_argument("--pause", action="store_true", help="Pause playback")
    parser.add_argument("--resume", action="store_true", help="Resume playback")
    parser.add_argument("--stop", action="store_true", help="Stop playback")
    parser.add_argument("--info", action="store_true", help="View active playback info")
    parser.add_argument("--volume", type=int, metavar="0-15", help="Set system volume level (0-15)")
    parser.add_argument("--scan", nargs="?", const="/sdcard/Music", metavar="PATH", help="Re-index MediaStore")
    parser.add_argument("--diag", action="store_true", help="Audio hardware diagnostics")
    parser.add_argument("--browse", action="store_true", help="Launch interactive hierarchical audio explorer")
    parser.add_argument("--json", action="store_true", help="JSON output mode")

    args = parser.parse_args()

    if args.play:
        play_media(args.play)
    elif args.pause:
        pause_media()
    elif args.resume:
        resume_media()
    elif args.stop:
        stop_media()
    elif args.info:
        get_media_info(json_mode=args.json)
    elif args.volume is not None:
        set_volume(args.volume)
    elif args.scan:
        scan_mediastore(args.scan)
    elif args.diag:
        get_audio_diag(json_mode=args.json)
    elif args.browse:
        browse_and_play()
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
