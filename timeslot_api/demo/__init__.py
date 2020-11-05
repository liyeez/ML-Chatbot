# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask

import z5133975_TimeSlot_API_0


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        z5133975_TimeSlot_API_0.bp,
        url_prefix='/z5133975/TimeSlot_API/0')
    return app

if __name__ == '__main__':
    create_app().run(debug=True)