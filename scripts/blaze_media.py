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
import shutil
import time
import re
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

DEFAULT_DOWNLOADS_DIR = os.path.expanduser("~/Downloads")
AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".flac", ".aac", ".ogg", ".opus", ".m4b", ".mid"}

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

def run_ssh(cmd, timeout=8):
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

def run_fzf(options, prompt="Blaze Media > ", header=None):
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

def set_clipboard(text):
    """Copies text to Windows clipboard."""
    try:
        subprocess.run(["powershell", "-Command", f"Set-Clipboard -Value @'\n{text}\n'@"], check=True)
        return True
    except Exception:
        return False

def safe_pause(msg="Press Enter to continue..."):
    """Safely prompts user to press Enter with signal protection."""
    try:
        input(f"{DIM}{msg}{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

# --- Playback Engine ---

def play_media(file_path):
    """Plays audio track on phone hardware speakers with visual status."""
    clean_p = file_path.strip('"').strip("'")
    safe_p = clean_p.replace('"', '\\"')
    fname = os.path.basename(clean_p)
    print(f"\n{CYAN}▶️ Starting playback on Blaze: '{fname}'...{RESET}")
    out, err, code = run_ssh(f'termux-media-player play "{safe_p}" && termux-toast -g middle -b "#1B5E20" -c "white" "▶️ Playing: {fname}"')
    if code == 0:
        print(f"\n{GREEN}{BOLD}✅ AUDIO PLAYBACK STARTED ON BLAZE!{RESET}")
        print("┌────────────────────────────────────────────────────────┐")
        print(f"│ 🎶 {BOLD}Track:{RESET}    {CYAN}{BOLD}{fname[:38]:<39}{RESET}│")
        print(f"│ 📂 {BOLD}Path:{RESET}     {clean_p[:38]:<39}│")
        print("└────────────────────────────────────────────────────────┘\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Playback failed: {err}{RESET}\n")

def pause_media():
    """Pauses active media playback."""
    print(f"\n{YELLOW}⏸️ Pausing playback on Blaze...{RESET}")
    out, err, code = run_ssh('termux-media-player pause && termux-toast -g middle -b "#FF6F00" -c "black" "⏸️ Paused"')
    if code == 0:
        print(f"{GREEN}✅ Playback paused on phone.{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to pause: {err}{RESET}\n")

def resume_media():
    """Resumes paused media playback."""
    print(f"\n{GREEN}▶️ Resuming playback on Blaze...{RESET}")
    out, err, code = run_ssh('termux-media-player play && termux-toast -g middle -b "#1B5E20" -c "white" "▶️ Resumed"')
    if code == 0:
        print(f"{GREEN}✅ Playback resumed on phone.{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to resume: {err}{RESET}\n")

def stop_media():
    """Stops playback and releases media resources."""
    print(f"\n{RED}⏹️ Stopping playback on Blaze...{RESET}")
    out, err, code = run_ssh('termux-media-player stop && termux-toast -g middle -b "#B71C1C" -c "white" "⏹️ Stopped"')
    if code == 0:
        print(f"{GREEN}✅ Playback stopped.{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to stop: {err}{RESET}\n")

def get_media_info(json_mode=False):
    """Displays real-time playback radar and progress bar."""
    out, err, code = run_ssh("termux-media-player info")
    if code != 0 or not out or "No track" in out:
        if code == 255:
            render_unreachable_card()
        elif json_mode:
            print(json.dumps({"status": "idle", "track": None}))
        else:
            print(f"\n{YELLOW}⚠️ No active audio track currently playing on Blaze.{RESET}\n")
        return None

    try:
        data = json.loads(out)
        if json_mode:
            print(json.dumps(data, indent=2))
            return data

        status = data.get("status", "UNKNOWN").upper()
        track = data.get("current_track", "Unknown Track")
        pos = data.get("current_position", "00:00")
        dur = data.get("duration", "00:00")

        # Progress calculation
        prog_bar = "──────────"
        try:
            p_parts = [int(x) for x in pos.split(":")]
            d_parts = [int(x) for x in dur.split(":")]
            p_sec = p_parts[0] * 60 + p_parts[1] if len(p_parts) == 2 else p_parts[0] * 3600 + p_parts[1] * 60 + p_parts[2]
            d_sec = d_parts[0] * 60 + d_parts[1] if len(d_parts) == 2 else d_parts[0] * 3600 + d_parts[1] * 60 + d_parts[2]
            if d_sec > 0:
                pct = min(1.0, max(0.0, p_sec / d_sec))
                fill = int(pct * 15)
                prog_bar = "█" * fill + "░" * (15 - fill)
        except Exception:
            pass

        stat_col = GREEN if status == "PLAYING" else (YELLOW if status == "PAUSED" else RED)
        print(f"\n{BOLD}{CYAN}🎵 BLAZE AUDIO PLAYBACK RADAR{RESET}")
        print("┌────────────────────────────────────────────────────────┐")
        print(f"│ 📻 {BOLD}State:{RESET}     {stat_col}{status:<39}{RESET}│")
        print(f"│ 🎶 {BOLD}Track:{RESET}     {CYAN}{BOLD}{track[:38]:<39}{RESET}│")
        print(f"│ ⏱️ {BOLD}Progress:{RESET}  [{prog_bar}] {pos} / {dur}{'':<12}│")
        print("└────────────────────────────────────────────────────────┘\n")
        return data
    except Exception:
        print(f"{CYAN}📻 Status:{RESET} {out}\n")
        return None

# --- Volume Master Console ---

def set_volume(level, stream="music"):
    """Sets Android hardware volume level with stream selector."""
    lvl = max(0, min(15, int(level)))
    out, err, code = run_ssh(f'termux-volume {stream} {lvl} && termux-toast -g middle -b "#006064" -c "white" "🔊 {stream.capitalize()} Volume: {lvl}/15"')
    if code == 0:
        bar = "█" * lvl + "░" * (15 - lvl)
        print(f"\n{GREEN}{BOLD}✅ Volume updated [{stream.upper()}]:{RESET} [{bar}] ({lvl}/15)\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to set volume: {err}{RESET}\n")

def interactive_volume_console():
    """Interactive FZF Volume Console for all audio streams."""
    streams = [
        "1. 🎵 Music & Media Stream     ──► Background audio, Spotify & video sound",
        "2. 🔔 Ringtone Stream          ──► Incoming call ring volume",
        "3. 💬 Notification Alerts      ──► SMS, messages & app alert chimes",
        "4. ⏰ Alarm Clock Stream       ──► Morning alarms & timer sounds",
        "5. ⚙️ System Sounds            ──► Keypad clicks & touch tones",
        "6. 📞 Voice Call In-Ear        ──► Earpiece volume during phone calls",
        "0. 🔙 Return to Menu           ──► Cancel"
    ]
    chosen = run_fzf(streams, prompt="Audio Stream > ", header="🔊 VOLUME MASTER CONSOLE")
    if not chosen or "0. 🔙" in chosen:
        return

    mapping = {
        "1. 🎵": ("music", 15),
        "2. 🔔": ("ring", 15),
        "3. 💬": ("notification", 15),
        "4. ⏰": ("alarm", 15),
        "5. ⚙️": ("system", 15),
        "6. 📞": ("call", 7)
    }
    stream_key, max_v = "music", 15
    for k, v in mapping.items():
        if k in chosen:
            stream_key, max_v = v
            break

    vol_presets = [
        f"1. 🔇 Mute (0/{max_v})",
        f"2. 🔉 Low (2/{max_v})",
        f"3. 🔉 Moderate ({max_v//3}/{max_v})",
        f"4. 🔊 Balanced ({max_v//2}/{max_v})",
        f"5. 🔊 High ({int(max_v*0.8)}/{max_v})",
        f"6. 📢 Maximum ({max_v}/{max_v})",
        "7. ⌨️ Enter Custom Level",
        "0. 🔙 Cancel"
    ]
    v_sel = run_fzf(vol_presets, prompt=f"Set {stream_key.upper()} Volume > ")
    if not v_sel or "0. 🔙" in v_sel:
        return

    if "1. 🔇" in v_sel: set_volume(0, stream_key)
    elif "2. 🔉 Low" in v_sel: set_volume(2, stream_key)
    elif "3. 🔉 Mod" in v_sel: set_volume(max_v//3, stream_key)
    elif "4. 🔊 Bal" in v_sel: set_volume(max_v//2, stream_key)
    elif "5. 🔊 High" in v_sel: set_volume(int(max_v*0.8), stream_key)
    elif "6. 📢 Max" in v_sel: set_volume(max_v, stream_key)
    elif "7. ⌨️" in v_sel:
        try:
            val = input(f"{CYAN}Enter level (0-{max_v}): {RESET}").strip()
            if val.isdigit():
                set_volume(int(val), stream_key)
        except (KeyboardInterrupt, EOFError):
            pass
    safe_pause()

# --- Hierarchical Remote Audio Browser ---

def browse_and_play(initial_path="/sdcard/Music"):
    """Interactive FZF audio explorer for browsing folders and managing tracks."""
    current_dir = initial_path

    while True:
        out, err, code = run_ssh(f'ls -laL "{current_dir}" 2>/dev/null')
        if code != 0 or not out:
            if code == 255:
                render_unreachable_card()
                break
            print(f"{RED}❌ Failed to access '{current_dir}': {err}{RESET}\n")
            safe_pause()
            break

        fzf_items = []
        entries = []

        if current_dir not in ["/", "/sdcard", "/storage/emulated/0"]:
            fzf_items.append("📁 .. [Parent Directory]")
            entries.append(("..", True))

        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 9 and parts[8] not in [".", ".."]:
                is_dir = line.startswith("d")
                size = parts[4]
                name = " ".join(parts[8:])
                ext = os.path.splitext(name)[1].lower()

                if not is_dir and ext not in AUDIO_EXTENSIONS:
                    continue

                try:
                    s_int = int(size)
                    if s_int > 1048576:
                        s_str = f"{s_int/1048576:.1f} MB"
                    elif s_int > 1024:
                        s_str = f"{s_int/1024:.1f} KB"
                    else:
                        s_str = f"{s_int} B"
                except Exception:
                    s_str = size

                icon = "📁" if is_dir else "🎵"
                fzf_items.append(f"{icon} {name:<32} │ {s_str:>8}")
                entries.append((name, is_dir))

        if not fzf_items:
            fzf_items.append("📁 .. [Parent Directory]")
            entries.append(("..", True))

        header_str = f"🎵 AUDIO EXPLORER: {current_dir} ({len(fzf_items)} items)"
        chosen = run_fzf(fzf_items, prompt="Select Track/Folder > ", header=header_str)
        if not chosen:
            break

        if "📁 .. [Parent Directory]" in chosen:
            current_dir = os.path.dirname(current_dir.rstrip("/"))
            if not current_dir:
                current_dir = "/sdcard"
            continue

        match_name = chosen[2:].split("│")[0].strip()
        matched_entry = next((e for e in entries if e[0] == match_name), None)
        if not matched_entry:
            continue

        name, is_dir = matched_entry
        target_path = f"{current_dir.rstrip('/')}/{name}"

        if is_dir:
            current_dir = target_path
        else:
            # Action Sheet
            actions = [
                f"▶️ 1. Play on Phone Speakers    ──► Play '{name}' via Termux Media Player",
                "🔊 2. Stream to PC (Scrcpy Audio) ──► Stream phone sound to PC speakers",
                "📥 3. Pull Track to PC Downloads ──► Save copy directly to ~/Downloads/",
                "📱 4. Open in Android App/Chooser──► Launch in VLC, Spotify or system player",
                "📋 5. Copy Track Remote Path     ──► Copy path to Windows clipboard",
                "🗑️ 6. Delete Audio File          ──► Remove track from phone",
                "0. 🔙 Back to Folder              ──► Return to audio list"
            ]
            act = run_fzf(actions, prompt=f"Action on {name} > ", header=f"Track: {name}")
            if not act or "0. 🔙" in act:
                continue

            if "1. Play" in act:
                play_media(target_path)
                safe_pause()
            elif "2. Stream" in act:
                play_media(target_path)
                print(f"\n{CYAN}🔊 Launching Scrcpy Audio Stream to Motobook Speakers (Opus)...{RESET}")
                try:
                    subprocess.Popen(["scrcpy", "--no-video", "--audio-codec=opus"])
                    print(f"{GREEN}✅ Audio stream active.{RESET}\n")
                except Exception as e:
                    print(f"{RED}❌ Scrcpy error: {e}{RESET}\n")
                safe_pause()
            elif "3. Pull" in act:
                clean_target = os.path.join(DEFAULT_DOWNLOADS_DIR, name)
                print(f"\n{CYAN}📥 Pulling '{name}' ➔ PC Downloads...{RESET}")
                res = subprocess.run(["scp", "-o", "ConnectTimeout=8", f"blaze:{target_path}", clean_target], capture_output=True, text=True)
                if res.returncode == 0:
                    print(f"{GREEN}✅ Saved in: {clean_target}{RESET}\n")
                else:
                    print(f"{RED}❌ Pull failed: {res.stderr.strip()}{RESET}\n")
                safe_pause()
            elif "4. Open" in act:
                run_ssh(f'termux-open --chooser "{target_path}" || termux-open "{target_path}"')
                print(f"\n{GREEN}✅ Opened in Android music player.{RESET}\n")
                safe_pause()
            elif "5. Copy" in act:
                set_clipboard(target_path)
                print(f"\n{GREEN}✅ '{target_path}' copied to Windows clipboard!{RESET}\n")
                safe_pause()
            elif "6. Delete" in act:
                conf = run_fzf(["1. ❌ YES, Delete Track", "0. 🔙 Cancel"], prompt=f"Delete {name}? > ")
                if conf and "YES" in conf:
                    run_ssh(f'rm -f "{target_path}"')
                    print(f"\n{GREEN}✅ Track deleted.{RESET}\n")
                    safe_pause()

# --- Sound & Speech Synthesis ---

def speak_tts(text):
    """Speaks text aloud on Blaze using native Android TTS synthesizer."""
    safe_t = text.replace('"', '\\"')
    print(f"\n{CYAN}🗣️ Speaking on Blaze: \"{text}\"...{RESET}")
    out, err, code = run_ssh(f'termux-tts-speak "{safe_t}"')
    if code == 0:
        print(f"{GREEN}✅ Speech synthesized on phone speakers.{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ TTS failed: {err}{RESET}\n")

def vibrate_phone(duration_ms=500):
    """Vibrates phone motor for specified milliseconds."""
    out, err, code = run_ssh(f'termux-vibrate -d {duration_ms}')
    if code == 0:
        print(f"{GREEN}📳 Phone vibrated ({duration_ms}ms).{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Vibration failed: {err}{RESET}\n")

def scan_mediastore(target_path="/sdcard/Music"):
    """Triggers Android MediaStore scanner to index new songs."""
    print(f"\n{CYAN}🔄 Refreshing Android MediaStore on '{target_path}'...{RESET}")
    out, err, code = run_ssh(f'termux-media-scan "{target_path}" && termux-toast -g middle -b "#1B5E20" -c "white" "🔄 MediaStore Refreshed"')
    if code == 0:
        print(f"{GREEN}✅ MediaStore re-indexed! Audio tracks are visible in all players.{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to scan MediaStore: {err}{RESET}\n")

def show_help_manual(pause=True):
    """Displays formatted command reference."""
    print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-MEDIA COMMAND & CLI REFERENCE                 │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-media                       │
│ • Play Audio Track:  blaze-media --play <path>         │
│ • Pause Playback:    blaze-media --pause               │
│ • Resume Playback:   blaze-media --resume              │
│ • Stop Playback:     blaze-media --stop                │
│ • Playback Radar:    blaze-media --info                │
│ • Set Volume:        blaze-media --volume <0-15>       │
│ • Browse Audio:      blaze-media --browse [dir]        │
│ • Speak Text (TTS):  blaze-media --speak "<text>"      │
│ • Vibrate Motor:     blaze-media --vibrate [ms]        │
│ • Sync MediaStore:   blaze-media --scan [path]         │
│ • JSON Machine Mode: blaze-media --json                │
└────────────────────────────────────────────────────────┘{RESET}
""")
    if pause:
        safe_pause("Press Enter to return...")

# --- Interactive Main Menu ---

def interactive_menu():
    """Interactive FZF terminal menu matching blaze standard."""
    menu_items = [
        "📁 1. Hierarchical Audio Explorer   ──► Browse folders, 1-click play, stream & pull (FZF)",
        "📻 2. Media Playback Radar         ──► Real-time track, position & progress bar",
        "⏸️ 3. Pause Audio Playback          ──► Pause currently playing track",
        "▶️ 4. Resume Audio Playback         ──► Resume playback",
        "⏹️ 5. Stop Audio Playback           ──► Stop and release media engine",
        "🔊 6. Volume Master Console         ──► Set hardware volume for Music, Ring, Alarm, Call",
        "🗣️ 7. Text-to-Speech (TTS Engine)   ──► Speak arbitrary text aloud on phone speakers",
        "📳 8. Haptic Vibration Pulse        ──► Trigger vibration pulse on phone motor",
        "🔄 9. Re-index Android MediaStore   ──► Refresh gallery & music player library",
        "📖 10. Help & CLI Reference         ──► Flags, command switches & examples",
        "🚪 0. Exit                         ──► Return to PowerShell terminal"
    ]

    while True:
        try:
            chosen = run_fzf(menu_items, prompt="Blaze Media > ", header="🎵 BLAZE AUDIO BROWSER & MEDIA COMMAND HUB")
            if not chosen or "0. Exit" in chosen:
                print(f"{DIM}👋 Exited.{RESET}\n")
                break

            if "1. Hierarchical" in chosen:
                dir_opts = [
                    "1. 🎵 /sdcard/Music/     ──► Primary music collection",
                    "2. 📥 /sdcard/Download/  ──► Downloaded audio & voice notes",
                    "3. 💻 /sdcard/Motobook/  ──► Motobook sync folder",
                    "4. 📂 /sdcard/ (Root)    ──► Entire storage directory",
                    "0. 🔙 Back to Menu       ──► Cancel"
                ]
                d_sel = run_fzf(dir_opts, prompt="Music Folder > ", header="SELECT INITIAL AUDIO DIRECTORY")
                if d_sel and "0. 🔙" not in d_sel:
                    target_d = "/sdcard/Music"
                    if "Download" in d_sel: target_d = "/sdcard/Download"
                    elif "Motobook" in d_sel: target_d = "/sdcard/Motobook"
                    elif "Root" in d_sel: target_d = "/sdcard"
                    browse_and_play(target_d)
            elif "2. Media Playback" in chosen:
                get_media_info()
                safe_pause()
            elif "3. Pause Audio" in chosen:
                pause_media()
                safe_pause()
            elif "4. Resume Audio" in chosen:
                resume_media()
                safe_pause()
            elif "5. Stop Audio" in chosen:
                stop_media()
                safe_pause()
            elif "6. Volume Master" in chosen:
                interactive_volume_console()
            elif "7. Text-to-Speech" in chosen:
                try:
                    txt = input(f"{CYAN}Enter text to speak on Blaze: {RESET}").strip()
                    if txt:
                        speak_tts(txt)
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "8. Haptic Vibration" in chosen:
                try:
                    ms_str = input(f"{CYAN}Enter vibration duration in ms [default: 500]: {RESET}").strip() or "500"
                    if ms_str.isdigit():
                        vibrate_phone(int(ms_str))
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "9. Re-index" in chosen:
                scan_mediastore()
                safe_pause()
            elif "10. Help" in chosen:
                show_help_manual(pause=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}\n")
            break

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blaze Hierarchical Audio Browser, Media Player & Sound Engine Hub",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("--play", metavar="PATH", help="Play audio file on Blaze")
        parser.add_argument("--pause", action="store_true", help="Pause playback")
        parser.add_argument("--resume", action="store_true", help="Resume playback")
        parser.add_argument("--stop", action="store_true", help="Stop playback")
        parser.add_argument("--info", action="store_true", help="View active playback radar")
        parser.add_argument("--volume", type=int, metavar="0-15", help="Set system volume level (0-15)")
        parser.add_argument("--stream", default="music", choices=["music", "ring", "notification", "alarm", "system", "call"], help="Target audio volume stream")
        parser.add_argument("--speak", metavar="TEXT", help="Speak text aloud via Android TTS synthesizer")
        parser.add_argument("--vibrate", type=int, nargs="?", const=500, metavar="MS", help="Vibrate phone motor (ms)")
        parser.add_argument("--scan", nargs="?", const="/sdcard/Music", metavar="PATH", help="Re-index MediaStore")
        parser.add_argument("--browse", metavar="DIR", nargs="?", const="/sdcard/Music", help="Launch interactive audio explorer")
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
            set_volume(args.volume, stream=args.stream)
        elif args.speak:
            speak_tts(args.speak)
        elif args.vibrate is not None:
            vibrate_phone(args.vibrate)
        elif args.scan:
            scan_mediastore(args.scan)
        elif args.browse:
            browse_and_play(args.browse)
        else:
            interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Exited gracefully.{RESET}")

if __name__ == "__main__":
    main()
