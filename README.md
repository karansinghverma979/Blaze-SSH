# ⚡ Blaze: Android Mobile Integration & Automation Hub

> **Device Pair**: `Motobook` (Windows 11 Pro) ⇄ `Blaze` (Lava Blaze 5G / Android 14)  
> **SSH Ports**: `22` (PC) / `8022` (Phone) | **Wireless ADB**: Port `5555`  
> **Author**: Karan Singh Verma & Antigravity Assistant  
> **Repository**: [https://github.com/karansinghverma979/Blaze-SSH](https://github.com/karansinghverma979/Blaze-SSH)

---

## 🎯 Purpose & Overview

**Blaze** is a unified multi-device automation and control ecosystem connecting a Windows 11 workstation with an Android Termux node. It features dual-mode operation:
- **Interactive Inline FZF Menus (Default)**: Lightweight, non-intrusive fuzzy-search control hubs that render directly beneath the cursor in your active terminal.
- **Fast-Path CLI Flags**: Instant single-shot execution (`--otp`, `--pull`, `--push`, `--stealth`, `--dialog`) for power-users, shell scripts, and AI agent automation.
- **Dual-Transport Foreground Intent Engine**: Combines low-latency SSH commands on port `8022` with ADB shell foreground intents on port `5555` to open files, browser URLs, and media on the physical screen without Android 10+ background app restrictions.

---

## 🚀 The 10 Core Command Hubs

```text
┌───────────────────┬───────────────────────────────────────────┬───────────────────────────────────────┐
│ Command           │ Primary Responsibilities                  │ Key CLI Switches                      │
├───────────────────┼───────────────────────────────────────────┼───────────────────────────────────────┤
│ ⚡ blaze           │ Dynamic IP Auto-Discovery & Termux Shell  │ blaze "<remote_command>"              │
│ 📊 blaze-status   │ Hardware Telemetry & Battery HUD          │ --battery, --wifi, --storage, --json  │
│ 📱 blaze-phone    │ Calls, SMS Inbox, Contacts, 5G Telemetry  │ --otp, --sms, --call, --speaker       │
│ 📍 blaze-location │ GPS, Network Radar & Reverse Geocoding    │ --live, --gps, --network, --open      │
│ 🌐 blaze-wifi     │ Wi-Fi Radar, Scrcpy Streaming, ADB Hub    │ --info, --scan, --stealth, --camera   │
│ 🎵 blaze-media    │ Audio Browser, Scrcpy Opus Stream, Volume │ --play, --pause, --volume, --scan     │
│ 🎙️ blaze-speak    │ 20 Neural Edge-TTS Personas, REPL & Siren │ "<text>", -v <persona>, --clip, --alert│
│ 📋 blaze-clip     │ Bidirectional Clipboard Bridge (API v2)   │ --pull, --push, --sync, --send        │
│ 🔔 blaze-notifs   │ Status Bar Alerts, Screen Toasts, Dialogs │ --list, --otp, --toast, --dialog      │
│ 📂 blaze-file     │ File Bridge, Downloads Pull, Native Open  │ --drop, --pull, --browse, --open, --url│
└───────────────────┴───────────────────────────────────────────┴───────────────────────────────────────┘
```

---

## 📖 Interactive Menu Specifications (`Interfaces/`)

Every command features a visual layout and menu specification in the [`Interfaces/`](Interfaces/) directory:

| Interface Specification | Hub Scope & Documented Flow |
| :--- | :--- |
| ⚡ [`Interfaces/blaze.md`](Interfaces/blaze.md) | Terminal HUD, 3-Tier IP discovery, remote command fast-path. |
| 📊 [`Interfaces/blaze_status.md`](Interfaces/blaze_status.md) | Left-anchored instant telemetry HUD, filtered power/storage views, machine JSON. |
| 📱 [`Interfaces/blaze_phone.md`](Interfaces/blaze_phone.md) | 1-Click OTP extraction card, SMS inbox (newest-first), fuzzy contact book, earpiece/speakerphone dialer. |
| 📍 [`Interfaces/blaze_location.md`](Interfaces/blaze_location.md) | GPS radar HUD, reverse geocoded street address, Google Maps browser launch. |
| 🌐 [`Interfaces/blaze_wifi.md`](Interfaces/blaze_wifi.md) | Wi-Fi / Hotspot radar, Scrcpy streaming studio (7 presets), 1-click USB ADB wizard. |
| 🎵 [`Interfaces/blaze_media.md`](Interfaces/blaze_media.md) | Hierarchical audio explorer, playback radar, Scrcpy Opus PC streaming, 6-channel volume console. |
| 🎙️ [`Interfaces/blaze_speak.md`](Interfaces/blaze_speak.md) | Voice Center, Live Voice Chat REPL, persistent default persona, emergency siren. |
| 📋 [`Interfaces/blaze_clip.md`](Interfaces/blaze_clip.md) | Termux API v2 pull/push flows, side-by-side visual diff radar. |
| 🔔 [`Interfaces/blaze_notifs.md`](Interfaces/blaze_notifs.md) | Notification browser, 13-widget Mobile Dialog Studio, centered screen toast designer. |
| 📂 [`Interfaces/blaze_file.md`](Interfaces/blaze_file.md) | Remote storage explorer, local drop wizard, Downloads pull, dual-transport intent engine. |

---

## 🛠️ Complete Setup & PowerShell Profile Installation

### 1. Prerequisites
- **Windows PC**: Python 3.10+, OpenSSH Client/Server, Scoop (`scoop install scrcpy adb fzf`)
- **Android Phone**: Termux & Termux:API (`pkg install openssh termux-api python`)
- **SSH Key Trust**: Copy your `~/.ssh/id_ed25519.pub` from PC into Termux `~/.ssh/authorized_keys`.

---

### 2. How to Configure Your PowerShell Profile

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

## ⚡ Quick Start & Common Commands

```powershell
# 1. Instant 1-Click SMS / Notification OTP to PC Clipboard:
blaze-phone --otp

# 2. Pull Phone Clipboard to PC:
blaze-clip --pull

# 3. Drop a Local File to Phone (/sdcard/Download) + Auto MediaStore Scan:
blaze-file --drop "C:\Users\karan\Downloads\report.pdf"

# 4. Pull a Remote File from Phone directly to PC Downloads:
blaze-file --pull "/sdcard/Download/invoice.pdf"

# 5. Launch 60fps Wireless Screen Stream (Stealth - Phone Screen Off):
blaze-wifi --stealth

# 6. Open Interactive Voice Center (Neural Edge-TTS):
blaze-speak

# 7. Check Instant Battery, Wi-Fi & Storage Telemetry:
blaze-status
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
├── Interfaces/         # 10 High-density visual terminal interface specifications
│   ├── blaze.md
│   ├── blaze_status.md
│   ├── blaze_phone.md
│   ├── blaze_location.md
│   ├── blaze_wifi.md
│   ├── blaze_media.md
│   ├── blaze_speak.md
│   ├── blaze_clip.md
│   ├── blaze_notifs.md
│   └── blaze_file.md
└── scripts/
    ├── blaze_status.py # System telemetry, battery HUD, Wi-Fi & storage radar
    ├── blaze_phone.py  # Telephony, SMS, Contacts & Cellular hub
    ├── blaze_wifi.py   # Wi-Fi radar, Scrcpy streaming & ADB hub
    ├── blaze_media.py  # Remote audio browser, player & volume hub
    ├── blaze_clip.py   # Unified clipboard sync & bridge hub
    ├── blaze_notifs.py # Notification inbox, alerts & mobile dialogs
    ├── blaze_file.py   # Filesystem transfer & foreground intent hub
    ├── blaze_speak.py  # Studio HD Neural Edge-TTS engine (20 voices)
    └── blaze_location.py# GPS radar, reverse geocoding & maps
```

---

## 📜 Governance & Architecture
- [RULES.md](RULES.md): Architectural invariants and safety protocols.
- [INSTRUCTIONS.md](INSTRUCTIONS.md): Detailed installation runbook.
- [ARCHITECTURE.md](ARCHITECTURE.md): System diagrams and data flow.
- [SKILL.md](SKILL.md): Antigravity AI Agent definition.
