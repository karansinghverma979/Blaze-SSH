# 🎙️ `blaze-speak` — Studio HD Neural Voice Synthesis & Assistant Speech Interface

> **Command**: `blaze-speak`  
> **Source Script**: [`scripts/blaze_speak.py`](file:///scripts/blaze_speak.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeTTS` (Alias: `blaze-speak`)  
> **Voice Engines**: Microsoft Edge-TTS Cloud Neural + Google Assistant TTS (`gTTS`) + Offline Android TTS  
> **Audio Delivery**: SSH SCP + Blaze OpenSL ES Hardware Engine (`mpv --ao=opensles --volume=140`)  
> **Permanent Configuration**: `~/.config/blaze_default_voice.txt`

---

## 🖥️ 1. Main Interactive Voice Center Menu

When running `blaze-speak` from PowerShell without arguments, it launches the interactive inline FZF Voice Center:

```text
┌── 🎙️ BLAZE STUDIO HD VOICE SYNTHESIS COMMAND CENTER ────────────────────────────────────────┐
│ 💬 1. Live Voice Chat Console    ──► Real-time voice conversation REPL                     │
│ 🎭 2. Voice Persona Explorer     ──► Preview & test 20 Studio HD personas                  │
│ ⭐ 3. Set Permanent Default Voice──► Current Default: [ava]                                │
│ 📋 4. Read Clipboard Out Loud    ──► Speak contents of Windows clipboard                   │
│ 🔋 5. Spoken Telemetry Briefing  ──► Speak live battery % & network status                 │
│ 🚨 6. Emergency Siren Alert      ──► Loud alert siren bypassing silent mode                │
│ 📖 7. Help & CLI Reference       ──► Standard Linux manual, flags & examples               │
│ 🚪 0. Exit                       ──► Return to PowerShell terminal                         │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Blaze Voice > _
```

---

## 💬 2. Live Voice Chat REPL (`Option 1`)

An interactive conversational voice console that synthesizes your typed messages directly onto Blaze hardware in real time:

```text
💬 Voice Chat REPL started (Active Voice: ava)
💡 Type anything to speak on Blaze.
💡 Shortcuts: /voice, /default, /status, /clip, /alert, /menu, /exit

[ava] > Greetings Karan, all systems operational.
🎙️ Speaking: "Greetings Karan, all systems operational." [ava]

[ava] > /voice
```

### In-REPL Voice Switcher (`/voice`)
```text
┌── Choose REPL Voice Persona ───────────────────────────────────────────────────────────────┐
│ google-in    │ Google Assistant (Indian English) [Online 🌐]                               │
│ google-hi    │ Google Assistant (Hindi) [Online 🌐]                                        │
│ ava          │ Ava (US Female - Natural & Expressive) [Online 🌐]                          │
│ brian        │ Brian (US Male - Clear & Authoritative) [Online 🌐]                         │
│ neerja       │ Neerja (Indian English Female - Expressive) [Online 🌐]                     │
│ jarvis       │ Jarvis / Prabhat (Indian English Male - Assistant) [Online 🌐]              │
│ swara        │ Swara (Hindi Female - Expressive) [Online 🌐]                               │
│ madhur       │ Madhur (Hindi Male - Clear) [Online 🌐]                                     │
│ maisie       │ Maisie (British Female - Crisp) [Online 🌐]                                 │
│ andrew       │ Andrew (US Male - Warm) [Online 🌐]                                         │
│ emma         │ Emma (US Female - Cheerful) [Online 🌐]                                     │
│ jenny        │ Jenny (US Female - Friendly) [Online 🌐]                                    │
│ aria         │ Aria (US Female - Balanced) [Online 🌐]                                     │
│ sonia        │ Sonia (British Female - Formal) [Online 🌐]                                 │
│ libby        │ Libby (British Female - Casual) [Online 🌐]                                 │
│ natasha      │ Natasha (Australian Female) [Online 🌐]                                     │
│ clara        │ Clara (Canadian Female) [Online 🌐]                                         │
│ emily        │ Emily (Irish Female) [Online 🌐]                                            │
│ native       │ Native Android TTS (Built-in Device Voice) [Offline ⚡]                      │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Select Voice > _
```

```text
⭐ Switched active voice to: jarvis

[jarvis] > Commencing security patrol on perimeter.
🎙️ Speaking: "Commencing security patrol on perimeter." [jarvis]
```

### In-REPL Actions Sheet (`/menu` or `/help`)
```text
┌── Live Voice Chat In-Session Actions Menu ─────────────────────────────────────────────────┐
│ 🎙️  1. Switch Active Voice Persona (Current: jarvis)   │ switch_voice                      │
│ ⭐  2. Set Active Voice (jarvis) as Permanent Default   │ set_default                       │
│ 📊  3. Spoken System Telemetry & Battery Briefing      │ briefing                          │
│ 📋  4. Read Windows Clipboard Out Loud                 │ clipboard                         │
│ 🚨  5. Trigger High-Priority Emergency Siren           │ siren                             │
│ 🔙  6. Resume Voice Chat REPL                          │ resume                            │
│ 🚪  7. Exit Chat to Main Hub Menu                      │ exit                              │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Chat Actions > _
```

---

## 🎭 3. Voice Persona Explorer (`Option 2`)

Test and preview all 20 neural voices with studio sample text:

```text
┌── Select Persona to Preview Speech ────────────────────────────────────────────────────────┐
│ ava          │ Ava (US Female - Natural & Expressive) [Online 🌐]                          │
│ jarvis       │ Jarvis / Prabhat (Indian English Male - Assistant) [Online 🌐]              │
│ neerja       │ Neerja (Indian English Female - Expressive) [Online 🌐]                     │
│ swara        │ Swara (Hindi Female - Expressive) [Online 🌐]                               │
│ maisie       │ Maisie (British Female - Crisp) [Online 🌐]                                 │
│ 🔙 [Back to Main Menu]                                                                     │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Test Voice > _
```

```text
▶ Previewing voice: jarvis (Jarvis / Prabhat (Indian English Male - Assistant) [Online 🌐])...
🎙️ Speaking: "Greetings Karan! Antigravity executive assistant systems are..." [jarvis]
```

---

## ⭐ 4. Permanent Default Voice Setting (`Option 3` / `/default`)

Allows locking a permanent default voice persona that persists across reboots, PowerShell sessions, and CLI switches:

```text
┌── Current Default Voice: ava ──────────────────────────────────────────────────────────────┐
│ ava          │ Ava (US Female - Natural & Expressive) [Online 🌐]                          │
│ jarvis       │ Jarvis / Prabhat (Indian English Male - Assistant) [Online 🌐]              │
│ neerja       │ Neerja (Indian English Female - Expressive) [Online 🌐]                     │
│ swara        │ Swara (Hindi Female - Expressive) [Online 🌐]                               │
│ 🔙 [Cancel]                                                                                │
└────────────────────────────────────────────────────────────────────────────────────────────┘
Set Default > _
```

```text
⭐ Default assistant voice set to: jarvis (Jarvis / Prabhat (Indian English Male - Assistant) [Online 🌐])
🎙️ Speaking: "Voice persona jarvis set as default assistant voice." [jarvis]
```

---

## 📋 5. Read Clipboard Out Loud (`Option 4` / `--clip`)

Reads your active Windows clipboard text aloud through phone speakers:

```text
📋 Reading clipboard (142 characters)...
🎙️ Speaking: "The architecture review is complete. All 10 Blaze CLI hubs..." [jarvis]
```

---

## 🔋 6. Spoken Telemetry & Battery Briefing (`Option 5` / `--status`)

Fetches live device health telemetry and synthesizes an executive voice report:

```text
🔄 Fetching status from Blaze for spoken briefing...
🎙️ Speaking: "Sir, Blaze node telemetry report: Battery level is at 88 percent and currently discharging. Temperature is 31.4 degrees Celsius. All systems optimal." [jarvis]
```

---

## 🚨 7. Emergency Siren Alert (`Option 6` / `--alert`)

Overrides Android silent/vibrate mode, maxes out all volume streams to 15, engages haptic motor, pops high-priority toast, and speaks an alert warning in the configured default voice:

```text
🚨 Triggering high-priority emergency siren on Blaze...
🎙️ Speaking: "Warning! Critical high-priority mission alert!" [jarvis]
[Android Screen Notification Pop-up: 🚨 CRITICAL EMERGENCY ALERT]
```

---

## 📖 8. Linux-Standard Help Manual (`Option 7` / `-h` / `--help`)

```text
NAME
       blaze-speak - Studio HD Voice Synthesis & Assistant Speech Hub

SYNOPSIS
       blaze-speak [OPTIONS] [TEXT]

DESCRIPTION
       High-definition neural voice synthesis engine streaming cloud-grade
       Microsoft Edge-TTS and Google Assistant voices directly over SSH
       to Lava Blaze 5G OpenSL ES audio output with volume boost.
       Features 20 diverse personas, interactive voice chat REPL,
       live telemetry spoken briefings, and clipboard reading.

OPTIONS
       -h, --help
              Display this standard Linux manual page and exit.

       [TEXT]
              Spoken text sentence or message to synthesize.

       -v, --voice <PERSONA>
              Choose voice persona (e.g. ava, swara, neerja, brian, jarvis, maisie).

       --clip
              Read current Windows or phone clipboard content out loud.

       --status
              Speak live battery percentage and network connection briefing.

       --alert
              Trigger loud emergency alert siren on phone.

       --native
              Fallback to Termux offline local TTS speech engine.

POPULAR PERSONAS
       • ava     : US English (Female, warm & natural)
       • brian   : US English (Male, authoritative)
       • neerja  : Indian English (Female, crisp & clear)
       • jarvis  : Indian English (Male, Prabhat Neural)
       • swara   : Hindi (Female, expressive)
       • maisie  : British English (Female)

EXAMPLES
       blaze-speak
              Launch interactive Voice Center (Live Chat REPL, Persona tester).

       blaze-speak "System build complete and verified"
              Speak using default configured persona.

       blaze-speak "Mission objective reached" -v jarvis
              Speak using Jarvis Indian English neural voice.

       blaze-speak --clip
              Read clipboard out loud.

       blaze-speak --status
              Speak spoken battery and connectivity briefing.
```
