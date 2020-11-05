# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.appointments_day_of_week import AppointmentsDayOfWeek
from .api.appointments import Appointments


routes = [
    dict(resource=AppointmentsDayOfWeek, urls=['/appointments/<day_of_week>'], endpoint='appointments_day_of_week'),
    dict(resource=Appointments, urls=['/appointments'], endpoint='appointments'),
]