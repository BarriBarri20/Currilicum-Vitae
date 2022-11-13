# ------------------------------------------------------------------------------
# The MIT License (MIT)
#
# Copyright (c) 2014-2021 Digital Sapphire
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# ------------------------------------------------------------------------------
import logging
import typing as t

try:
    from flask import Flask, g, request
except ImportError:
    Flask = None
    g = None
    request = None

log = logging.getLogger(__name__)


class DSFlaskResponse:
    bad_request = 400
    conflict = 409
    created = 201
    forbidden = 403
    not_found = 404
    ok = 200
    unauthorized = 401

    @staticmethod
    def log_request(**kwargs):
        if Flask is None:
            raise RuntimeError('dsdev-utils[flask] is not installed')

        log.info("Path: %s", request.path)
        log.info("Method: %s", request.method)
        log.info("Remote Addr: %s", request.remote_addr)
        if hasattr(g, "user"):
            log.info("User ID: %s", g.user.get_id())

        parsed_data = dict()

        for k, v in request.headers.items():
            if "Authorization" in k:
                v = "*****"
            parsed_data[k] = v

        data = None
        if 'data' in kwargs.keys():
            data = kwargs['data']
            del kwargs['data']

        parsed_data.update(kwargs)

        msg = f"Headers: {parsed_data}"
        log.info(msg)
        if data is not None:
            DSFlaskResponse.log_request_data(data)

    @staticmethod
    def log_request_data(data):
        if "password" in data.keys():
            temp_password = data["password"]
            data["password"] = "*****"
            msg = f"Request Data: {data}"
            data["password"] = temp_password
        else:
            msg = f"Request Data: {data}"

        log.info(msg)

    @staticmethod
    def resp_data(
        data: t.Union[t.Dict, t.List], status_code: int
    ) -> t.Tuple[t.Dict[str, t.Any], int]:
        return (
            {
                "data": data,
            },
            status_code,
        )

    @staticmethod
    def resp_data_created(data: t.Union[t.Dict, t.List]):
        return DSFlaskResponse.resp_data(data, DSFlaskResponse.created)

    @staticmethod
    def resp_data_ok(data: t.Union[t.Dict, t.List]):
        return DSFlaskResponse.resp_data(data, DSFlaskResponse.ok)

    @staticmethod
    def resp_message(msg, status_code) -> t.Tuple[t.Dict[str, t.Any], int]:
        return (
            {
                "message": msg,
            },
            status_code,
        )

    @staticmethod
    def resp_message_bad_request(msg="Bad Request") -> t.Tuple[t.Dict[str, t.Any], int]:
        return DSFlaskResponse.resp_message(msg, DSFlaskResponse.bad_request)

    @staticmethod
    def resp_message_conflict(msg="Conflict") -> t.Tuple[t.Dict[str, t.Any], int]:
        return DSFlaskResponse.resp_message(msg, DSFlaskResponse.conflict)

    @staticmethod
    def resp_message_forbidden(msg="Forbidden") -> t.Tuple[t.Dict[str, t.Any], int]:
        return DSFlaskResponse.resp_message(msg, DSFlaskResponse.forbidden)

    @staticmethod
    def resp_message_not_found(msg="Not Found") -> t.Tuple[t.Dict[str, t.Any], int]:
        return DSFlaskResponse.resp_message(msg, DSFlaskResponse.not_found)

    @staticmethod
    def resp_message_unauthorized(
        msg="Unauthorized",
    ) -> t.Tuple[t.Dict[str, t.Any], int]:
        return DSFlaskResponse.resp_message(msg, DSFlaskResponse.not_found)
