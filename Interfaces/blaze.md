# ⚡ `blaze` — Core SSH Shell Connector & Network Discovery Interface

> **Command**: `blaze` (or `blaze "<remote_command>"`)  
> **Source Module**: [`C:\Users\karan\Void\Blaze\blaze_profile.ps1`](file:///C:/Users/karan/Void/Blaze/blaze_profile.ps1)  
> **PowerShell Function**: `Connect-BlazePhone` (Alias: `blaze`)  
> **Target Node**: Lava Blaze 5G (`u0_a46@blaze:8022` running Termux Zsh)  
> **Security Protocol**: Zero-Password Ed25519 Cryptographic Handshake (`~/.ssh/id_ed25519`)

---

## 🖥️ 1. Interactive Terminal Session Flow

When running `blaze` from PowerShell without arguments:

```text
PS C:\Users\karan> blaze
⚡ Connecting to Blaze at 10.154.149.220...

[Android Screen Notification Pop-up: ⚡ Motobook terminal connected]

┌── 📱 BLAZE TERMINAL HUD ──────────────────────────────────────────┐
│ 🔋 Battery: 88% (Discharging) | 🌡️ Temp: 31.4°C                  │
│ 📡 Net: 10.154.149.220 (Mobile Hotspot AP0)                       │
│ ⚡ Uptime: up 4 days, 3 hours                                      │
└───────────────────────────────────────────────────────────────────┘

u0_a46@blaze ~ $ _
```

---

## ⚡ 2. Single-Line Remote Execution (Fast-Path Mode)

When passing arbitrary remote commands to `blaze`:

```text
PS C:\Users\karan> blaze "termux-battery-status"
{
  "health": "GOOD",
  "percentage": 88,
  "plugged": "UNPLUGGED",
  "status": "DISCHARGING",
  "temperature": 31.4
}
```

```text
PS C:\Users\karan> blaze "ls -la ~/storage/shared/Download"
total 248
drwxrwx--x  4 root sdcard_rw   4096 Sep 13 22:30 .
drwxrwx--x 32 root sdcard_rw   4096 Sep 10 14:15 ..
-rw-rw----  1 root sdcard_rw 245760 Sep 13 22:15 report.pdf
```

---

## 🔍 3. 3-Tier Dynamic IP Discovery Pipeline

Every execution of `blaze` invokes `Get-BlazeTargetIP`, probing the network across 3 cascading stages in `<200ms`:

```text
┌─────────────────────────────────────────────────────────────┐
│ 🔍 DYNAMIC BLAZE IP DISCOVERY RADAR                         │
├─────────────────────────────────────────────────────────────┤
│ 1. TIER 1: Mobile Hotspot Gateway Probe (0.0.0.0/0 NetRoute)│
│    ──► Tests default gateway on TCP port 8022               │
│                                                             │
│ 2. TIER 2: Hardware MAC Match Probe (F6-DC-F9-03-FA-07)     │
│    ──► Scans ARP neighbor table for phone physical MAC      │
│                                                             │
│ 3. TIER 3: Cached / SSH Config Probe                        │
│    ──► Fast-validates last known working IP address         │
└─────────────────────────────────────────────────────────────┘
```

Once resolved, it dynamically regenerates `~/.ssh/config`:

```sshconfig
Host blaze phone
    HostName 10.154.149.220
    Port 8022
    User u0_a46
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
    ServerAliveInterval 3
    ServerAliveCountMax 2
    ConnectTimeout 3
```

---

## ⚠️ 4. Unreachable & Disconnect Error States

### Unreachable State Box (Blaze Offline / SSH Server Down)
```text
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ BLAZE SSH SERVER UNREACHABLE (Port 8022)                 │
├─────────────────────────────────────────────────────────────┤
│ • Status:   Could not locate Blaze on current network.      │
│ • Action:   1. Ensure Termux is running 'sshd' on phone.    │
│             2. Ensure phone is on the same Wi-Fi / Hotspot. │
└─────────────────────────────────────────────────────────────┘
```

### Connection Dropped State (Network Switch / Node Slept)
```text
⚠️ [Connection Dropped] Blaze disconnected or network switched.
💡 Run 'blaze' to reconnect whenever device is back online.
```
