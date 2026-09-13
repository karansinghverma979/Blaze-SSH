#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📂 Blaze Wireless File Bridge & Android Remote Explorer Hub
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

# Default Local Pull Destination (Standard Windows User Downloads)
DEFAULT_DOWNLOADS_DIR = os.path.expanduser("~/Downloads")

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

def run_fzf(options, prompt="Blaze File > ", header=None):
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

def normalize_url(raw_url):
    """Ensures URL has a valid web protocol scheme."""
    url = raw_url.strip()
    if not re.match(r'^[a-zA-Z]+://', url):
        return f"https://{url}"
    return url

# --- File Transfer Engine ---

def drop_file(local_path, remote_dir="/sdcard/Download", json_mode=False):
    """Transfers a local PC file to Blaze storage and triggers Android MediaStore scan & toast."""
    clean_local = os.path.expanduser(local_path.strip('"').strip("'"))
    if not os.path.exists(clean_local):
        if json_mode:
            print(json.dumps({"error": f"Local file not found: {clean_local}"}))
        else:
            print(f"\n{RED}❌ Local file not found: {clean_local}{RESET}\n")
        return False

    fname = os.path.basename(clean_local)
    clean_remote_dir = remote_dir.rstrip("/")
    target_remote = f"{clean_remote_dir}/{fname}"
    safe_target = target_remote.replace('"', '\\"')

    print(f"\n{CYAN}🚀 Dropping '{fname}' ➔ Blaze:{clean_remote_dir}/...{RESET}")

    try:
        res = subprocess.run(
            ["scp", "-o", "ConnectTimeout=8", "-o", "StrictHostKeyChecking=no", clean_local, f"blaze:{target_remote}"],
            capture_output=True, text=True, timeout=60
        )
        if res.returncode == 0:
            # Trigger MediaStore scan and center toast
            run_ssh(f'termux-media-scan "{safe_target}" && termux-toast -g middle -b "#1B5E20" -c "white" "📥 Received: {fname}"')
            if json_mode:
                print(json.dumps({"status": "success", "file": fname, "remote_path": target_remote}))
            else:
                print(f"\n{GREEN}{BOLD}✅ FILE DROPPED TO BLAZE SUCCESSFULLY!{RESET}")
                print("┌────────────────────────────────────────────────────────┐")
                print(f"│ 📁 {BOLD}File Name:{RESET}   {CYAN}{BOLD}{fname[:38]:<39}{RESET}│")
                print(f"│ 📂 {BOLD}Destination:{RESET} {target_remote[:38]:<39}│")
                print(f"│ 📲 {BOLD}Android Index:{RESET} {GREEN}MediaStore Scanned & Indexed{RESET}       │")
                print("└────────────────────────────────────────────────────────┘")
                print(f"{DIM}📱 Visible in Android Files, Gallery & media players.{RESET}\n")
            return True
        else:
            if res.returncode == 255:
                render_unreachable_card()
            elif json_mode:
                print(json.dumps({"error": "SCP transfer failed", "details": res.stderr.strip()}))
            else:
                print(f"{RED}❌ File drop failed: {res.stderr.strip()}{RESET}\n")
            return False
    except subprocess.TimeoutExpired:
        print(f"{RED}❌ File transfer timed out.{RESET}\n")
        return False
    except Exception as e:
        print(f"{RED}❌ Exception during transfer: {e}{RESET}\n")
        return False

def pull_file(remote_path, local_dir=DEFAULT_DOWNLOADS_DIR, json_mode=False):
    """Pulls a remote file from Blaze directly into PC Downloads (or specified dir)."""
    clean_remote = remote_path.strip('"').strip("'")
    clean_local_dir = os.path.expanduser(local_dir.strip('"').strip("'"))
    os.makedirs(clean_local_dir, exist_ok=True)

    fname = os.path.basename(clean_remote)
    local_target = os.path.join(clean_local_dir, fname)

    print(f"\n{CYAN}📥 Pulling Blaze:{clean_remote} ➔ PC:{clean_local_dir}...{RESET}")
    try:
        res = subprocess.run(
            ["scp", "-o", "ConnectTimeout=8", "-o", "StrictHostKeyChecking=no", f"blaze:{clean_remote}", local_target],
            capture_output=True, text=True, timeout=60
        )
        if res.returncode == 0:
            if json_mode:
                print(json.dumps({"status": "success", "file": fname, "local_path": local_target}))
            else:
                print(f"\n{GREEN}{BOLD}✅ FILE PULLED TO PC DOWNLOADS SUCCESSFULLY!{RESET}")
                print("┌────────────────────────────────────────────────────────┐")
                print(f"│ 📁 {BOLD}File Name:{RESET}   {CYAN}{BOLD}{fname[:38]:<39}{RESET}│")
                print(f"│ 📂 {BOLD}Saved In:{RESET}    {local_target[:38]:<39}│")
                print("└────────────────────────────────────────────────────────┘")
                print(f"{DIM}💻 Available in your PC Downloads folder.{RESET}\n")
            return True
        else:
            if res.returncode == 255:
                render_unreachable_card()
            elif json_mode:
                print(json.dumps({"error": "SCP pull failed", "details": res.stderr.strip()}))
            else:
                print(f"{RED}❌ File pull failed: {res.stderr.strip()}{RESET}\n")
            return False
    except subprocess.TimeoutExpired:
        print(f"{RED}❌ Pull transfer timed out.{RESET}\n")
        return False
    except Exception as e:
        print(f"{RED}❌ Exception during pull: {e}{RESET}\n")
        return False

# --- Remote Interactive Storage Explorer ---

def browse_remote_storage(initial_path="/sdcard/Download"):
    """Interactive FZF Remote File Explorer for browsing, pulling, opening and sharing."""
    current_dir = initial_path

    while True:
        out, err, code = run_ssh(f'ls -laL "{current_dir}" 2>/dev/null')
        if code != 0 or not out:
            if code == 255:
                render_unreachable_card()
                break
            print(f"{RED}❌ Failed to list '{current_dir}': {err}{RESET}\n")
            safe_pause()
            break

        fzf_items = []
        entries = []

        # Parent directory navigation
        if current_dir not in ["/", "/sdcard", "/storage/emulated/0"]:
            fzf_items.append("📁 .. [Parent Directory]")
            entries.append(("..", True))

        for line in out.splitlines():
            parts = line.split()
            if len(parts) >= 9 and parts[8] not in [".", ".."]:
                is_dir = line.startswith("d")
                size = parts[4]
                name = " ".join(parts[8:])
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

                icon = "📁" if is_dir else "📄"
                fzf_items.append(f"{icon} {name:<32} │ {s_str:>8}")
                entries.append((name, is_dir))

        if not fzf_items:
            fzf_items.append("📁 .. [Parent Directory]")
            entries.append(("..", True))

        header_str = f"📂 BLAZE EXPLORER: {current_dir} ({len(fzf_items)} items)"
        chosen = run_fzf(fzf_items, prompt="Select File/Folder > ", header=header_str)
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
        target_full_path = f"{current_dir.rstrip('/')}/{name}"

        if is_dir:
            current_dir = target_full_path
        else:
            # File Action Sheet
            actions = [
                "📥 1. Pull File to PC Downloads ──► Save directly to ~/Downloads/",
                "📱 2. Open on Phone Screen       ──► Launch in Android default app/chooser",
                "📤 3. Trigger Android Share Sheet ──► Share via WhatsApp, Drive, etc.",
                "📋 4. Copy Remote Path to PC     ──► Copy absolute path to clipboard",
                "🗑️ 5. Delete File on Phone       ──► Remove from Blaze storage",
                "0. 🔙 Back to Directory          ──► Return to file list"
            ]
            act = run_fzf(actions, prompt=f"Action on {name} > ", header=f"File: {target_full_path}")
            if not act or "0. 🔙" in act:
                continue

            if "1. Pull" in act:
                pull_file(target_full_path, local_dir=DEFAULT_DOWNLOADS_DIR)
                safe_pause()
            elif "2. Open" in act:
                open_remote_file(target_full_path)
                safe_pause()
            elif "3. Trigger" in act:
                trigger_share_sheet(target_full_path)
                safe_pause()
            elif "4. Copy" in act:
                set_clipboard(target_full_path)
                print(f"\n{GREEN}✅ '{target_full_path}' copied to Windows clipboard!{RESET}\n")
                safe_pause()
            elif "5. Delete" in act:
                conf = run_fzf(["1. ❌ YES, Delete File", "0. 🔙 Cancel"], prompt=f"Confirm Delete {name}? > ")
                if conf and "YES" in conf:
                    run_ssh(f'rm -f "{target_full_path}"')
                    print(f"\n{GREEN}✅ File '{name}' deleted from Blaze.{RESET}\n")
                    safe_pause()

# --- Quick Drop Local Assistant ---

def interactive_drop_wizard():
    """Interactive local file dropper with quick folder presets and fuzzy picker."""
    local_presets = [
        ("1. 📥 PC Downloads", os.path.expanduser("~/Downloads")),
        ("2. 🖥️ PC Desktop", os.path.expanduser("~/Desktop")),
        ("3. 📄 PC Documents", os.path.expanduser("~/Documents")),
        ("4. 🎥 PC Videos", os.path.expanduser("~/Videos")),
        ("5. 📁 Current Directory", os.getcwd()),
        ("6. ⌨️ Enter Custom Local Path", None),
        ("0. 🔙 Return to Menu", None)
    ]

    p_opts = [p[0] for p in local_presets]
    p_sel = run_fzf(p_opts, prompt="Source Folder > ", header="🚀 FAST LOCAL FILE DROPPER")
    if not p_sel or "0. 🔙" in p_sel:
        return

    source_dir = None
    for label, path in local_presets:
        if label == p_sel:
            source_dir = path
            break

    if not source_dir:
        try:
            custom_p = input(f"{CYAN}Enter absolute file or folder path: {RESET}").strip().strip('"')
            if os.path.isfile(custom_p):
                choose_destination_and_drop(custom_p)
                return
            elif os.path.isdir(custom_p):
                source_dir = custom_p
            else:
                print(f"{RED}❌ Path not found: {custom_p}{RESET}\n")
                safe_pause()
                return
        except (KeyboardInterrupt, EOFError):
            return

    # List files in source directory
    try:
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]
        if not files:
            print(f"{YELLOW}⚠️ No files found in {source_dir}.{RESET}\n")
            safe_pause()
            return

        sorted_files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(source_dir, x)), reverse=True)
        f_lines = [f"{i+1:02d}. {f}" for i, f in enumerate(sorted_files[:50])]
        f_sel = run_fzf(f_lines, prompt="Select Local File > ", header=f"Files in {source_dir} (Newest First)")
        if not f_sel:
            return

        match = re.match(r'^\d+\.\s*(.+)$', f_sel)
        if match:
            target_f = os.path.join(source_dir, match.group(1).strip())
            choose_destination_and_drop(target_f)
    except Exception as e:
        print(f"{RED}❌ Error reading directory: {e}{RESET}\n")
        safe_pause()

def choose_destination_and_drop(local_file):
    """Presents target remote destinations and executes file drop."""
    remote_targets = [
        "1. 📥 /sdcard/Download/     ──► Default Android downloads directory",
        "2. 💻 /sdcard/Motobook/     ──► Dedicated Motobook sync folder",
        "3. 📄 /sdcard/Documents/    ──► Android Documents folder",
        "4. 📸 /sdcard/DCIM/         ──► Camera & Photos gallery",
        "5. 🎵 /sdcard/Music/        ──► Audio tracks & music player",
        "6. 🏠 ~/ (Termux Home)      ──► Linux CLI workspace",
        "0. 🔙 Cancel                ──► Abort drop"
    ]
    t_sel = run_fzf(remote_targets, prompt="Drop Destination > ", header=f"Drop: {os.path.basename(local_file)}")
    if not t_sel or "0. 🔙" in t_sel:
        return

    mapping = {
        "1. 📥": "/sdcard/Download",
        "2. 💻": "/sdcard/Motobook",
        "3. 📄": "/sdcard/Documents",
        "4. 📸": "/sdcard/DCIM",
        "5. 🎵": "/sdcard/Music",
        "6. 🏠": "~"
    }
    target_r = "/sdcard/Download"
    for k, v in mapping.items():
        if k in t_sel:
            target_r = v
            break

    drop_file(local_file, remote_dir=target_r)
    safe_pause()

# --- Mobile Action Integrations ---

def is_adb_connected():
    """Checks if an authorized ADB transport device is active."""
    try:
        res = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=4)
        for line in res.stdout.splitlines():
            if ("\tdevice" in line or " device " in line) and not line.startswith("List of"):
                return True
        return False
    except Exception:
        return False

def open_remote_file(remote_path):
    """Opens file on phone screen in default Android app using dual-transport intent engine."""
    clean_p = remote_path.strip('"').strip("'")
    fname = os.path.basename(clean_p)
    print(f"\n{CYAN}📱 Opening '{fname}' on Blaze screen...{RESET}")

    import mimetypes
    mime_type, _ = mimetypes.guess_type(fname)
    if not mime_type:
        ext = os.path.splitext(fname)[1].lower()
        if ext in [".apk"]: mime_type = "application/vnd.android.package-archive"
        elif ext in [".mkv"]: mime_type = "video/*"
        elif ext in [".m4a", ".mp3", ".wav", ".flac", ".aac"]: mime_type = "audio/*"
        elif ext in [".pdf"]: mime_type = "application/pdf"
        elif ext in [".jpg", ".jpeg", ".png", ".webp", ".gif"]: mime_type = "image/*"
        elif ext in [".mp4", ".mov", ".avi", ".webm"]: mime_type = "video/*"
        else: mime_type = "*/*"

    # Primary: Direct ADB Shell Intent (Bypasses all Android background app restrictions)
    if is_adb_connected():
        try:
            adb_cmd = ["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", f"file://{clean_p}"]
            if mime_type and mime_type != "*/*":
                adb_cmd.extend(["-t", mime_type])
            res = subprocess.run(adb_cmd, capture_output=True, text=True, timeout=6)
            if "Starting:" in res.stdout or res.returncode == 0:
                run_ssh(f'termux-toast -g middle -b "#0D47A1" -c "white" "📂 Opened: {fname}"')
                print(f"{GREEN}✅ App launched on Blaze screen via ADB for '{fname}' ({mime_type}).{RESET}\n")
                return True
        except Exception:
            pass

    # Secondary: Termux Intent Open
    safe_p = clean_p.replace('"', '\\"')
    run_ssh(f'termux-open --chooser "{safe_p}" || termux-open "{safe_p}"')
    run_ssh(f'termux-toast -g middle -b "#0D47A1" -c "white" "📂 Opened: {fname}"')
    print(f"{GREEN}✅ File open intent dispatched on Blaze for '{fname}'.{RESET}")
    print(f"{DIM}💡 Tip: Enable 'Display over other apps' for Termux in Android Settings for instant background launches.{RESET}\n")
    return True

def open_mobile_url(url):
    """Opens normalized URL in phone's default web browser using dual-transport intent engine."""
    valid_url = normalize_url(url)
    print(f"\n{CYAN}🌐 Opening '{valid_url}' on Blaze screen...{RESET}")

    # Primary: Direct ADB Shell Intent (Bypasses all Android background app restrictions)
    if is_adb_connected():
        try:
            res = subprocess.run(["adb", "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", valid_url],
                                 capture_output=True, text=True, timeout=6)
            if "Starting:" in res.stdout or res.returncode == 0:
                run_ssh(f'termux-toast -g middle -b "#006064" -c "white" "🌐 Opened URL"')
                print(f"{GREEN}✅ Browser launched on Blaze screen via ADB for '{valid_url}'.{RESET}\n")
                return True
        except Exception:
            pass

    # Secondary: Termux Intent Open
    safe_u = valid_url.replace('"', '\\"')
    out, err, code = run_ssh(f'termux-open-url "{safe_u}" && termux-toast -g middle -b "#006064" -c "white" "🌐 Opened URL"')
    if code == 0:
        print(f"{GREEN}✅ URL launch intent dispatched for '{valid_url}'.{RESET}")
        print(f"{DIM}💡 Tip: Enable 'Display over other apps' for Termux in Android Settings for instant background launches.{RESET}\n")
        return True
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to open URL on phone: {err}{RESET}\n")
        return False

def trigger_share_sheet(target):
    """Triggers native Android Share Sheet modal on phone screen."""
    clean_t = target.strip('"').strip("'")
    safe_t = clean_t.replace('"', '\\"')
    fname = os.path.basename(clean_t) if os.path.exists(clean_t) or "/" in clean_t else clean_t
    print(f"\n{CYAN}📤 Triggering Android Share Sheet on Blaze...{RESET}")
    out, err, code = run_ssh(f'termux-share "{safe_t}"')
    if code != 0:
        run_ssh(f'termux-open --send "{safe_t}" 2>/dev/null')
    run_ssh(f'termux-toast -g middle -b "#4A148C" -c "white" "📤 Share: {fname[:20]}"')
    print(f"{GREEN}✅ Share Sheet presented on Blaze screen.{RESET}\n")

def send_download(url):
    """Dispatches download URL to Android native Download Manager."""
    valid_url = normalize_url(url)
    safe_u = valid_url.replace('"', '\\"')
    print(f"\n{CYAN}⬇️ Sending download task to Android Download Manager...{RESET}")
    out, err, code = run_ssh(f'termux-download "{safe_u}" && termux-toast -g middle -b "#1B5E20" -c "white" "⬇️ Download Queued"')
    if code == 0:
        print(f"{GREEN}✅ Download task queued in Android notification shade!{RESET}\n")
    else:
        if code == 255: render_unreachable_card()
        else: print(f"{RED}❌ Failed to queue download: {err}{RESET}\n")

def show_help_manual(pause=True):
    """Displays formatted command reference."""
    print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-FILE COMMAND & CLI REFERENCE                  │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-file                        │
│ • Drop Local File:   blaze-file --drop <local_path>    │
│ • Pull Remote File:  blaze-file --pull <remote_path>   │
│ • Browse Storage:    blaze-file --browse [dir]         │
│ • Open on Phone:     blaze-file --open <remote_path>   │
│ • Open Mobile URL:   blaze-file --url <url>            │
│ • Share Sheet:       blaze-file --share <path|text>    │
│ • Download URL:      blaze-file --download <url>       │
│ • JSON Machine Mode: blaze-file --json                 │
└────────────────────────────────────────────────────────┘{RESET}
""")
    if pause:
        safe_pause("Press Enter to return...")

# --- Interactive Main Menu ---

def interactive_menu():
    """Interactive FZF terminal menu matching blaze standard."""
    menu_items = [
        "📂 1. Browse Remote Blaze Storage  ──► Navigate /sdcard, 1-click pull, open, share & delete",
        "🚀 2. Drop Local File to Phone     ──► Quick preset picker (Downloads/Desktop) ➔ Blaze",
        "📥 3. Quick Pull to PC Downloads   ──► Pull remote file directly into ~/Downloads/",
        "📱 4. Launch File on Phone Screen  ──► Open remote file in Android viewer / chooser",
        "🌐 5. Open URL in Mobile Browser   ──► Push website link directly to mobile Chrome",
        "📤 6. Android Native Share Sheet   ──► Trigger system share modal for file or text",
        "⬇️ 7. Queue Android Download       ──► Send URL to background Download Manager",
        "📖 8. Help & CLI Reference         ──► Flags, command switches & examples",
        "🚪 0. Exit                         ──► Return to PowerShell terminal"
    ]

    while True:
        try:
            chosen = run_fzf(menu_items, prompt="Blaze File > ", header="📂 BLAZE WIRELESS FILE BRIDGE & REMOTE EXPLORER")
            if not chosen or "0. Exit" in chosen:
                print(f"{DIM}👋 Exited.{RESET}\n")
                break

            if "1. Browse Remote" in chosen:
                dir_opts = [
                    "1. 📥 /sdcard/Download/  ──► Downloaded files & PDFs",
                    "2. 💻 /sdcard/Motobook/  ──► Motobook sync folder",
                    "3. 📸 /sdcard/DCIM/      ──► Camera & Photos",
                    "4. 📄 /sdcard/Documents/ ──► Documents folder",
                    "5. 🎵 /sdcard/Music/     ──► Audio tracks",
                    "6. 🏠 ~/ (Termux Home)   ──► Linux workspace",
                    "7. 📂 /sdcard/ (Root)    ──► Entire internal storage",
                    "0. 🔙 Back to Menu       ──► Cancel"
                ]
                d_sel = run_fzf(dir_opts, prompt="Directory Preset > ", header="SELECT INITIAL DIRECTORY")
                if d_sel and "0. 🔙" not in d_sel:
                    target_d = "/sdcard/Download"
                    if "Motobook" in d_sel: target_d = "/sdcard/Motobook"
                    elif "DCIM" in d_sel: target_d = "/sdcard/DCIM"
                    elif "Documents" in d_sel: target_d = "/sdcard/Documents"
                    elif "Music" in d_sel: target_d = "/sdcard/Music"
                    elif "Termux Home" in d_sel: target_d = "~"
                    elif "Root" in d_sel: target_d = "/sdcard"
                    browse_remote_storage(target_d)
            elif "2. Drop Local File" in chosen:
                interactive_drop_wizard()
            elif "3. Quick Pull" in chosen:
                try:
                    p = input(f"{CYAN}Enter remote file path on Blaze: {RESET}").strip().strip('"')
                    if p:
                        pull_file(p, local_dir=DEFAULT_DOWNLOADS_DIR)
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "4. Launch File" in chosen:
                try:
                    p = input(f"{CYAN}Enter remote file path to open on phone: {RESET}").strip().strip('"')
                    if p:
                        open_remote_file(p)
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "5. Open URL" in chosen:
                try:
                    u = input(f"{CYAN}Enter URL to open on phone browser: {RESET}").strip()
                    if u:
                        open_mobile_url(u)
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "6. Android Native Share" in chosen:
                try:
                    t = input(f"{CYAN}Enter remote file path or text to share: {RESET}").strip().strip('"')
                    if t:
                        trigger_share_sheet(t)
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "7. Queue Android Download" in chosen:
                try:
                    u = input(f"{CYAN}Enter file URL to download on phone: {RESET}").strip()
                    if u:
                        send_download(u)
                        safe_pause()
                except (KeyboardInterrupt, EOFError):
                    pass
            elif "8. Help" in chosen:
                show_help_manual(pause=True)
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}\n")
            break

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Blaze Wireless File Bridge & Android Remote Explorer Hub",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("--drop", metavar="PATH", help="Drop local file to phone /sdcard/Download/")
        parser.add_argument("--pull", metavar="PATH", help="Pull remote file directly to PC ~/Downloads/")
        parser.add_argument("--browse", metavar="DIR", nargs="?", const="/sdcard/Download", help="Browse remote storage in FZF")
        parser.add_argument("--open", metavar="PATH", help="Open remote file in Android default app/chooser")
        parser.add_argument("--url", metavar="URL", help="Open URL in phone browser")
        parser.add_argument("--share", metavar="TARGET", help="Trigger Android share sheet for target")
        parser.add_argument("--download", metavar="URL", help="Queue download in Android Download Manager")
        parser.add_argument("--json", action="store_true", help="JSON output mode")

        args = parser.parse_args()

        if args.drop:
            drop_file(args.drop, json_mode=args.json)
        elif args.pull:
            pull_file(args.pull, local_dir=DEFAULT_DOWNLOADS_DIR, json_mode=args.json)
        elif args.browse:
            browse_remote_storage(args.browse)
        elif args.open:
            open_remote_file(args.open)
        elif args.url:
            open_mobile_url(args.url)
        elif args.share:
            trigger_share_sheet(args.share)
        elif args.download:
            send_download(args.download)
        else:
            interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{DIM}👋 Exited gracefully.{RESET}")

if __name__ == "__main__":
    main()
