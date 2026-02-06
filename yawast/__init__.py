#  Copyright (c) 2013 - 2026. See LICENSE and CONTRIBUTORS.md for details.
#  This file is part of yawast-ng which is released under the MIT license.
#  See the LICENSE file for full license details.

try:
    from ._version import __version__

    __all__ = ["__version__"]
    del _version  # remove to avoid confusion with __version__
except Exception:
    # if we get here, something is very wrong - running under python2?
    pass
