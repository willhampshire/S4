"""
Shim setup.py, remove redundant gensetup.py.sh in favour of this file.
Uses config in setup.cfg (toml file)

Win:

Uses precompiled lib file, which should contain paths to .obj files from Makefile
e.g. run lib /LIST conda_recipe\s4\libS4.lib (lib.exe is part of VS build tools, available in Developer CMD,
    or by activating vcvars64 etc.)
and observe:

C:\...\S4\conda_recipe\s4\build\S4k\S4.obj
C:\...\S4\conda_recipe\s4\build\S4k\rcwa.obj
...
boost_serialization.dll

Then, setup.py compiles main_python, using the functions in the lib file, to a Python package.

Unix:

Same largely but with .a/.o instead of .lib/.obj. Compilation is more forgiving.

"""

from setuptools import setup, Extension
import os
import sys
import numpy
from pathlib import Path


SRC_DIR = Path(os.environ.get("SRC_DIR", "."))
BUILD_PREFIX = Path(os.environ.get("BUILD_PREFIX", "."))
# use pathlib to normalise all paths for different OS avoiding mixed slashes etc

sys_extra_compile_args: list[str]
extra_link_args: list[str]
package_data: dict
sources: list
libraries: list

if sys.platform == "win32":
    sys_extra_compile_args = ['/O2', '/MD', '/EHsc', "/DBOOST_ALL_NO_LIB"]  # MD - dynamic, boost no lib - disable auto linking
    package_data = {"": ["libS4.lib"]} # win compiles to .lib
    sources=[str(SRC_DIR / "S4" / "main_python.cpp")] # win requires cpp compilation
    libraries = [
        "S4",
        "mkl_rt",
        "cholmod",
        "amd",
        "colamd",
        "camd",
        "ccolamd",
        "suitesparseconfig",
        "metis",
        "boost_serialization",
        "libboost_exception",
    ]
    # extra_link_args = [str(BUILD_PREFIX / "Library" / "lib" / "libboost_serialization.lib"),
    #                     str(BsUILD_PREFIX / "Library" / "lib" / "cholmod.lib")]
    
else:
    sys_extra_compile_args=["-Wall", "-O3", "-fPIC"]
    package_data = {"": ["libS4.a"]} # unix compiles to .a
    sources=[str(SRC_DIR / "S4" / "main_python.cpp")]
    libraries = ["S4", "boost_serialization", "cholmod", "stdc++"]

ext_modules = [
    Extension(
        "S4", # Python import module name
        sources=sources,
        include_dirs=[
            str(SRC_DIR / "S4"),
            str(SRC_DIR / "S4" / "RNP"),
            str(SRC_DIR / "S4" / "kiss_fft"),
            str(SRC_DIR / "S4" / "fmm"),
            str(SRC_DIR / "S4" / "pattern"),
            numpy.get_include(),
            str(BUILD_PREFIX / "include"),
        ],
        library_dirs=[
            str(SRC_DIR / "conda_recipe" / "s4"),
            str(BUILD_PREFIX / "Library" / "lib"),
        ],
        libraries=libraries,  # S4 => libS4.a
        extra_compile_args=sys_extra_compile_args,
        # extra_link_args=extra_link_args,
        # define_macros=[("BOOST_ALL_NO_LIB", None)],
    )
]

setup(
    ext_modules=ext_modules,
    package_data=package_data,
)
