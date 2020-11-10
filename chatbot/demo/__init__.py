# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask

import MLChatBot


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        MLChatBot.bp,
        url_prefix='/MLChatBot')
    return app

if __name__ == '__main__':
    create_app().run(debug=True)