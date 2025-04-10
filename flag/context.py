from ctypes import (
    CDLL, c_bool, c_char_p, c_size_t, c_uint64,
    POINTER, string_at
)
from os import path
import typing

class LibFlagContext:
    FLAG_LIBRARY = path.join(
        path.dirname(__file__), "lib", "libflag.so"
    )

    decoding : str = "utf-8"
    encoding : str = "utf-8"
    cache    : typing.List[bytes] = []
    argv     : POINTER(c_char_p)
    lib      : object = CDLL(FLAG_LIBRARY)
    libc     : object = CDLL(None)

class FlagBool:
    ptr : POINTER(c_bool)

    def __init__(this, ptr: POINTER(c_bool)) -> None:
        this.ptr = ptr

    def __bool__(this) -> bool:
        return this.ptr.contents.value

class FlagUint64:
    ptr : POINTER(c_uint64)

    def __init__(this, ptr: POINTER(c_uint64)) -> None:
        this.ptr = ptr

    def __int__(this) -> int:
        return this.ptr.contents.value

class FlagSizeT:
    ptr : POINTER(c_size_t)

    def __init__(this, ptr: POINTER(c_size_t)) -> None:
        this.ptr = ptr

    def __int__(this) -> int:
        return this.ptr.contents.value

class FlagStr:
    ptr : POINTER(c_char_p)

    def __init__(this, ptr: POINTER(c_char_p)) -> None:
        this.ptr = ptr

    def __add__(this, other) -> str:
        if isinstance(other, FlagStr):
            return string_at(this.ptr[0]).decode() +    \
                string_at(other.ptr[0]).decode()
        elif isinstance(other, str):
            return string_at(this.ptr[0]).decode() + other
        else:
            name = type(other).__name__
            raise NotImplementedError(f"No Implementation for: {name}")

    def __str__(this) -> str:
        return string_at(this.ptr[0]).decode()

__all__ = ["LibFlagContext", "FlagBool", "FlagUint64", "FlagSizeT", "FlagStr"]