$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
Set-Location $root
if ($env:LIVE_TRADING_ENABLED -ne 'true' -or $env:LIVE_CONFIRMATION -ne 'I_UNDERSTAND_LIVE_RISK') {
  Write-Host 'LIVE BOT LOCKED. Set LIVE_TRADING_ENABLED=true and LIVE_CONFIRMATION=I_UNDERSTAND_LIVE_RISK after order API review.' -ForegroundColor Yellow
  Read-Host 'Press Enter to close'; exit 2
}
$env:KIS_MODE='live'
Write-Host 'LIVE BOT REQUESTED; current LiveBroker remains locked until execution adapter review.' -ForegroundColor Red
& 'C:\Users\user\AppData\Local\Programs\Python\Python312\python.exe' -c "from kis_bot.broker import LiveBroker; from kis_bot.broker import Order; LiveBroker().submit(Order('000000','BUY',1,1))"
