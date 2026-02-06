#  Copyright (c) 2013 - 2026. See LICENSE and CONTRIBUTORS.md for details.
#  This file is part of yawast-ng which is released under the MIT license.
#  See the LICENSE file for full license details.


class PluginBase:
    """
    Base class for all plugins.
    """

    def __init__(self):
        self.name = "PluginBase"
        self.description = "Base class for all plugins."
        self.version = "1.0.0"
