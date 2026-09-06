$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $project
$python = 'C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe'
$env:PAPER_SYMBOLS = if ($env:PAPER_SYMBOLS) { $env:PAPER_SYMBOLS } else { '005930,000660,035420' }
Write-Host "KIS PAPER TRADING - MOCK ONLY" -ForegroundColor Cyan
Write-Host "Symbols: $env:PAPER_SYMBOLS"
Write-Host "Press Ctrl+C to stop. Orders are local MockBroker orders only."
& $python scripts/run_websocket_paper_session.py
Read-Host 'Session stopped. Press Enter to close'
