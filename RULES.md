# 📜 Blaze Project Rules & Invariants

> **Project**: Blaze Mobile Integration & Automation Hub  
> **Hosts**: `Motobook` (Windows 11 Pro) ⇄ `Blaze` (Lava Blaze 5G / Android 14)  
> **Author**: Karan Singh Verma & Antigravity AI Assistant

---

## 🏛️ Core Principles & Invariants

### 1. Dual-Interface Governance
- **Zero Arguments = Interactive UI**: Running any `blaze-*` command without arguments **must always** launch a rich, colored ASCII / numbered interactive menu. It must never require mandatory flags to be usable by a human.
- **Flags = Instant Fast-Path**: Passing explicit CLI flags (e.g. `--otp`, `--pull`, `--push`, `--mount`, `--stealth`) **must bypass all interactive prompts** and execute the operation immediately in <500ms.
- **Machine Readability**: All scripts must provide `--json` and `--raw` flags to allow headless programmatic parsing by the AI Assistant or shell pipelines.

### 2. Synchronization & Ecosystem Integrity Mandate (CRITICAL)
Whenever any script is modified, new flags added, or workflows updated:
- **`README.md`**: Must be updated to reflect newly available switches and command syntax.
- **`ARCHITECTURE.md`**: Must be updated if communication topology, ports, or execution pipelines evolve.
- **`INSTRUCTIONS.md`**: Must maintain up-to-date prerequisite versions and installation steps.
- **`SKILL.md`**: Must maintain synchronous command references so the AI Assistant (/blaze) knows all switches.
- **`blaze_profile.ps1`**: Must be updated in lockstep whenever new functions or aliases are introduced.
- **`~/.config/` & `$PROFILE`**: Production scripts must stay mirrored to ensure existing local terminals work without interruption.

### 3. Network & Port Allocations
- **Motobook (PC) SSH**: Port `22` (OpenSSH for Windows, User: `karan`).
- **Blaze (Phone) SSH**: Port `8022` (Termux OpenSSH, User: `u0_a46`).
- **Wireless ADB**: Port `5555`.
- **Subnet Standard**: `10.242.186.0/24` (Lava Blaze 5G Hotspot Gateway: `10.242.186.1`).
- **Authentication**: Strict cryptographic Ed25519 public key trust (`id_ed25519`). Zero hardcoded passwords in scripts.

### 4. Graceful Signal Handling & Non-Blocking Resilience
- **Ctrl+C / Esc Invariant**: Pressing `Ctrl+C` or `Esc` anywhere across interactive loops must cleanly catch `KeyboardInterrupt` and output `👋 Exited gracefully.` with zero raw Python tracebacks.
- **Connection Timeout Guard**: All SSH network calls must enforce `-o ConnectTimeout=3` (or maximum 5 seconds). An offline phone must never hang the terminal indefinitely.
- **UTF-8 Safety**: Windows console output must always initialize `sys.stdout.reconfigure(encoding='utf-8')` to prevent `UnicodeEncodeError` on emojis and box-drawing characters.

### 5. Storage & Filesystem Discipline
- **Local Dropped Files**: Files sent to PC from phone are saved to `~/Blaze/` by default.
- **Phone Dropped Files**: Files dropped to phone from PC land in `/sdcard/Download/` and automatically trigger `termux-media-scan` so Android gallery and media players index them immediately.
- **Drive Z:\\ Mount**: Remote storage is mounted exclusively via Rclone SFTP + WinFsp. Clean unmounting must terminate all child `rclone` processes cleanly.

---

## 🛡️ Prohibited Practices
1. **Never hardcode dynamic IP addresses** in script files — rely on `ssh blaze` or runtime resolution.
2. **Never leave orphan Rclone processes** running when an unmount is requested.
3. **Never write destructive filesystem commands** (e.g. `rm -rf`) over SSH without interactive confirmation.
4. **Never update a Python script without synchronizing `SKILL.md`, `blaze_profile.ps1`, and `README.md`**.
