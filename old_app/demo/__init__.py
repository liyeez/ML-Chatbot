# -*- coding: utf-8 -*-
from __future__ import absolute_import
from flask import Flask

import z5133975_ChatBotAss2_0


def create_app():
    app = Flask(__name__, static_folder='static',instance_relative_config=False)
    app.register_blueprint(
        z5133975_ChatBotAss2_0.bp,
        url_prefix='/z5133975/ChatBotAss2/0')

    return app

if __name__ == '__main__':
    create_app().run(debug=True)