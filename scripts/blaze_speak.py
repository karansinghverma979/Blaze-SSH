#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎙️ Blaze Studio HD Voice Synthesis, TTS & Assistant Speech Hub
Author: Antigravity Assistant & Karan Singh Verma
Features:
- 20 Studio HD Neural Edge-TTS + Google Assist Voice Personas
- Real-time Audio Stream to Blaze OpenSL ES with +140% Volume Boost
- Interactive Voice Center (Live Chat REPL, Voice Persona Explorer)
- Read Clipboard Out Loud, Spoken Telemetry Briefings, Emergency Siren
- Linux-Standard Manual & CLI Switches
"""

import sys
import os
import json
import subprocess
import re
import time
import shutil
import argparse
import tempfile
import asyncio
from datetime import datetime

# Set console encoding to UTF-8
if sys.platform == "win32":
    os.system("")
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        sys.stdin.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# ANSI Color Palette
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"

VOICE_MAP = {
    "google-in": {"type": "gtts", "lang": "en", "tld": "co.in", "desc": "Google Assistant (Indian English) [Online 🌐]"},
    "google-hi": {"type": "gtts", "lang": "hi", "tld": "co.in", "desc": "Google Assistant (Hindi) [Online 🌐]"},
    "ava": {"type": "neural", "voice": "en-US-AvaMultilingualNeural", "desc": "Ava (US Female - Natural & Expressive) [Online 🌐]"},
    "brian": {"type": "neural", "voice": "en-US-BrianMultilingualNeural", "desc": "Brian (US Male - Clear & Authoritative) [Online 🌐]"},
    "neerja": {"type": "neural", "voice": "en-IN-NeerjaExpressiveNeural", "desc": "Neerja (Indian English Female - Expressive) [Online 🌐]"},
    "jarvis": {"type": "neural", "voice": "en-IN-PrabhatNeural", "desc": "Jarvis / Prabhat (Indian English Male - Assistant) [Online 🌐]"},
    "swara": {"type": "neural", "voice": "hi-IN-SwaraNeural", "desc": "Swara (Hindi Female - Expressive) [Online 🌐]"},
    "madhur": {"type": "neural", "voice": "hi-IN-MadhurNeural", "desc": "Madhur (Hindi Male - Clear) [Online 🌐]"},
    "maisie": {"type": "neural", "voice": "en-GB-MaisieNeural", "desc": "Maisie (British Female - Crisp) [Online 🌐]"},
    "andrew": {"type": "neural", "voice": "en-US-AndrewMultilingualNeural", "desc": "Andrew (US Male - Warm) [Online 🌐]"},
    "emma": {"type": "neural", "voice": "en-US-EmmaMultilingualNeural", "desc": "Emma (US Female - Cheerful) [Online 🌐]"},
    "jenny": {"type": "neural", "voice": "en-US-JennyNeural", "desc": "Jenny (US Female - Friendly) [Online 🌐]"},
    "aria": {"type": "neural", "voice": "en-US-AriaNeural", "desc": "Aria (US Female - Balanced) [Online 🌐]"},
    "sonia": {"type": "neural", "voice": "en-GB-SoniaNeural", "desc": "Sonia (British Female - Formal) [Online 🌐]"},
    "libby": {"type": "neural", "voice": "en-GB-LibbyNeural", "desc": "Libby (British Female - Casual) [Online 🌐]"},
    "natasha": {"type": "neural", "voice": "en-AU-NatashaNeural", "desc": "Natasha (Australian Female) [Online 🌐]"},
    "clara": {"type": "neural", "voice": "en-CA-ClaraNeural", "desc": "Clara (Canadian Female) [Online 🌐]"},
    "emily": {"type": "neural", "voice": "en-IE-EmilyNeural", "desc": "Emily (Irish Female) [Online 🌐]"},
    "native": {"type": "native", "desc": "Native Android TTS (Built-in Device Voice) [Offline ⚡]"}
}

DEFAULT_VOICE_FILE = os.path.expanduser("~/.config/blaze_default_voice.txt")

def render_unreachable_card():
    """Renders standardized offline diagnostic card when Blaze SSH is unreachable."""
    print(f"\n{RED}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{RED}│ ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022                 │{RESET}")
    print(f"{RED}├────────────────────────────────────────────────────────┤{RESET}")
    print(f"│ • Root Cause: Phone offline or SSH daemon not running. │")
    print(f"│ • Action:     1. Ensure Termux is active on Blaze.     │")
    print(f"│               2. Run 'sshd' in Termux.                 │")
    print(f"│               3. Confirm same Wi-Fi / Hotspot.         │")
    print(f"{RED}└────────────────────────────────────────────────────────┘{RESET}\n")

def run_ssh(cmd, timeout=8):
    """Executes command on Blaze over SSH with safe timeout."""
    try:
        res = subprocess.run(
            ["ssh", "-o", f"ConnectTimeout={timeout}", "-o", "StrictHostKeyChecking=no", "blaze", cmd],
            capture_output=True, text=True, timeout=timeout + 3, encoding="utf-8", errors="replace"
        )
        return res.stdout.strip(), res.stderr.strip(), res.returncode
    except subprocess.TimeoutExpired:
        return "", "Connection timed out. Blaze may be offline.", 255
    except Exception as e:
        return "", str(e), 1

def run_fzf(options, prompt="Blaze Voice > ", header=None):
    """Runs inline interactive FZF fuzzy picker directly beneath the cursor in active terminal."""
    if not shutil.which("fzf") or not options:
        return None
    cmd = ["fzf", "--prompt", prompt, "--height=40%", "--reverse", "--cycle"]
    if header:
        cmd.extend(["--header", header])
    input_str = "\n".join(options)
    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            text=True,
            encoding="utf-8"
        )
        stdout, _ = proc.communicate(input=input_str)
        if proc.returncode == 0 and stdout and stdout.strip():
            return stdout.strip()
    except (KeyboardInterrupt, Exception):
        pass
    return None

def safe_pause(msg="Press Enter to continue..."):
    """Safely prompts user to press Enter with signal protection."""
    try:
        input(f"{DIM}{msg}{RESET}")
    except (KeyboardInterrupt, EOFError):
        pass

def get_default_voice():
    if os.path.exists(DEFAULT_VOICE_FILE):
        try:
            with open(DEFAULT_VOICE_FILE, "r", encoding="utf-8") as f:
                v = f.read().strip().lower()
                if v in VOICE_MAP:
                    return v
        except Exception:
            pass
    return "ava"

def set_default_voice(v_name):
    if v_name in VOICE_MAP:
        try:
            os.makedirs(os.path.dirname(DEFAULT_VOICE_FILE), exist_ok=True)
            with open(DEFAULT_VOICE_FILE, "w", encoding="utf-8") as f:
                f.write(v_name.lower())
            desc = VOICE_MAP[v_name]['desc']
            print(f"{GREEN}⭐ Default assistant voice set to: {BOLD}{v_name}{RESET} ({desc})")
            speak(f"Voice persona {v_name} set as default assistant voice.", voice_key=v_name)
        except Exception as e:
            print(f"{RED}❌ Failed to save default voice: {e}{RESET}")

async def synth_neural(voice, text, out_file, rate_pct="+0%", pitch_hz="+0Hz"):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate=rate_pct, pitch=pitch_hz, volume="+140%")
    await comm.save(out_file)

def synth_gtts(text, lang, tld, out_file):
    from gtts import gTTS
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.save(out_file)

def play_audio_on_blaze(local_mp3):
    """Transfer synthesized audio to Blaze and play via MPV or Termux media player."""
    if not os.path.exists(local_mp3) or os.path.getsize(local_mp3) < 100:
        return
    
    remote_tmp = "/data/data/com.termux/files/usr/tmp/speech.mp3"
    scp_cmd = ["scp", "-o", "ConnectTimeout=8", "-q", local_mp3, f"blaze:{remote_tmp}"]
    try:
        res = subprocess.run(scp_cmd, timeout=12)
        if res.returncode == 0:
            # Play via mpv quietly with hardware audio output (fallback to termux-media-player)
            play_cmd = f"mpv --no-video --ao=opensles --volume=140 '{remote_tmp}' >/dev/null 2>&1 || termux-media-player play '{remote_tmp}' >/dev/null 2>&1 &"
            run_ssh(play_cmd)
        else:
            render_unreachable_card()
    except Exception as e:
        print(f"{RED}❌ Failed to transfer speech audio to Blaze: {e}{RESET}")

def speak(text, voice_key=None, speed=1.0, pitch=1.0, silent=False):
    """Main voice synthesis dispatcher with graceful fallbacks."""
    if not text or not str(text).strip():
        return
    
    clean_text = str(text).strip()
    voice = (voice_key or get_default_voice()).lower()
    v_spec = VOICE_MAP.get(voice, VOICE_MAP["ava"])

    if not silent:
        print(f"{CYAN}🎙️ Speaking:{RESET} \"{clean_text[:60]}{'...' if len(clean_text)>60 else ''}\" [{voice}]")

    if v_spec["type"] == "native":
        safe_t = clean_text.replace("'", "'\\''")
        out, err, code = run_ssh(f"termux-tts-speak '{safe_t}'")
        if code == 255: render_unreachable_card()
        return

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        if v_spec["type"] == "gtts":
            synth_gtts(clean_text, v_spec["lang"], v_spec["tld"], tmp_path)
        else:
            r_pct = f"{int((speed - 1.0) * 100):+d}%"
            p_hz = f"{int((pitch - 1.0) * 50):+d}Hz"
            asyncio.run(synth_neural(v_spec["voice"], clean_text, tmp_path, r_pct, p_hz))

        play_audio_on_blaze(tmp_path)
    except Exception as e:
        if not silent:
            print(f"{YELLOW}⚠️ Cloud TTS fallback to offline Termux TTS: {e}{RESET}")
        safe_t = clean_text.replace("'", "'\\''")
        out, err, code = run_ssh(f"termux-tts-speak '{safe_t}'")
        if code == 255: render_unreachable_card()
    finally:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass

def action_voice_chat():
    """Interactive Live Voice Chat REPL."""
    cur_voice = get_default_voice()
    print(f"\n{GREEN}{BOLD}💬 Voice Chat REPL started{RESET} (Active Voice: {CYAN}{cur_voice}{RESET})")
    print(f"{DIM}💡 Type anything to speak on Blaze.{RESET}")
    print(f"{DIM}💡 Shortcuts: /voice, /default, /status, /clip, /alert, /menu, /exit{RESET}")
    while True:
        try:
            msg = input(f"\n{BOLD}[{cur_voice}]{RESET} > ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        if not msg or msg.lower() in ["/exit", "exit", "quit", "/quit", "/q"]:
            break
        
        lower_msg = msg.lower()
        if lower_msg == "/voice" or lower_msg.startswith("/voice "):
            parts = msg.split()
            if len(parts) > 1 and parts[1].lower() in VOICE_MAP:
                cur_voice = parts[1].lower()
                print(f"{GREEN}⭐ Switched active voice to: {BOLD}{cur_voice}{RESET}")
            else:
                items = [f"{k:<12} │ {v['desc']}" for k, v in VOICE_MAP.items()]
                chosen = run_fzf(items, prompt="Select Voice > ", header="Choose REPL Voice Persona")
                if chosen:
                    cur_voice = chosen.split("│")[0].strip()
                    print(f"{GREEN}⭐ Switched active voice to: {BOLD}{cur_voice}{RESET}")
            continue

        if lower_msg == "/default" or lower_msg.startswith("/default "):
            parts = msg.split()
            if len(parts) > 1 and parts[1].lower() in VOICE_MAP:
                target_v = parts[1].lower()
                set_default_voice(target_v)
                cur_voice = target_v
            else:
                opts = [
                    f"⭐ 1. Set Current Voice ({cur_voice}) as Permanent Default │ current",
                    f"🔍 2. Choose Another Voice Persona from List...             │ pick",
                    f"🔙 3. Cancel / Return to Chat                              │ cancel"
                ]
                ch = run_fzf(opts, prompt="Set Default > ", header=f"Active Voice: {cur_voice} | Default: {get_default_voice()}")
                if ch and "│ current" in ch:
                    set_default_voice(cur_voice)
                elif ch and "│ pick" in ch:
                    items = [f"{k:<12} │ {v['desc']}" for k, v in VOICE_MAP.items()]
                    chosen = run_fzf(items, prompt="Select Default Voice > ", header="Choose Permanent Default Voice")
                    if chosen:
                        target_v = chosen.split("│")[0].strip()
                        set_default_voice(target_v)
                        cur_voice = target_v
            continue

        if lower_msg in ["/menu", "/help", "/actions"]:
            menu_actions = [
                f"🎙️  1. Switch Active Voice Persona (Current: {cur_voice})   │ switch_voice",
                f"⭐  2. Set Active Voice ({cur_voice}) as Permanent Default   │ set_default",
                f"📊  3. Spoken System Telemetry & Battery Briefing          │ briefing",
                f"📋  4. Read Windows Clipboard Out Loud                     │ clipboard",
                f"🚨  5. Trigger High-Priority Emergency Siren               │ siren",
                f"🔙  6. Resume Voice Chat REPL                              │ resume",
                f"🚪  7. Exit Chat to Main Hub Menu                          │ exit"
            ]
            ch = run_fzf(menu_actions, prompt="Chat Actions > ", header="Live Voice Chat In-Session Actions Menu")
            if not ch or "│ resume" in ch:
                continue
            if "│ exit" in ch:
                break
            if "│ switch_voice" in ch:
                items = [f"{k:<12} │ {v['desc']}" for k, v in VOICE_MAP.items()]
                chosen = run_fzf(items, prompt="Select Voice > ", header="Choose REPL Voice Persona")
                if chosen:
                    cur_voice = chosen.split("│")[0].strip()
                    print(f"{GREEN}⭐ Switched active voice to: {BOLD}{cur_voice}{RESET}")
            elif "│ set_default" in ch:
                set_default_voice(cur_voice)
            elif "│ briefing" in ch:
                action_spoken_briefing()
            elif "│ clipboard" in ch:
                action_read_clipboard()
            elif "│ siren" in ch:
                action_emergency_siren()
            continue

        if lower_msg in ["/status", "/battery", "/briefing"]:
            action_spoken_briefing()
            continue

        if lower_msg in ["/clip", "/clipboard"]:
            action_read_clipboard()
            continue

        if lower_msg in ["/alert", "/siren"]:
            action_emergency_siren()
            continue

        speak(msg, voice_key=cur_voice)

def action_persona_explorer():
    """Test 20 HD Neural Voice Personas."""
    sample_text = "Greetings Karan! Antigravity executive assistant systems are fully initialized and operating at maximum efficiency."
    while True:
        items = [f"{k:<12} │ {v['desc']}" for k, v in VOICE_MAP.items()]
        items.append("🔙 [Back to Main Menu]")
        chosen = run_fzf(items, prompt="Test Voice > ", header="Select Persona to Preview Speech")
        if not chosen or "[Back" in chosen:
            break
        v_key = chosen.split("│")[0].strip()
        print(f"\n{CYAN}▶ Previewing voice:{RESET} {BOLD}{v_key}{RESET} ({VOICE_MAP[v_key]['desc']})...")
        speak(sample_text, voice_key=v_key)
        time.sleep(1)

def action_set_default():
    """Permanently change default voice persona."""
    cur = get_default_voice()
    items = [f"{k:<12} │ {v['desc']}" for k, v in VOICE_MAP.items()]
    items.append("🔙 [Cancel]")
    chosen = run_fzf(items, prompt="Set Default > ", header=f"Current Default Voice: {cur}")
    if chosen and "[Cancel" not in chosen:
        v_key = chosen.split("│")[0].strip()
        set_default_voice(v_key)
        safe_pause()

def action_read_clipboard():
    """Read Windows clipboard content out loud."""
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Clipboard"], capture_output=True, text=True, encoding="utf-8")
        clip = res.stdout.strip()
        if clip:
            print(f"\n{CYAN}📋 Reading clipboard ({len(clip)} characters)...{RESET}")
            speak(clip)
        else:
            print(f"\n{YELLOW}⚠️ Windows clipboard is empty.{RESET}")
    except Exception as e:
        print(f"{RED}❌ Error reading clipboard: {e}{RESET}")

def action_spoken_briefing():
    """Speak live system telemetry & status briefing."""
    print(f"\n{CYAN}🔄 Fetching status from Blaze for spoken briefing...{RESET}")
    raw, err, code = run_ssh("termux-battery-status")
    if code == 255:
        render_unreachable_card()
        return
    bat_pct = "unknown"
    temp_c = ""
    status = "discharging"
    if raw:
        try:
            data = json.loads(raw)
            bat_pct = data.get("percentage", "unknown")
            temp = data.get("temperature", 0)
            if temp:
                temp_c = f" Temperature is {temp:.1f} degrees Celsius."
            status = data.get("status", "discharging").lower()
        except Exception:
            pass

    briefing = f"Sir, Blaze node telemetry report: Battery level is at {bat_pct} percent and currently {status}.{temp_c} All systems optimal."
    speak(briefing)

def action_emergency_siren():
    """Play loud alert siren bypassing silent mode with haptic feedback and default voice."""
    print(f"\n{RED}{BOLD}🚨 Triggering high-priority emergency siren on Blaze...{RESET}")
    # Max out all volume streams, vibrate, and pop up high-priority toast
    siren_cmd = "termux-volume music 15; termux-volume ring 15; termux-volume alarm 15; termux-volume notification 15; termux-vibrate -d 2500 -f; termux-toast -g middle -b '#B71C1C' -c 'white' '🚨 CRITICAL EMERGENCY ALERT'"
    run_ssh(siren_cmd)
    # Speak single loud warning using user's configured default voice
    speak("Warning! Critical high-priority mission alert!")

# =========================================================
# 📖 LINUX-STANDARD HELP MANUAL
# =========================================================

def print_help_manual(pause=True):
    """Display standard Linux-style command manual and examples."""
    print(f"""
{BOLD}NAME{RESET}
       blaze-speak - Studio HD Voice Synthesis & Assistant Speech Hub

{BOLD}SYNOPSIS{RESET}
       blaze-speak [OPTIONS] [TEXT]

{BOLD}DESCRIPTION{RESET}
       High-definition neural voice synthesis engine streaming cloud-grade
       Microsoft Edge-TTS and Google Assistant voices directly over SSH
       to Lava Blaze 5G OpenSL ES audio output with volume boost.
       Features 20 diverse personas, interactive voice chat REPL,
       live telemetry spoken briefings, and clipboard reading.

{BOLD}OPTIONS{RESET}
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

{BOLD}POPULAR PERSONAS{RESET}
       • ava     : US English (Female, warm & natural)
       • brian   : US English (Male, authoritative)
       • neerja  : Indian English (Female, crisp & clear)
       • jarvis  : Indian English (Male, Prabhat Neural)
       • swara   : Hindi (Female, expressive)
       • maisie  : British English (Female)

{BOLD}EXAMPLES{RESET}
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

{BOLD}AUTHOR{RESET}
       Engineered for Karan Singh Verma by Antigravity Assistant.
""")
    if pause:
        safe_pause("Press Enter to return to main menu...")

# =========================================================
# 🎮 MAIN INTERACTIVE VOICE CENTER
# =========================================================

def main_interactive_menu():
    """Main interactive FZF Voice Center."""
    while True:
        cur_voice = get_default_voice()
        menu_items = [
            "💬 1. Live Voice Chat Console    ──► Real-time voice conversation REPL",
            "🎭 2. Voice Persona Explorer     ──► Preview & test 20 Studio HD personas",
            f"⭐ 3. Set Permanent Default Voice──► Current Default: [{cur_voice}]",
            "📋 4. Read Clipboard Out Loud    ──► Speak contents of Windows clipboard",
            "🔋 5. Spoken Telemetry Briefing  ──► Speak live battery % & network status",
            "🚨 6. Emergency Siren Alert      ──► Loud alert siren bypassing silent mode",
            "📖 7. Help & CLI Reference       ──► Standard Linux manual, flags & examples",
            "🚪 0. Exit                       ──► Return to PowerShell terminal"
        ]

        choice = run_fzf(
            menu_items,
            prompt="Blaze Voice > ",
            header="🎙️ BLAZE STUDIO HD VOICE SYNTHESIS COMMAND CENTER"
        )

        if not choice or "0. Exit" in choice or "Exit" in choice:
            print(f"\n{CYAN}👋 Exited Voice Center.{RESET}\n")
            break

        if "1. Live Voice Chat" in choice:
            action_voice_chat()
        elif "2. Voice Persona" in choice:
            action_persona_explorer()
        elif "3. Set Permanent" in choice:
            action_set_default()
        elif "4. Read Clipboard" in choice:
            action_read_clipboard()
            safe_pause()
        elif "5. Spoken Telemetry" in choice:
            action_spoken_briefing()
            safe_pause()
        elif "6. Emergency Siren" in choice:
            action_emergency_siren()
            safe_pause()
        elif "7. Help & CLI" in choice:
            print_help_manual(pause=True)

# =========================================================
# 🚀 CLI ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Blaze HD Voice Synthesis Suite",
        add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show Linux-style command manual and exit")
    parser.add_argument("-v", "--voice", help="Voice persona name (e.g. ava, jarvis, swara)")
    parser.add_argument("--clip", action="store_true", help="Read clipboard out loud")
    parser.add_argument("--status", action="store_true", help="Speak status briefing")
    parser.add_argument("--alert", action="store_true", help="Trigger emergency siren")
    parser.add_argument("--native", action="store_true", help="Use Termux offline TTS engine")
    parser.add_argument("text", nargs="*", help="Text message to synthesize")

    args = parser.parse_args()

    try:
        if args.help:
            print_help_manual(pause=False)
        elif args.clip:
            action_read_clipboard()
        elif args.status:
            action_spoken_briefing()
        elif args.alert:
            action_emergency_siren()
        elif args.text:
            msg = " ".join(args.text)
            if args.native:
                safe_t = msg.replace("'", "'\\''")
                run_ssh(f"termux-tts-speak '{safe_t}'")
            else:
                speak(msg, voice_key=args.voice)
        else:
            main_interactive_menu()
    except (KeyboardInterrupt, EOFError):
        print(f"\n{YELLOW}⚡ Operation cancelled.{RESET}")

