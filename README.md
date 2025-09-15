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
- Compilation on Windows now works, after configuring a conda env as above
- Updated some int to size_t in RNP/TLASupport.h ApplyElementaryReflectorBlocked

