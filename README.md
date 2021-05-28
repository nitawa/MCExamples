# MCExamples
using MEDCOUPLING C++


Windows build
-------------

```
 configure MEDCOUPLING RUNTIME environment
 configure Visual Studio 2017 environment
 call "C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
 cmake -DMEDCOUPLING_ROOT_DIR=%MEDCOUPLING_ROOT_DIR% -DCMAKE_INSTALL_PREFIX=..\W64 -DCMAKE_BUILD_TYPE=Release -DCMAKE_GENERATOR:STRING="Visual Studio 15 2017 Win64" ..
 msbuild  /p:Configuration=Release /p:Platform=x64 ALL_BUILD.vcxproj
 msbuild  /p:Configuration=Release /p:Platform=x64 INSTALL.vcxproj

```
