$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:KIS_MODE='mock'; $env:LIVE_TRADING_ENABLED='false'
& 'C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe' scripts/run_websocket_paper_session.py
