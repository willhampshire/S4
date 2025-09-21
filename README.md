# S4 RCWA Solver

This fork purely focuses on Python extension - Lua and R are ignored.

## Description

See http://fan.group.stanford.edu/S4/ (auth. Victor Liu) and https://s4utils.readthedocs.io (auth. Paul Goulain) for information about the package.
This fork compiles Python extension for newer Python versions, 3.10 through 3.12, that previous builds do not.
It is currently pre-compiled to conda package for Windows and Intel Mac, and available on my conda channel;
refer to `willhampshire` in place of `paulgoulain` when installing conda package as in the above docs, or see below.

## Installation instructions

Conda package created due to platform independence. Currently compiled for WIN and OSX.

- Create new conda environment, `conda create -n s4-venv-name python=3.12` (3.10 to 3.12 compatible)
- `conda activate s4-venv-name`
- `conda install -c willhampshire s4`

It is possible to run into dependancy issues with `numpy`, in which case simply install the required version before installing `s4` again.

## Developer Build Instructions

### Windows

Install Visual Studio developer tools to access ```nmake```, ```cl``` and ```lib```.
Create ```conda create -n "build-env" python=3.12```.
Activate build-env.

My working conda build environment uses the following packages (`conda list`):

| Name                   | Version   | Build                     | Channel       |
|------------------------|-----------|----------------------------|----------------|
| boost                  | 1.82.0    | hd42ba9a_3                | conda-forge    |
| boost-cpp              | 1.82.0    | h92ca6c8_2                | conda-forge    |
| bzip2                  | 1.0.8     | h2bbff1b_6                |                |
| ca-certificates        | 2025.9.9  | haa95532_0                |                |
| expat                  | 2.7.1     | h8ddb27b_0                |                |
| libarchive             | 3.8.1     | h815d515_0                |                |
| libblas                | 3.9.0     | 35_h5709861_mkl           | conda-forge    |
| libboost-headers       | 1.82.0    | h57928b3_3                | conda-forge    |
| libboost-python        | 1.82.0    | py312h4f1204c_3           | conda-forge    |
| libboost-python-devel  | 1.82.0    | py312hd42ba9a_3           | conda-forge    |
| libcblas               | 3.9.0     | 35_h2a3cdd5_mkl           | conda-forge    |
| libexpat               | 2.7.1     | hac47afa_0                | conda-forge    |
| libffi                 | 3.4.4     | hd77b12b_1                |                |
| libhwloc               | 2.12.1    | default_h88281d1_1000     | conda-forge    |
| libiconv               | 1.16      | h2bbff1b_3                |                |
| liblapack              | 3.9.0     | 35_hf9ab0e9_mkl           | conda-forge    |
| libsqlite              | 3.50.4    | hf5d6505_0                | conda-forge    |
| libwinpthread          | 12.0.0.r4.gg4f2fc60ca | h57928b3_9     | conda-forge    |
| libxml2                | 2.13.8    | h866ff63_0                |                |
| libzlib                | 1.3.1     | h02ab6af_0                |                |
| llvm-openmp            | 20.1.8    | hfa2b4ca_2                | conda-forge    |
| lz4-c                  | 1.9.4     | h2bbff1b_1                |                |
| metis                  | 5.2.1     | hcfcfb64_0                | conda-forge    |
| mkl                    | 2024.2.2  | h57928b3_16               | conda-forge    |
| numpy                  | 1.26.4    | py312h8753938_0           | conda-forge    |
| openssl                | 3.5.3     | h725018a_0                | conda-forge    |
| pip                    | 25.2      | pyhc872135_0              |                |
| python                 | 3.12.7    | hce54a09_0_cpython        | conda-forge    |
| python_abi             | 3.12      | 8_cp312                   | conda-forge    |
| setuptools             | 78.1.1    | py312haa95532_0           |                |
| sqlite                 | 3.50.2    | hda9a48d_1                |                |
| tbb                    | 2021.13.0 | h18a62a1_3                | conda-forge    |
| tk                     | 8.6.15    | hf199647_0                |                |
| tzdata                 | 2025b     | h04d1e81_0                |                |
| ucrt                   | 10.0.22621.0 | haa95532_0            |                |
| vc                     | 14.3      | h2df5915_10               |                |
| vc14_runtime           | 14.44.35208 | h4927774_10           |                |
| vs2015_runtime         | 14.44.35208 | ha6b5a95_10           |                |
| vs2015_win-64          | 14.0.25420 | h55c1224_11           |                |
| wheel                  | 0.45.1    | py312haa95532_0           |                |
| xz                     | 5.6.4     | h4754444_1                |                |
| zlib                   | 1.3.1     | h02ab6af_0                |                |
| zstd                   | 1.5.7     | h56299aa_0                |                |

Most of these are automatically installed when creating the environment. 

Configure VS build tools file location in ```build.bat```, if using different version.
Run the commands in the build script manually to check filepaths and tools are installed.
Verify valid contents of .lib files using ```lib /LIST <.lib file>```, where to use lib, 
build tools must be activated (open Developer Command Prompt or run the ```vcvars__``` file manually).

To build the conda packages, run ```conda build conda_recipe\s4```.

### Mac (Intel tested)

Like Windows, initialise the conda environment.

PASTE DEPS HERE


## Patch Notes

- Rewrote build config PEP 517/518
- Change main file to C++
- Compilation on Windows works after configuring a conda env appropriately
- Updated some int to size_t in RNP/TLASupport.h ApplyElementaryReflectorBlocked
- Changed conditional logic on pointers in Simulation_ComputeLayerSolution, Simulation_GetLayerSolution
- Sorted eigenvalues for least evanescent solutions
- Rewrote SolveInterior(RCWA.cpp)
- Added LAPACK flag to Makefile.win, to use MKL (should add flag to Makefile.unix for equivalent tool)
- Other debugging


## Fixed issues

- Eigensolver not working on Windows. May have been due to: eigenvalue solver solution ordering, null pointers, not defining to use LAPACK in compilation flags
- Compilation issues MSVC. Cannot import files including C++ from a C main file.

## Future work

Ironing out compilation warnings would be sensible. These may be specific to my build environment.
There are several C++ warnings from the legacy code, such as 

```
S4\RNP\Eigensystems.cpp(4331): warning C4267: 'argument': conversion from 'size_t' to 'int', possible loss of data
S4\RNP\Eigensystems.cpp(4331): warning C4267: '=': conversion from 'size_t' to 'int', possible loss of data
S4\fmm\fmm_PolBasisVL.cpp(216): warning C4996: 'strcpy': This function or variable may be unsafe. Consider using strcpy_s instead.
%SRC_DIR%\S4\fmm\../RNP/TBLAS.h(1682): warning C4127: conditional expression is constant
%SRC_DIR%\S4\fmm\../RNP/TBLAS.h(1675): warning C4127: conditional expression is constant
S4\pattern\predicates.c(700): warning C4131: 'grow_expansion': uses old-style declarator
%SRC_DIR%\S4\pattern\predicates.c(2960) : warning C4701: potentially uninitialized local variable 'axtbclen' used
```


```
WARNING (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): Needed DSO Library/bin/boost_serialization.dll found in ['defaults/win-64::libb]
WARNING (s4,Lib/site-packages/S4.cp312-win_amd64.pyd): .. but ['defaults/win-64::libboost==1.82.0=h3399ecb_2'] not in reqs/run
```

```
mkl_rt.lib(mkl_rt.2.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll); second definition d
cholmod.lib(cholmod.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll); second definition d
amd.lib(amd.dll) : warning LNK4006: __imp___isa_available_default already defined in cholmod.lib(cholmod.dll); second definition ignord
amd.lib(amd.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll); second definition ignored  
colamd.lib(colamd.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll); second definition igd
camd.lib(camd.dll) : warning LNK4006: __imp___isa_available_default already defined in cholmod.lib(cholmod.dll); second definition ignd
camd.lib(camd.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll); second definition ignored
ccolamd.lib(ccolamd.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll); second definition d
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: __imp_printf already defined in cholmod.lib(cholmod.dll); second defind
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition d
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: __imp__vfprintf_l already defined in cholmod.lib(cholmod.dll); second d
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definid
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: __imp___local_stdio_printf_options already defined in cholmod.lib(chold
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dld
suitesparseconfig.lib(suitesparseconfig.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.dll)d
metis.lib(balance.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiod
metis.lib(balance.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(balance.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(balance.c.obj) : warning LNK4006: fabsf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(checkgraph.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definid
metis.lib(checkgraph.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored      
metis.lib(checkgraph.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(coarsen.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiod
metis.lib(coarsen.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(coarsen.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(compress.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitid
metis.lib(compress.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored        
metis.lib(compress.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(contig.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(contig.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(contig.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(debug.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition d
metis.lib(debug.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(debug.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(fm.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignd
metis.lib(fm.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(fm.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(graph.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition d
metis.lib(graph.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(graph.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(graph.c.obj) : warning LNK4006: _vsnprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(graph.c.obj) : warning LNK4006: _vsprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(graph.c.obj) : warning LNK4006: sprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(initpart.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitid
metis.lib(initpart.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored        
metis.lib(initpart.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(kmetis.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(kmetis.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(kmetis.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(kwayfm.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(kwayfm.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(kwayfm.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(mcutil.c.obj) : warning LNK4006: fabsf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(mesh.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition id
metis.lib(mesh.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(mesh.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(minconn.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiod
metis.lib(minconn.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(minconn.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(mincover.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitid
metis.lib(mincover.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored        
metis.lib(mincover.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(ometis.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(ometis.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(ometis.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(options.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiod
metis.lib(options.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(options.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(parmetis.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitid
metis.lib(parmetis.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored        
metis.lib(parmetis.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(pmetis.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(pmetis.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(pmetis.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(separator.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitd
metis.lib(separator.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored       
metis.lib(separator.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(sfm.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition igd
metis.lib(sfm.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(sfm.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(stat.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition id
metis.lib(stat.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(stat.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(timing.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(timing.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(timing.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(wspace.c.obj) : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definitiond
metis.lib(wspace.c.obj) : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
metis.lib(wspace.c.obj) : warning LNK4006: printf already defined in cholmod.lib(cholmod.dll); second definition ignored
boost_serialization.lib(boost_serialization.dll) : warning LNK4006: __NULL_IMPORT_DESCRIPTOR already defined in mkl_rt.lib(libimalloc.d
cubature.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignored    
cubature.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
cubature.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
kiss_fftnd.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignored  
kiss_fftnd.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
kiss_fftnd.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
numalloc.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignored    
numalloc.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
numalloc.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
fmm_PolBasisJones.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition id
fmm_PolBasisJones.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
fmm_PolBasisJones.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
fmm_PolBasisVL.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignod
fmm_PolBasisVL.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
fmm_PolBasisVL.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
fmm_PolBasisNV.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignod
fmm_PolBasisNV.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
fmm_PolBasisNV.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
rcwa.obj : warning LNK4006: "int __cdecl RNP::Eigensystem(unsigned __int64,class std::complex<double> *,unsigned __int64,class std::cod
S4.obj : warning LNK4006: __local_stdio_printf_options already defined in cholmod.lib(cholmod.dll); second definition ignored
S4.obj : warning LNK4006: _vfprintf_l already defined in cholmod.lib(cholmod.dll); second definition ignored
S4.obj : warning LNK4006: fprintf already defined in cholmod.lib(cholmod.dll); second definition ignored
S4.obj : warning LNK4006: "private: virtual int __cdecl boost::archive::codecvt_null<wchar_t>::do_encoding(void)const " (?do_encoding@d
S4.obj : warning LNK4006: "private: virtual bool __cdecl boost::archive::codecvt_null<wchar_t>::do_always_noconv(void)const " (?do_alwd
S4.obj : warning LNK4006: "private: virtual int __cdecl boost::archive::codecvt_null<wchar_t>::do_max_length(void)const " (?do_max_lend
S4.obj : warning LNK4006: "public: void __cdecl boost::archive::codecvt_null<wchar_t>::`default constructor closure'(void)" (??_F?$codd
S4.obj : warning LNK4006: "private: bool & __cdecl boost::serialization::singleton_module::get_lock(void)" (?get_lock@singleton_moduled
S4.obj : warning LNK4006: "public: void __cdecl boost::serialization::singleton_module::lock(void)" (?lock@singleton_module@serializatd
S4.obj : warning LNK4006: "public: void __cdecl boost::serialization::singleton_module::unlock(void)" (?unlock@singleton_module@seriald
S4.obj : warning LNK4006: "public: bool __cdecl boost::serialization::singleton_module::is_locked(void)" (?is_locked@singleton_module@d
```