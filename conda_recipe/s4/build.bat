@echo on
REM --- Set environment variables ---
set SRC_DIR=%CD%
set OBJDIR=%SRC_DIR%\conda_recipe\s4\build
set CONDA_INC=%BUILD_PREFIX%\Library\include
set CONDA_LIB=%BUILD_PREFIX%\Library\lib

echo ren .c to .cpp: %SRC_DIR%\S4\main_python.c
ren "%SRC_DIR%\S4\main_python.c" main_python.cpp

REM --- Activate MSVC (may need hardcoded path if VSINSTALLDIR is undefined) ---
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Auxiliary\Build\vcvars64.bat"
echo cl
cl

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

set DISTUTILS_USE_SDK=1
set MSSdk=1

REM --- Build and install the wheel ---
echo PYTHON: %PYTHON%
%PYTHON% -m pip wheel "%SRC_DIR%\conda_recipe\s4" -w dist --verbose

REM --- Find the built wheel ---
for %%f in (dist\*.whl) do set WHEEL=%%f

REM --- Install the wheel if found ---
if defined WHEEL (
    %PYTHON% -m pip install "%WHEEL%" --no-deps -vv
) else (
    echo ERROR: No wheel file found in dist\
    exit /b 1
)

