# 🔔 `blaze-notifs` — Notification Studio, Mobile Dialogs & Screen Toast Interface

> **Command**: `blaze-notifs`  
> **Source Script**: [`scripts/blaze_notifs.py`](file:///scripts/blaze_notifs.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeNotifs` (Alias: `blaze-notifs`)  
> **Android Subsystems**: `termux-notification`, `termux-notification-list`, `termux-toast`, `termux-dialog`  
> **Key Capabilities**: 13-Widget Mobile Dialog Studio, Centered Screen Toasts with Color Palettes, Notification Tag/ID Dismissal, Live Polling Radar

---

## 🖥️ 1. Main Interactive Terminal Menu

When executing `blaze-notifs` from PowerShell without arguments, it launches the interactive inline FZF control center:

```text
┌── 🔔 BLAZE NOTIFICATIONS & MOBILE UI HUB ──────────────────────────────────────────────────┐
│ 📋 1. Browse Active Notifications  ──► Fuzzy search & 1-click inspect / dismiss (FZF)      │
│ 🔑 2. Extract Notification OTP    ──► Scan active status bar alerts for 2FA code           │
│ 📤 3. Send Push Notification      ──► Dispatch native Android alert to phone screen        │
│ 🍞 4. Screen Center Toast         ──► Display centered floating overlay toast              │
│ 📱 5. Mobile Dialog Studio        ──► Rich interactive dialogs (text, confirm, voice, pick)│
│ 🗑️ 6. Dismiss Notification by ID  ──► Remove target notification from status bar           │
│ 👀 7. Live Notification Watcher   ──► Real-time live streaming notification radar          │
│ 📖 8. Help & CLI Reference        ──► Flags, command switches & examples                   │
│ 🚪 0. Exit                        ──► Return to PowerShell terminal                        │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze Notifs > _
```

---

## 📋 2. Active Notification Browser (`Option 1` / `--list`)

### Step 1: Inline FZF Notification Browser (Newest First)
```text
┌── 🔔 ACTIVE NOTIFICATIONS (Newest First | Enter to inspect | Esc to back) ─────────────────┐
│ 01. Whatsapp     │ Rohit Sharma         │ Can you check the build logs?                    │
│ 02. Github       │ Antigravity CI       │ Workflow #42 passed on main                      │
│ 03. Messages     │ VK-HDFCBK            │ 839201 is your OTP for transaction               │
│ 04. Termux       │ Background Service   │ SSH server active on port 8022                   │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select Notification > _
```

### Step 2: Inspection Card & Action Sheet
```text
🔔 NOTIFICATION #1
┌────────────────────────────────────────────────────────┐
│ 📦 App:     Whatsapp                                   │
│ 🏷️ Title:   Rohit Sharma                               │
│ 🕒 Time:    2026-09-14 00:25:10                        │
│ 🆔 ID/Tag:  1042                                       │
├────────────────────────────────────────────────────────┤
│ Content:                                               │
│   Can you check the build logs?                        │
└────────────────────────────────────────────────────────┘

┌── Notification from Whatsapp ──────────────────────────────────────────────────────────────┐
│ 1. 📋 Copy Notification Text     ──► Copy title & body to PC clipboard                     │
│ 2. 🗑️ Dismiss Notification (1042)──► Clear notification from status bar                    │
│ 0. 🔙 Back to Notifications       ──► Return to notification list                           │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Action on Whatsapp > _
```

---

## 📱 3. Mobile Dialog Studio (`Option 5` / `--dialog <widget>`)

Spawns rich interactive GUI modals directly on the phone's physical screen and retrieves user input back to Motobook (with auto-copy to Windows clipboard):

```text
┌── 📱 MOBILE DIALOG STUDIO (Design & Dispatch) ─────────────────────────────────────────────┐
│ 1. 📝 Text Input          ──► Standard keyboard prompt                                     │
│ 2. 🔒 Password / Secret    ──► Masked text entry (PIN/Password)                             │
│ 3. 📄 Multiline Text Area  ──► Large paragraph / note editor                                │
│ 4. 🔢 Number Input         ──► Numeric keypad input                                         │
│ 5. ❓ Confirmation Prompt  ──► Yes / No (OK / Cancel) modal                                 │
│ 6. 🔘 Radio Buttons        ──► Single choice from options list                              │
│ 7. ☑️ Checkbox Selector    ──► Multiple choices from list                                   │
│ 8. 📜 Sliding Bottom Sheet ──► Native Android slide-up picker                               │
│ 9. 🎯 Dropdown Spinner     ──► Compact dropdown select menu                                 │
│ 10. 🔢 Numeric Counter     ──► Stepper / Range counter                                      │
│ 11. 🎤 Voice / Mic Input   ──► Speech-to-text via phone microphone                          │
│ 12. 📅 Date Picker         ──► Interactive calendar selector                                │
│ 13. 🕒 Time Picker         ──► Interactive clock selector                                   │
│ 0. 🔙 Return to Main Menu ──► Cancel                                                       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Dialog Type > _
```

### Dialog Return Card (Input Received from Phone Screen)
```text
📱 MOBILE DIALOG RESPONSE RECEIVED:
┌────────────────────────────────────────────────────────┐
│ 🏷️ Dialog Type:  TEXT                                   │
│ 📌 Title:        Motobook Mission Brief                │
│ 💬 Input Text:   Security sweep complete. All clear.   │
└────────────────────────────────────────────────────────┘
📋 'Security sweep complete. All clear.' automatically copied to Windows clipboard!
```

---

## 🍞 4. Screen Center Toast Designer (`Option 4` / `--toast`)

Displays floating onscreen toasts centered on the phone display with custom background palettes:

```text
┌── 🍞 TOAST DESIGNER (Screen Center) ───────────────────────────────────────────────────────┐
│ 1. 💬 Standard Slate      ──► Screen Center | Slate Gray (#37474F)                         │
│ 2. 🟢 Emerald Green (OK)   ──► Screen Center | Forest Green (#1B5E20)                       │
│ 3. 🔴 Crimson Alert (War) ──► Screen Center | Ruby Red (#B71C1C)                           │
│ 4. 🔵 Neon Cyber Cyan     ──► Screen Center | Deep Cyan (#006064)                          │
│ 5. 🟡 Amber Gold (Warning) ──► Screen Center | Warm Amber (#FF6F00)                         │
│ 6. 🟣 Deep Purple Matrix   ──► Screen Center | Regal Purple (#4A148C)                       │
│ 7. 🌑 Midnight Stealth     ──► Screen Center | Jet Black (#121212)                          │
│ 8. ☀️ Solar Sunshine       ──► Screen Center | Bright Yellow (#FFD600)                      │
│ 9. 🌊 Sapphire Blue        ──► Screen Center | Royal Blue (#0D47A1)                         │
│ 10. 🎨 Custom Palette & Pos ──► Choose Custom Colors (Hex/Name) & Gravity                   │
│ 0. 🔙 Return to Menu                                                                       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Toast Theme > _
```

### Screen Confirmation Card:
```text
✅ Toast displayed in screen (middle): "Build complete and deployed!"
[Android Screen Visual: Floating green pill in center of screen]
```

---

## 📤 5. Native Push Notification Dispatcher (`Option 3`)

```text
Notification Title: Antigravity Alert
Notification Body: Backup completed successfully.
✅ Notification pushed with ID: 9421
[Android Screen Notification Shade: 🔔 Antigravity Alert - Backup completed successfully.]
```

---

## 👀 6. Live Notification Streaming Radar (`Option 7` / `--watch`)

```text
👀 Starting Live Notification Watcher (Polling every 3s)... [Ctrl+C to stop]

[00:26:12] Whatsapp: Rohit Sharma ──► Can you check the build logs?
[00:26:45] Github: Antigravity CI ──► Workflow #42 passed on main
[00:27:01] Messages: VK-HDFCBK ──► 839201 is your OTP for transaction
```

---

## 📖 7. Help & CLI Reference Screen (`Option 8` / `-h` / `--help`)

```text
┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-NOTIFS COMMAND & CLI REFERENCE                │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-notifs                      │
│ • List Notifications:blaze-notifs --list               │
│ • Extract OTP:       blaze-notifs --otp                │
│ • Push Notification: blaze-notifs --title <t> --body <b>│
│ • Centered Toast:    blaze-notifs --toast "<message>"  │
│ • Rich Mobile Dialog:blaze-notifs --dialog <widget>    │
│   (text, password, multiline, confirm, radio, sheet,   │
│    checkbox, spinner, counter, speech, date, time)     │
│ • Dismiss by ID/Tag: blaze-notifs --dismiss <id|tag>   │
│ • Live Watcher:      blaze-notifs --watch [seconds]    │
│ • JSON Machine Mode: blaze-notifs --json               │
└────────────────────────────────────────────────────────┘
```
