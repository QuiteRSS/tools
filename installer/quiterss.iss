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
DefaultDirName={pf}\{#_AppName}
DefaultGroupName={#_AppName}
Compression=lzma/Max
InternalCompressLevel=Max
SolidCompression=true
VersionInfoCompany={#_AppPublisher}
VersionInfoDescription={#_AppName} {#_AppVerName} Setup
MinVersion=5.0.2195
AppPublisherURL=http://code.google.com/p/quite-rss/
WizardImageFile=logo.bmp
WizardSmallImageFile=logo55.bmp
WizardImageStretch=false
WizardImageBackColor=clWhite
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
Source: Data\codecs\*; DestDir: {app}\codecs;
Source: Data\iconengines\*; DestDir: {app}\iconengines;
Source: Data\imageformats\*; DestDir: {app}\imageformats;
Source: Data\lang\*; DestDir: {app}\lang;
Source: Data\phonon_backend\*; DestDir: {app}\phonon_backend;
Source: Data\sound\*; DestDir: {app}\sound;
Source: Data\sqldrivers\*; DestDir: {app}\sqldrivers;
Source: Data\style\*; DestDir: {app}\style;

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
Name: "el"; MessagesFile: "compiler:Languages\Greek.isl"
Name: "hu"; MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "it"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "pl"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "pt_BR"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "sr"; MessagesFile: "compiler:Languages\SerbianCyrillic.isl"
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "uk"; MessagesFile: "compiler:Languages\Ukrainian.isl"
Name: "fi"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "sl"; MessagesFile: "compiler:Languages\Slovenian.isl"

[INI]
Filename: {app}\{#_AppName}.url; Section: InternetShortcut; Key: URL; String: http://code.google.com/p/quite-rss/

[UninstallDelete]
Type: files; Name: {app}\{#_AppName}.url

[Run]
Filename: "{app}\{#_AppName}.exe"; Description: "{cm:LaunchProgram,{#StringChange(_AppName, "&", "&&")}}"; Flags: nowait postinstall skipifsilent

