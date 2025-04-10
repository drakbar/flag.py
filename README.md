# flag.py

This is a python wrapper for [flag.h](https://github.com/tsoding/flag.h)
Currently, linux-only as it loads `glibc` at runtime, mingw might make it portable but it is untested.

## Building

### Building [flag.h](https://github.com/tsoding/flag.h) as shared library

Being a python wrapper around the header only library, first grab the `C source`. It is a submodule of this project in the `external` folder.
```shell
make submodule
```

Once the code is cloned everything is ready to build the shared library. Run one of the following `make` recipes.
```shell
make shared
```
or just
```shell
make
```
`libflag.so` should be located at `flag/lib/`.

### Building wheel
Once all `C` dependencies have been resolved the python wheel can be constructed. The `python` env requires `setuptools build` packages in order to construct the wheel. Once the toolchain is in place, execute the following:
```shell
make whl
```
There should be a wheel located at `dist/`.

## Acknowledgements

[Alexey Kutepov (Tsoding)](https://github.com/tsoding)