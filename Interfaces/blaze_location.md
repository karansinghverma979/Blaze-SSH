# 📍 `blaze-location` — Geolocation, GPS Radar & Reverse Geocoding Interface

> **Command**: `blaze-location`  
> **Source Script**: [`scripts/blaze_location.py`](file:///scripts/blaze_location.py)  
> **PowerShell Cmdlet**: `Invoke-BlazeLocation` (Alias: `blaze-location`)  
> **Location Providers**: Multi-Tier Cascade (`gps` ➔ `network` ➔ `passive`)  
> **Reverse Geocoding**: OpenStreetMap Nominatim Engine (`lat,lon` ➔ Street Address)  
> **Browser Integration**: Direct Google Maps Link Dispatcher

---

## 🖥️ 1. Main Interactive Terminal Menu

When executing `blaze-location` from PowerShell without arguments, it launches the interactive menu:

```text
┌── 📍 BLAZE LOCATION & GPS RADAR HUB ──────────────────────────
│
│  1  ⚡ Fast Network Location (Instant Last Fix)
│  2  🛰️ Live GPS Satellite Fix (Fresh Request)
│  3  🗺️ Fetch Location & Open in Google Maps
│  4  📡 Passive Provider Fix (Lowest Power)
│  0  🚪 Exit
│
└── ⚡ Select Option [0-4]

Blaze-Location ❯ _
```

---

## 📍 2. Geolocation Radar HUD Screen (`Option 1` / `--network`)

Acquires instantaneous cellular/Wi-Fi triangulation fix, performs online reverse-geocoding, and renders the single-column visual card:

```text
┌── 📍 BLAZE GEOLOCATION & GPS RADAR ───────────────────────────
│
│ 🌐 Latitude:          28.613939
│ 🌐 Longitude:         77.209021
│ 🎯 Fix Accuracy:      ±15.0 meters
│ ⛰️  Altitude:          216.0 m (Vert ±4.2 m)
│ 📡 Location Provider: NETWORK
│ 🧭 Bearing / Speed:   0.0° / 0.0 m/s
│ ⏱️  Fix Age:           1.2s ago
│
├── 🗺️ Resolved Address & Map ──────────────────────────────────
│
│ 🏠 Reverse Address:   Rajpath, Central Secretariat, New Delhi, Delhi, 110001, India
│ 🔗 Google Maps URL:   https://www.google.com/maps/search/?api=1&query=28.613939,77.209021
│
└── 🚀 Fix Acquired & Validated
```

---

## 🛰️ 3. Fresh Satellite GPS Fix (`Option 2` / `--live`)

Engages physical hardware GPS receiver on phone for high-precision satellite coordinates:

```text
🛰️ Acquiring fresh GPS satellite fix (may take 2-4s)...

┌── 📍 BLAZE GEOLOCATION & GPS RADAR ───────────────────────────
│
│ 🌐 Latitude:          28.613942
│ 🌐 Longitude:         77.209025
│ 🎯 Fix Accuracy:      ±3.5 meters
│ ⛰️  Altitude:          218.4 m (Vert ±1.2 m)
│ 📡 Location Provider: GPS
│ 🧭 Bearing / Speed:   124.0° / 0.2 m/s
│ ⏱️  Fix Age:           0.4s ago
│
├── 🗺️ Resolved Address & Map ──────────────────────────────────
│
│ 🏠 Reverse Address:   Rajpath, Central Secretariat, New Delhi, Delhi, 110001, India
│ 🔗 Google Maps URL:   https://www.google.com/maps/search/?api=1&query=28.613942,77.209025
│
└── 🚀 Fix Acquired & Validated
```

---

## 🗺️ 4. Google Maps Browser Launcher (`Option 3` / `-o` / `--open`)

Fetches current coordinates and automatically launches your PC browser to the exact pinpoint location:

```text
🌍 Opening Google Maps in default browser...
[PC Browser opens: https://www.google.com/maps/search/?api=1&query=28.613939,77.209021]
```

---

## 🤖 5. Machine JSON Output Mode (`--json`)

```json
{
  "status": "SUCCESS",
  "latitude": 28.613939,
  "longitude": 77.209021,
  "accuracy_meters": 15.0,
  "altitude_meters": 216.0,
  "vertical_accuracy": 4.2,
  "provider": "NETWORK",
  "speed": 0.0,
  "bearing": 0.0,
  "elapsed_ms": 1200,
  "address": "Rajpath, Central Secretariat, New Delhi, Delhi, 110001, India",
  "maps_url": "https://www.google.com/maps/search/?api=1&query=28.613939,77.209021"
}
```

---

## ⚠️ 6. Diagnostic Cards & Error Defenses

### Location Service Turned OFF on Android
```text
┌── ⚠️ LOCATION SERVICES DISABLED / UNAVAILABLE ────────────────
│
│ • Root Cause: Android Location (GPS/Network) is OFF or Termux:API lacks Location permission.
│ • Action:     1. Pull down quick settings on Blaze and turn ON Location 📍.
│               2. Go to Settings > Apps > Termux:API > Permissions > Location > Allow.
│               3. Ensure Termux:API app is installed on phone.
│
└── 💡 Retrying with alternate providers (network/gps/passive)...
```

### Blaze Unreachable
```text
┌── ⚠️ BLAZE NODE UNREACHABLE ON PORT 8022 ─────────────────────
│
│ • Root Cause: Phone offline or SSH daemon (sshd) not running.
│ • Action:     1. Ensure Termux is active on Blaze.
│               2. Run 'sshd' in Termux.
│               3. Ensure phone is connected to same Wi-Fi / Hotspot.
│
└── ⏱️ Connection Timeout (3s)
```
