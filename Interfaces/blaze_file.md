# 📂 `blaze-file` — Remote Explorer & Wireless Bridge Interface

> **Command**: `blaze-file`  
> **Source Script**: [`C:\Users\karan\Void\Blaze\scripts\blaze_file.py`](file:///C:/Users/karan/Void/Blaze/scripts/blaze_file.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeFile` (Alias: `blaze-file`)  
> **Local Destination**: Windows Downloads (`C:\Users\karan\Downloads\`)  
> **Remote Roots**: `/sdcard/Download`, `/sdcard/Motobook`, `/sdcard/DCIM`, `/sdcard/Documents`, `~`  
> **Foreground Intent Dispatcher**: Dual-Transport (`adb shell am start` with `termux-open` fallback)

---

## 🖥️ 1. Main Interactive Terminal Menu

When running `blaze-file` without arguments, it launches the interactive inline FZF selector:

```text
┌── 📂 BLAZE WIRELESS FILE BRIDGE & REMOTE EXPLORER ─────────────────────────────────────────┐
│ 📂 1. Browse Remote Blaze Storage  ──► Navigate /sdcard, 1-click pull, open, share & delete│
│ 🚀 2. Drop Local File to Phone     ──► Quick preset picker (Downloads/Desktop) ➔ Blaze     │
│ 📥 3. Quick Pull to PC Downloads   ──► Pull remote file directly into ~/Downloads/         │
│ 📱 4. Launch File on Phone Screen  ──► Open remote file in Android viewer / chooser        │
│ 🌐 5. Open URL in Mobile Browser   ──► Push website link directly to mobile Chrome         │
│ 📤 6. Android Native Share Sheet   ──► Trigger system share modal for file or text         │
│ ⬇️ 7. Queue Android Download       ──► Send URL to background Download Manager             │
│ 📖 8. Help & CLI Reference         ──► Flags, command switches & examples                  │
│ 🚪 0. Exit                         ──► Return to PowerShell terminal                       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze File > _
```

---

## 📂 2. Remote Storage Explorer Submenu (`Option 1` / `--browse`)

### Step 1: Initial Directory Preset Selection
```text
┌── SELECT INITIAL DIRECTORY ────────────────────────────────────────────────────────────────┐
│ 1. 📥 /sdcard/Download/  ──► Downloaded files & PDFs                                       │
│ 2. 💻 /sdcard/Motobook/  ──► Motobook sync folder                                          │
│ 3. 📸 /sdcard/DCIM/      ──► Camera & Photos                                               │
│ 4. 📄 /sdcard/Documents/ ──► Documents folder                                              │
│ 5. 🎵 /sdcard/Music/     ──► Audio tracks                                                  │
│ 6. 🏠 ~/ (Termux Home)   ──► Linux workspace                                               │
│ 7. 📂 /sdcard/ (Root)    ──► Entire internal storage                                       │
│ 0. 🔙 Back to Menu       ──► Cancel                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Directory Preset > _
```

### Step 2: Interactive FZF Directory Listing
```text
┌── 📂 BLAZE EXPLORER: /sdcard/Download (14 items) ──────────────────────────────────────────┐
│ 📁 .. [Parent Directory]                                                                   │
│ 📄 invoice_2026.pdf              │   1.2 MB                                                │
│ 📄 system_architecture.png       │ 842.0 KB                                                │
│ 📄 backup_archive.zip            │  45.3 MB                                                │
│ 📁 Project_Artifacts             │   4.0 KB                                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select File/Folder > _
```

### Step 3: File Action Sheet (Triggered upon selecting any file)
```text
┌── File: /sdcard/Download/invoice_2026.pdf ──────────────────────────────────────────────────┐
│ 📥 1. Pull File to PC Downloads ──► Save directly to ~/Downloads/                          │
│ 📱 2. Open on Phone Screen       ──► Launch in Android default app/chooser                 │
│ 📤 3. Trigger Android Share Sheet ──► Share via WhatsApp, Drive, etc.                      │
│ 📋 4. Copy Remote Path to PC     ──► Copy absolute path to clipboard                       │
│ 🗑️ 5. Delete File on Phone       ──► Remove from Blaze storage                             │
│ 0. 🔙 Back to Directory          ──► Return to file list                                   │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Action on invoice_2026.pdf > _
```

---

## 🚀 3. Local Drop Wizard (`Option 2` / `--drop`)

### Step 1: Source Folder Selection on PC
```text
┌── 🚀 FAST LOCAL FILE DROPPER ──────────────────────────────────────────────────────────────┐
│ 1. 📥 PC Downloads                                                                         │
│ 2. 🖥️ PC Desktop                                                                           │
│ 3. 📄 PC Documents                                                                         │
│ 4. 🎥 PC Videos                                                                            │
│ 5. 📁 Current Directory                                                                    │
│ 6. ⌨️ Enter Custom Local Path                                                              │
│ 0. 🔙 Return to Menu                                                                       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Source Folder > _
```

### Step 2: Local File Selector (Sorted Newest-First)
```text
┌── Files in C:\Users\karan\Downloads (Newest First) ────────────────────────────────────────┐
│ 01. project_report_final.pdf                                                               │
│ 02. screenshot_20260914.png                                                                │
│ 03. firmware_update.bin                                                                    │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select Local File > _
```

### Step 3: Remote Destination Picker
```text
┌── Drop: project_report_final.pdf ──────────────────────────────────────────────────────────┐
│ 1. 📥 /sdcard/Download/     ──► Default Android downloads directory                        │
│ 2. 💻 /sdcard/Motobook/     ──► Dedicated Motobook sync folder                             │
│ 3. 📄 /sdcard/Documents/    ──► Android Documents folder                                   │
│ 4. 📸 /sdcard/DCIM/         ──► Camera & Photos gallery                                    │
│ 5. 🎵 /sdcard/Music/        ──► Audio tracks & music player                                │
│ 6. 🏠 ~/ (Termux Home)      ──► Linux CLI workspace                                        │
│ 0. 🔙 Cancel                ──► Abort drop                                                 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Drop Destination > _
```

### Step 4: Drop Execution & Android MediaScan Confirmation
```text
🚀 Dropping 'project_report_final.pdf' ➔ Blaze:/sdcard/Download/...

✅ FILE DROPPED TO BLAZE SUCCESSFULLY!
┌────────────────────────────────────────────────────────┐
│ 📁 File Name:    project_report_final.pdf              │
│ 📂 Destination:  /sdcard/Download/project_report_final.pdf│
│ 📲 Android Index: MediaStore Scanned & Indexed         │
└────────────────────────────────────────────────────────┘
📱 Visible in Android Files, Gallery & media players.
[Android Screen Notification Pop-up: 📥 Received: project_report_final.pdf]
```

---

## 📥 4. Pull to PC Downloads Confirmation (`Option 3` / `--pull`)

```text
📥 Pulling Blaze:/sdcard/Download/invoice_2026.pdf ➔ PC:C:\Users\karan\Downloads...

✅ FILE PULLED TO PC DOWNLOADS SUCCESSFULLY!
┌────────────────────────────────────────────────────────┐
│ 📁 File Name:    invoice_2026.pdf                      │
│ 📂 Saved In:     C:\Users\karan\Downloads\invoice_2026.pdf│
└────────────────────────────────────────────────────────┘
💻 Available in your PC Downloads folder.
```

---

## 📱 5. Foreground Intent Launchers (`Options 4 & 5`)

### File Open on Screen (`--open`)
- **Primary Transport**: `adb shell am start -a android.intent.action.VIEW -d "file:///sdcard/Download/..." -t "<mime-type>"`
- **Fallback Transport**: `ssh blaze "termux-open --chooser '/sdcard/Download/...'"`
```text
📱 Opening 'invoice_2026.pdf' on Blaze screen...
✅ App launched on Blaze screen via ADB for 'invoice_2026.pdf' (application/pdf).
[Android Screen Notification Pop-up: 📂 Opened: invoice_2026.pdf]
```

### URL Open in Mobile Browser (`--url`)
- **Primary Transport**: `adb shell am start -a android.intent.action.VIEW -d "https://..."`
- **Fallback Transport**: `ssh blaze "termux-open-url 'https://...'"`
```text
🌐 Opening 'https://github.com' on Blaze screen...
✅ Browser launched on Blaze screen via ADB for 'https://github.com'.
[Android Screen Notification Pop-up: 🌐 Opened URL]
```

---

## 📖 6. Help & CLI Reference Screen (`Option 8` / `-h` / `--help`)

```text
┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-FILE COMMAND & CLI REFERENCE                  │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-file                        │
│ • Drop Local File:   blaze-file --drop <local_path>    │
│ • Pull Remote File:  blaze-file --pull <remote_path>   │
│ • Browse Storage:    blaze-file --browse [dir]         │
│ • Open on Phone:     blaze-file --open <remote_path>   │
│ • Open Mobile URL:   blaze-file --url <url>            │
│ • Share Sheet:       blaze-file --share <path|text>    │
│ • Download URL:      blaze-file --download <url>       │
│ • JSON Machine Mode: blaze-file --json                 │
└────────────────────────────────────────────────────────┘
```
