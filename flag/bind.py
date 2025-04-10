from ctypes import (
    c_bool, c_char_p, c_int, c_size_t, c_uint64, c_void_p,
    POINTER, string_at
)
import io, sys, typing
from functools import singledispatch


from .context import *
ctx = LibFlagContext()


"""
    char* flag_name(void *val)
"""
ctx.lib.flag_name.argtypes = [c_void_p]
ctx.lib.flag_name.restype  = c_char_p

def name(value: typing.Any) -> str:
    c_name = ctx.lib.flag_name(c_void_p(value))
    return c_name.value.decode()


"""
    bool* flag_bool(const char *name, bool def, const char *desc)
"""
ctx.lib.flag_bool.argtypes = [c_char_p, c_bool, c_char_p]
ctx.lib.flag_bool.restype  = POINTER(c_bool)

def bool(name: str, default: bool, desc: str) -> FlagBool:
    c_name = bytes(name, encoding = ctx.encoding)
    c_desc = bytes(desc, encoding = ctx.encoding)

    # need to cache a long lived ref to the bytes
    ctx.cache.append(c_name)
    ctx.cache.append(c_desc)

    boolean = FlagBool(ctx.lib.flag_bool(c_name, default, c_desc))
    return boolean


"""
    uint64_t* flag_uint64(const char *name, uint64_t def, const char *desc)
"""
ctx.lib.flag_uint64.argtypes = [c_char_p, c_uint64, c_char_p]
ctx.lib.flag_uint64.restype  = POINTER(c_uint64)

def uint64(name: str, default: int, desc: str) -> FlagUint64:
    c_name = bytes(name, encoding = ctx.encoding)
    c_desc = bytes(desc, encoding = ctx.encoding)

    # need to cache a long lived ref to the bytes
    ctx.cache.append(c_name)
    ctx.cache.append(c_desc)

    uint64 = FlagUint64(ctx.lib.flag_uint64(c_name, default, c_desc))
    return uint64


"""
    size_t* flag_size(const char *name, uint64_t def, const char *desc)
"""
ctx.lib.flag_size.argtypes = [c_char_p, c_uint64, c_char_p]
ctx.lib.flag_size.restype  = POINTER(c_size_t)

def size(name: str, default: int, desc: str) -> FlagSizeT:
    c_name = bytes(name, encoding = ctx.encoding)
    c_desc = bytes(desc, encoding = ctx.encoding)

    # need to cache a long lived ref to the bytes
    ctx.cache.append(c_name)
    ctx.cache.append(c_desc)

    size_t = FlagSizeT(ctx.lib.flag_size(c_name, default, c_desc))
    return size_t


"""
    char** flag_str(const char *name, const char *def, const char *desc)
"""
ctx.lib.flag_str.argtypes = [c_char_p, c_char_p, c_char_p]
ctx.lib.flag_str.restype  = POINTER(c_char_p)

def str(name: str, default: str, desc: str) -> FlagStr:
    c_name = bytes(name,    encoding = ctx.encoding)
    c_def  = bytes(default, encoding = ctx.encoding)
    c_desc = bytes(desc,    encoding = ctx.encoding)

    # need to cache a long lived ref to the bytes
    ctx.cache.append(c_name)
    ctx.cache.append(c_def)
    ctx.cache.append(c_desc)

    c_str = FlagStr(ctx.lib.flag_str(c_name, c_def, c_desc))
    return c_str


"""
    bool flag_parse(int argc, char **argv)
"""
ctx.lib.flag_parse.argtypes = [c_int, POINTER(c_char_p)]
ctx.lib.flag_parse.restype  = c_bool

def parse(argc: int, argv: typing.List[str]) -> bool:
    # need to cache a long lived ref to the array of bytes
    ctx.argv = (c_char_p * len(argv))()

    for i, py_str in enumerate(argv):
        c_str = bytes(py_str, encoding = ctx.encoding)
        ctx.argv[i] = c_str

    return ctx.lib.flag_parse(argc, ctx.argv)


"""
    int flag_rest_argc(void)
"""
ctx.lib.flag_rest_argc.argtypes = []
ctx.lib.flag_rest_argc.restype  = c_int

def rest_argc() -> int:
    return ctx.lib.flag_rest_argc()


"""
    char** flag_rest_argv(void);
"""
ctx.lib.flag_rest_argv.argtypes = []
ctx.lib.flag_rest_argv.restype  = POINTER(c_char_p)

def rest_argv() -> typing.List[str]:
    c_argc = ctx.lib.flag_rest_argc()
    c_argv = ctx.lib.flag_rest_argv()

    argv = []

    for i in range(c_argc):
        char_ptr = c_argv[i]                      # dereference the pointer to get char*
        if not char_ptr: break                    # check for null termination
        argv.append(string_at(char_ptr).decode()) # convert the char* to a python bytes
    return argv


"""
    in order to pass FILE* to functions from objects such as
    sys.stdout, and sys.stderr a lower level libc function 
    [fdopen, fopen] needs to be available to retrieve those pointers.
"""

ctx.libc.fdopen.argtypes = [c_int, c_char_p]
ctx.libc.fdopen.restype  = POINTER(c_void_p)

ctx.libc.fopen.argtypes = [c_char_p, c_char_p]
ctx.libc.fopen.restype  = POINTER(c_void_p)

"""
    void flag_print_error(FILE *stream)
"""
ctx.lib.flag_print_error.argtypes = [POINTER(c_void_p)]
ctx.lib.flag_print_error.restype  = None

@singledispatch
def print_error(stream) -> None:
    raise NotImplementedError(f"No Implementation for: {type(stream).__name__}")

@print_error.register(io.IOBase)
def _(stream : io.IOBase) -> None:
    if stream is sys.stderr or stream is sys.stdout:
        """ sys.stdout and sys.stderr """
        fd = stream.fileno()
        file_pointer = ctx.libc.fdopen(fd, b"w")
        ctx.lib.flag_print_error(file_pointer)
    else:
        """ file-like objects context manager """
        file_pointer = ctx.libc.fopen(bytes(stream.name, encoding = ctx.encoding), b"a")
        ctx.lib.flag_print_error(file_pointer)


"""
    void flag_print_options(FILE *stream)
"""
ctx.lib.flag_print_options.argtypes = [POINTER(c_void_p)]
ctx.lib.flag_print_options.restype  = None

@singledispatch
def print_options(stream) -> None:
    raise NotImplementedError(f"No Implementation for: {type(stream).__name__}")

@print_options.register(io.IOBase)
def _(stream: io.TextIOWrapper) -> None:
    if stream is sys.stderr or stream is sys.stdout:
        """ sys.stdout and sys.stderr """
        fd = stream.fileno()
        file_pointer = ctx.libc.fdopen(fd, b"w")
        ctx.lib.flag_print_options(file_pointer)
    else:
        """ file-like objects context manager """
        file_pointer = ctx.libc.fopen(bytes(stream.name, encoding = ctx.encoding), b"a")
        ctx.lib.flag_print_options(file_pointer)


__all__ = [
    "name", "bool", "uint64", "size", "str", "parse",
    "rest_argc", "rest_argv", "print_error", "print_options",
]