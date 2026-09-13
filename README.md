# ⚡ Blaze: Android Mobile Integration & Automation Hub

> **Device Pair**: `Motobook` (Windows 11 Pro) ⇄ `Blaze` (Lava Blaze 5G / Android 14)  
> **SSH Ports**: `22` (PC) / `8022` (Phone) | **Subnet**: `10.242.186.0/24`  
> **Author**: Karan Singh Verma & Antigravity Assistant

---

## 🎯 Purpose & Overview

**Blaze** is a unified multi-device automation suite connecting a Windows 11 workstation with an Android Termux node. It features dual-mode operation: **interactive ASCII terminal menus** for human exploration, and **instant CLI switches (`--otp`, `--pull`, `--mount`)** for fast execution and AI assistant headless automation.

---

## 🚀 The 7 Core Command Hubs

```text
┌─────────────────┬───────────────────────────────────┬───────────────────────────────────────┐
│ Command         │ Primary Responsibilities          │ Key CLI Switches                      │
├─────────────────┼───────────────────────────────────┼───────────────────────────────────────┤
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

## 📁 Repository Structure

```text
C:\Users\karan\Void\Blaze\
├── .gitignore          # Exclusions for Python cache & temp files
├── README.md           # Master repository documentation
├── RULES.md            # Invariants, safety rules & port allocations
├── INSTRUCTIONS.md     # Installation guide & usage instructions
├── ARCHITECTURE.md     # System topology & network specifications
└── scripts/
    ├── blaze_phone.py  # Telephony, SMS, Contacts & Cellular hub
    ├── blaze_wifi.py   # Wi-Fi radar, Scrcpy streaming & ADB hub
    ├── blaze_media.py  # Remote audio browser, player & volume hub
    ├── blaze_clip.py   # Unified clipboard sync & bridge hub
    ├── blaze_notifs.py # Notification inbox, alerts & mobile dialogs
    ├── blaze_file.py   # Filesystem transfer & Drive Z:\ mount hub
    └── blaze_speak.py  # Studio HD Neural Edge-TTS engine (20 voices)
```

---

## ⚡ Quick Start

```powershell
# 1. 1-Click OTP to PC Clipboard:
blaze-phone --otp

# 2. Pull Phone Clipboard:
blaze-clip --pull

# 3. Mount Phone as Drive Z:\ in Windows Explorer:
blaze-file --mount

# 4. Launch Wireless Screen Stream in Stealth Mode (Screen Off):
blaze-wifi --stealth

# 5. Open Interactive Voice Center:
blaze-speak
```

---

## 📜 Documentation & Governance
- [RULES.md](file:///C:/Users/karan/Void/Blaze/RULES.md): Architectural invariants and safety protocols.
- [INSTRUCTIONS.md](file:///C:/Users/karan/Void/Blaze/INSTRUCTIONS.md): Detailed installation & operational runbook.
- [ARCHITECTURE.md](file:///C:/Users/karan/Void/Blaze/ARCHITECTURE.md): System diagrams and data flow.
