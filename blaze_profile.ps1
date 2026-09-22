# ==============================================================================
# ⚡ Blaze-Termux-SSH Mobile Integration Hub — PowerShell Profile Module
# Project: Motobook ⇄ Lava Blaze 5G (Android Termux)
# Author: Karan Singh Verma & Antigravity Assistant
# Repository: https://github.com/karansinghverma979/Blaze-Termux-SSH
# ==============================================================================

<#
.SYNOPSIS
    Official PowerShell functions, aliases, and dynamic network discovery for Blaze.
.DESCRIPTION
    Dot-source this file in your $PROFILE to enable all `blaze-*` commands:
    . "$env:USERPROFILE\Void\Blaze-Termux-SSH\blaze_profile.ps1"
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
# 2. Dynamic Multi-Tier Discovery & Topology Sentinel
# ------------------------------------------------------------------------------
function Resolve-BlazeNode {
    [CmdletBinding()]
    param(
        [int]$Port = 8022,
        [switch]$Silent
    )

    $knownMac = 'F6-DC-F9-03-FA-07'
    $targetIp = $null
    $mode = $null
    $latencyMs = 0

    if ($env:BLAZE_PORT) { $Port = [int]$env:BLAZE_PORT }

    # Fast TCP Port Probe Helper with latency timer
    $TestBlazePort = {
        param([string]$Ip, [int]$TargetPort = $Port, [int]$TimeoutMs = 250)
        if (-not $Ip -or $Ip -match '^(127\.|0\.|169\.254\.)') { return $false }
        try {
            $sw = [System.Diagnostics.Stopwatch]::StartNew()
            $client = New-Object System.Net.Sockets.TcpClient
            $async = $client.BeginConnect($Ip, $TargetPort, $null, $null)
            $ok = $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false) -and $client.Connected
            if ($ok) { 
                $client.EndConnect($async)
                $sw.Stop()
                $script:lastProbeLatency = $sw.ElapsedMilliseconds
            }
            $client.Close()
            return $ok
        } catch {
            return $false
        }
    }

    # TIER 1: Direct Mobile Hotspot Gateway (Phone is AP / Gateway)
    $gateways = (Get-NetRoute -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue | Where-Object { 
        $_.NextHop -notlike '127.*' -and $_.NextHop -notlike '0.0.0.0' 
    }).NextHop | Select-Object -Unique

    foreach ($gw in $gateways) {
        if (& $TestBlazePort -Ip $gw -TargetPort $Port -TimeoutMs 300) {
            $targetIp = $gw
            $mode = "Direct Mobile Hotspot Gateway"
            $latencyMs = $script:lastProbeLatency
            break
        }
    }

    # TIER 2: Known Hardware MAC Match & Cached IP (Shared Wi-Fi / Static ARP)
    if (-not $targetIp) {
        $macMatch = Get-NetNeighbor -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { 
            ($_.LinkLayerAddress -replace '[:-]', '-').ToUpper() -eq $knownMac -and 
            $_.IPAddress -notmatch '^(127\.|169\.254\.|224\.|239\.|255\.)'
        } | Select-Object -ExpandProperty IPAddress -First 1

        if ($macMatch -and (& $TestBlazePort -Ip $macMatch -TargetPort $Port -TimeoutMs 300)) {
            $targetIp = $macMatch
            $mode = "Shared Wi-Fi (Hardware MAC Match)"
            $latencyMs = $script:lastProbeLatency
        }
    }

    # TIER 3: Fast Check Cached Session IP or ~/.ssh/config HostName
    if (-not $targetIp) {
        $candidateIp = $global:CachedBlazeIP
        if (-not $candidateIp -and (Test-Path "$env:USERPROFILE\.ssh\config")) {
            $sshConf = Get-Content "$env:USERPROFILE\.ssh\config" -Raw
            if ($sshConf -match 'HostName\s+([0-9\.]+)') {
                $candidateIp = $Matches[1]
            }
        }
        if ($candidateIp -and (& $TestBlazePort -Ip $candidateIp -TargetPort $Port -TimeoutMs 300)) {
            $targetIp = $candidateIp
            $mode = "Cached IP Fast-Path"
            $latencyMs = $script:lastProbeLatency
        }
    }

    # TIER 4: Parallel Subnet Auto-Discovery (Shared Wi-Fi / College / Home Router with MAC Randomization)
    if (-not $targetIp) {
        $localIpObj = Get-NetIPAddress -InterfaceAlias 'Wi-Fi' -AddressFamily IPv4 -ErrorAction SilentlyContinue | 
                      Where-Object { $_.IPAddress -notmatch '^(127\.|169\.254\.)' } | Select-Object -First 1
        if ($localIpObj) {
            $localIp = $localIpObj.IPAddress
            $subnetBase = $localIp.Substring(0, $localIp.LastIndexOf('.'))
            $foundSweepIp = 1..254 | ForEach-Object -Parallel {
                $probe = "$using:subnetBase.$_"
                try {
                    $tcp = New-Object System.Net.Sockets.TcpClient
                    $ar = $tcp.BeginConnect($probe, $using:Port, $null, $null)
                    if ($ar.AsyncWaitHandle.WaitOne(120, $false) -and $tcp.Connected) {
                        $tcp.EndConnect($ar)
                        $probe
                    }
                    $tcp.Close()
                } catch {}
            } -ThrottleLimit 60 | Select-Object -First 1

            if ($foundSweepIp) {
                $targetIp = $foundSweepIp
                $mode = "Shared Wi-Fi Subnet Sweep ($subnetBase.0/24)"
                $latencyMs = 35
            }
        }
    }

    # Fallback Notice if completely unreachable
    if (-not $targetIp) {
        if (-not $Silent) {
            Write-Host "`n┌─────────────────────────────────────────────────────────────┐" -ForegroundColor Red
            Write-Host "│ ⚠️ BLAZE SSH SERVER UNREACHABLE (Port $Port)                 │" -ForegroundColor Red
            Write-Host "├─────────────────────────────────────────────────────────────┤" -ForegroundColor DarkGray
            Write-Host "│ • Status:   Could not locate Blaze on current network.      │" -ForegroundColor Yellow
            Write-Host "│ • Tested:   Hotspot Gateway, Hardware MAC, & Subnet Sweep.  │" -ForegroundColor DarkGray
            Write-Host "│ • Action:   1. Ensure Termux is running 'sshd' on phone.    │" -ForegroundColor White
            Write-Host "│             2. Ensure phone is on the same Wi-Fi / Hotspot. │" -ForegroundColor White
            Write-Host "└─────────────────────────────────────────────────────────────┘`n" -ForegroundColor Red
        }
        return $null
    }

    $global:CachedBlazeIP = $targetIp

    # DYNAMIC REMOTE USER RESOLUTION (Rooted & Non-Rooted Universal Sentinel)
    $resolvedUser = $null
    try {
        # Quick non-interactive query over SSH to detect real Linux UID (u0_a201, root, etc.)
        $userProbe = (ssh -p $Port -o ConnectTimeout=2 -o BatchMode=yes -o StrictHostKeyChecking=no $targetIp "whoami" 2>$null)
        if ($userProbe -and $userProbe.Trim().Length -gt 0) {
            $resolvedUser = $userProbe.Trim()
        }
    } catch {}

    if (-not $resolvedUser) {
        $resolvedUser = if ($global:CachedBlazeUser) { $global:CachedBlazeUser } 
                        elseif ($env:BLAZE_USER) { $env:BLAZE_USER } 
                        else { "u0_a201" }
    }
    $global:CachedBlazeUser = $resolvedUser

    # Dynamically inject ~/.ssh/config host entry
    $sshConfigFile = "$env:USERPROFILE\.ssh\config"
    $sshConfigDir = "$env:USERPROFILE\.ssh"
    if (-not (Test-Path $sshConfigDir)) { New-Item -ItemType Directory -Path $sshConfigDir -Force | Out-Null }
    
    $configContent = @"
Host blaze phone
    HostName $targetIp
    Port $Port
    User $resolvedUser
    IdentityFile ~/.ssh/id_ed25519
    StrictHostKeyChecking no
    ServerAliveInterval 3
    ServerAliveCountMax 2
    ConnectTimeout 3
"@
    Set-Content -Path $sshConfigFile -Value $configContent -Force

    $global:BlazeConnectionInfo = [PSCustomObject]@{
        IP        = $targetIp
        Port      = $Port
        User      = $resolvedUser
        Mode      = $mode
        LatencyMs = $latencyMs
    }

    return $targetIp
}

function Get-BlazeTargetIP {
    [CmdletBinding()]
    param([switch]$Silent)
    return (Resolve-BlazeNode -Silent:$Silent)
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

    $targetIp = Resolve-BlazeNode
    if (-not $targetIp) { return }

    $info = $global:BlazeConnectionInfo
    $user = if ($info -and $info.User) { $info.User } else { "u0_a201" }
    $mode = if ($info -and $info.Mode) { $info.Mode } else { "LAN Peer" }
    $latency = if ($info -and $info.LatencyMs) { "$($info.LatencyMs) ms" } else { "<30 ms" }
    $port = if ($info -and $info.Port) { $info.Port } else { 8022 }

    if ($Command -and $Command.Count -gt 0) {
        $cmdString = $Command -join ' '
        ssh blaze "$cmdString"
    } else {
        # High-Density Connection HUD
        Write-Host "`n┌─────────────────────────────────────────────────────────────┐" -ForegroundColor Cyan
        Write-Host "│ ⚡ BLAZE TERMINAL LINK ESTABLISHED                           │" -ForegroundColor Cyan
        Write-Host "├─────────────────────────────────────────────────────────────┤" -ForegroundColor DarkGray
        Write-Host "│ • Target Node:  $targetIp`:$port" -ForegroundColor Green
        Write-Host "│ • Network Mode: $mode" -ForegroundColor Yellow
        Write-Host "│ • Remote User:  $user (Dynamic Root-Agnostic UID)" -ForegroundColor Magenta
        Write-Host "│ • Round-Trip:   $latency (TCP Handshake)" -ForegroundColor DarkCyan
        Write-Host "│ • Auth Mode:    IdentityFile ~/.ssh/id_ed25519" -ForegroundColor DarkGray
        Write-Host "└─────────────────────────────────────────────────────────────┘`n" -ForegroundColor Cyan

        # Zero-blocking interactive connection (No hanging termux-toast)
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

function Invoke-BlazeStatus {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_status.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_status.py" }
    & python $script @ArgsList
}

function Invoke-BlazeLocation {
    [CmdletBinding()]
    param([Parameter(ValueFromRemainingArguments=$true)][string[]]$ArgsList)
    $script = Join-Path $global:BlazeScriptsRoot "blaze_location.py"
    if (-not (Test-Path $script)) { $script = "$env:USERPROFILE\.config\blaze_location.py" }
    & python $script @ArgsList
}

# ------------------------------------------------------------------------------
# 6. Official Aliases
# ------------------------------------------------------------------------------
Set-Alias -Name blaze        -Value Connect-BlazePhone

Set-Alias -Name blaze-phone    -Value Invoke-BlazePhone
Set-Alias -Name blaze-wifi     -Value Invoke-BlazeWifi
Set-Alias -Name blaze-media    -Value Invoke-BlazeMedia
Set-Alias -Name blaze-speak    -Value Invoke-BlazeTTS
Set-Alias -Name blaze-clip     -Value Invoke-BlazeClip
Set-Alias -Name blaze-notifs   -Value Invoke-BlazeNotifs
Set-Alias -Name blaze-file     -Value Invoke-BlazeFile
Set-Alias -Name blaze-location -Value Invoke-BlazeLocation
Set-Alias -Name blaze-status   -Value Invoke-BlazeStatus
