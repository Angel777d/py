SET FILE_NAME=run.pyw
set TARGET='%cd%\%FILE_NAME%'
set SHORTCUT='%UserProfile%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\[Autorun link] %FILE_NAME%.lnk'
set PWS=powershell.exe -ExecutionPolicy Bypass -NoLogo -NonInteractive -NoProfile

%PWS% -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut(%SHORTCUT%); $s.TargetPath = %TARGET%; $s.WorkingDirectory = '%cd%'; $s.Save()"
