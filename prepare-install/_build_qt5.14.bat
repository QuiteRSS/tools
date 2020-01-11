set QTDIR=C:\Qt\5.14.0\msvc2017
set PATH=C:\Qt\5.14.0\msvc2017\bin;C:\Qt\Tools\QtCreator\bin;C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.16.27023\bin\HostX86\x86;%PATH%
set INCLUDE=C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.16.27023\include;C:\Program Files (x86)\Windows Kits\10\include\10.0.18362.0\ucrt;C:\Program Files (x86)\Windows Kits\10\include\10.0.18362.0\shared;C:\Program Files (x86)\Windows Kits\10\include\10.0.18362.0\um;C:\Program Files (x86)\Windows Kits\10\include\10.0.18362.0\winrt;C:\Program Files (x86)\Windows Kits\10\include\10.0.18362.0\cppwinrt
set LIB=C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\VC\Tools\MSVC\14.16.27023\lib\x86;C:\Program Files (x86)\Windows Kits\10\lib\10.0.18362.0\ucrt\x86;C:\Program Files (x86)\Windows Kits\10\lib\10.0.18362.0\um\x86;
python prepare-install_qt5.14.py --build
