# 📋 `blaze-clip` — Bidirectional Clipboard Sync & Visual Diff Interface

> **Command**: `blaze-clip`  
> **Source Script**: [`scripts/blaze_clip.py`](file:///scripts/blaze_clip.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeClip` (Alias: `blaze-clip`)  
> **Protocol**: Termux API v2 Protocol (`/data/data/com.termux/files/usr/libexec/termux-api Clipboard -e api_version 2`)  
> **Windows Engine**: Native PowerShell `Get-Clipboard` / `Set-Clipboard`  
> **Key Capabilities**: Sub-second Bidirectional Sync, Side-by-Side Visual Diff Radar, Direct Custom Text Injection

---

## 🖥️ 1. Main Interactive Terminal Menu

When running `blaze-clip` from PowerShell without arguments, it launches the interactive inline FZF sync hub:

```text
┌── 📋 BLAZE UNIFIED CLIPBOARD COMMAND HUB ──────────────────────────────────────────────────┐
│ 📥 1. Pull Phone Clipboard ➔ PC    ──► Copy Blaze text into Windows clipboard              │
│ 📤 2. Push PC Clipboard ➔ Phone    ──► Send Windows clipboard to Blaze phone               │
│ 🔄 3. Side-by-Side Visual Diff     ──► Compare Motobook vs Blaze and sync                  │
│ ✍️ 4. Send Custom Text to Phone    ──► Type arbitrary text straight to Blaze               │
│ 📖 5. Help & CLI Reference         ──► Flags, command switches & examples                  │
│ 🚪 0. Exit                         ──► Return to PowerShell terminal                       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze Clip > _
```

---

## 📥 2. Pull Phone Clipboard to PC (`Option 1` / `--pull`)

Retrieves the active clipboard text from Blaze and injects it directly into the Windows clipboard:

```text
✅ PULLED FROM BLAZE ➔ PC CLIPBOARD
┌────────────────────────────────────────────────────────┐
│ https://github.com/karansinghverma979/Blaze-SSH        │
└────────────────────────────────────────────────────────┘
📋 Ready to paste (Ctrl+V) on Motobook.
```

---

## 📤 3. Push PC Clipboard to Phone (`Option 2` / `--push`)

Reads the active Windows clipboard and transmits it over SSH directly into Android's system clipboard:

```text
✅ PUSHED TO BLAZE CLIPBOARD ➔ PHONE
┌────────────────────────────────────────────────────────┐
│ export OPENAI_API_KEY="sk-antigravity-99482104"        │
└────────────────────────────────────────────────────────┘
📱 Phone received toast and clipboard updated.
[Android Screen Notification Pop-up: 📋 Copied from Motobook]
```

---

## 🔄 4. Side-by-Side Visual Diff & Conflict Radar (`Option 3` / `--sync`)

Displays a dual-column comparison card between Motobook (PC) and Blaze (Phone) text, prompting for sync resolution direction:

```text
📋 SIDE-BY-SIDE CLIPBOARD RADAR
┌────────────────────────────┬────────────────────────────┐
│ 💻 MOTOBOOK (PC)           │ 📱 BLAZE (Phone)           │
├────────────────────────────┼────────────────────────────┤
│ export OPENAI_API_KEY="..  │ https://github.com/karan.. │
└────────────────────────────┴────────────────────────────┘

┌── Select Clipboard Direction ──────────────────────────────────────────────────────────────┐
│ 1. 📤 Push PC to Phone  ──► Overwrite Blaze clipboard with PC text                         │
│ 2. 📥 Pull Phone to PC  ──► Overwrite Motobook clipboard with Phone text                  │
│ 0. 🔙 Cancel            ──► Return to menu                                                 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Sync Action > _
```

---

## ✍️ 5. Send Custom Text Prompt (`Option 4` / `--send "<text>"`)

Quickly injects arbitrary text or links to the phone without having to place them in your PC clipboard first:

```text
Enter text to push to Blaze: meeting-link: https://meet.google.com/abc-defg-hij

✅ PUSHED TO BLAZE CLIPBOARD ➔ PHONE
┌────────────────────────────────────────────────────────┐
│ meeting-link: https://meet.google.com/abc-defg-hij     │
└────────────────────────────────────────────────────────┘
📱 Phone received toast and clipboard updated.
```

---

## 📖 6. Help & CLI Reference Screen (`Option 5` / `-h` / `--help`)

```text
┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-CLIP COMMAND & CLI REFERENCE                  │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-clip                        │
│ • Pull Phone to PC:  blaze-clip --pull                 │
│ • Push PC to Phone:  blaze-clip --push                 │
│ • Send Direct Text:  blaze-clip --send "<text>"        │
│ • Side-by-Side Sync: blaze-clip --sync                 │
│ • Raw Output Mode:   blaze-clip --raw                  │
│ • JSON Machine Mode: blaze-clip --json                 │
└────────────────────────────────────────────────────────┘
```
