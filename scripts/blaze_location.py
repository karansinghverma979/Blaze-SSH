#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📍 Blaze Location, GPS Radar & Geolocation Hub
Author: Antigravity Assistant & Karan Singh Verma
Project: Blaze (Motobook ⇄ Lava Blaze 5G Node)
Dual Mode: Fast-Path CLI switches & Rich Interactive Terminal Radar
Layout Standard: Single-column metrics, left-anchored open cards, symmetrical spacing, 0 right borders
"""

import sys
import os
import json
import subprocess
import argparse
import webbrowser
import urllib.request
import urllib.parse
from datetime import datetime

# UTF-8 Console Safety
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

def render_unreachable_card():
    """Renders standardized offline diagnostic card when Blaze SSH is unreachable."""
    print()
    print(f"{RED}┌── ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022 ─────────────────────{RESET}")
    print(f"{RED}│{RESET}")
    print(f"│ • Root Cause: Phone offline or SSH daemon (sshd) not running.")
    print(f"│ • Action:     1. Ensure Termux is active on Blaze.")
    print(f"│               2. Run 'sshd' in Termux.")
    print(f"│               3. Ensure phone is connected to same Wi-Fi / Hotspot.")
    print(f"{RED}│{RESET}")
    print(f"{RED}└── ⏱️ Connection Timeout (3s){RESET}")
    print()

def render_location_off_card():
    """Renders standardized error card when Location / GPS is turned off or blocked."""
    print()
    print(f"{YELLOW}┌── ⚠️ LOCATION SERVICES DISABLED / UNAVAILABLE ────────────────{RESET}")
    print(f"{YELLOW}│{RESET}")
    print(f"│ • Root Cause: Android Location (GPS/Network) is OFF or Termux:API lacks Location permission.")
    print(f"│ • Action:     1. Pull down quick settings on Blaze and turn ON Location 📍.")
    print(f"│               2. Go to Settings > Apps > Termux:API > Permissions > Location > Allow.")
    print(f"│               3. Ensure Termux:API app is installed on phone.")
    print(f"{YELLOW}│{RESET}")
    print(f"{YELLOW}└── 💡 Retrying with alternate providers (network/gps/passive)...{RESET}")
    print()

def run_ssh(cmd, timeout=5):
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

def reverse_geocode(lat, lon, timeout=4):
    """Performs reverse geocoding via OpenStreetMap Nominatim with graceful timeout."""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Blaze-SSH/1.0 (karan@motobook)'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get("display_name", "Unknown Address")
    except Exception:
        return "Online geocoding unavailable (Offline/Rate Limited)"

def fetch_location_data(provider="network", request_type="last"):
    """
    Queries location from Termux with intelligent fallback cascade:
    1. Requested provider (e.g. network/gps)
    2. Fallback cascade (network -> passive -> gps)
    Returns parsed dictionary or error structure.
    """
    providers_to_try = [provider]
    if provider == "gps":
        providers_to_try.extend(["network", "passive"])
    elif provider == "network":
        providers_to_try.extend(["passive", "gps"])
    else:
        providers_to_try.extend(["network", "gps"])

    last_err = ""
    ssh_unreachable = False

    for prov in providers_to_try:
        cmd = f"termux-location -p {prov} -r {request_type}"
        out, err, code = run_ssh(cmd, timeout=6)
        
        if code == 255:
            ssh_unreachable = True
            break
        
        if code != 0 or not out:
            last_err = err or "No response from termux-location"
            continue

        try:
            data = json.loads(out)
            if "API_ERROR" in data:
                last_err = data.get("API_ERROR", "Failed to get location")
                continue
            
            if "latitude" in data and "longitude" in data:
                # Success
                return data, None
        except Exception:
            last_err = f"Failed to parse location JSON: {out}"
            continue

    if ssh_unreachable:
        return None, "SSH_UNREACHABLE"
    return None, last_err or "LOCATION_OFF_OR_UNAVAILABLE"

def display_location_radar(provider="network", request_type="last", open_map=False, json_mode=False, raw_mode=False):
    """Renders the Location Radar HUD adhering strictly to symmetrical UI invariants."""
    data, err = fetch_location_data(provider=provider, request_type=request_type)

    if err == "SSH_UNREACHABLE":
        if json_mode:
            print(json.dumps({"error": "SSH_UNREACHABLE", "details": "Blaze SSH port 8022 is unreachable"}))
        else:
            render_unreachable_card()
        return

    if not data or err:
        if json_mode:
            print(json.dumps({"error": "LOCATION_UNAVAILABLE", "details": err}))
        else:
            render_location_off_card()
        return

    lat = data.get("latitude")
    lon = data.get("longitude")
    acc = data.get("accuracy", 0.0)
    alt = data.get("altitude", 0.0)
    vert_acc = data.get("vertical_accuracy", 0.0)
    prov = data.get("provider", provider).upper()
    speed = data.get("speed", 0.0)
    bearing = data.get("bearing", 0.0)
    elapsed = data.get("elapsedMs", 0)

    # Reverse Geocode
    address = reverse_geocode(lat, lon)
    map_url = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"

    if json_mode:
        payload = {
            "status": "SUCCESS",
            "latitude": lat,
            "longitude": lon,
            "accuracy_meters": acc,
            "altitude_meters": alt,
            "vertical_accuracy": vert_acc,
            "provider": prov,
            "speed": speed,
            "bearing": bearing,
            "elapsed_ms": elapsed,
            "address": address,
            "maps_url": map_url
        }
        print(json.dumps(payload, indent=2))
        return

    if raw_mode:
        print(f"{lat},{lon}")
        return

    # Symmetrical Single-Column UI Radar
    print()
    print(f"{CYAN}┌── 📍 BLAZE GEOLOCATION & GPS RADAR ───────────────────────────{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"│ 🌐 {BOLD}Latitude:{RESET}          {GREEN}{lat}{RESET}")
    print(f"│ 🌐 {BOLD}Longitude:{RESET}         {GREEN}{lon}{RESET}")
    print(f"│ 🎯 {BOLD}Fix Accuracy:{RESET}      {YELLOW}±{acc:.1f} meters{RESET}")
    print(f"│ ⛰️  {BOLD}Altitude:{RESET}          {alt:.1f} m (Vert ±{vert_acc:.1f} m)")
    print(f"│ 📡 {BOLD}Location Provider:{RESET} {CYAN}{prov}{RESET}")
    print(f"│ 🧭 {BOLD}Bearing / Speed:{RESET}   {bearing}° / {speed} m/s")
    print(f"│ ⏱️  {BOLD}Fix Age:{RESET}           {elapsed / 1000.0:.1f}s ago")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}├── 🗺️ Resolved Address & Map ──────────────────────────────────{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"│ 🏠 {BOLD}Reverse Address:{RESET}   {address}")
    print(f"│ 🔗 {BOLD}Google Maps URL:{RESET}   {CYAN}{map_url}{RESET}")
    print(f"{CYAN}│{RESET}")
    print(f"{CYAN}└── 🚀 Fix Acquired & Validated{RESET}")
    print()

    if open_map:
        print(f"{CYAN}🌍 Opening Google Maps in default browser...{RESET}")
        webbrowser.open(map_url)

def interactive_menu():
    """Interactive CLI menu loop for Blaze Location operations."""
    while True:
        print()
        print(f"{CYAN}┌── 📍 BLAZE LOCATION & GPS RADAR HUB ──────────────────────────{RESET}")
        print(f"{CYAN}│{RESET}")
        print(f"│  {BOLD}1{RESET}  ⚡ Fast Network Location (Instant Last Fix)")
        print(f"│  {BOLD}2{RESET}  🛰️ Live GPS Satellite Fix (Fresh Request)")
        print(f"│  {BOLD}3{RESET}  🗺️ Fetch Location & Open in Google Maps")
        print(f"│  {BOLD}4{RESET}  📡 Passive Provider Fix (Lowest Power)")
        print(f"│  {BOLD}0{RESET}  🚪 Exit")
        print(f"{CYAN}│{RESET}")
        print(f"{CYAN}└── ⚡ Select Option [0-4]{RESET}")
        print()
        try:
            choice = input(f"{BOLD}Blaze-Location ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}👋 Exited gracefully.{RESET}")
            break

        if choice == "1":
            display_location_radar(provider="network", request_type="last")
        elif choice == "2":
            print(f"{CYAN}🛰️ Acquiring fresh GPS satellite fix (may take 2-4s)...{RESET}")
            display_location_radar(provider="gps", request_type="once")
        elif choice == "3":
            display_location_radar(provider="network", request_type="last", open_map=True)
        elif choice == "4":
            display_location_radar(provider="passive", request_type="last")
        elif choice in ["0", "q", "exit"]:
            print(f"{DIM}👋 Exited.{RESET}")
            break
        else:
            print(f"{YELLOW}⚠️ Invalid choice. Select 0-4.{RESET}")

def main():
    parser = argparse.ArgumentParser(
        description="Blaze Location, GPS Radar & Geolocation Hub",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("--live", action="store_true", help="Acquire fresh live GPS satellite fix")
    parser.add_argument("--gps", action="store_true", help="Request GPS provider explicitly")
    parser.add_argument("--network", action="store_true", help="Request Network provider explicitly (default)")
    parser.add_argument("--open", "-o", action="store_true", help="Automatically open Google Maps link in browser")
    parser.add_argument("--json", action="store_true", help="Output complete location telemetry in JSON format")
    parser.add_argument("--raw", action="store_true", help="Output raw 'latitude,longitude' string")

    args = parser.parse_args()

    prov = "gps" if args.gps else "network"
    req = "once" if args.live else "last"

    # If any specific flag is passed, execute fast-path
    if args.live or args.gps or args.network or args.open or args.json or args.raw:
        display_location_radar(
            provider=prov,
            request_type=req,
            open_map=args.open,
            json_mode=args.json,
            raw_mode=args.raw
        )
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
