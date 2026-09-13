# 🌐 `blaze-wifi` — Interface & Terminal Interactive Specification

> **Command**: `blaze-wifi`  
> **Source Script**: [`C:\Users\karan\Void\Blaze\scripts\blaze_wifi.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_wifi.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeWifi` (Alias: `blaze-wifi`)  
> **Target Subsystems**: Lava Blaze 5G Wi-Fi Radio, Hotspot AP, Wireless ADB (`port 5555`), Scrcpy Display/Camera/Audio Streaming Engine.

---

## 🖥️ 1. Main Interactive Terminal Menu

When running `blaze-wifi` without arguments, it launches the interactive inline FZF selector:

```text
┌── 🌐 BLAZE WIRELESS, NETWORK RADAR & STREAMING HUB ────────────────────────────────────────┐
│ 📶 1. Wi-Fi & Hotspot Network Radar   ──► Active SSID, BSSID, RSSI bars, and throughput   │
│ 🔍 2. Spectrum Scanner (Visible APs)  ──► Scan nearby Wi-Fi networks with signal rating   │
│ 📺 3. Scrcpy Wireless Streaming Suite ──► Stealth display, 60fps mirror, webcam & recorder│
│ 🔌 4. Wireless ADB Transport Hub       ──► Connect, pair, restart and inspect ADB sessions │
│ 🔄 5. Bounce Wi-Fi Radio (Power Reset) ──► Power cycle Wi-Fi hardware on Blaze             │
│ ⚡ 6. Toggle Wi-Fi Power (ON / OFF)    ──► Enable or disable Wi-Fi client radio            │
│ 📖 7. Help & CLI Reference             ──► Flags, command switches & examples              │
│ 🚪 0. Exit                             ──► Return to PowerShell terminal                   │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze Wi-Fi > _
```

---

## 📊 2. Screen Render: Wi-Fi & Hotspot Radar (`Option 1` / `--info`)

### Case A: Mobile Hotspot Mode (Active AP)
```text
📶 BLAZE WIRELESS & NETWORK RADAR
┌────────────────────────────────────────────────────────┐
│ 📡 Mode:         🔥 Mobile Hotspot (AP Active)         │
│ 💻 Hotspot IP:   10.154.149.220                        │
│ 🔗 Uplink:       5G / LTE Mobile Cellular Uplink       │
└────────────────────────────────────────────────────────┘
```

### Case B: Wi-Fi Client Connected Mode
```text
📶 BLAZE WIRELESS & NETWORK RADAR
┌────────────────────────────────────────────────────────┐
│ 📡 Mode:         Wi-Fi Client Connected                │
│ 🌐 SSID:         Home_Network_5G                       │
│ 📻 BSSID:        e4:c3:2a:8f:12:00                     │
│ 📶 Signal:       -52 dBm [█████]                       │
│ ⚡ Throughput:   433 Mbps                              │
│ 📻 Band:         5180 MHz (5 GHz)                      │
│ 💻 Local IP:     192.168.1.45                          │
└────────────────────────────────────────────────────────┘
```

---

## 🔍 3. Screen Render: Spectrum Scanner (`Option 2` / `--scan`)

```text
🔍 BLAZE NEARBY WI-FI SPECTRUM SCANNER
┌────────────────────────────────────────────────────────┐
│ 📡 Home_Network_5G         -52 dBm [█████] Excellent   │
│ 📡 Airtel_Fiber_2.4G       -68 dBm [████░] Good        │
│ 📡 Neighbor_Wi-Fi          -79 dBm [███░░] Fair        │
│ 📡 Office_Guest            -88 dBm [█░░░░] Weak        │
└────────────────────────────────────────────────────────┘
Total Networks Discovered: 4
```

---

## 📺 4. Submenu: Scrcpy Wireless Streaming Suite (`Option 3`)

```text
┌── 📺 SCRCPY WIRELESS STREAMING STUDIO ─────────────────────────────────────────────────────┐
│ 1. 📺 Stealth Mirror (Screen OFF)  ──► Control phone quietly (H.265, 60fps)                │
│ 2. 🖥️ Live Display (Screen ON)     ──► Mirror with phone screen visible                    │
│ 3. ⚡ Ultra-Low Latency Mode       ──► 1080p, 8 Mbps bitrate, 0 display buffer             │
│ 4. 🔊 Audio-Only Stream to PC      ──► Play phone audio through PC speakers (Opus)         │
│ 5. 📷 Wireless HD PC Webcam        ──► Stream rear or selfie camera as webcam              │
│ 6. 🎥 Screen & Audio Recorder      ──► Record session directly to MP4 in Videos            │
│ 7. 🎮 OTG Keyboard/Mouse Pass      ──► Direct hardware input pass-through                  │
│ 0. 🔙 Return to Main Menu          ──► Cancel                                              │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Scrcpy Preset > _
```

### Sub-dialog: Camera Lens Selector (`Option 5`)
```text
Camera Lens > 
1. 📷 Rear / Main Camera
2. 🤳 Front / Selfie Camera
0. 🔙 Cancel
```

---

## 🔌 5. Submenu: Wireless ADB Transport Hub (`Option 4`)

```text
┌── 🔌 WIRELESS ADB TRANSPORT HUB ───────────────────────────────────────────────────────────┐
│ 1. 🔌 Connect Wireless ADB (Auto-IP: 5555)  ──► Connect to Blaze on port 5555              │
│ 2. ⚡ USB ➔ Wireless Setup Wizard (tcpip)   ──► Plug USB once to enable wireless ADB       │
│ 3. 🔢 Connect Custom IP:Port (Dynamic Port) ──► Connect to specific port on phone         │
│ 4. 🔑 Pair Wireless ADB (Pairing Code)      ──► Android 11+ Wi-Fi Debugging Pair           │
│ 5. 📱 List Connected ADB Devices             ──► Check transport status & IDs               │
│ 6. 🔄 Restart ADB Server                     ──► Kill and restart local adb daemon          │
│ 7. ❌ Disconnect All Devices                 ──► Disconnect all active wireless sessions    │
│ 0. 🔙 Return to Main Menu                   ──► Cancel                                     │
└────────────────────────────────────────────────────────────────────────────────────────────┘
ADB Hub > _
```

### ⚡ 1-Click USB ➔ Wireless Switch Wizard Flow (`Option 2`)
```text
🔌 1-CLICK USB WIRELESS ADB SWITCH WIZARD
1. Connect your Blaze phone to PC via USB cable.
2. Ensure USB Debugging is enabled on phone.
Press Enter once USB is connected...

⚡ Switching ADB daemon on phone to TCP/IP mode on port 5555...
restarting in TCP mode port: 5555

🎉 TCP Mode Enabled on Phone!
┌────────────────────────────────────────────────────────┐
│ 🔌 You can now UNPLUG the USB cable from your PC.      │
│ 🌐 Attempting wireless connection to 10.154.149.220:5555...
└────────────────────────────────────────────────────────┘

✅ Successfully connected to Wireless ADB (10.154.149.220:5555)!
```

---

## ⚡ 6. Power State Toggle Submenu (`Option 6`)

```text
Power State > 
1. ⚡ Power ON Wi-Fi
2. 🛑 Power OFF Wi-Fi
0. 🔙 Cancel
```

---

## 📖 7. Help & CLI Reference Screen (`Option 7` / `-h` / `--help`)

```text
┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-WIFI COMMAND & CLI REFERENCE                  │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-wifi                        │
│ • Wi-Fi Radar:       blaze-wifi --info                 │
│ • Spectrum Scanner:  blaze-wifi --scan                 │
│ • Power ON / OFF:    blaze-wifi --on / --off           │
│ • Bounce Radio:      blaze-wifi --bounce               │
│ • Scrcpy Stealth:    blaze-wifi --stealth              │
│ • Scrcpy Live:       blaze-wifi --live                 │
│ • Audio Stream:      blaze-wifi --audio-only           │
│ • HD PC Webcam:      blaze-wifi --camera [back|front]  │
│ • Screen Record:     blaze-wifi --record               │
│ • ADB Devices:       blaze-wifi --adb-devices          │
│ • ADB Connect:       blaze-wifi --adb-connect [ip:port]│
│ • JSON Machine Mode: blaze-wifi --json                 │
└────────────────────────────────────────────────────────┘
```

---

## 🛠️ 8. Diagnostic & Error States

### Unreachable State Box (Node Offline / SSH Server Down)
```text
┌────────────────────────────────────────────────────────┐
│ ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022                 │
├────────────────────────────────────────────────────────┤
│ • Root Cause: Phone offline or SSH daemon not running. │
│ • Action:     1. Ensure Termux is active on Blaze.     │
│               2. Run 'sshd' in Termux.                 │
│               3. Confirm same Wi-Fi / Hotspot.         │
└────────────────────────────────────────────────────────┘
```

### Zombie ADB Daemon Auto-Recovery
- Timeout threshold: `12–15s`.
- Triggered Action: `taskkill /F /IM adb.exe` $\to$ `adb start-server` $\to$ Reconnect.
