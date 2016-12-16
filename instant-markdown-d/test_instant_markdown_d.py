#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import tornado
import tornado.testing
import tornado.websocket

from instant_markdown_d import Application

class WebSocketTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        self.connected_body = "Hi, This is the message"
        stream = io.StringIO(self.connected_body)
        app = Application(stream)
        return app

    @tornado.testing.gen_test
    def test_get_body_on_connected(self):
        ws_url = "ws://localhost:{0}/websocket".format(self.get_http_port())
        ws_client = yield tornado.websocket.websocket_connect(ws_url)

        response = yield ws_client.read_message()
        self.assertEqual(response, self.connected_body)
