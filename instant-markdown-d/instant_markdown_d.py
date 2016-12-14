#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import tornado
import tornado.web
import tornado.websocket
from tornado.ioloop import IOLoop

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
listen_ip =  '0.0.0.0' if os.environ.get('INSTANT_MARKDOWN_OPEN_TO_THE_WORLD') else '127.0.0.1'
listen_port = os.environ.get('INSTANT_MARKDOWN_DAEMON_PORT', 8090)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print("WebSocket closed")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/websocket", WebSocketHandler),
        ]
        settings = dict(
            debug=True,
            template_path=os.path.join(BASE_DIR, 'templates'),
            static_path=os.path.join(BASE_DIR, 'static'),
        )
        super(Application, self).__init__(handlers, **settings)


def main():
    app = Application()
    app.listen(listen_port, listen_ip)
    IOLoop.current().start()


if __name__ == '__main__':
    main()
