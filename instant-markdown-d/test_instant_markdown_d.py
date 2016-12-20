#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import tornado
import tornado.testing
import tornado.websocket

from instant_markdown_d import Application

class WebSocketTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = Application(self.stream)
        return app

    def setUp(self):
        self.server_init_message = "Hi, This is the init message"
        self.stream = io.StringIO(self.server_init_message)
        super(WebSocketTestCase, self).setUp()

    def tearDown(self):
        super(WebSocketTestCase, self).tearDown()
        self.stream.close()

    @tornado.testing.gen_test
    def test_get_body_on_connected(self):
        ws_url = "ws://localhost:{0}/websocket".format(self.get_http_port())
        self.ws_client = yield tornado.websocket.websocket_connect(ws_url)
        response = yield self.ws_client.read_message()
        self.assertEqual(response, self.server_init_message)

    @tornado.testing.gen_test
    def test_update_the_body_by_put(self):
        """ 测试客户端更新信息

        TODO
        客户端向服务端发送 PUT 请求，检查写入到 stream 中的信息是否被更新了
        返回的信息应该包括初始信息和更新信息
        """

        self.assertEqual(1, 0)
        ws_url = "ws://localhost:{0}/websocket".format(self.get_http_port())
        ws_client = yield tornado.websocket.websocket_connect(ws_url)

        update_message = "Hi, This is the update message"
        self.stream.write(update_message)

        response = yield ws_client.read_message()
        self.assertEqual(response, update_message)
