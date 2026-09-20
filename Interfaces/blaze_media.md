# 🎵 `blaze-media` — Hierarchical Audio Explorer, Playback Engine & Sound Master Interface

> **Command**: `blaze-media`  
> **Source Script**: [`scripts/blaze_media.py`](file:///scripts/blaze_media.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeMedia` (Alias: `blaze-media`)  
> **Supported Formats**: `.mp3`, `.m4a`, `.wav`, `.flac`, `.aac`, `.ogg`, `.opus`, `.m4b`, `.mid`  
> **Audio Transports**: Termux Media Player Engine + Scrcpy Opus Streaming to PC Speakers  
> **Hardware Governors**: 6-Channel Android Volume Master + Haptic Vibrator + Android MediaStore Scanner

---

## 🖥️ 1. Main Interactive Terminal Menu

When executing `blaze-media` from PowerShell without arguments, it launches the full interactive inline FZF audio suite:

```text
┌── 🎵 BLAZE AUDIO BROWSER & MEDIA COMMAND HUB ──────────────────────────────────────────────┐
│ 📁 1. Hierarchical Audio Explorer   ──► Browse folders, 1-click play, stream & pull (FZF)  │
│ 📻 2. Media Playback Radar         ──► Real-time track, position & progress bar           │
│ ⏸️ 3. Pause Audio Playback          ──► Pause currently playing track                      │
│ ▶️ 4. Resume Audio Playback         ──► Resume playback                                    │
│ ⏹️ 5. Stop Audio Playback           ──► Stop and release media engine                      │
│ 🔊 6. Volume Master Console         ──► Set hardware volume for Music, Ring, Alarm, Call   │
│ 🗣️ 7. Text-to-Speech (TTS Engine)   ──► Speak arbitrary text aloud on phone speakers       │
│ 📳 8. Haptic Vibration Pulse        ──► Trigger vibration pulse on phone motor             │
│ 🔄 9. Re-index Android MediaStore   ──► Refresh gallery & music player library             │
│ 📖 10. Help & CLI Reference         ──► Flags, command switches & examples                 │
│ 🚪 0. Exit                         ──► Return to PowerShell terminal                       │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze Media > _
```

---

## 📁 2. Hierarchical Audio Explorer (`Option 1` / `--browse`)

### Step 1: Initial Music Folder Preset Selection
```text
┌── SELECT INITIAL AUDIO DIRECTORY ──────────────────────────────────────────────────────────┐
│ 1. 🎵 /sdcard/Music/     ──► Primary music collection                                      │
│ 2. 📥 /sdcard/Download/  ──► Downloaded audio & voice notes                                │
│ 3. 💻 /sdcard/Motobook/  ──► Motobook sync folder                                          │
│ 4. 📂 /sdcard/ (Root)    ──► Entire storage directory                                      │
│ 0. 🔙 Back to Menu       ──► Cancel                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Music Folder > _
```

### Step 2: Interactive FZF Track & Folder Navigator
```text
┌── 🎵 AUDIO EXPLORER: /sdcard/Music (18 items) ─────────────────────────────────────────────┐
│ 📁 .. [Parent Directory]                                                                   │
│ 🎵 Nightfall_Cyberpunk_Synth.mp3 │   8.4 MB                                                │
│ 🎵 Morning_Meditation_Flac.flac  │  24.1 MB                                                │
│ 🎵 Acoustic_Guitar_Session.m4a   │   4.2 MB                                                │
│ 📁 LoFi_Beats_Collection         │   4.0 KB                                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select Track/Folder > _
```

### Step 3: Track Action Sheet (Triggered on selecting any audio file)
```text
┌── Track: Nightfall_Cyberpunk_Synth.mp3 ────────────────────────────────────────────────────┐
│ ▶️ 1. Play on Phone Speakers    ──► Play 'Nightfall_Cyberpunk_Synth.mp3' via Termux Media   │
│ 🔊 2. Stream to PC (Scrcpy Audio) ──► Stream phone sound to PC speakers                    │
│ 📥 3. Pull Track to PC Downloads ──► Save copy directly to ~/Downloads/                    │
│ 📱 4. Open in Android App/Chooser──► Launch in VLC, Spotify or system player               │
│ 📋 5. Copy Track Remote Path     ──► Copy path to Windows clipboard                        │
│ 🗑️ 6. Delete Audio File          ──► Remove track from phone                               │
│ 0. 🔙 Back to Folder              ──► Return to audio list                                 │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Action on Nightfall_Cyberpunk_Synth.mp3 > _
```

---

## 📻 3. Playback Engine & Real-Time Radar (`Option 2` / `--info`)

### When Audio is Playing on Blaze:
```text
🎵 BLAZE AUDIO PLAYBACK RADAR
┌────────────────────────────────────────────────────────┐
│ 📻 State:     PLAYING                                  │
│ 🎶 Track:     Nightfall_Cyberpunk_Synth.mp3            │
│ ⏱️ Progress:  [████████░░░░░░░] 02:15 / 04:30           │
└────────────────────────────────────────────────────────┘
```

### When Media Engine is Idle:
```text
⚠️ No active audio track currently playing on Blaze.
```

---

## 🔊 4. Volume Master Console (`Option 6` / `--volume`)

### Step 1: Hardware Audio Stream Selector
```text
┌── 🔊 VOLUME MASTER CONSOLE ────────────────────────────────────────────────────────────────┐
│ 1. 🎵 Music & Media Stream     ──► Background audio, Spotify & video sound                 │
│ 2. 🔔 Ringtone Stream          ──► Incoming call ring volume                               │
│ 3. 💬 Notification Alerts      ──► SMS, messages & app alert chimes                        │
│ 4. ⏰ Alarm Clock Stream       ──► Morning alarms & timer sounds                           │
│ 5. ⚙️ System Sounds            ──► Keypad clicks & touch tones                             │
│ 6. 📞 Voice Call In-Ear        ──► Earpiece volume during phone calls                      │
│ 0. 🔙 Return to Menu           ──► Cancel                                                  │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Audio Stream > _
```

### Step 2: Stream Volume Slider Presets
```text
Set MUSIC Volume > 
1. 🔇 Mute (0/15)
2. 🔉 Low (2/15)
3. 🔉 Moderate (5/15)
4. 🔊 Balanced (7/15)
5. 🔊 High (12/15)
6. 📢 Maximum (15/15)
7. ⌨️ Enter Custom Level
0. 🔙 Cancel
```

### Screen Confirmation Card:
```text
✅ Volume updated [MUSIC]: [████████████░░░] (12/15)
[Android Screen Notification Pop-up: 🔊 Music Volume: 12/15]
```

---

## 🎧 5. Direct Streaming to PC Speakers (`Scrcpy Audio Stream`)

When selecting `Stream to PC (Scrcpy Audio)`:
```text
▶️ Starting playback on Blaze: 'Nightfall_Cyberpunk_Synth.mp3'...

✅ AUDIO PLAYBACK STARTED ON BLAZE!
┌────────────────────────────────────────────────────────┐
│ 🎶 Track:    Nightfall_Cyberpunk_Synth.mp3             │
│ 📂 Path:     /sdcard/Music/Nightfall_Cyberpunk_Synth.mp3│
└────────────────────────────────────────────────────────┘

🔊 Launching Scrcpy Audio Stream to Motobook Speakers (Opus Codec)...
✅ Audio stream active. (Sound routed wirelessly to PC headphones/speakers with ultra-low latency)
```

---

## 🗣️ 6. Text-to-Speech & Haptic Studio (`Options 7 & 8`)

### Spoken TTS Synthesizer (`--speak`)
```text
Enter text to speak on Blaze: Antigravity audio engine verified.
🗣️ Speaking on Blaze: "Antigravity audio engine verified."...
✅ Speech synthesized on phone speakers.
```

### Haptic Vibration Pulse (`--vibrate`)
```text
Enter vibration duration in ms [default: 500]: 800
📳 Phone vibrated (800ms).
```

---

## 🔄 7. Android MediaStore Sync (`Option 9` / `--scan`)

```text
🔄 Refreshing Android MediaStore on '/sdcard/Music'...
✅ MediaStore re-indexed! Audio tracks are visible in all players.
[Android Screen Notification Pop-up: 🔄 MediaStore Refreshed]
```

---

## 📖 8. Help & CLI Reference Screen (`Option 10` / `-h` / `--help`)

```text
┌────────────────────────────────────────────────────────┐
│ 📖 BLAZE-MEDIA COMMAND & CLI REFERENCE                 │
├────────────────────────────────────────────────────────┤
│ • Interactive Hub:   blaze-media                       │
│ • Play Audio Track:  blaze-media --play <path>         │
│ • Pause Playback:    blaze-media --pause               │
│ • Resume Playback:   blaze-media --resume              │
│ • Stop Playback:     blaze-media --stop                │
│ • Playback Radar:    blaze-media --info                │
│ • Set Volume:        blaze-media --volume <0-15>       │
│ • Browse Audio:      blaze-media --browse [dir]        │
│ • Speak Text (TTS):  blaze-media --speak "<text>"      │
│ • Vibrate Motor:     blaze-media --vibrate [ms]        │
│ • Sync MediaStore:   blaze-media --scan [path]         │
│ • JSON Machine Mode: blaze-media --json                │
└────────────────────────────────────────────────────────┘
```
