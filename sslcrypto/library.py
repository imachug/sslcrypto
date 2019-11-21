import os
import sys
import ctypes
import ctypes.util


# Discover OpenSSL library
def discover_paths():
    # Search local files first
    if "win" in sys.platform:
        # Windows
        openssl_paths = [
            "libeay32.dll"
        ]
        if hasattr(sys, "_MEIPASS"):
            openssl_paths += [os.path.join(sys._MEIPASS, path) for path in openssl_paths]
        openssl_paths.append(ctypes.util.find_library("libeay32"))
    elif "darwin" in sys.platform:
        # Mac OS
        names = [
            "libcrypto.dylib",
            "libcrypto.1.1.0.dylib",
            "libcrypto.1.0.2.dylib",
            "libcrypto.1.0.1.dylib",
            "libcrypto.1.0.0.dylib",
            "libcrypto.0.9.8.dylib"
        ]
        openssl_paths = [os.path.abspath(path) for path in names]
        openssl_paths += names
        openssl_paths += [
            "/usr/local/opt/openssl/lib/libcrypto.dylib"
        ]
        if hasattr(sys, "_MEIPASS") and "RESOURCEPATH" in os.environ:
            openssl_paths += [
                os.path.join(os.environ["RESOURCEPATH"], "..", "Frameworks", name)
                for name in names
            ]
        openssl_paths.append(ctypes.util.find_library("ssl"))
    else:
        # Linux, BSD and such
        names = [
            "libcrypto.so",
            "libssl.so",
            "libcrypto.so.1.1.0",
            "libssl.so.1.1.0",
            "libcrypto.so.1.0.2",
            "libssl.so.1.0.2",
            "libcrypto.so.1.0.1",
            "libssl.so.1.0.1",
            "libcrypto.so.1.0.0",
            "libssl.so.1.0.0",
            "libcrypto.so.0.9.8",
            "libssl.so.0.9.8"
        ]
        openssl_paths = [os.path.abspath(path) for path in names]
        openssl_paths += names
        if hasattr(sys, "_MEIPASS"):
            openssl_paths += [os.path.join(sys._MEIPASS, path) for path in names]
        openssl_paths.append(ctypes.util.find_library("ssl"))

    return openssl_paths


def discover_library():
    for path in discover_paths():
        if path:
            try:
                return ctypes.CDLL(path)
            except OSError:
                pass
    raise OSError("OpenSSL is unavailable")
