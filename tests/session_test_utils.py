# Copyright (c) 2013 - 2026. See LICENSE and CONTRIBUTORS.md for details.
# This file is part of yawast-ng which is released under the MIT license.
# See the LICENSE file for full license details.

from argparse import Namespace

from yawast.scanner.session import Session


def make_test_session(url="http://example.com"):
    args = Namespace()
    args.proxy = None
    args.user_agent = None
    args.headless = True
    args.window_size = None
    args.incognito = False
    args.disable_images = False
    args.disable_javascript = False
    args.pass_reset_page = url
    return Session(args, url)
