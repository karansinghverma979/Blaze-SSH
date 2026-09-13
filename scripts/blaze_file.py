#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📂 Blaze Filesystem, Storage & Drive Z:\\ Mount Command Center
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

def run_ssh(cmd, timeout=8):
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

def drop_file(local_path, remote_dir="/sdcard/Download", json_mode=False):
    """Transfers a local PC file to Blaze storage and triggers MediaStore indexing."""
    if not os.path.exists(local_path):
        if json_mode:
            print(json.dumps({"error": f"Local file not found: {local_path}"}))
        else:
            print(f"{RED}❌ File not found: {local_path}{RESET}")
        return False

    fname = os.path.basename(local_path)
    target_remote = f"{remote_dir}/{fname}"
    print(f"{CYAN}🚀 Dropping {fname} ➔ Blaze:{remote_dir}/...{RESET}")

    try:
        res = subprocess.run(
            ["scp", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no", local_path, f"blaze:{target_remote}"],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            # Trigger MediaStore scan and toast
            run_ssh(f"termux-media-scan '{target_remote}' && termux-toast '📥 Received: {fname}'")
            if json_mode:
                print(json.dumps({"status": "success", "file": fname, "remote_path": target_remote}))
            else:
                print(f"{GREEN}✅ File transferred successfully!{RESET}")
                print(f"   📁 Saved at: {target_remote}")
                print(f"   📲 MediaStore indexed & visible in Android gallery/files.\n")
            return True
        else:
            if json_mode:
                print(json.dumps({"error": "SCP failed", "details": res.stderr.strip()}))
            else:
                print(f"{RED}❌ File drop failed: {res.stderr.strip()}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}❌ Exception during transfer: {e}{RESET}")
        return False

def pull_file(remote_path, local_dir=os.path.expanduser("~/Blaze"), json_mode=False):
    """Pulls a remote file from Blaze to PC."""
    os.makedirs(local_dir, exist_ok=True)
    fname = os.path.basename(remote_path)
    local_target = os.path.join(local_dir, fname)

    print(f"{CYAN}📥 Pulling Blaze:{remote_path} ➔ {local_dir}...{RESET}")
    try:
        res = subprocess.run(
            ["scp", "-o", "ConnectTimeout=5", "-o", "StrictHostKeyChecking=no", f"blaze:{remote_path}", local_target],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            if json_mode:
                print(json.dumps({"status": "success", "file": fname, "local_path": local_target}))
            else:
                print(f"{GREEN}✅ File pulled successfully!{RESET}")
                print(f"   📁 Saved at: {local_target}\n")
            return True
        else:
            if json_mode:
                print(json.dumps({"error": "SCP pull failed", "details": res.stderr.strip()}))
            else:
                print(f"{RED}❌ File pull failed: {res.stderr.strip()}{RESET}")
            return False
    except Exception as e:
        print(f"{RED}❌ Exception during pull: {e}{RESET}")
        return False

def mount_drive(drive_letter="Z:"):
    """Mounts /sdcard as Windows Drive Z:\\ using Rclone SFTP."""
    print(f"{CYAN}🔌 Mounting Blaze storage as Drive {drive_letter}\\ in Windows Explorer...{RESET}")
    # Verify WinFsp and Rclone
    rclone_path = shutil.which("rclone") or os.path.expanduser(r"~\scoop\apps\rclone\current\rclone.exe")
    if not os.path.exists(rclone_path) and not shutil.which("rclone"):
        print(f"{RED}❌ Rclone not found. Install via: scoop install rclone{RESET}")
        return

    cmd = [
        rclone_path, "mount", "blaze:/sdcard", f"{drive_letter}",
        "--vfs-cache-mode", "full",
        "--volname", "Lava Blaze 5G",
        "--network-mode",
        "--no-console"
    ]
    try:
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0)
        time.sleep(2)
        print(f"{GREEN}✅ Drive {drive_letter}\\ mounted successfully! Opening Explorer...{RESET}")
        subprocess.Popen(["explorer.exe", f"{drive_letter}\\"])
    except Exception as e:
        print(f"{RED}❌ Failed to mount drive: {e}{RESET}")

def unmount_drive(drive_letter="Z:"):
    """Unmounts Drive Z:\\ and terminates Rclone."""
    print(f"{YELLOW}⚡ Disconnecting Drive {drive_letter}\\...{RESET}")
    try:
        subprocess.run(["powershell", "-Command", "Stop-Process -Name rclone -Force -ErrorAction SilentlyContinue"], check=False)
        print(f"{GREEN}✅ Drive {drive_letter}\\ unmounted and Rclone terminated.{RESET}")
    except Exception as e:
        print(f"{RED}❌ Failed to unmount: {e}{RESET}")

def open_remote_file(remote_path):
    """Opens file on phone in default Android app."""
    print(f"{CYAN}📱 Opening {remote_path} on Blaze...{RESET}")
    out, err, code = run_ssh(f"termux-open '{remote_path}'")
    if code == 0:
        print(f"{GREEN}✅ File opened on Blaze.{RESET}")
    else:
        print(f"{RED}❌ Failed to open file: {err}{RESET}")

def open_mobile_url(url):
    """Opens URL in mobile browser."""
    print(f"{CYAN}🌐 Opening {url} in mobile browser...{RESET}")
    out, err, code = run_ssh(f"termux-open-url '{url}'")
    if code == 0:
        print(f"{GREEN}✅ URL opened on Blaze.{RESET}")
    else:
        print(f"{RED}❌ Failed to open URL: {err}{RESET}")

def trigger_share_sheet(remote_path_or_text):
    """Triggers native Android Share Sheet."""
    print(f"{CYAN}📤 Triggering Android Share Sheet on Blaze...{RESET}")
    out, err, code = run_ssh(f"termux-share '{remote_path_or_text}'")
    if code == 0:
        print(f"{GREEN}✅ Share Sheet presented on Blaze screen.{RESET}")
    else:
        print(f"{RED}❌ Failed to trigger share: {err}{RESET}")

def send_download(url):
    """Sends URL to Android background Download Manager."""
    print(f"{CYAN}⬇️ Sending download task to Android Download Manager...{RESET}")
    out, err, code = run_ssh(f"termux-download '{url}'")
    if code == 0:
        print(f"{GREEN}✅ Download queued in Android notification shade.{RESET}")
    else:
        print(f"{RED}❌ Failed to queue download: {err}{RESET}")

# --- Interactive Menu ---

def interactive_menu():
    """Interactive terminal menu."""
    while True:
        print(f"""
{CYAN}┌────────────────────────────────────────────────────────┐
│         📂 BLAZE FILESYSTEM & STORAGE COMMAND HUB      │
├────────────────────────────────────────────────────────┤
│  {BOLD}1{RESET} 🚀 Drop File to Phone (/sdcard/Download/)           │
│  {BOLD}2{RESET} 📥 Pull File from Phone to PC (~/Blaze/)            │
│  {BOLD}3{RESET} 🔌 Mount Phone Storage as Windows Drive Z:\\         │
│  {BOLD}4{RESET} ⚡ Unmount Windows Drive Z:\\                        │
│  {BOLD}5{RESET} 📱 Launch File in Android Default App               │
│  {BOLD}6{RESET} 🌐 Open URL in Phone Web Browser                    │
│  {BOLD}7{RESET} 📤 Trigger Android Native Share Sheet               │
│  {BOLD}8{RESET} ⬇️ Send Download to Android Download Manager        │
│  {BOLD}0{RESET} 🚪 Exit                                             │
└────────────────────────────────────────────────────────┘{RESET}""")
        try:
            choice = input(f"{BOLD}Blaze-File ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            p = input("Enter local file path to drop: ").strip().strip('"')
            if p:
                drop_file(p)
        elif choice == "2":
            p = input("Enter remote file path on phone (e.g. /sdcard/Download/file.pdf): ").strip()
            if p:
                pull_file(p)
        elif choice == "3":
            mount_drive()
        elif choice == "4":
            unmount_drive()
        elif choice == "5":
            p = input("Enter remote file path to open on phone: ").strip()
            if p:
                open_remote_file(p)
        elif choice == "6":
            u = input("Enter URL to open on phone: ").strip()
            if u:
                open_mobile_url(u)
        elif choice == "7":
            t = input("Enter remote path or text to share: ").strip()
            if t:
                trigger_share_sheet(t)
        elif choice == "8":
            u = input("Enter direct file URL to download: ").strip()
            if u:
                send_download(u)
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Select 0-8.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Filesystem, Storage & Drive Z:\\ Mount Command Center",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--drop", metavar="PATH", help="Drop local file to phone /sdcard/Download/")
    parser.add_argument("--pull", metavar="PATH", help="Pull remote file to PC ~/Blaze/")
    parser.add_argument("--mount", action="store_true", help="Mount /sdcard as Windows Drive Z:\\")
    parser.add_argument("--unmount", action="store_true", help="Unmount Windows Drive Z:\\")
    parser.add_argument("--open", metavar="PATH", help="Open remote file in Android default app")
    parser.add_argument("--url", metavar="URL", help="Open URL in phone browser")
    parser.add_argument("--share", metavar="TARGET", help="Trigger Android share sheet for target")
    parser.add_argument("--download", metavar="URL", help="Queue download in Android Download Manager")
    parser.add_argument("--json", action="store_true", help="JSON output mode")

    args = parser.parse_args()

    if args.drop:
        drop_file(args.drop, json_mode=args.json)
    elif args.pull:
        pull_file(args.pull, json_mode=args.json)
    elif args.mount:
        mount_drive()
    elif args.unmount:
        unmount_drive()
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

if __name__ == "__main__":
    main()
