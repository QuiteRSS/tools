; -- QuiteRSS.iss --

#define _AppName "QuiteRSS"
#define _AppVersion GetStringFileInfo("Data\QuiteRSS.exe", FILE_VERSION)
#define _AppVerName GetStringFileInfo("Data\QuiteRSS.exe", PRODUCT_VERSION)
#define _AppPublisher "QuiteRSS Team"

[Setup]
AppID={{372E76B7-3389-4057-B06A-53B104094844}
AppName={#_AppName}
AppVersion={#_AppVerName}
AppPublisher={#_AppPublisher}
VersionInfoVersion={#_AppVersion}
DefaultDirName={autopf}\{#_AppName}
DefaultGroupName={#_AppName}
Compression=lzma/Max
InternalCompressLevel=Max
SolidCompression=true
VersionInfoCompany={#_AppPublisher}
VersionInfoDescription={#_AppName} {#_AppVerName} Setup
MinVersion=6.1.7600
AppPublisherURL=http://quiterss.org
WizardImageFile=logo.bmp
WizardSmallImageFile=logo55.bmp
WizardImageStretch=false
OutputDir=Setup
OutputBaseFilename={#_AppName}-{#_AppVerName}-Setup
RestartIfNeededByRun=false
ShowTasksTreeLines=true
SetupIconFile=Setup.ico
LanguageDetectionMethod=locale
PrivilegesRequired=none

[Files]
Source: {#_AppName}.exe; DestDir: {app}; Flags: skipifsourcedoesntexist
Source: Data\*; DestDir: {app};
Source: Data\audio\*; DestDir: {app}\audio;
Source: Data\bearer\*; DestDir: {app}\bearer;
Source: Data\iconengines\*; DestDir: {app}\iconengines;
Source: Data\imageformats\*; DestDir: {app}\imageformats;
Source: Data\lang\*; DestDir: {app}\lang;
Source: Data\mediaservice\*; DestDir: {app}\mediaservice;
Source: Data\platforms\*; DestDir: {app}\platforms;
Source: Data\printsupport\*; DestDir: {app}\printsupport;
Source: Data\sound\*; DestDir: {app}\sound;
Source: Data\sqldrivers\*; DestDir: {app}\sqldrivers;
Source: Data\style\*; DestDir: {app}\style;
Source: Data\styles\*; DestDir: {app}\styles;

[Icons]
Name: {group}\{#_AppName}; Filename: {app}\{#_AppName}.exe; WorkingDir: {app}
Name: {userdesktop}\{#_AppName}; Filename: {app}\{#_AppName}.exe; WorkingDir: {app}
Name: {group}\{cm:UninstallProgram, {#_AppName}}; Filename: {uninstallexe}

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
Name: "cs"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "nl"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "it"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "pl"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "uk"; MessagesFile: "compiler:Languages\Ukrainian.isl"
Name: "fi"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "sl"; MessagesFile: "compiler:Languages\Slovenian.isl"

[INI]
Filename: {app}\{#_AppName}.url; Section: InternetShortcut; Key: URL; String: http://quiterss.org

[InstallDelete]
Type: files; Name: {app}\*dll
Type: filesandordirs; Name: {app}\audio
Type: filesandordirs; Name: {app}\bearer
Type: filesandordirs; Name: {app}\iconengines
Type: filesandordirs; Name: {app}\imageformats
Type: filesandordirs; Name: {app}\lang
Type: filesandordirs; Name: {app}\mediaservice
Type: filesandordirs; Name: {app}\platforms
Type: filesandordirs; Name: {app}\printsupport
Type: filesandordirs; Name: {app}\sqldrivers
Type: filesandordirs; Name: {app}\styles

[UninstallDelete]
Type: filesandordirs; Name: {app}

[Run]
Filename: "{app}\{#_AppName}.exe"; Description: "{cm:LaunchProgram,{#StringChange(_AppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent

