# 🏛️ Blaze System Architecture & Protocol Specification

---

## 🌐 1. Topology & Network Flow

```text
┌────────────────────────────────────────────────────────┐
│             💻 MOTOBOOK (Windows 11 Node)              │
│  PowerShell Profile + 7 Blaze Hub Engines (Python)     │
│  OpenSSH Server (Port 22) | User: karan                │
└──────────────────────────┬─────────────────────────────┘
                           │ Zero-Password Ed25519 Trust
                           │ Fast ARP Sweeps (<200ms)
                           ▼ Hotspot Subnet: 10.242.186.0/24
┌────────────────────────────────────────────────────────┐
│              📱 BLAZE (Lava Blaze 5G Node)             │
│  Termux Zsh + OpenSSH (Port 8022) | User: u0_a46       │
│  Termux:API + Rclone SFTP Server + Scrcpy/ADB Wireless │
└────────────────────────────────────────────────────────┘
```

---

## ⚡ 2. Execution Pipeline

```text
[Human Terminal]   ──►  Run `blaze-phone` (No Args)    ──► Interactive ASCII Menu
[Human Terminal]   ──►  Run `blaze-phone --otp`        ──► Instant Fast-Path Extraction (<300ms)
[AI Assistant]     ──►  Run `blaze-phone --otp --json` ──► Headless JSON Payload
                               │
                               ▼
                   Subprocess SSH Tunnel (`blaze:8022`)
                               │
                               ▼
                   `termux-sms-list` JSON Stream
                               │
                               ▼
                   Regex Extraction & Windows Clipboard Sync
```

---

## 📁 3. Directory Layout

```text
Blaze/
├── .gitignore
├── README.md
├── RULES.md
├── INSTRUCTIONS.md
├── ARCHITECTURE.md
└── scripts/
    ├── blaze_status.py  # System Telemetry, Battery HUD, Wi-Fi & Storage
    ├── blaze_phone.py   # Telephony, SMS, Contacts & 5G Telemetry
    ├── blaze_wifi.py    # Wireless Radar, Spectrum, Scrcpy & ADB
    ├── blaze_media.py   # Hierarchical Audio Browser, Queue & Volume
    ├── blaze_clip.py    # Bidirectional Clipboard Sync & Push/Pull
    ├── blaze_notifs.py  # Notifications, Screen Toasts & Dialogs
    ├── blaze_file.py    # Storage Transfer, Drive Z:\ Mount & Intents
    └── blaze_speak.py   # Neural Edge-TTS Voice Center (20 Personas)
```
