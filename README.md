# S4 RCWA Solver
See http://fan.group.stanford.edu/S4/ and https://s4utils.readthedocs.io for information about the package.
This fork enables usage of newer Python versions, 3.10 and 3.12, that previous builds do not.
Refer to `willhampshire` in place of `paulgoulain` when installing conda package as in the above.

## Installation instructions
Conda package created due to platform independence.
- Create new conda environment using `conda create -n s4-venv-name python=3.12` (3.10 to 3.12 available)
- `conda activate s4-venv-name`
- `conda install -c willhampshire s4`

Install in a new environment to avoid incompatabilities as above.
Refer to `marcus-o`'s [repo](https://github.com/marcus-o/S4) for more info.

## Manual local installation

See above repos / original forked repos for detailed instructions.
The Makefile will need paths adjusting - I only adjusted the conda recipe.


## Developer Build Instructions

### Windows

Install Visual Studio developer tools to access ```nmake```, ```cl``` and ```lib```.
Create ```conda create -n "build-env" python=3.12```.
Activate build-env.
Requires ```conda install``` of:
- ```boost``` 
- ```boost-cpp``` from default channel (gets static .lib called libboost_serialization.lib)
- ```libarchive``` from conda-forge channel
- ```setuptools```
- ```wheel```
- ```suitesparse```
- ```conda-build```
  
Configure VS build tools file location in ```build.bat```, if using different version.
Run the commands in the build script manually to check filepaths and tools are installed.
Verify valid contents of .lib files using ```lib /LIST <.lib file>```, where to use lib, 
build tools must be activated (open Developer Command Prompt or run the ```vcvars__``` file manually).

To build the conda packages, run ```conda build conda_recipe\s4```.


## Patch Notes

- Rewrote build config PEP 517/518
- Compilation on Windows now works, after configuring a conda env as above (which instances of each tool being used in build needs verifying)
- Updated some int to size_t in RNP/TLASupport.h ApplyElementaryReflectorBlocked


## Problems

- When compiling on Windows, RCWA produces NaN values when providing anisotropic tensor; 
```
S.SetMaterial(Name ='Mat'+str(m+1), Epsilon = ((permittivity_xx[lb,m], 0, 0),
                                                (0, permittivity_yy[lb,m], 0),
                                                (0, 0, permittivity_zz[lb,m])
                                                ))
```

## Misc

```
mber of files: 8
   INFO: sysroot: 'C:/Windows/' files: '['win.ini', 'twain_32/wiatwain.ds', 'twain_32.dll', 'system.ini']'
WARNING (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO Library/bin/boost_serialization.dll found in ['defaults/win-64::libboost==1.8]
WARNING (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): .. but ['defaults/win-64::libboost==1.82.0=h3399ecb_2'] not in reqs/run, (i.e. it is ove)
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/MSVCP140.dll found in $SYSROOT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO python312.dll found in defaults/win-64::python==3.12.11=h716150d_0
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/KERNEL32.dll found in $SYSROOT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/VCRUNTIME140.dll found in $SYSROOT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/VCRUNTIME140_1.dll found in $SYSROOT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/downlevel/api-ms-win-crt-heap-l1-1-0.dll found in $SYSROOT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/downlevel/api-ms-win-crt-stdio-l1-1-0.dll found in $SYSROT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/downlevel/api-ms-win-crt-string-l1-1-0.dll found in $SYSRT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/downlevel/api-ms-win-crt-math-l1-1-0.dll found in $SYSROOT
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/downlevel/api-ms-win-crt-runtime-l1-1-0.dll found in $SYST
   INFO (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO C:/Windows/System32/downlevel/api-ms-win-crt-utility-l1-1-0.dll found in $SYST
WARNING (s4): plugin library (Python) package defaults/win-64::mkl-service==2.4.0=py312h827c3e9_3 in requirements/run but it is not used (i.e. )
WARNING (s4): run-exports library package defaults/win-64::suitesparse==7.8.3=h8cb7590_0 in requirements/run but it is not used (i.e. it is ove)
WARNING (s4): dso library package defaults/win-64::mkl==2025.0.0=h5da7b33_930 in requirements/run but it is not used (i.e. it is overdepending )
```


```
 C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\_h_env\Lib\site-packages\numpy\core\include\numpy\npy_1_7_deprecated_api.h(14N
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(328): warning C4244: '=': conversion from 'Py_ssize_ta
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(466): warning C4244: '=': conversion from 'Py_ssize_ta
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(505): warning C4244: '=': conversion from 'Py_ssize_ta
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(528): warning C4244: '=': conversion from 'Py_ssize_ta
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(635): warning C4244: 'argument': conversion from 'Py_a
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(673): warning C4101: 'err': unreferenced local variabe
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(685): warning C4101: 'err': unreferenced local variabe
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(1164): warning C4101: 'ret': unreferenced local variae
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(1541): warning C4267: '=': conversion from 'size_t' ta
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(1551): warning C4244: '=': conversion from 'Py_ssize_a
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(1552): warning C4244: '=': conversion from 'Py_ssize_a
  C:\Users\WilliamHampshire\miniconda3\conda-bld\s4_1758060030514\work\S4\main_python.cpp(2179): warning C4101: 'layerName': unreferenced locale
```


```
numalloc.c
S4\numalloc.c(25): warning C4273: '_aligned_malloc': inconsistent dll linkage
C:\Program Files (x86)\Windows Kits\10\include\10.0.26100.0\ucrt\corecrt_malloc.h(154): note: see previous definition of '_aligned_malloc'      
S4\numalloc.c(26): warning C4273: '_aligned_free': inconsistent dll linkage
C:\Program Files (x86)\Windows Kits\10\include\10.0.26100.0\ucrt\corecrt_malloc.h(148): note: see previous definition of '_aligned_free'  
```

```
rcwa.cpp
S4\rcwa.cpp(332): warning C4244: 'argument': conversion from 'size_t' to 'const std::complex<double>::_Ty', possible loss of data
S4\rcwa.cpp(515): warning C4244: 'argument': conversion from 'size_t' to 'const std::complex<double>::_Ty', possible loss of data
S4\rcwa.cpp(807): warning C4244: 'argument': conversion from 'const size_t' to 'const std::complex<double>::_Ty', possible loss of data
S4\rcwa.cpp(1638): warning C4267: 'initializing': conversion from 'size_t' to 'int', possible loss of data
S4\rcwa.cpp(1638): warning C4267: 'initializing': conversion from 'size_t' to 'const int', possible loss of data
S4\rcwa.cpp(1639): warning C4267: 'initializing': conversion from 'size_t' to 'int', possible loss of data
S4\rcwa.cpp(1639): warning C4267: 'initializing': conversion from 'size_t' to 'const int', possible loss of data
S4\rcwa.cpp(1742): warning C4267: 'initializing': conversion from 'size_t' to 'int', possible loss of data
S4\rcwa.cpp(1742): warning C4267: 'initializing': conversion from 'size_t' to 'const int', possible loss of data
S4\rcwa.cpp(1743): warning C4267: 'initializing': conversion from 'size_t' to 'int', possible loss of data
S4\rcwa.cpp(1743): warning C4267: 'initializing': conversion from 'size_t' to 'const int', possible loss of data
```