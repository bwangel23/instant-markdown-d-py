#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
import tornado
import tornado.testing
import tornado.websocket

from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.escape import json_decode

from instant_markdown_d import Application

class WebSocketTestCase(tornado.testing.AsyncHTTPTestCase):
    def get_app(self):
        app = Application(self.stream)
        return app

    def setUp(self):
        self.server_init_message = "Hi, This is the init message"
        self.stream = io.StringIO(self.server_init_message)
        # 注意这个父类的初始化函数一定要放在 run_sync 之前，要不然 io_loop 还未初始化
        super(WebSocketTestCase, self).setUp()
        self.io_loop.run_sync(self._init_client)

    def tearDown(self):
        self.stream.close()
        self.ws_client.close()
        self.client.close()
        super(WebSocketTestCase, self).tearDown()

    @gen.coroutine
    def _init_client(self):
        ws_url = "ws://localhost:{0}/websocket".format(self.get_http_port())
        self.ws_client = yield tornado.websocket.websocket_connect(ws_url)
        self.client = AsyncHTTPClient(self.io_loop)

    @tornado.testing.gen_test
    def test_get_body_on_connected(self):
        response = yield self.ws_client.read_message()
        self.assertEqual(response, self.server_init_message)

    @tornado.testing.gen_test
    def test_update_the_body_by_put(self):
        """ 测试客户端更新信息

        TODO
        客户端向服务端发送 PUT 请求，检查写入到 stream 中的信息是否被更新了
        返回的信息应该包括初始信息和更新信息
        """

        update_message = "Hi, This is the update message"
        self.stream.write(update_message)

        resp = yield self.client.fetch(
            "http://localhost:{}/".format(self.get_http_port()),
            method="PUT",
            body="",
        )

        self.assertEqual(resp.code, 200)
        self.assertEqual(json_decode(resp.body), {"status": "ok"})

        response = yield self.ws_client.read_message()
        self.assertEqual(response, update_message + self.server_init_message)
