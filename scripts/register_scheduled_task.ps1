# Windows Task Scheduler — түнгі 03:00
# PowerShell-ді Administrator ретінде іске қос:

$ProjectPath = "C:\Users\USER\OneDrive\Desktop\Mega_project\Mega_project"
$BatPath = Join-Path $ProjectPath "scripts\run_nightly.bat"

$Action = New-ScheduledTaskAction -Execute $BatPath -WorkingDirectory $ProjectPath
$Trigger = New-ScheduledTaskTrigger -Daily -At "03:00"
$Settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -DontStopOnIdleEnd

Register-ScheduledTask `
    -TaskName "MegaProjectNightlyPipeline" `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Description "Run ETL + ML pipeline and send Telegram alert"

Write-Host "Task registered: MegaProjectNightlyPipeline (daily 03:00)"
