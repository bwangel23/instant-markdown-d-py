#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado
import tornado.testing
import tornado.websocket

from instant_markdown_d import Application

class WebSocketTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = Application()
        return app

    @tornado.testing.gen_test
    def test_websocket_echo(self):
        ws_url = "ws://localhost:{0}/websocket".format(self.get_http_port())
        ws_client = yield tornado.websocket.websocket_connect(ws_url)

        message = "Hi, This is the message"
        ws_client.write_message(message)
        response = yield ws_client.read_message()
        self.assertEqual(response, message)
