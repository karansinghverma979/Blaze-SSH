# 📖 Blaze Operational & Deployment Instructions

This guide details how to install, configure, and operate the entire **Motobook ⇄ Blaze** multi-device suite.

---

## 🛠️ 1. Prerequisites & Environment Setup

### PC Node (Motobook - Windows 11)
1. **Python 3.10+**: Ensure Python is added to system `PATH`.
2. **OpenSSH Client & Server**:
   ```powershell
   Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
   Start-Service sshd
   ```
3. **Scoop Portable Tools**:
   ```powershell
   scoop install scrcpy adb rclone
   ```
4. **SSH Key Pair**:
   Ensure `~/.ssh/id_ed25519.pub` exists and is appended to Termux `~/.ssh/authorized_keys`.

### Phone Node (Blaze - Lava Blaze 5G / Android 14)
1. **Termux & Termux:API**: Install Termux and Termux:API app from F-Droid.
2. **Termux Packages**:
   ```bash
   pkg update && pkg install openssh termux-api python zsh -y
   ```
3. **Boot Persistence & Wake-Lock**:
   ```bash
   termux-wake-lock
   sshd
   ```

---

## 🚀 2. PowerShell Profile Setup Walkthrough

### Step 1: Open Your PowerShell Profile
Run this command in any terminal:
```powershell
notepad $PROFILE
```
*(If the file does not exist, run `New-Item -ItemType File -Path $PROFILE -Force` first).*

### Step 2: Add Dot-Source Loader
Add this single line at the end of `$PROFILE`:
```powershell
. "$env:USERPROFILE\Void\Blaze\blaze_profile.ps1"
```

### Step 3: Reload Your Shell
```powershell
. $PROFILE
```
Now all commands (`blaze`, `blaze-phone`, `blaze-wifi`, `blaze-media`, `blaze-speak`, `blaze-clip`, `blaze-notifs`, `blaze-file`, `blaze-status`, `blaze-location`) are active!

---

## ⚡ 3. Command Reference & Fast Triggers

| Command | Fast-Path Switch | Description |
| :--- | :--- | :--- |
| `blaze-phone` | `--otp` | 1-Click OTP extraction from SMS directly to PC clipboard. |
| `blaze-phone` | `--contacts [query]` | Search address book contacts with phone/SMS actions. |
| `blaze-phone` | `--logs` | View recent incoming/outgoing/missed call history. |
| `blaze-phone` | `--cell` | Inspect live 5G NR / LTE cellular carrier telemetry. |
| `blaze-wifi` | `--info` | View active Wi-Fi SSID, BSSID, RSSI dBm, link speed, and IP. |
| `blaze-wifi` | `--scan` | Scan visible Wi-Fi networks spectrum sorted by signal. |
| `blaze-wifi` | `--stealth` | Launch 60fps Scrcpy wireless stream with phone screen turned off. |
| `blaze-wifi` | `--audio-only` | Stream phone audio to PC speakers via low-latency Opus codec. |
| `blaze-clip` | `--pull` | Pull phone clipboard to PC clipboard. |
| `blaze-clip` | `--push` | Push PC clipboard to phone with overlay toast. |
| `blaze-clip` | `--sync` | Side-by-side visual diff and bidirectional sync. |
| `blaze-notifs`| `--list` | View incoming active Android notifications. |
| `blaze-notifs`| `--otp` | Extract OTP from active notifications. |
| `blaze-notifs`| `--toast "Text"` | Display floating toast on phone screen. |
| `blaze-file` | `--drop <path>` | Transfer PC file to `/sdcard/Download/` + auto MediaStore scan. |
| `blaze-file` | `--pull <path>` | Download remote file from phone to `~/Blaze/`. |
| `blaze-file` | `--mount` | Mount phone storage as native Windows Drive **`Z:\`**. |
| `blaze-file` | `--unmount` | Disconnect Drive **`Z:\`** and stop Rclone. |
| `blaze-speak`| `"<text>"` | Synthesize neural voice on phone speaker via Edge-TTS. |
| `blaze-speak`| `--clip` | Read Windows clipboard out loud on phone. |
| `blaze-speak`| `--status` | Speak battery % and network connectivity briefing. |
