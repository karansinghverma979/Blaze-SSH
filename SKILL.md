---
name: blaze
description: Authoritative command center, network protocol specification, and automation runbook for the bi-directional ecosystem between Motobook (Windows 11) and Blaze (Android Termux).
trigger: /blaze
---

# 📱 Blaze Ecosystem & Mobile Command Center Skill

Use this skill whenever Karan invokes `/blaze` or requests any action, query, automation, file transfer, screen streaming, audio synthesis, camera capture, telephony, or diagnostic task involving **Blaze** (Lava Blaze 5G / Android 14 / Termux) and **Motobook** (Windows 11 PC).

> **Single Source of Truth**: This skill is the authoritative operational governor, network protocol specification, and automation engine for the **Motobook ⇄ Blaze Ecosystem**.

---

## 🏛️ System Architecture & Connectivity Topology

```
┌────────────────────────────────────────────────────────┐
│             💻 MOTOBOOK (Windows 11 Node)              │
│  PowerShell Profile (16 blaze-* Cmds) + Scoop Tools    │
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

### 📂 Device Profiles & Network Topology
- **Motobook (PC)**:
  - OS: Windows 11 Pro | User: `karan`
  - OpenSSH Server: Port `22` (Service: `sshd`)
  - SSH Key: `~/.ssh/id_ed25519`
  - Public Key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPCNjdCpyt8IFlrtDnJNjZq6bWAMg6PUtfX/GYEaL3zF karan@Motobook`
- **Blaze (Phone)**:
  - Hardware: Lava Blaze 5G (Android 14) | User: `u0_a46`
  - OpenSSH Server: Port `8022` (`sshd` running in Termux)
  - Public Key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIB+dDpYExt6orFFlwv0YaSUVDs5zuLpNL7wTLaR1diuw blaze@termux`
  - Hotspot Subnet: `10.242.186.0/24` (SSID: `Lava Blaze 5G 290`)
  - Background Immunity: `termux-wake-lock` held automatically by default on every boot/startup
  - Termux Storage Root: `~/storage/shared/` (`/sdcard`)
  - Termux Downloads: `~/storage/downloads/` (`/sdcard/Download`)

---

## 📁 Key File Locations & Storage Registry

| Layer / Component | File Location | Purpose & Function |
| :--- | :--- | :--- |
| **PowerShell Profile** | `C:\Users\karan\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` | Houses all 17 `blaze-*` native cmdlets & aliases |
| **Scoop Apps** | `C:\Users\karan\scoop\apps\` (`scrcpy`, `adb`, `rclone`) | User-space portable tooling (Zero registry bloat) |
| **Rclone SFTP Config**| `C:\Users\karan\scoop\apps\rclone\current\rclone.conf` | SFTP remote config (`[blaze]`, port `8022`, key auth) |
| **WinFsp Driver** | User-mode filesystem proxy | Bridges Rclone SFTP into native Windows Drive `Z:\` |
| **SSH Config (PC)** | `C:\Users\karan\.ssh\config` | Dynamic host target `Host blaze` auto-updated by ARP sweep |
| **Termux Zsh Config** | `~/.zshrc` (on Blaze) | Termux terminal engine, aliases, extra-keys, `motobook` connector, auto wake-lock |
| **Termux Extra-Keys** | `~/.termux/termux.properties` | 14-button full-color 2×7 mobile extra-keys layout |
| **Termux Boot Script** | `~/.termux/boot/start-services.sh` | Device boot persistence script (`termux-wake-lock`, `sshd`) |
| **Termux Tasker Directory** | `~/.termux/tasker/` | Sandbox for callable automation scripts (`notify.sh`, `torch.sh`, `wake.sh`) |

---

## 🔑 SSH Setup & Auto-Discovery Mechanics

### 1. Motobook ➔ Blaze (`blaze` / `ssh blaze`)
- **Dynamic ARP Sweep**: PowerShell sweeps local subnet `10.242.186.0/24` asynchronously on port `8022` in <200ms.
- **Config Injection**: Dynamically writes `Host blaze` with `HostName <discovered-ip>`, `Port 8022`, `User u0_a46`, `IdentityFile ~/.ssh/id_ed25519`.
- **Resilience**: `ServerAliveInterval 3`, `ServerAliveCountMax 2`, `ConnectTimeout 3`. Intercepts dropped Wi-Fi with clean retry notice.

### 2. Blaze ➔ Motobook (`motobook`)
- **Default Route Probe**: Zsh checks `~/.ssh_last_client` or `ip route | grep default` to detect Motobook's IP.
- **Config Injection**: Updates `~/.ssh/config` (`Host motobook`) with `Port 22`, `User karan`.
- **Zero-Password Trust**: Motobook public key is permanently authorized in Termux `~/.ssh/authorized_keys`.

---

## 🎮 Complete 16 Operational Commands Suite

### 1. Audio, Speech & Media Operational Guide

* **`blaze-speak`** (Direct PowerShell Studio HD Voice Synthesis & TTS Engine):
  - **What**: Cloud-grade Edge-TTS neural speech synthesis streamed over SSH to Blaze's OpenSL ES audio output with +140% volume boost.
  - **Underlying Engine**: `~/.config/motobook_say.py` & `~/.config/blaze_say.py`
  - **Underlying Native Termux Fallbacks**:
    - Native TTS: `termux-tts-speak -r 1.0 "<text>"`
    - List Offline Engines: `termux-tts-engines`
  - **Interactive FZF Voice Center Features**:
    1. 💬 **Live Voice Chat Console**: Real-time voice conversation REPL with on-the-fly voice switching (`/ava`, `/swara`, `/google-in`), `:default` save, and visual FZF voice picker.
    2. 🎭 **Voice Persona Explorer**: Visual testing of 20 Studio HD personas (Indian English, Hindi, US, UK, Australian, Canadian, Irish) with 3 long-form passages (Casual & Friendly, Executive Mission Brief, Technical Systems).
    3. ⭐ **Set Permanent Default**: Persistently saves chosen assistant voice across PC and phone.
    4. 📋 **Read Clipboard Out Loud**: Speaks contents of Windows or phone clipboard.
    5. 🔋 **Live Telemetry Spoken Briefing**: Speaks live battery %, temperature, and 5G carrier state.
    6. 🚨 **Emergency Siren Alert**: High-priority alert siren bypassing phone silent mode.
  - **Direct CLI Fast Triggers**:
    - Direct Speech: `pwsh -Command "blaze-speak '<text>'"`
    - Specific Persona: `pwsh -Command "blaze-speak '<text>' -Persona swara"`
    - Read Clipboard: `pwsh -Command "blaze-speak -Clip"`
    - Spoken Status Briefing: `pwsh -Command "blaze-speak -Brief"`
    - Emergency Alarm: `pwsh -Command "blaze-speak -Alarm"`
    - Open Live Voice Chat: `pwsh -Command "blaze-speak -Chat"`
    - Set Default Voice: `pwsh -Command "blaze-speak -SetDefault"`
  - **Raw SSH Fallback**: `ssh blaze "python3 ~/.config/blaze_say.py '<text>' google-in 1.0 1.0"`

* **`blaze-volume`** (Hardware Volume Governor):
  - **What**: Adjusts the Android hardware audio stream levels (`music`, `ring`, `alarm`, `call`, `notification`, `system`) with visual 0–15 slider.
  - **Underlying Native Termux Tool**: **`termux-volume`**
  - **When to Use**: When Karan says *"Set phone volume to <N>"*, *"Mute phone"*, *"Max volume"*, or *"Lower volume"*.
  - **How to Use**:
    - Interactive FZF Stream & Slider: `pwsh -Command "blaze-volume"`
    - Direct Level: `pwsh -Command "blaze-volume 15 music"` (or `blaze-volume max`, `blaze-volume mute`)
    - Raw SSH: `ssh blaze "termux-volume music 15"`

* **`blaze-media`** (Unified Interactive Media Player & Track Library Hub):
  - **What**: Interactive FZF media hub and CLI controller uniting remote track browser, live playback controls, queue management, volume slider, MediaStore scanner, and hardware audio diagnostics.
  - **Underlying Script**: `~/.config/blaze_media.py` & `~/.config/blaze_player.py`
  - **Underlying Native Termux Tools**:
    - Media Playback: `termux-media-player play <file> | pause | stop | info`
    - MediaStore Scan: `termux-media-scan <file_or_dir>`
    - Audio Routing Info: `termux-audio-info`
  - **Interactive FZF Hub Modules**:
    1. 🎵 **Browse & Play Track**: Scans `/sdcard/Music`, `/sdcard/Download`, `/sdcard/Movies` for audio files (`.mp3`, `.m4a`, `.wav`, `.flac`, `.aac`, `.ogg`) $\to$ instant playback on phone.
    2. ⏯️ **Playback Controls**: Toggle Play / Pause, Resume, Stop.
    3. ⏭️ / ⏮️ **Next & Previous**: Track skip forward and backward in queue.
    4. 📋 **Manage Active Queue**: View playlist, jump directly to any track, or clear entire queue.
    5. ➕ **Add Tracks / Folders**: Multi-select tracks with `TAB` to append to queue.
    6. 🔁 **Repeat Mode Governor**: Repeat All (🔁), Repeat One (🔂), Repeat Off (➡️).
    7. 🔀 **Shuffle Mode Toggle**: Enable / Disable randomized playlist playback.
    8. 🔊 **Adjust Music Volume**: Visual 0–15 level slider for phone speaker.
    9. 🔍 **Scan & Re-Index MediaStore**: Forces Android MediaStore to refresh without rebooting.
    10. 📊 **Audio Diagnostics**: Primary speaker, Bluetooth A2DP, and wired headset routing state.
    11. 🚪 **Exit**: Clean exit.
  - **Direct CLI Fast Triggers**:
    - *Interactive Hub*: `pwsh -Command "blaze-media"`
    - *Playback Info Card*: `pwsh -Command "blaze-media -Info"`
    - *Play Specific Track*: `pwsh -Command "blaze-media -Play '/sdcard/Music/song.mp3'"`
    - *Pause Playback*: `pwsh -Command "blaze-media -Pause"`
    - *Resume Playback*: `pwsh -Command "blaze-media -Resume"`
    - *Stop Playback*: `pwsh -Command "blaze-media -Stop"`
    - *Skip Track*: `pwsh -Command "blaze-media -Next"` / `pwsh -Command "blaze-media -Prev"`
    - *View Active Queue*: `pwsh -Command "blaze-media -Queue"`
    - *Set Repeat Mode*: `pwsh -Command "blaze-media -Repeat all"` (or `one`, `off`)
    - *Toggle Shuffle*: `pwsh -Command "blaze-media -Shuffle"`
    - *Re-Index MediaStore*: `pwsh -Command "blaze-media -Scan"`
  - **Direct Raw SSH Fallback**:
    - *Play File*: `ssh blaze "termux-media-player play '/sdcard/Music/song.mp3'"`
    - *Pause*: `ssh blaze "termux-media-player pause"`
    - *Stop*: `ssh blaze "termux-media-player stop"`
    - *Info*: `ssh blaze "termux-media-player info"`

* **`termux-microphone-record`** (Silent Hardware Microphone Recorder):
  - **What**: Silently records audio from phone's hardware microphone directly to high-quality `.wav` or `.m4a`.
  - **When to Use**: When Karan says *"Record a voice note"*, *"Record audio for <N> seconds"*, or *"Capture audio note to Obsidian"*.
  - **How to Use**:
    - Start 30s Recording: `ssh blaze "termux-microphone-record -f ~/storage/shared/Download/memo.wav -l 30 -e wav"`
    - Pull directly to Obsidian: `scp blaze:~/storage/shared/Download/memo.wav "%USERPROFILE%\Obsidian\Clippings\memo_$(date +%s).wav"`
    - Stop active recording early: `ssh blaze "termux-microphone-record -d"`

* **`termux-speech-to-text`** (Mobile Speech-to-Text Transcription Engine):
  - **What**: Activates Android Google Voice Recognition to transcribe spoken words into raw text strings.
  - **When to Use**: When Karan says *"Listen to my voice and transcribe"*, *"Dictate text from phone"*, or *"Speech to text"*.
  - **How to Use**:
    - Execute: `ssh blaze "termux-speech-to-text"` (Returns live transcribed JSON string).

* **`termux-media-scan`** (MediaStore Gallery & Audio Re-Indexer):
  - **What**: Forces Android MediaStore to re-index files immediately so downloaded MP3s, audiobooks, or photos appear in phone gallery / music player without device reboot.
  - **When to Use**: Whenever Karan says *"Re-index phone gallery"*, *"Scan downloaded songs"*, or automatically after dropping media via `blaze-drop-file`.
  - **How to Use**:
    - Scan Downloads: `ssh blaze "termux-media-scan ~/storage/downloads/*"`
    - Scan Specific File: `ssh blaze "termux-media-scan ~/storage/shared/Download/track.mp3"`

* **`termux-audio-info`** (Audio Routing & Stream Diagnostics):
  - **What**: Dumps JSON containing active audio output device (Speaker / Bluetooth / Wired Headset), call state, and stream volumes.
  - **When to Use**: When diagnosing why audio isn't audible or checking Bluetooth headphone connectivity.
  - **How to Use**: `ssh blaze "termux-audio-info"`

### 2. Camera, Vision & Hardware Sensors Operational Guide

> **Execution Protocol**: These commands operate directly over the SSH tunnel (`ssh blaze "<command>"`). No extra PowerShell wrapper is required.

* **`termux-camera-photo`** (Hardware Lens Snapshot Engine):
  - **What**: Captures a high-resolution photo from the physical camera sensor and saves as JPEG.
  - **Syntax / Help**: `termux-camera-photo [-c <camera_id>] <output_file.jpg>`
    - `-c 0`: Rear 50MP primary camera sensor (Default, 4032×2272 max resolution).
    - `-c 1`: Front-facing selfie camera sensor.
  - **When to Use**: When Karan says *"Take a photo from phone"*, *"Capture rear camera shot"*, *"Take a selfie"*, or *"Take photo and save to Obsidian"*.
  - **How to Use (SSH Tunnel)**:
    - *Rear Photo to PC*:
      ```powershell
      ssh blaze "termux-camera-photo -c 0 ~/temp_photo.jpg"
      scp blaze:~/temp_photo.jpg "$PWD/capture.jpg"
      ssh blaze "rm -f ~/temp_photo.jpg"
      ```
    - *Direct to Obsidian Vault*:
      ```powershell
      $stamp = (Get-Date -Format 'yyyyMMdd_HHmmss')
      ssh blaze "termux-camera-photo -c 0 ~/temp_photo.jpg"
      scp blaze:~/temp_photo.jpg "$env:USERPROFILE\Obsidian\Clippings\Photo_$stamp.jpg"
      ssh blaze "rm -f ~/temp_photo.jpg"
      ```

* **`termux-camera-info`** (Camera Hardware Specs Inspector):
  - **What**: Dumps JSON array of all camera sensors, supported image dimensions, focal lengths, and capabilities.
  - **Syntax / Help**: `termux-camera-info`
  - **When to Use**: When checking camera IDs, supported resolutions, or sensor orientation.
  - **How to Use**: `ssh blaze "termux-camera-info"`

* **`termux-sensor`** (Real-Time Hardware Sensor Telemetry):
  - **What**: Streams live telemetry from phone hardware sensors (Accelerometer, Gyroscope, Ambient Light, Proximity, Step Counter).
  - **Syntax / Help**: `termux-sensor [-a] [-l] [-s <sensors>] [-d <delay_ms>] [-n <limit>] [-c]`
    - `-l, --list`: Lists all available sensors on Lava Blaze 5G.
    - `-s, --sensors`: Sensor name or partial match (e.g. `step_counter`, `light`, `gravity`, `accelerometer`).
    - `-n, --limit`: Number of readings to take before stopping (e.g. `-n 1` for single reading).
    - `-d, --delay`: Delay interval between samples in milliseconds.
    - `-c, --cleanup`: Releases sensor resources.
    - `-a, --all`: Reads all sensors (Warning: high battery consumption).
  - **When to Use**: When Karan says *"Check phone sensors"*, *"Get step count"*, *"Check room light level from phone"*, or *"List hardware sensors"*.
  - **How to Use (SSH Tunnel)**:
    - *List all sensors*: `ssh blaze "termux-sensor -l"`
    - *Read ambient light level once*: `ssh blaze "termux-sensor -s light -n 1"`
    - *Read step counter*: `ssh blaze "termux-sensor -s step_counter -n 1"`
    - *Clean up sensor listeners*: `ssh blaze "termux-sensor -c"`

* **`termux-fingerprint`** (Biometric Physical Touch Authenticator):
  - **What**: Prompts biometric fingerprint scanner on phone screen and returns verification status.
  - **Syntax / Help**: `termux-fingerprint [-t <title>] [-d <description>] [-s <subtitle>] [-c <cancel_text>]`
    - `-t`: Title displayed on biometric prompt dialog.
    - `-d`: Description string.
    - `-s`: Subtitle string.
    - `-c`: Custom cancel button text.
  - **When to Use**: When Karan says *"Authenticate with fingerprint"*, or to enforce physical biometric touch before executing high-risk PC operations.
  - **How to Use (SSH Tunnel)**:
    - `ssh blaze "termux-fingerprint -t 'Motobook Security' -d 'Touch fingerprint sensor to verify'"`
    - *Return Payload*: `{"auth_result": "AUTH_RESULT_SUCCESS"}`

* **`termux-infrared-frequencies`** & **`termux-infrared-transmit`** (IR Blaster):
  - **What**: Controls IR transmitter hardware.
  - **Syntax / Help**: `termux-infrared-transmit -f <frequency_hz> <pattern_array>`
  - **When to Use**: When transmitting IR remote control signals.
  - **How to Use**: `ssh blaze "termux-infrared-frequencies"`

### 3. Hardware Controls, Power & Display Operational Guide

> **Execution Protocol**:
> - Direct PowerShell: `blaze-status`, `blaze-screen`
> - SSH Tunnel: `ssh blaze "termux-torch"`, `ssh blaze "termux-vibrate"`, `ssh blaze "termux-brightness"`, `ssh blaze "termux-wallpaper"`

* **`blaze-status`** (Direct PowerShell Telemetry Dashboard):
  - **What**: Comprehensive system radar parsing battery %, temperature, 5G carrier/signal, and Wi-Fi link parameters into a color box dashboard.
  - **When to Use**: When Karan says *"Check phone status"*, *"Check battery"*, *"Is phone hot?"*, or *"Blaze telemetry"*.
  - **How to Use (Direct PowerShell)**: `pwsh -Command "blaze-status"`

* **`termux-torch`** (Hardware Flashlight Governor):
  - **What**: Toggles the physical rear LED flash on or off.
  - **Syntax / Help**: `termux-torch [on | off]`
  - **When to Use**: When Karan says *"Turn on torch"*, *"Turn off torch"*, *"Toggle flashlight"*, or *"Torch on for <N> seconds"*.
  - **How to Use (SSH Tunnel)**:
    - *Turn ON*: `ssh blaze "termux-torch on"`
    - *Turn OFF*: `ssh blaze "termux-torch off"`
    - *5-Second Flash*: `ssh blaze "termux-torch on && sleep 5 && termux-torch off"`

* **`termux-vibrate`** (Haptic Alert Motor):
  - **What**: Triggers device haptic vibration motor for physical alerts and feedback.
  - **Syntax / Help**: `termux-vibrate [-d <duration_ms>] [-f]`
    - `-d <ms>`: Duration in milliseconds (Default: `1000`).
    - `-f`: Force vibration even if device is set to silent / DND mode.
  - **When to Use**: When Karan says *"Vibrate phone"*, *"Buzz phone"*, or to provide silent physical feedback when a long background compilation/build finishes.
  - **How to Use (SSH Tunnel)**:
    - *Short Pulse (300ms)*: `ssh blaze "termux-vibrate -d 300 -f"`
    - *Double Buzz*: `ssh blaze "termux-vibrate -d 200 && sleep 0.2 && termux-vibrate -d 400"`

* **`termux-brightness`** (Screen Display Brightness):
  - **What**: Controls the Android LCD screen backlight brightness.
  - **Syntax / Help**: `termux-brightness <0-255 | auto>`
    - `0–255`: Integer brightness value (`0` = minimum, `255` = maximum).
    - `auto`: Enables automatic ambient light sensor brightness.
  - **When to Use**: When Karan says *"Set screen brightness to <0-255>"*, *"Set auto brightness"*, or *"Dim phone screen"*.
  - **How to Use (SSH Tunnel)**:
    - *Dim to Minimum*: `ssh blaze "termux-brightness 10"`
    - *Full Brightness*: `ssh blaze "termux-brightness 255"`
    - *Auto Mode*: `ssh blaze "termux-brightness auto"`

* **`termux-wallpaper`** (Dynamic Wallpaper Engine):
  - **What**: Sets the home screen or lock screen background from a local image file or URL.
  - **Syntax / Help**: `termux-wallpaper [-f <file>] [-u <url>] [-l]`
    - `-f <path>`: Local image path on Blaze.
    - `-u <url>`: Direct web image URL.
    - `-l`: Applies wallpaper specifically to lock screen (Default: home screen).
  - **When to Use**: When Karan says *"Set phone wallpaper to <file/url>"*, *"Update lock screen wallpaper"*, or pushing generated Obsidian study cards as mobile wallpaper.
  - **How to Use (SSH Tunnel)**:
    - *From URL*: `ssh blaze "termux-wallpaper -u 'https://example.com/image.jpg'"`
    - *From Local File*: `ssh blaze "termux-wallpaper -f ~/storage/downloads/agenda.png"`
    - *Lock Screen*: `ssh blaze "termux-wallpaper -f ~/storage/downloads/agenda.png -l"`

* **`termux-wake-lock`** & **`termux-wake-unlock`** (Android CPU Wake-Lock):
  - **What**: Prevents Android OS and battery governors from freezing Termux and background daemons (`sshd`).
  - **When to Use**: Enforced automatically by default on every boot and shell startup.
  - **How to Use (SSH Tunnel)**:
    - *Acquire*: `ssh blaze "termux-wake-lock"`
    - *Release*: `ssh blaze "termux-wake-unlock"`

* **`blaze-screen`** (Wireless 60 FPS Scrcpy HUD with Stealth Mode):
  - **What**: Low-latency wireless screen mirror via user-space Scrcpy v4.1.
  - **When to Use**: When Karan says *"Mirror screen"*, *"View phone screen"*, or *"Blaze HUD"*.
  - **How to Use (Direct PowerShell)**:
    - *Default Stealth Mode (Zero Backlight IPS Protection)*: `pwsh -Command "blaze-screen"`
    - *Display On*: `pwsh -Command "blaze-screen -ScreenOn"`

---

### 4. Geolocation & Satellites Operational Guide

* **`blaze-location`** (Direct PowerShell Geolocation Radar):
  - **What**: Formatted GPS radar displaying latitude, longitude, accuracy radius, MSL altitude, speed, bearing, and clickable Google Maps & OpenStreetMap links.
  - **Underlying Native Termux Tool**: **`termux-location`**
  - **Direct Raw SSH Fallback (If PowerShell wrapper is unavailable)**:
    - Fast cached fix: `ssh blaze "termux-location -p gps -r last"`
    - Live satellite lock: `ssh blaze "termux-location -p gps -r once"`
    - Network cell/Wi-Fi trilateration: `ssh blaze "termux-location -p network -r once"`
  - **Native Syntax / Help**: `termux-location [-p provider] [-r request]`
    - `-p provider`: `gps` (hardware satellite receiver, default), `network` (Wi-Fi/cell tower trilateration), `passive` (reuses location requests from other apps).
    - `-r request`: `once` (triggers active hardware sensor lock, default), `last` (instant return of last cached coordinates, 0% battery drain), `updates` (continuous coordinate stream).
  - **When to Use**: When Karan says *"Where is my phone?"*, *"Get GPS coordinates"*, *"Open phone location in Google Maps"*, or *"Log current location in Obsidian"*.
  - **How to Use (Direct PowerShell)**:
    - *Standard Fast Radar*: `pwsh -Command "blaze-location"`
    - *Force Live Satellite Lock*: `pwsh -Command "blaze-location -Live"`
    - *Open Google Maps in Browser*: `pwsh -Command "blaze-location -Open"`
    - *Copy Google Maps Link to Clipboard*: `pwsh -Command "blaze-location -Copy"`
    - *Raw JSON Output*: `pwsh -Command "blaze-location -Raw"`
  - **Obsidian Travel Logging Recipe**:
    - Extract coordinates and stamp into Obsidian Daily Note:
      ```powershell
      $loc = blaze-location -Raw
      $mapsLink = "https://www.google.com/maps?q=$($loc.latitude),$($loc.longitude)"
      Add-Content -Path "$env:USERPROFILE\Obsidian\Daily Notes\$(Get-Date -f 'yyyy-MM-dd').md" -Value "`n### 📍 Geolocation Checkpoint ($(Get-Date -f 'HH:mm'))`n- **Coordinates**: $($loc.latitude)°, $($loc.longitude)° (±$($loc.accuracy)m)`n- **Map**: [Google Maps]($mapsLink)`n"
      ```

---

### 5. Telephony, Contacts & Messaging Operational Guide

* **`blaze-phone`** (Direct PowerShell Unified Telephony & Messaging Hub):
  - **What**: Interactive FZF control center uniting phone calls, searchable address book, SMS composer, recent call logs with call-back, and 1-click 2FA OTP clipboard extractor.
  - **Underlying Script**: `~/.config/blaze_phone.py`
  - **Underlying Native Termux Tools**:
    - Calls: `termux-telephony-call <number>`
    - SMS Dispatch: `termux-sms-send -n <number> "<message>"`
    - Address Book: `termux-contact-list`
    - SMS Inbox & OTP: `termux-sms-list -l <limit>`
    - Call History: `termux-call-log -l <limit>`
    - Cell Tower Signal: `termux-telephony-cellinfo`
    - SIM/Device Info: `termux-telephony-deviceinfo`
  - **Interactive FZF Hub Modules**:
    1. 📞 **Make a Call**: Choose from Searchable Contacts, type number directly, or dial from Call Logs.
    2. ✉️ **Send SMS**: Choose recipient from Contacts or type number $\to$ prompt message body $\to$ dispatch.
    3. 📇 **Search Contacts**: Instant fuzzy search across entire address book $\to$ [Call] / [Send SMS] / [Copy Number].
    4. 🔑 **Extract Latest OTP**: Instant 1-click scan and copy of latest 2FA/banking code to Windows clipboard.
    5. 📨 **View SMS Inbox**: Formatted SMS inbox (newest first) $\to$ [Copy OTP] / [Reply SMS] / [Call Sender].
    6. 📜 **View Call Logs**: Visual history (🔴 Missed, 🟢 Incoming, 🔵 Outgoing) $\to$ [Call Back] / [SMS Back] / [Copy Number].
    7. 📡 **5G & Cell Towers**: Live 5G/LTE tower generation, frequency band (e.g. Band n28/n78), signal dBm & ASU.
    8. 📱 **SIM & Device Info**: SIM operator name, dual SIM status, radio type, roaming state & baseband version.
    9. 🚪 **Exit / Back**: Clean navigation with zero trapped loops.
  - **Direct CLI Fast Triggers**:
    - *Open Interactive Hub*: `pwsh -Command "blaze-phone"`
    - *Extract Latest OTP to Windows Clipboard*: `pwsh -Command "blaze-phone -Otp"`
    - *Dial Number Directly*: `pwsh -Command "blaze-phone -Call 9876543210"`
    - *Send SMS Directly*: `pwsh -Command "blaze-phone -Sms 9876543210 -Message 'Meeting at 5pm'"`
    - *Search Address Book*: `pwsh -Command "blaze-phone -Contacts"`
    - *Inspect Call Logs*: `pwsh -Command "blaze-phone -Logs"`
    - *Query 5G / Cell Tower Signal*: `pwsh -Command "blaze-phone -Cell"`
    - *Query SIM & Device Telephony Specs*: `pwsh -Command "blaze-phone -Device"`
  - **Direct Raw SSH Fallbacks (If PowerShell wrapper is unavailable)**:
    - *Dial Phone*: `ssh blaze "termux-telephony-call <number>"`
    - *Send SMS*: `ssh blaze "termux-sms-send -n <number> '<message>'"`
    - *Dump Contacts JSON*: `ssh blaze "termux-contact-list"`
    - *Dump Recent SMS*: `ssh blaze "termux-sms-list -l 10"`
    - *Dump Call History*: `ssh blaze "termux-call-log -l 10"`
    - *Dump 5G Cell Towers*: `ssh blaze "termux-telephony-cellinfo"`
    - *Dump SIM Info*: `ssh blaze "termux-telephony-deviceinfo"`

### 6. Network, Wireless & Display Streaming Operational Guide

* **`blaze-wifi`** (Unified Wireless, Hotspot, Display & ADB Command Center):
  - **What**: Interactive FZF control center uniting active Wi-Fi telemetry, 2.4/5GHz spectrum scanner, wireless Scrcpy display mirroring (stealth, live, audio-only, silent, recording, webcam, gaming, custom presets), radio power toggle/bounce, wireless ADB diagnostics, and USB/NFC hardware radar.
  - **Underlying Script**: `~/.config/blaze_wifi.py`
  - **Underlying Native Tools**:
    - Active Connection: `termux-wifi-connectioninfo`
    - Spectrum Scanner: `termux-wifi-scaninfo`
    - Radio Toggle: `termux-wifi-enable <true|false>`
    - Wireless Display & Audio: `scrcpy` (Port 5555 over Wireless ADB)
    - Wireless ADB: `adb connect`, `adb pair`, `adb devices`
    - Peripherals: `termux-usb`, `termux-nfc`
  - **Interactive FZF Hub Modules**:
    1. 📡 **Active Wi-Fi Connection Radar**: Network SSID, BSSID, Signal dBm, Link Throughput (Mbps), Wireless Band (2.4/5 GHz), and assigned phone IP.
    2. 🔍 **Wi-Fi Spectrum Radar**: Scans nearby visible access points with signal quality bars, channel/frequency, security type $\to$ 1-click copy SSID / BSSID to clipboard.
    3. 🖥️ **Wireless Display & Scrcpy Mirroring**:
       - 🥷 *Stealth Mirror*: Phone display OFF, 60fps H.265, Stay Awake, Audio Forwarding.
       - 📱 *Live Mirror*: Phone display ON, 60fps H.265, Audio Forwarding.
       - 🎧 *Audio-Only Stream*: Stream phone audio straight to PC speakers with no video window.
       - 🔇 *Silent Video Stream*: Video stream with screen off and muted audio.
       - 🎥 *Screen & Audio Recording Studio*: Timestamped MP4/MKV recording to `~/Videos/Blaze_Recordings/`.
       - 📷 *HD Camera Mirror*: Turn rear or front camera into high-resolution wireless PC webcam.
       - 🎮 *Gaming & Low-Latency Mode*: 720p 60fps 8Mbps ultra-responsive stream.
       - 🖥️ *Fullscreen Presentation Mode*: Fullscreen zero-distraction display.
       - ⌨️ *Physical Keyboard & Mouse*: Native UHID hardware input control.
       - ⚙️ *Custom Stream Preset Builder*: Step-by-step resolution, FPS, codec, audio, and display customizer.
    4. ⚡ **Toggle / Bounce Wi-Fi Radio**: Turn Wi-Fi ON, OFF, or perform a clean 3-second reboot/bounce cycle.
    5. 🔌 **Wireless ADB & Device Diagnostics**: Reconnect, pair via 6-digit code, restart daemon, view attached device status.
    6. 🔌 **Hardware Peripherals Radar**: Lists attached USB OTG devices and NFC controller status.
    7. 🚪 **Exit / Back**: Clean non-trapped navigation.
  - **How to Use**:
    - *Interactive Hub*: `blaze-wifi`
  - **Direct Raw SSH Fallbacks**:
    - *Dump Connection Info*: `ssh blaze "termux-wifi-connectioninfo"`
    - *Dump Spectrum Scan*: `ssh blaze "termux-wifi-scaninfo"`
    - *Enable Wi-Fi*: `ssh blaze "termux-wifi-enable true"`
    - *Disable Wi-Fi*: `ssh blaze "termux-wifi-enable false"`
    - *Check USB*: `ssh blaze "termux-usb -l"`

---

### 7. Clipboard, Notifications & Mobile UI Operational Guide

* **`blaze-clip`** (Unified Interactive Clipboard Bridge):
  - **What**: Interactive FZF clipboard hub and CLI tool uniting push, pull, side-by-side visual diff & sync, and custom string dispatch.
  - **Underlying Script**: `~/.config/blaze_clip.py`
  - **Underlying Native Termux Tools**:
    - Push: `termux-clipboard-set`
    - Pull: `termux-clipboard-get`
  - **Interactive FZF Hub Modules**:
    1. 📥 **Pull Phone Clipboard**: Pulls phone clipboard $\to$ displays preview card $\to$ copies to PC clipboard.
    2. 📤 **Push PC Clipboard**: Pushes Windows clipboard straight to phone with toast feedback.
    3. 🔄 **Side-by-Side Visual Diff & Sync**: Compares both clipboards and lets you sync in either direction with 1 click.
    4. ✏️ **Type & Push Custom String**: Text prompt to dispatch arbitrary text directly to Blaze.
    5. 🚪 **Exit / Back**: Clean non-trapped navigation.
  - **Direct CLI Fast Triggers**:
    - *Interactive Hub*: `pwsh -Command "blaze-clip"`
    - *Pull from Phone*: `pwsh -Command "blaze-clip -Pull"` (or `blaze-pull-clip`)
    - *Push to Phone*: `pwsh -Command "blaze-clip -Push 'Text'"` (or `blaze-push-clip`)
    - *Sync Visual Diff*: `pwsh -Command "blaze-clip -Sync"` (or `blaze-sync-clip`)
  - **Direct Raw SSH Fallbacks**:
    - *Pull*: `ssh blaze "termux-clipboard-get"`
    - *Push*: `ssh blaze "termux-clipboard-set '<text>'"`

* **`blaze-notifs`** (Unified Notification, Toast & Mobile UI Command Center):
  - **What**: Interactive FZF control center uniting live notification feed, 1-click OTP/2FA extraction, custom push notifications, floating toasts, notification dismissal, mobile dialog spawner, and live streaming watcher.
  - **Underlying Script**: `~/.config/blaze_notifs.py`
  - **Underlying Native Termux Tools**:
    - List Notifications: `termux-notification-list`
    - Send Notification: `termux-notification --title "..." --content "..."`
    - Dismiss Notification: `termux-notification-remove <id>`
    - Toast Spawner: `termux-toast "<msg>"`
    - Mobile Dialog Prompts: `termux-dialog <text|confirm|date|time|radio>`
  - **Interactive FZF Hub Modules**:
    1. 📱 **View Active Notification Inbox**: Formatted feed (newest first) color-coded by app (WhatsApp, Banking, SMS, Calls, System) with 1-click OTP copy, full text copy, or dismissal by ID.
    2. 🔑 **1-Click 2FA / OTP Code Extractor**: Instant regex scan across active notifications and recent SMS $\to$ copies code straight to Windows clipboard.
    3. 🔔 **Dispatch Push Notification**: Sends high-priority push notification with sound to Blaze screen.
    4. 🍞 **Spawn Floating Toast**: Shows floating overlay toast message on phone screen (`termux-toast`).
    5. 💬 **Spawn Mobile Dialog Prompt**: Triggers interactive mobile UI on phone (Text input, Yes/No confirm, Date picker, Time picker, Radio choice) and captures user input back to PC.
    6. 👀 **Live Notification Stream Watcher**: Real-time daemon monitoring incoming alerts every $N$ seconds.
    7. 🚪 **Exit / Back**: Clean non-trapped navigation.
  - **Direct CLI Fast Triggers**:
    - *Interactive Hub*: `pwsh -Command "blaze-notifs"`
    - *Extract Latest OTP*: `pwsh -Command "blaze-notifs -Otp"`
    - *List Notifications*: `pwsh -Command "blaze-notifs -List"`
    - *Spawn Toast*: `pwsh -Command "blaze-notifs -Toast 'Directive executed'"`
    - *Send Push Notification*: `pwsh -Command "blaze-notifs -SendTitle 'Mission Alert' -SendBody 'Build finished'"`
    - *Start Live Watcher*: `pwsh -Command "blaze-notifs -Watch 3"`
    - *Dismiss Notification*: `pwsh -Command "blaze-notifs -Dismiss <id>"`
  - **Direct Raw SSH Fallbacks**:
    - *List*: `ssh blaze "termux-notification-list"`
    - *Toast*: `ssh blaze "termux-toast 'Hello'"`
    - *Send*: `ssh blaze "termux-notification --title 'Hi' --content 'Test'"`
    - *Dismiss*: `ssh blaze "termux-notification-remove <id>"`
    - *Prompt*: `ssh blaze "termux-dialog text -t 'Input'"`

---

### 8. Filesystem, Storage & Drive Mounting Operational Guide

* **`blaze-file`** (Unified Filesystem, Storage & Transfer Command Center):
  - **What**: Interactive FZF storage manager uniting local-to-remote file dropping, remote-to-local file pulling, SFTP Drive `Z:\` mounting, Android default app launcher, web link opener, native Android share sheet, and background download manager.
  - **Underlying Script**: `~/.config/blaze_file.py`
  - **Underlying Native Termux Tools**:
    - File Drop: `scp <local> blaze:~/storage/downloads/` + `termux-media-scan`
    - File Pull: `scp blaze:<remote> .`
    - Drive Mount: Rclone SFTP + WinFsp (Drive `Z:\`)
    - Open File: `termux-open <path>`
    - Open Link: `termux-open-url <url>`
    - Android Share Sheet: `termux-share -a send <file_or_text>`
    - Download Manager: `termux-download -t "<title>" <url>`
  - **Interactive FZF Hub Modules**:
    1. 📤 **Drop / Send Local File to Blaze**: Interactive local file browser $\to$ transfers to `/sdcard/Download/` $\to$ automatically triggers `termux-media-scan` & toast on phone.
    2. 📥 **Pull File from Blaze**: Interactive remote storage browser across `/sdcard/` $\to$ downloads selected file straight to PC.
    3. 📂 **Mount / Unmount Storage Drive**: 1-click mount `/sdcard` as Drive **`Z:\`** in Windows Explorer (or clean unmount).
    4. 📱 **Open File on Phone**: Browse remote files and launch directly in Android's default app (`termux-open`).
    5. 🌐 **Open URL in Mobile Browser**: Send any link to open instantly in phone's default browser (`termux-open-url`).
    6. 📤 **Trigger Android Share Sheet**: Dispatch any file or text to Android's native share modal (`termux-share`).
    7. ⬇️ **Send Download Task**: Send direct file URL to Android background Download Manager (`termux-download`).
    8. 🚪 **Exit / Back**: Clean non-trapped navigation.
  - **Direct CLI Fast Triggers**:
    - *Interactive Hub*: `pwsh -Command "blaze-file"`
    - *Drop File*: `pwsh -Command "blaze-file -Drop 'C:\path\file.pdf'"` (or `blaze-drop-file`)
    - *Pull File*: `pwsh -Command "blaze-file -Pull '/sdcard/Download/file.pdf'"` (or `blaze-pull-file`)
    - *Mount Drive Z:*: `pwsh -Command "blaze-file -Mount"` (or `blaze-mount`)
    - *Unmount Drive Z:*: `pwsh -Command "blaze-file -Unmount"` (or `blaze-unmount`)
    - *Open File / URL*: `pwsh -Command "blaze-file -Open 'https://github.com'"` (or `blaze-open-link`)
    - *Trigger Share Sheet*: `pwsh -Command "blaze-file -Share"`
    - *Send Download*: `pwsh -Command "blaze-file -Download 'https://example.com/file.zip'"`
  - **Direct Raw SSH Fallbacks**:
    - *Open File*: `ssh blaze "termux-open /sdcard/Download/doc.pdf"`
    - *Open URL*: `ssh blaze "termux-open-url 'https://google.com'"`
    - *Share File*: `ssh blaze "termux-share -a send /sdcard/Download/doc.pdf"`
    - *Download*: `ssh blaze "termux-download -t 'File' 'https://example.com/file.zip'"`

---

### 9. Boot, Tasker & Mobile Automation Engine

* **Termux Boot Persistence**:
  - Script: `~/.termux/boot/start-services.sh`
  - Enforces `termux-wake-lock` and `sshd` upon device restart.
* **Tasker Callable Scripts**:
  - Directory: `~/.termux/tasker/` (`-rwx------`)
  - `notify.sh`: Spawns custom Android notifications.
  - `torch.sh`: Toggles flashlight.
  - `wake.sh`: Background wake-lock keeper.
* **App Interoperability**:
  - `allow-external-apps = true` in `~/.termux/termux.properties`.

---

## ⚡ AI Assistant Fast Execution Matrix (<50ms)

When Karan issues natural language mobile instructions, the assistant executes direct shell calls without unnecessary tool chains:

| Natural Language Request | Exact Execution Command |
| :--- | :--- |
| *"Where is my phone / get location"* | `pwsh -Command "blaze-location"` |
| *"Get live GPS satellite location"* | `pwsh -Command "blaze-location -Live"` |
| *"Open phone location in map"* | `pwsh -Command "blaze-location -Open"` |
| *"Speak on my phone: `<text>`"* | `pwsh -Command "blaze-speak '<text>'"` |
| *"Mount phone storage"* | `pwsh -Command "blaze-mount"` |
| *"Unmount phone storage"* | `pwsh -Command "blaze-unmount"` |
| *"Mirror screen in stealth"* | `pwsh -Command "blaze-screen"` |
| *"Mirror screen with display on"* | `pwsh -Command "blaze-screen -ScreenOn"` |
| *"Copy to phone clipboard: `<text>`"* | `pwsh -Command "blaze-push-clip '<text>'"` |
| *"Get phone clipboard"* | `pwsh -Command "blaze-pull-clip"` |
| *"Drop `<file>` to phone downloads"* | `pwsh -Command "blaze-drop-file '<file>'"` |
| *"Pull `<file>` from phone"* | `pwsh -Command "blaze-pull-file '<file>'"` |
| *"Open link `<url>` on phone"* | `pwsh -Command "blaze-open-link '<url>'"` |
| *"Check phone status & battery"* | `pwsh -Command "blaze-status"` |
| *"View phone notifications"* | `pwsh -Command "blaze-notifs"` |
| *"Set phone volume to `<0-15>`"* | `pwsh -Command "blaze-volume <0-15>"` |

---

## 🚀 Future Expansion Roadmap & AI Construction Recipes

The assistant can autonomously construct and integrate any of the following modules into PowerShell profile on demand:

### 1. `blaze-cam` (Silent Multi-Camera Capture)
- **Objective**: Capture high-resolution photo from rear (`-c 0`) or front (`-c 1`) camera and auto-save directly to PC or Obsidian vault.
- **Execution Blueprint**:
  ```powershell
  function Invoke-BlazeCam {
      param([ValidateSet("rear","front")]$Camera = "rear", [string]$OutPath = "$PWD/capture_$(Get-Date -f 'yyyyMMdd_HHmmss').jpg")
      $camId = if ($Camera -eq "front") { 1 } else { 0 }
      ssh blaze "termux-camera-photo -c $camId ~/temp_cam.jpg"
      scp blaze:~/temp_cam.jpg "$OutPath"
      ssh blaze "rm -f ~/temp_cam.jpg"
      Write-Host "📸 Captured to: $OutPath" -ForegroundColor Green
  }
  ```

### 2. `blaze-torch` (Hardware Flashlight Control)
- **Objective**: Instantly toggle rear LED torch.
- **Execution Blueprint**: `ssh blaze "termux-torch on"` (or `off`).

### 3. `blaze-sms` & `blaze-call` (Telephony & OTP Reader)
- **Objective**: Send SMS, trigger phone calls, or read incoming OTP messages directly from terminal.
- **Execution Blueprint**:
  - *Send SMS*: `ssh blaze "termux-sms-send -n <number> '<message>'"`
  - *Read SMS / OTP*: `ssh blaze "termux-sms-list -l 5"` (JSON parser extracts latest OTP code).
  - *Make Call*: `ssh blaze "termux-telephony-call <number>"`

### 4. `blaze-sentry` (Background Battery & Health Daemon)
- **Objective**: Lightweight watcher on PC that monitors Blaze battery level every 5 minutes and triggers a desktop popup / voice warning when battery < 20% or temperature > 42°C.

### 5. `blaze-vibrate` (Haptic Feedback)
- **Objective**: Vibrate phone for specified milliseconds (e.g. alert notification).
- **Execution Blueprint**: `ssh blaze "termux-vibrate -d 500"`

---

## 🛡️ Operational Guardrails & Best Practices

1. **Package Priority Hierarchy**:
   - **1st Scoop (`~/scoop/`)** > **2nd winget** > **3rd Standalone Portable Binary**.
   - Recorded permanently in `~/.gemini/memory/learnings.md`. Never install global MSI/system bloat when user-space scoop package exists.
2. **Token Splitting Guardrail**:
   - Never pass raw spaced strings into `Start-Process` array arguments. Use formatted quoted strings or Base64 `-EncodedCommand`.
3. **CRLF Invariant**:
   - Termux shell scripts and shared configs must always use Unix LF (`\n`). Strip `\r` before remote piping.
