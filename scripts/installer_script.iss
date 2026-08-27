[Setup]
AppName=Tree
AppVersion=1.0.0
AppPublisher=Sadik Laskar
AppPublisherURL=https://github.com/Sadik/Tree
DefaultDirName={autopf}\Tree
DefaultGroupName=Tree
UninstallDisplayIcon={app}\tree.exe
SetupIconFile=app_icon.ico
Compression=lzma2
SolidCompression=yes
OutputDir=..\releases\v1.0.0
OutputBaseFilename=tree_installer_v1.0.0

; === THESE LINES FIX THE PROPERTIES TAB SHOWN IN YOUR IMAGE ===
VersionInfoVersion=1.0.0.0
VersionInfoCompany=Sadik Laskar
VersionInfoDescription=Tree Setup
VersionInfoCopyright=Copyright (C) 2026 Sadik Laskar
VersionInfoProductName=Tree
VersionInfoProductVersion=1.0.0.0

[Files]
Source: "..\releases\v1.0.0\tree.exe"; DestDir: "{app}"; Flags: ignoreversion

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var
  Path: String;
begin
  if CurStep = ssPostInstall then
  begin
    if RegQueryStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', Path) then
    begin
      if Pos(ExpandConstant('{app}'), Path) = 0 then
      begin
        Path := Path + ';' + ExpandConstant('{app}');
        RegWriteStringValue(HKEY_CURRENT_USER, 'Environment', 'Path', Path);
      end;
    end;
  end;
end;