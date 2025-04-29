[Setup]
AppName=BPLA
AppVersion=1.0
DefaultDirName={pf}\BPLA
OutputDir=output
OutputBaseFilename=BPLA_Installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "install.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "backend\*"; DestDir: "{app}\backend"; Flags: recursesubdirs ignoreversion
Source: "src\*"; DestDir: "{app}\src"; Flags: recursesubdirs ignoreversion
Source: ".env"; DestDir: "{app}"; Flags: ignoreversion

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\install.ps1"""; Flags: runhidden
