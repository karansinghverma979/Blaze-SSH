# 📱 `blaze-phone` — Telephony, SMS Inbox, Contacts & 5G Cellular Interface

> **Command**: `blaze-phone`  
> **Source Script**: [`scripts/blaze_phone.py`](file:///scripts/blaze_phone.py)  
> **PowerShell Cmdlet**: `Invoke-BlazePhone` (Alias: `blaze-phone`)  
> **Subsystems**: Android Telephony API (`termux-telephony-call`, `termux-sms-send`, `termux-sms-list`, `termux-contact-list`, `termux-call-log`)  
> **Key Capabilities**: 1-Click OTP Extraction to PC Clipboard, In-Ear & Speakerphone Dialer, Interactive SMS Threading, Fuzzy Address Book

---

## 🖥️ 1. Main Interactive Terminal Menu

When running `blaze-phone` from PowerShell without arguments, it launches the full interactive telephony hub:

```text
┌── 📱 BLAZE TELEPHONY & CELLULAR COMMAND HUB ───────────────────────────────────────────────┐
│ 🔑 1. 1-Click OTP Extractor       ──► Auto-extract & copy latest OTP to PC                 │
│ 📬 2. Interactive SMS Inbox       ──► Browse & search SMS messages (FZF)                   │
│ 📨 3. Send SMS Message           ──► Pick contact or type number & message                 │
│ 📇 4. Search Address Book         ──► Instant fuzzy search & dial / SMS (FZF)               │
│ 📞 5. Dial Phone / Make Call      ──► Initiate native cellular call on Blaze               │
│ 📜 6. View Call History           ──► Browse call logs & 1-click callback (FZF)            │
│ 📡 7. 5G NR & Cell Telemetry      ──► View live carrier & tower radio signals              │
│ 📱 8. SIM & Telephony Specs       ──► Inspect baseband hardware & operator                 │
│ 📖 9. Help & CLI Reference        ──► Command switches, options & examples                 │
│ 🚪 0. Exit                       ──► Return to PowerShell terminal                         │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze Phone > _
```

---

## 🔑 2. 1-Click OTP Extraction Engine (`Option 1` / `--otp`)

Scans incoming SMS inbox (latest-first), uses regex pattern matching to extract 4–8 digit verification codes, and automatically copies the OTP to your Windows clipboard:

```text
✨ OTP DETECTED & COPIED TO CLIPBOARD!
┌────────────────────────────────────────────────────────┐
│ 🔑 OTP Code:   482910                                  │
│ 👤 Sender:     VK-GOOGTX                               │
│ 🕒 Received:   2026-09-14 00:22:15                     │
└────────────────────────────────────────────────────────┘
📋 Ready to paste (Ctrl+V) anywhere on Motobook.
```

---

## 📬 3. Interactive SMS Inbox & Thread Inspector (`Option 2` / `--sms`)

### Step 1: Inline FZF SMS Browser (Newest Messages First)
```text
┌── 📬 SMS INBOX (Newest First | Type to filter | Enter to inspect | Esc to back) ────────────┐
│ 01. VK-GOOGTX        │ 2026-09-14 00:22:15 │ 482910 is your Google verification code.      │
│ 02. +919876543210    │ 2026-09-13 21:40:02 │ Hey Karan, are the server metrics ready?      │
│ 03. AX-HDFCBK        │ 2026-09-13 18:15:30 │ Alert: Rs 1,500.00 debited for Cloud Server.  │
│ 04. JIO-ALRT         │ 2026-09-13 12:00:00 │ Daily high-speed data balance 50% consumed.   │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select SMS > _
```

### Step 2: Message Inspection Card & Action Sheet
```text
📨 SMS MESSAGE #2
┌────────────────────────────────────────────────────────┐
│ 👤 Sender:   +919876543210                             │
│ 🕒 Date:     2026-09-13 21:40:02                       │
├────────────────────────────────────────────────────────┤
│ Message Content:                                       │
│   Hey Karan, are the server metrics ready?             │
└────────────────────────────────────────────────────────┘

┌── Message from +919876543210 ──────────────────────────────────────────────────────────────┐
│ 1. 📨 Reply via SMS              ──► Type text response to sender                          │
│ 2. 📞 Call Sender (+919876543210)──► Dial sender phone number                              │
│ 3. 📋 Copy Full Message Body     ──► Copy entire text to PC clipboard                      │
│ 0. 🔙 Back to Inbox              ──► Return to message list                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Action on +919876543210 > _
```

---

## 📇 4. Fuzzy Address Book & Contact Dialer (`Option 4` / `--contacts`)

### Step 1: Instant FZF Address Book Search
```text
┌── 📇 ADDRESS BOOK (Type to filter | Enter to select | Esc to back) ─────────────────────────┐
│ 001. Karan Singh Verma          │ +919876543210                                            │
│ 002. Rohit Sharma (Lead Dev)    │ +919123456789                                            │
│ 003. Vikram Malhotra (Security) │ +919988776655                                            │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Search Contacts > _
```

### Step 2: Contact Action Sheet
```text
┌── Contact: Rohit Sharma (Lead Dev) (+919123456789) ────────────────────────────────────────┐
│ 1. 📞 Call Rohit Sharma (Normal)      ──► Cellular call via earpiece                       │
│ 2. 🔊 Call Rohit Sharma (Speaker)     ──► Cellular call on Speakerphone                    │
│ 3. 📨 Send SMS to Rohit Sharma        ──► Compose and dispatch text                        │
│ 4. 📋 Copy Number (+919123456789)     ──► Copy to PC clipboard                             │
│ 0. 🔙 Back                            ──► Return to address book                           │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Action on Rohit Sharma > _
```

---

## 📞 5. Dual-Mode Phone Dialer Engine (`Option 5` / `--call` / `--speaker`)

### Normal Earpiece Mode (`--call <number>`)
```text
📞 Initiating call to "+919876543210" on Blaze [EARPIECE / NORMAL 📱]...
✅ Phone call dispatched on Blaze for "+919876543210".
💡 Check your phone screen if Android requires manual SIM slot confirmation.
```

### Loud Speakerphone Mode (`--speaker <number>`)
```text
📞 Initiating call to "+919876543210" on Blaze [SPEAKER MODE 🔊]...
✅ Phone call dispatched on Blaze for "+919876543210".
🔊 Hardware volume stream boosted for speakerphone routing.
```

---

## 📜 6. Call History & Logs (`Option 6` / `--logs`)

```text
┌── 📜 CALL HISTORY (Latest 25 - Newest First) ──────────────────────────────────────────────┐
│ 01. 📥 INCOMING │ +919876543210          │ 2026-09-13 21:38:12 │ 02m 45s                   │
│ 02. 📤 OUTGOING │ +919123456789          │ 2026-09-13 19:12:00 │ 05m 12s                   │
│ 03. ❌ MISSED   │ +919988776655          │ 2026-09-13 14:05:22 │ 00m 00s                   │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select Call > _
```

---

## 📡 7. 5G NR Cellular Telemetry & Baseband Hardware (`Options 7 & 8`)

```text
📡 5G / CELLULAR TELEMETRY RADAR
────────────────────────────────────────────────────────────
• Radio Type: NR (5G Standalone) [REGISTERED / ACTIVE]
  └─ mcc: 404
  └─ mnc: 45
  └─ pci: 320
  └─ tac: 18452
  └─ ssRsrp: -85 dBm (Strong 5G Signal)
────────────────────────────────────────────────────────────
```

```text
📱 HARDWARE & SIM TELEPHONY SPECS
────────────────────────────────────────────────────────────
• Operator Name: Jio 5G
• Sim State: Ready
• Network Type: NR (5G)
• Phone Type: GSM / LTE / NR
• Data State: Connected
────────────────────────────────────────────────────────────
```

---

## 📖 8. Command Reference & Fast-Path Switches (`Option 9` / `-h`)

```text
┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-PHONE COMMAND & CLI REFERENCE                 │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-phone (Runs FZF control hub)│
│ • Extract OTP:       blaze-phone --otp                 │
│ • View SMS Inbox:    blaze-phone --sms                 │
│ • Send SMS:          blaze-phone --send-sms <num> <msg>│
│ • Dial Normal Call:  blaze-phone --call <number>       │
│ • Dial Speaker Call: blaze-phone --speaker <number>    │
│ • Search Contacts:   blaze-phone --contacts [query]    │
│ • Call Logs:         blaze-phone --logs                │
│ • 5G Cell Towers:    blaze-phone --cell                │
│ • SIM Hardware:      blaze-phone --device              │
│ • JSON Machine Mode: blaze-phone --json                │
└────────────────────────────────────────────────────────┘
```
