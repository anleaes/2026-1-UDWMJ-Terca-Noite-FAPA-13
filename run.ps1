$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot
& "$ProjectRoot\.venv\Scripts\python.exe" manage.py runserver @args
