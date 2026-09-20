# 📊 `blaze-status` — System Telemetry, Battery & Network Status Radar Interface

> **Command**: `blaze-status`  
> **Source Script**: [`scripts/blaze_status.py`](file:///scripts/blaze_status.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeStatus` (Alias: `blaze-status`)  
> **Query Engine**: Bundled Sub-Second SSH Query (`ConnectTimeout=4`)  
> **Layout Specification**: Clean Left-Anchored Open Cards (Single column, symmetrical spacing, 0 right borders)

---

## 🖥️ 1. Full Interactive Terminal HUD (`blaze-status`)

Executing `blaze-status` renders an instant unified hardware telemetry card across all critical subsystems:

```text
┌── 📱 BLAZE HARDWARE & TELEMETRY RADAR ────────────────────────
│
│ 📱 Device Model:       Lava Blaze 5G (Android 14)
│ ⏱️  System Uptime:      up 4 days, 3 hours
│
├── 🔋 Battery & Power ─────────────────────────────────────────
│
│ 🔋  Charge Level:       [████████░░] 84%
│ 🔌 Power State:        Discharging
│ 🌡️  Temperature:        31.4°C
│ 🩺 Battery Health:     GOOD
│
├── 📶 Network & Wireless Connectivity ─────────────────────────
│
│ 🌐 Access Point:       Home_Network_5G
│ 📻 Frequency Band:     5 GHz (5180 MHz)
│ 📡 Signal Strength:    [█████] -52 dBm
│ ⚡ Link Throughput:    433 Mbps
│ 💻 Local IP Address:   192.168.1.45 (Port 8022/SSH)
│
├── 💾 Storage & Filesystem (/sdcard) ──────────────────────────
│
│ 📁 Storage Usage:      42G / 118G (36%)
│ 🟢 Available Space:    76G
│
└── 🚀 Node Live & Operational
```

---

## 🔋 2. Filtered Subsystem Views

### Battery & Power Only (`--battery`)
```text
┌── 🔋 BLAZE BATTERY & POWER TELEMETRY ────────────────────────
│
│ ⚡  Charge Level:       [█████████░] 92%
│ 🔌 Power State:        Charging (USB)
│ 🌡️  Temperature:        33.1°C
│ 🩺 Battery Health:     GOOD
│
└──
```

### Network & Wi-Fi Only (`--wifi`)
```text
┌── 📶 BLAZE NETWORK & WIRELESS RADAR ─────────────────────────
│
│ 🌐 Access Point:       Mobile Hotspot (AP Active)
│ 📻 Frequency Band:     5 GHz (5745 MHz)
│ 📡 Signal Strength:    [█████] -45 dBm
│ ⚡ Link Throughput:    866 Mbps
│ 💻 Local IP Address:   10.154.149.220 (Port 8022/SSH)
│
└──
```

### Storage Telemetry Only (`--storage`)
```text
┌── 💾 BLAZE STORAGE TELEMETRY (/sdcard) ──────────────────────
│
│ 📁 Used Space:         42G / 118G (36%)
│ 🟢 Available Space:    76G
│
└──
```

---

## 🤖 3. Machine JSON Mode (`--json`)

```json
{
  "device": "Lava Blaze 5G (Android 14)",
  "battery": {
    "health": "GOOD",
    "percentage": 84,
    "plugged": "UNPLUGGED",
    "status": "DISCHARGING",
    "temperature": 31.4
  },
  "wifi": {
    "bssid": "e4:c3:2a:8f:12:00",
    "frequency_mhz": 5180,
    "ip": "192.168.1.45",
    "link_speed_mbps": 433,
    "rssi": -52,
    "ssid": "Home_Network_5G"
  },
  "storage": {
    "total": "118G",
    "used": "42G",
    "free": "76G",
    "pct": "36%"
  },
  "uptime": "4 days, 3 hours"
}
```

---

## ⚠️ 4. Unreachable State Diagnostic Card

```text
┌── ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022 ─────────────────────
│
│ • Root Cause: Phone offline or SSH daemon (sshd) not running.
│ • Action:     1. Ensure Termux is active on Blaze.
│               2. Run 'sshd' in Termux.
│               3. Ensure phone is connected to same Wi-Fi / Hotspot.
│
└── ⏱️ Connection Timeout (4s)
```
