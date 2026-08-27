#define MyAppName "TreeVCS"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Sadik Laskar"
#define MyAppURL "https://github.com/labsadik/TreeVCS"
#define MyAppExeName "tree.exe"
#define MyAppOutputBaseFilename "tree_installer_v1.0.0"

[Setup]
; App Identification & Metadata
AppId={{A3D89E74-8422-4B2E-9FBA-4A8E0D1B2C3D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} v{#MyAppVersion} by {#MyAppPublisher}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
AppCopyright=Copyright (C) 2026 {#MyAppPublisher}

; Windows File Properties (Removes "Unknown Author / Publisher")
VersionInfoCompany={#MyAppPublisher}
VersionInfoCopyright=Copyright (C) 2026 {#MyAppPublisher}
VersionInfoDescription=TreeVCS Setup Installer created by {#MyAppPublisher}
VersionInfoOriginalFileName={#MyAppOutputBaseFilename}.exe
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
VersionInfoVersion=1.0.0.0

; Installation Directories & Output Options
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=..\releases\v1.0.0
OutputBaseFilename={#MyAppOutputBaseFilename}
SetupIconFile=..\scripts\app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
ShowLanguageDialog=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Messages]
WelcomeLabel2=This will install [name] on your computer.%n%nDeveloper & Publisher: {#MyAppPublisher}%nWebsite: {#MyAppURL}%n%nIt is recommended that you close all other applications before continuing.

[Tasks]
Name: "modpath"; Description: "Add TreeVCS to system PATH (Recommended for command-line usage)"; Flags: checkedonce

[Files]
Source: "..\releases\v1.0.0\tree.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[Code]
// Automatically add installation path to Windows Environment PATH variable
procedure CurStepChanged(CurStep: TSetupStep);
var
  Path: string;
begin
  if (CurStep = ssPostInstall) and WizardIsTaskSelected('modpath') then
  begin
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path) then
    begin
      if Pos(ExpandConstant('{app}'), Path) = 0 then
      begin
        Path := Path + ';' + ExpandConstant('{app}');
        RegWriteStringValue(HKEY_LOCAL_MACHINE, 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment', 'Path', Path);
      end;
    end;
  end;
end;