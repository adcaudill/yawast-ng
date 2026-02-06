#  Copyright (c) 2013 - 2026. See LICENSE and CONTRIBUTORS.md for details.
#  This file is part of yawast-ng which is released under the MIT license.
#  See the LICENSE file for full license details.

import pytest

from yawast.shared import network


class TestCheckWWWRedirect:
    def test_check_www_redirect_valid(self):
        result = network.check_www_redirect("https://www.adamcaudill.com/")
        assert result == "https://adamcaudill.com/"

    def test_check_www_redirect_none(self):
        result = network.check_www_redirect("https://adamcaudill.com/")
        assert result == "https://adamcaudill.com/"

    def test_check_www_redirect_www(self):
        result = network.check_www_redirect("https://apple.com/")
        assert result == "https://www.apple.com/"
