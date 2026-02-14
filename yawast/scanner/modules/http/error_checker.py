#  Copyright (c) 2013 - 2026. See LICENSE and CONTRIBUTORS.md for details.
#  This file is part of yawast-ng which is released under the MIT license.
#  See the LICENSE file for full license details.

import re
from typing import List, Union, cast

import pkg_resources
from requests import Response

from yawast.reporting.enums import Vulnerabilities
from yawast.reporting.evidence import Evidence
from yawast.reporting.result import Result
from yawast.shared import network, output


class _MatchRule:
    def __init__(self, data: str):
        # split and strip each field so trailing newlines/whitespace don't leak
        fields = [f.strip() for f in data.split("\t")]

        # ensure we have enough fields to avoid index errors
        while len(fields) < 5:
            fields.append("")

        # clean up regex, to eliminate issues from using Java-flavored regex
        pattern = fields[0].replace("}+", "}").replace("++", "+")
        self.pattern = re.compile(pattern)

        self.match_group = fields[1]
        self.type = fields[2]
        self.confidence = fields[4]


_data: List[_MatchRule] = []
_reports: List[str] = []


def check_response(
    url: str, res: Response, body: Union[str, None] = None
) -> List[Result]:
    global _data, _reports
    results = []

    try:
        # make sure we actually have something
        if res is None:
            return []

        if _data is None or len(_data) == 0:
            _get_data()

        if body is None:
            body = res.text

        for rule in _data:
            rule = cast(_MatchRule, rule)

            mtch = re.search(rule.pattern, body)

            if mtch:
                val = mtch.group(int(rule.match_group))

                err_start = body.find(val)

                # get the error, plus 25 characters on each side
                err = body[err_start - 25 : err_start + len(val) + 25]
                msg = (
                    f"Found error message (confidence: {rule.confidence}) "
                    f"on {url} ({res.request.method}): ...{err}..."
                )

                if msg not in _reports:
                    results.append(
                        Result.from_evidence(
                            Evidence.from_response(res),
                            msg,
                            Vulnerabilities.HTTP_ERROR_MESSAGE,
                        )
                    )

                    _reports.append(msg)

                    break
                else:
                    output.debug(f"Ignored duplicate error message: {msg}")
    except Exception:
        output.debug_exception()

    return results


def reset():
    global _reports

    _reports = []


def _get_data() -> None:
    global _data
    local_data: List[_MatchRule] = []
    remote_data: List[_MatchRule] = []

    # load the local version of the data - this is the local fallback in case the remote data cannot be loaded
    file_path = pkg_resources.resource_filename("yawast", "resources/match-rules.tab")

    try:
        with open(file_path) as local_file:
            for line in local_file:
                line = line.strip()
                if not line:
                    continue

                local_data.append(_MatchRule(line))
    except Exception as error:
        output.debug(f"Failed to load local error matching data: {error}")
        output.debug_exception()

    data_url = "https://raw.githubusercontent.com/augustd/burp-suite-error-message-checks/master/src/main/resources/burp/match-rules.tab"

    # try to load the remote version of the data - this is the preferred source,
    # as it can be updated independently of YAWAST releases
    try:
        raw = network.http_get(data_url).text

        for line in raw.splitlines():
            line = line.strip()
            if not line:
                continue

            remote_data.append(_MatchRule(line))

    except Exception as error:
        output.debug(f"Failed to get remote error matching data: {error}")
        output.debug_exception()

        # if we fail to load the remote data, we'll fall back to the local data,
        # which may be outdated but is better than nothing
        remote_data = []

    if len(remote_data) > 0:
        _data = remote_data
    else:
        _data = local_data
