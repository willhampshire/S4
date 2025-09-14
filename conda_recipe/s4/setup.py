"""
Shim setup.py, remove redundant gensetup.py.sh in favour of static file.
setup() call uses config in setup.cfg (toml file)
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
package_data: dict
sources: list

if sys.platform == "win32":
    sys_extra_compile_args = ['/O2', '/EHsc', "-DBOOST_ALL_NO_LIB"]  # MSVC optimization flag
    package_data = {"": ["libS4.lib"]} # win compiles to .lib
    sources=[str(SRC_DIR / "S4" / "main_python.cpp")]
    
else:
    sys_extra_compile_args=["-Wall", "-O3", "-fPIC"]
    package_data = {"": ["libS4.a"]} # unix compiles to .a
    sources=[str(SRC_DIR / "S4" / "main_python.c")]

ext_modules = [
    Extension(
        "S4",
        sources=sources,
        include_dirs=[
            str(SRC_DIR / "S4"),
            str(SRC_DIR / "S4" / "RNP"),
            str(SRC_DIR / "S4" / "kiss_fft"),
            numpy.get_include(),
            str(BUILD_PREFIX / "include"),
        ],
        library_dirs=[
            str(SRC_DIR / "conda_recipe" / "s4"),
            str(BUILD_PREFIX / "lib"),
        ],
        libraries=["S4", "boost_serialization", "cholmod"],  # S4 => libS4.a
        extra_compile_args=sys_extra_compile_args,
    )
]

setup(
    ext_modules=ext_modules,
    package_data=package_data,
)
