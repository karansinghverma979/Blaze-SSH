# 📖 Blaze Operational & Deployment Instructions

This guide details how to install, configure, and operate the entire **Motobook ⇄ Blaze** multi-device suite.

---

## 🛠️ 1. Prerequisites & Environment Setup

### PC Node (Motobook - Windows 11)
1. **Python 3.10+**: Ensure Python is in `PATH`.
2. **OpenSSH Client & Server**:
   ```powershell
   Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
   Start-Service sshd
   ```
3. **Scoop Packages**:
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

## 🚀 2. PowerShell Profile Integration

Add the following mappings to your `$PROFILE` (`Microsoft.PowerShell_profile.ps1`):

```powershell
# Blaze Command Hubs
function Invoke-BlazePhone  { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_phone.py" @args }
function Invoke-BlazeWifi   { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_wifi.py" @args }
function Invoke-BlazeMedia  { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_media.py" @args }
function Invoke-BlazeTTS    { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_speak.py" @args }
function Invoke-BlazeClip   { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_clip.py" @args }
function Invoke-BlazeNotifs { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_notifs.py" @args }
function Invoke-BlazeFile   { & python "$env:USERPROFILE\Void\Blaze\scripts\blaze_file.py" @args }

Set-Alias -Name blaze-phone  -Value Invoke-BlazePhone
Set-Alias -Name blaze-wifi   -Value Invoke-BlazeWifi
Set-Alias -Name blaze-media  -Value Invoke-BlazeMedia
Set-Alias -Name blaze-speak  -Value Invoke-BlazeTTS
Set-Alias -Name blaze-clip   -Value Invoke-BlazeClip
Set-Alias -Name blaze-notifs -Value Invoke-BlazeNotifs
Set-Alias -Name blaze-file   -Value Invoke-BlazeFile
```

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
