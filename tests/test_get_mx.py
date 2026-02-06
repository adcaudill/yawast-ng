#  Copyright (c) 2013 - 2026. See LICENSE and CONTRIBUTORS.md for details.
#  This file is part of yawast-ng which is released under the MIT license.
#  See the LICENSE file for full license details.

import pytest

from yawast.scanner.modules.dns import basic


class TestGetMx:
    def test_get_mx(self):
        recs = basic.get_mx("adamcaudill.com")

        assert len(recs) > 0

        for rec in recs:
            if rec[0].startswith("aspmx4"):
                assert rec[0] == "aspmx4.googlemail.com."
