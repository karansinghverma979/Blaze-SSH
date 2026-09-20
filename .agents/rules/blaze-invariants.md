# 📜 Blaze Project Rules & Invariants

> **Project**: Blaze Mobile Integration & Automation Hub  
> **Hosts**: `Motobook` (Windows 11 Pro) ⇄ `Blaze` (Lava Blaze 5G / Android 14)  
> **Author**: Karan Singh Verma & Antigravity AI Assistant

---

## 🏛️ Core Principles & Invariants

### 1. Dual-Interface & Help Governance
- **Zero Arguments = Interactive UI**: Running any `blaze-*` command without arguments **must always** launch a rich, colored ASCII / numbered interactive menu. It must never require mandatory flags to be usable by a human.
- **Mandatory Help Flag (`--help` / `-h`)**: Every script and command **must support `--help` and `-h`** with comprehensive, well-formatted descriptions, switches, and usage examples.
- **In-Menu Help Discovery**: Every interactive menu should include a clear option or note pointing to `--help` / `-h` switches so users discover fast-path flags easily.
- **Flags = Instant Fast-Path**: Passing explicit CLI flags (e.g. `--otp`, `--pull`, `--push`, `--mount`, `--stealth`) **must bypass all interactive prompts** and execute the operation immediately in <500ms.
- **Machine Readability**: All scripts must provide `--json` and `--raw` flags to allow headless programmatic parsing by the AI Assistant or shell pipelines.

### 2. Mandatory UI Standard: Symmetrical Spacing, Single-Column & Zero Right-Side Borders (CRITICAL)
Every script, menu, HUD, diagnostic card, or CLI tool in the Blaze project **must strictly adhere** to this visual UI layout:
- **One Datum Per Line**: Display strictly one piece of information / key-value metric per line. Never cram multiple metrics side-by-side on the same row.
- **Zero Right-Side `|` Borders**: Never use fixed right-side `|` box borders or dual-column vertical splitters (as ANSI color codes have 0 printed width but non-zero character lengths, causing right-side borders to misalign and look ragged).
- **Symmetrical Section Spacing**: Always place a blank spacer line (`│`) at both the top (below headers) and the bottom (before dividers) of every section.
- **Consistent Label Padding**: Maintain uniform label padding (e.g., 18 characters) across all keys so values are vertically aligned.
- **Left-Anchored Open Cards**: Always structure terminal cards using clean left-anchored box stems:
  ```text
  ┌── 📱 BLAZE COMPONENT RADAR ─────────────────────────────
  │
  │ 📱 Device Model:       Lava Blaze 5G (Android 14)
  │ ⏱️  System Uptime:      4 hours, 12 mins
  │
  ├── 🔋 Subsystem Section ─────────────────────────────────
  │
  │ ⚡  Metric Name:        Value
  │ 🔌 State Field:        Active Value
  │
  └── 🚀 Node Live & Operational
  ```

### 3. Resilient Fallback & Unresponsive Node Defense (CRITICAL)
Whenever designing or modifying any command, tool, or script:
- **Mandatory Connection Timeout**: Every SSH network invocation must enforce a strict `-o ConnectTimeout=3` (maximum 5 seconds). A disconnected phone or unresponsive daemon must **never hang or freeze the terminal indefinitely**.
- **Actionable Diagnostic Fallback**: If the phone is offline, unresponsive, or `sshd` is stopped:
  - **Human CLI Mode**: Output a standardized, red/yellow actionable diagnostic card showing:
    1. Root Cause (`Port 8022 Unreachable` / `Connection Dropped` / `Timeout`).
    2. Concrete Steps to Resolve (1. Ensure Termux is open, 2. Run `sshd`, 3. Confirm same Wi-Fi/Hotspot).
  - **Machine/JSON Mode**: Return a clean JSON error object (`{"error": "NODE_UNREACHABLE", "details": "..."}`) with non-zero exit code so automated callers never crash on unhandled exceptions.
- **Mid-Session Network Disconnect Recovery**: When interactive sessions (like `blaze` shell or `scrcpy` video streams) terminate unexpectedly due to Wi-Fi drops (Exit code 255), trap the signal cleanly and provide instant reconnect guidance.

### 4. Synchronization & Ecosystem Integrity Mandate (CRITICAL)
Whenever any script is modified, new flags added, or workflows updated:
- **`README.md`**: Must be updated to reflect newly available switches and command syntax.
- **`ARCHITECTURE.md`**: Must be updated if communication topology, ports, or execution pipelines evolve.
- **`INSTRUCTIONS.md`**: Must maintain up-to-date prerequisite versions and installation steps.
- **`SKILL.md`**: Must maintain synchronous command references so the AI Assistant (/blaze) knows all switches.
- **`blaze_profile.ps1`**: Must be updated in lockstep whenever new functions or aliases are introduced.
- **`~/.config/` & `$PROFILE`**: Production scripts must stay mirrored to ensure existing local terminals work without interruption.

### 5. Upstream Git Invariant: Milestone-Based Push to GitHub 🚀
- **Batched Command Push Protocol**: You do not need to execute `git push` on every intermediate micro-edit. Work, iterate, and verify locally. Once a command's development, refactor, or major milestone is completed and verified—or before transitioning to development on another command—commit and push the milestone upstream (`git push origin main`).
- **Zero Desync Before Handoff**: The GitHub remote (`karansinghverma979/Blaze-SSH`) must be kept up to date at every major milestone handoff.

### 6. Network & Port Allocations
- **Motobook (PC) SSH**: Port `22` (OpenSSH for Windows, User: `karan`).
- **Blaze (Phone) SSH**: Port `8022` (Termux OpenSSH, User: `u0_a46`).
- **Wireless ADB**: Port `5555`.
- **Subnet Standard**: `10.242.186.0/24` (Lava Blaze 5G Hotspot Gateway: `10.242.186.1`).
- **Authentication**: Strict cryptographic Ed25519 public key trust (`id_ed25519`). Zero hardcoded passwords in scripts.

### 7. Graceful Signal Handling & Non-Blocking Resilience
- **Ctrl+C / Esc Invariant**: Pressing `Ctrl+C` or `Esc` anywhere across interactive loops must cleanly catch `KeyboardInterrupt` and output `👋 Exited gracefully.` with zero raw Python tracebacks.
- **UTF-8 Safety**: Windows console output must always initialize `sys.stdout.reconfigure(encoding='utf-8')` to prevent `UnicodeEncodeError` on emojis and box-drawing characters.

### 8. Storage & Filesystem Discipline
- **Local Dropped Files**: Files sent to PC from phone are saved to `~/Blaze/` by default.
- **Phone Dropped Files**: Files dropped to phone from PC land in `/sdcard/Download/` and automatically trigger `termux-media-scan` so Android gallery and media players index them immediately.
- **Drive Z:\\ Mount**: Remote storage is mounted exclusively via Rclone SFTP + WinFsp. Clean unmounting must terminate all child `rclone` processes cleanly.

---

## 🛡️ Prohibited Practices
1. **Never hardcode dynamic IP addresses** in script files — rely on `ssh blaze` or runtime resolution.
2. **Never leave orphan Rclone processes** running when an unmount is requested.
3. **Never write destructive filesystem commands** (e.g. `rm -rf`) over SSH without interactive confirmation.
4. **Never update a Python script without synchronizing `SKILL.md`, `blaze_profile.ps1`, and `README.md`**.
5. **Never execute an SSH command without an explicit timeout (`ConnectTimeout=3`) and offline diagnostic fallback.**
6. **Never use fixed right-side `|` box borders or dual-column splitters in terminal UIs.**
7. **Never clutter terminal output without proper symmetrical blank line spacing and readable label alignment.**
