# ⚡ Blaze: Android Mobile Integration & Automation Hub

> **Device Pair**: `Motobook` (Windows 11 Pro) ⇄ `Blaze` (Lava Blaze 5G / Android 14)  
> **SSH Ports**: `22` (PC) / `8022` (Phone) | **Subnet**: `10.242.186.0/24`  
> **Author**: Karan Singh Verma & Antigravity Assistant

---

## 🎯 Purpose & Overview

**Blaze** is a unified multi-device automation suite connecting a Windows 11 workstation with an Android Termux node. It features dual-mode operation:
- **Interactive Terminal Menus (Default)**: Numbered ASCII menus for human exploration.
- **Fast-Path CLI Flags**: Instant single-shot execution (`--otp`, `--pull`, `--mount`) for power-users and headless AI automation.

---

## 🚀 The 7 Core Command Hubs

```text
┌─────────────────┬───────────────────────────────────┬───────────────────────────────────────┐
│ Command         │ Primary Responsibilities          │ Key CLI Switches                      │
├─────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
│ 📊 blaze-status │ Hardware Telemetry & Battery HUD  │ --battery, --wifi, --storage, --json  │
│ 📱 blaze-phone  │ Telephony, SMS, Contacts, 5G Info │ --otp, --sms, --contacts, --logs      │
│ 🌐 blaze-wifi   │ Wireless Radar, Scrcpy, ADB       │ --info, --scan, --stealth, --camera   │
│ 🎵 blaze-media  │ Audio Browser, Playback, Volume   │ --play, --pause, --volume, --scan     │
│ 🎙️ blaze-speak  │ Neural Edge-TTS Voice Center      │ "<text>", -v <persona>, --clip        │
│ 📋 blaze-clip   │ Bidirectional Clipboard Bridge    │ --pull, --push, --sync, --send        │
│ 🔔 blaze-notifs │ Notifications, Toasts & Dialogs   │ --list, --otp, --toast, --dialog      │
│ 📂 blaze-file   │ File Transfers, Drive Z:\ Mount   │ --drop, --pull, --mount, --unmount    │
└─────────────────┴───────────────────────────────────┴───────────────────────────────────────┘
```

---

## 🛠️ Complete Setup & PowerShell Profile Installation

### 1. Prerequisites
- **Windows PC**: Python 3.10+, OpenSSH Client/Server, Scoop (`scoop install scrcpy adb rclone`)
- **Android Phone**: Termux & Termux:API (`pkg install openssh termux-api python`)
- **SSH Key Trust**: Copy your `~/.ssh/id_ed25519.pub` from PC into Termux `~/.ssh/authorized_keys`.

---

### 2. How to Configure Your PowerShell Profile

You have **two easy methods** to integrate Blaze commands into your daily terminal:

#### 🌟 Method A: Dot-Source Standalone Module (Recommended & Easiest)
Open your PowerShell profile file by running:
```powershell
notepad $PROFILE
```
Add this single line at the bottom of the file:
```powershell
. "$env:USERPROFILE\Void\Blaze\blaze_profile.ps1"
```
*Save and reload your terminal (`. $PROFILE`). All `blaze-*` commands are now permanently active!*

---

#### 📋 Method B: Copy & Paste Directly into Profile
If you prefer embedding the code directly, open `blaze_profile.ps1` from this repository, copy its entire contents, and paste it into your `$PROFILE`.

---

### ⚙️ What to Customize (For Your Own Network & Phone)
If you are setting this up on a new device or router, edit the variables inside [`blaze_profile.ps1`](file:///C:/Users/karan/Void/Blaze/blaze_profile.ps1):
1. **Hardware MAC Address**: Set `$knownMac` to your phone's Wi-Fi MAC address for instantaneous router discovery.
2. **Termux Username**: If your Termux user differs from `u0_a46`, update `User <your-user>` in the `configContent` block.
3. **SSH Key Path**: Point `IdentityFile` to your desired private key (default: `~/.ssh/id_ed25519`).

---

## ⚡ Quick Start & Common Commands

```powershell
# 1. Instant 1-Click SMS OTP to PC Clipboard:
blaze-phone --otp

# 2. Pull Phone Clipboard to PC:
blaze-clip --pull

# 3. Mount Phone as Drive Z:\ in Windows Explorer:
blaze-file --mount

# 4. Launch 60fps Wireless Screen Stream (Stealth - Screen Off):
blaze-wifi --stealth

# 5. Open Interactive Voice Center:
blaze-speak
```

---

## 📁 Repository Structure

```text
C:\Users\karan\Void\Blaze\
├── .gitignore          # Exclusions for Python cache & temp files
├── README.md           # Master repository documentation & setup guide
├── RULES.md            # Invariants, safety rules & port allocations
├── INSTRUCTIONS.md     # In-depth operational runbook
├── ARCHITECTURE.md     # System topology & network specifications
├── SKILL.md            # Authoritative Antigravity AI assistant skill
├── blaze_profile.ps1   # Standalone PowerShell profile integration module
└── scripts/
    ├── blaze_status.py # System telemetry, battery HUD, Wi-Fi & storage radar
    ├── blaze_phone.py  # Telephony, SMS, Contacts & Cellular hub
    ├── blaze_wifi.py   # Wi-Fi radar, Scrcpy streaming & ADB hub
    ├── blaze_media.py  # Remote audio browser, player & volume hub
    ├── blaze_clip.py   # Unified clipboard sync & bridge hub
    ├── blaze_notifs.py # Notification inbox, alerts & mobile dialogs
    ├── blaze_file.py   # Filesystem transfer & Drive Z:\ mount hub
    └── blaze_speak.py  # Studio HD Neural Edge-TTS engine (20 voices)
```

---

## 📜 Governance & Architecture
- [RULES.md](file:///C:/Users/karan/Void/Blaze/RULES.md): Architectural invariants and safety protocols.
- [INSTRUCTIONS.md](file:///C:/Users/karan/Void/Blaze/INSTRUCTIONS.md): Detailed installation runbook.
- [ARCHITECTURE.md](file:///C:/Users/karan/Void/Blaze/ARCHITECTURE.md): System diagrams and data flow.
- [SKILL.md](file:///C:/Users/karan/Void/Blaze/SKILL.md): Antigravity AI Agent definition.
