# ==============================================================================
# ⚡ Blaze Mobile Integration & Automation Hub — PowerShell Profile Module
# Project: Motobook ⇄ Lava Blaze 5G (Android Termux)
# Author: Karan Singh Verma & Antigravity Assistant
# Repository: https://github.com/karansinghverma/Blaze
# ==============================================================================

<#
.SYNOPSIS
    Official PowerShell functions, aliases, and dynamic network discovery for Blaze.
.DESCRIPTION
    Dot-source this file in your $PROFILE to enable all `blaze-*` commands:
    . "$env:USERPROFILE\Void\Blaze\blaze_profile.ps1"
#>

# ------------------------------------------------------------------------------
# 1. Base Configuration & Paths
# ------------------------------------------------------------------------------
$global:BlazeScriptsRoot = Join-Path $PSScriptRoot "scripts"
if (-not (Test-Path $global:BlazeScriptsRoot)) {
    # Fallback to ~/.config/ if dot-sourced outside repository
    $global:BlazeScriptsRoot = "$env:USERPROFILE\.config"
}

# ------------------------------------------------------------------------------
# 2. Dynamic IP Discovery & SSH Auto-Configuration
# ------------------------------------------------------------------------------
function Get-BlazeTargetIP {
    [CmdletBinding()]
    param([switch]$Silent)

    $knownMac = 'F6-DC-F9-03-FA-07'
    $targetIp = $null

    # Fast TCP Port 8022 Probe Helper
    $TestBlazePort = {
        param([string]$Ip, [int]$TimeoutMs = 300)
        if (-not $Ip) { return $false }
        try {
            $client = New-Object System.Net.Sockets.TcpClient
            $async = $client.BeginConnect($Ip, 8022, $null, $null)
            $ok = $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false) -and $client.Connected
            if ($ok) { $client.EndConnect($async) }
            $client.Close()
            return $ok
        } catch {
            return $false
        }
    }

    # TIER 1: Mobile Hotspot Gateway (Phone is Host / Gateway)
    $gateways = (Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | Where-Object { 
        $_.NextHop -notlike '127.*' -and $_.NextHop -notlike '0.0.0.0' 
    }).NextHop | Select-Object -Unique

    foreach ($gw in $gateways) {
        if (& $TestBlazePort -Ip $gw -TimeoutMs 400) {
            $targetIp = $gw
            break
        }
    }

    # TIER 2: Known Hardware MAC Match & Cached IP
    if (-not $targetIp) {
        $macMatch = Get-NetNeighbor -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { 
            ($_.LinkLayerAddress -replace '[:-]', '-').ToUpper() -eq $knownMac -and 
            $_.IPAddress -notmatch '^(127\.|169\.254\.|224\.|239\.|255\.)'
        } | Select-Object -ExpandProperty IPAddress -First 1

        if ($macMatch -and (& $TestBlazePort -Ip $macMatch -TimeoutMs 400)) {
            $targetIp = $macMatch
        }
    }

    # TIER 3: Fast check cached IP or ~/.ssh/config IP
    if (-not $targetIp) {
        $candidateIp = $global:CachedBlazeIP
        if (-not $candidateIp -and (Test-Path "$env:USERPROFILE\.ssh\config")) {
            $sshConf = Get-Content "$env:USERPROFILE\.ssh\config" -Raw
            if ($sshConf -match 'HostName\s+([0-9\.]+)') {
                $candidateIp = $Matches[1]
            }
        }
        if ($candidateIp -and (& $TestBlazePort -Ip $candidateIp -TimeoutMs 400)) {
            $targetIp = $candidateIp
        }
    }

    # Fallback Notice
    if (-not $targetIp) {
        if (-not $Silent) {
            Write-Host "`n┌─────────────────────────────────────────────────────────────┐" -ForegroundColor Red
            Write-Host "│ ⚠️ BLAZE SSH SERVER UNREACHABLE (Port 8022)                 │" -ForegroundColor Red
            Write-Host "├─────────────────────────────────────────────────────────────┤" -ForegroundColor DarkGray
            Write-Host "│ • Status:   Could not locate Blaze on current network.      │" -ForegroundColor Yellow
            Write-Host "│ • Action:   1. Ensure Termux is running 'sshd' on phone.    │" -ForegroundColor White
            Write-Host "│             2. Ensure phone is on the same Wi-Fi / Hotspot. │" -ForegroundColor White
            Write-Host "└─────────────────────────────────────────────────────────────┘`n" -ForegroundColor Red
        }
        return $null
    }

    $global:CachedBlazeIP = $targetIp

    # Dynamically inject ~/.ssh/config host entry
    $sshConfigFile = "$env:USERPROFILE\.ssh\config"
    $sshConfigDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshConfigDir)) { New-Item -ItemType Directory -Path $sshConfigDir -Force | Out-Null }
    
    $configContent = @"
Host blaze phone
    HostName $targetIp
    Port 8022
    User u0_a46
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
    ServerAliveInterval 3
    ServerAliveCountMax 2
    ConnectTimeout 3
"@
    Set-Content -Path $sshConfigFile -Value $configContent -Force
    return $targetIp
}

# ------------------------------------------------------------------------------
# 3. Interactive Shell Connector
# ------------------------------------------------------------------------------
function Connect-BlazePhone {
    [CmdletBinding()]
    param(
        [Parameter(ValueFromRemainingArguments=$true)]
        [string[]]$Command
    )

    $targetIp = Get-BlazeTargetIP
    if (-not $targetIp) { return }

    if ($Command -and $Command.Count -gt 0) {
        $cmdString = $Command -join ' '
        ssh blaze "$cmdString"
    } else {
        Write-Host "⚡ Connecting to Blaze at $targetIp..." -ForegroundColor Cyan
        ssh -o ConnectTimeout=3 blaze "termux-toast '⚡ Motobook terminal connected'" 2>$null
        & ssh blaze
        $exitCode = $LASTEXITCODE
        if ($exitCode -eq 255) {
            Write-Host "`n⚠️ [Connection Dropped] Blaze disconnected or network switched." -ForegroundColor Yellow
            Write-Host "💡 Run 'blaze' to reconnect whenever device is back online.`n" -ForegroundColor DarkCyan
        }
    }
}

# ------------------------------------------------------------------------------
# 4. 7 Core Python Hub Delegations
# ------------------------------------------------------------------------------
function Invoke-BlazePhone {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_phone.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_phone.py" }
    & python $script @ArgsList
}

function Invoke-BlazeWifi {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_wifi.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_wifi.py" }
    & python $script @ArgsList
}

function Invoke-BlazeMedia {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_media.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_media.py" }
    & python $script @ArgsList
}

function Invoke-BlazeTTS {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_speak.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_speak.py" }
    & python $script @ArgsList
}

function Invoke-BlazeClip {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_clip.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_clip.py" }
    & python $script @ArgsList
}

function Invoke-BlazeNotifs {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_notifs.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_notifs.py" }
    & python $script @ArgsList
}

function Invoke-BlazeFile {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_file.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_file.py" }
    & python $script @ArgsList
}

# ------------------------------------------------------------------------------
# 5. Direct Status & GPS Utilities
# ------------------------------------------------------------------------------
function Get-BlazeStatus {
    [CmdletBinding()]
    param()
    $targetIp = Get-BlazeTargetIP -Silent
    if (-not $targetIp) {
        Write-Host "❌ Blaze unreachable on port 8022." -ForegroundColor Red
        return
    }
    Write-Host "📱 Querying Blaze Node ($targetIp)..." -ForegroundColor Cyan
    ssh -o ConnectTimeout=3 blaze "termux-battery-status"
}

function Get-BlazeLocation {
    [CmdletBinding()]
    param(
        [Parameter()][switch]$Live,
        [Parameter()][switch]$Open
    )
    $targetIp = Get-BlazeTargetIP -Silent
    if (-not $targetIp) {
        Write-Host "❌ Blaze unreachable on port 8022." -ForegroundColor Red
        return
    }
    $req = if ($Live) { "termux-location -p gps -r last" } else { "termux-location -r last" }
    Write-Host "📍 Fetching location from Blaze..." -ForegroundColor Cyan
    $locJson = ssh -o ConnectTimeout=5 blaze $req
    if ($locJson) {
        try {
            $loc = $locJson | ConvertFrom-Json
            Write-Host "Latitude:  $($loc.latitude)" -ForegroundColor Green
            Write-Host "Longitude: $($loc.longitude)" -ForegroundColor Green
            Write-Host "Accuracy:  $($loc.accuracy)m" -ForegroundColor Yellow
            Write-Host "Provider:  $($loc.provider)" -ForegroundColor DarkGray
            if ($Open -and $loc.latitude -and $loc.longitude) {
                $mapUrl = "https://www.google.com/maps/search/?api=1&query=$($loc.latitude),$($loc.longitude)"
                Start-Process $mapUrl
            }
        } catch {
            Write-Host $locJson
        }
    }
}

# ------------------------------------------------------------------------------
# 6. Official Aliases
# ------------------------------------------------------------------------------
Set-Alias -Name blaze        -Value Connect-BlazePhone

Set-Alias -Name blaze-phone  -Value Invoke-BlazePhone
Set-Alias -Name blaze-wifi   -Value Invoke-BlazeWifi
Set-Alias -Name blaze-media  -Value Invoke-BlazeMedia
Set-Alias -Name blaze-speak  -Value Invoke-BlazeTTS
Set-Alias -Name blaze-clip   -Value Invoke-BlazeClip
Set-Alias -Name blaze-notifs -Value Invoke-BlazeNotifs
Set-Alias -Name blaze-file   -Value Invoke-BlazeFile

Set-Alias -Name blaze-status -Value Get-BlazeStatus
Set-Alias -Name blaze-location -Value Get-BlazeLocation
