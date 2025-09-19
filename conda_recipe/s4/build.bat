@echo on
REM --- Set environment variables ---
set SRC_DIR=%CD%
set OBJDIR=%SRC_DIR%\conda_recipe\s4\build
set CONDA_INC=%BUILD_PREFIX%\Library\include
set CONDA_LIB=%BUILD_PREFIX%\Library\lib

REM --- Activate MSVC (may need hardcoded path if VSINSTALLDIR is undefined) ---
@REM call %VSINSTALLDIR%\VC\Auxiliary\Build\vcvars64.bat
cd C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build
call vcvars64.bat
cd %SRC_DIR%

echo cl.exe
where cl.exe
echo link.exe
where link.exe

REM --- Build using nmake ---
cd %SRC_DIR%
nmake /f conda_recipe\s4\Makefile.win SRC_DIR=%CD%

REM --- Copy output lib ---
copy /Y %SRC_DIR%\conda_recipe\s4\build\libS4.lib %SRC_DIR%\conda_recipe\s4\
ren "%SRC_DIR%\conda_recipe\s4\libS4.lib" S4.lib

REM --- Clean up any Unix-style build flags ---
echo CFLAGS: %CFLAGS%
echo CPPFLAGS: %CPPFLAGS%
echo LDFLAGS: %LDFLAGS%

@REM set CPPFLAGS=/DBOOST_ALL_NO_LIB
@REM set CFLAGS=/DBOOST_ALL_NO_LIB

set DISTUTILS_USE_SDK=1
set MSSdk=1

REM exit with success
exit /b 0
