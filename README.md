# ⚡ Blaze: Android Mobile Integration & Automation Hub

> **Device**: Lava Blaze 5G (Android 14)  
> **User**: `u0_a46` | **Shell**: Termux Zsh (Powerlevel10k)  
> **SSH Port**: `8022` | **Subnet**: `10.242.186.0/24`  
> **Host Pair**: `Motobook` (Windows 11 Pro, OpenSSH `:22`) ⇄ `Blaze` (Lava Blaze 5G, OpenSSH `:8022`)

---

## 🎯 Purpose & Scope

The **Blaze** project houses all multi-device automation scripts, bidirectional sync pipelines, Termux hooks, and ADB tooling connecting Karan's primary PC (`Motobook`) with his mobile workstation (`Blaze`).

---

## 📁 Repository Layout

```
C:\Users\karan\Void\Blaze\
├── .gitignore
├── README.md
└── scripts/
    ├── sync/         # Bidirectional file & Obsidian vault sync scripts
    ├── termux/       # Remote Termux command hooks & automations
    └── adb/          # ADB pairing, diagnostics, and wireless shell scripts
```

---

## 🔗 Key Endpoints & Connectivity

- **PC ➔ Phone (Termux)**: `ssh -p 8022 u0_a46@<blaze-ip>`
- **Phone ➔ PC (Motobook)**: `ssh -p 22 karan@<motobook-ip>`
- **Default Hotspot Subnet**: `10.242.186.0/24`
