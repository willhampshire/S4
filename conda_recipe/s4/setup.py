"""
Shim setup.py, remove redundant gensetup.py.sh in favour of static file
"""

from setuptools import setup, Extension
import os
import numpy
from pathlib import Path


SRC_DIR = Path(os.environ.get("SRC_DIR", "."))
BUILD_PREFIX = Path(os.environ.get("BUILD_PREFIX", "."))
# use pathlib to normalise all paths for different OS avoiding mixed slashes etc

ext_modules = [
    Extension(
        "S4",
        sources=[str(SRC_DIR / "S4" / "main_python.c")],
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
        extra_compile_args=["-Wall", "-O3", "-fPIC"],
    )
]

setup(
    name="s4",
    version="1.1",
    ext_modules=ext_modules,
)
