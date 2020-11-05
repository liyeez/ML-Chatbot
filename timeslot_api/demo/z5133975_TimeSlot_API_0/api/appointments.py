# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas


class Appointments(Resource):

    def post(self):
        print(g.json)

        return {'time_of_day': 'something', 'day_of_week': 'something', 'dentist_name': 'something', 'patient_name': 'something', 'status': False}, 200, None

    def delete(self):
        print(g.json)

        return None, 202, None