# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
import sqlite3
import datetime as DT
from datetime import time, timedelta
import re
from . import Resource
from .. import schemas

# accumulates records from past until 7 days from now
def configDB():
    conn = sqlite3.connect('timeslots.db')
    day = DT.date.today()

    for x in range(0,7): # loop next 7 days
        # get date
        day += DT.timedelta(days=1)
        # check if this date records exists yet
        
        cursor = conn.execute("SELECT * FROM timeslots WHERE date_appt='%s'" % day.strftime("%Y-%m-%d"))
        appt_records = cursor.fetchall()
        # print(appt_records)
        
        # if this day not in records yet but within 7 days range of current date, 
        # then create new empty records (8 slots for every dentist => 8*3 = 24 record rows per day)
        if len(appt_records) == 0:

            # loop 8 hours (9AM - 5PM)
            start_time = 9
            for y in range (0,8):

                timeslot_chang = (None,'Chang Low Ying', None, day.strftime("%A"), time(start_time, 00, 00).strftime("%H:%M%p"), day.strftime("%Y-%m-%d"))
                timeslot_asman = (None,'Asman Nematallah', None, day.strftime("%A"), time(start_time, 00, 00).strftime("%H:%M%p"), day.strftime("%Y-%m-%d"))
                timeslot_john = (None,'John Smith', None, day.strftime("%A"), time(start_time, 00, 00).strftime("%H:%M%p"), day.strftime("%Y-%m-%d"))
                    
                cursor.execute('INSERT INTO timeslots VALUES (?,?,?,?,?,?);' , timeslot_chang)
                cursor.execute('INSERT INTO timeslots VALUES (?,?,?,?,?,?);' , timeslot_asman)
                cursor.execute('INSERT INTO timeslots VALUES (?,?,?,?,?,?);' , timeslot_john)
                start_time += 1
        
    conn.commit()
    conn.close()

# get request with filter to find a certain appointment or any that matches the filter
class AppointmentsDayOfWeek(Resource):

    def get(self, day_of_week):
        try:
            dentist_name = g.args['dentist_name']
        except:
            dentist_name = ''

        try:
            time_of_day = g.args['time_of_day']
        except:
            time_of_day = '%'
        
        configDB()

        conn = sqlite3.connect('timeslots.db')
        # filter by day of week, dentist name and time of the day
        cursor = conn.execute("SELECT * FROM timeslots WHERE day_of_week=? and dentist_name like ? and time_of_day like ?", (day_of_week, '%'+dentist_name+'%', time_of_day))
        appt_records = cursor.fetchall()

        appts = []
        for i in range(len(appt_records)): 
            appt = {}
            appt['time_of_day'] = appt_records[i][4]
            appt['day_of_week'] = appt_records[i][3]
            appt['dentist_name'] = appt_records[i][1]
            appt['patient_name'] = appt_records[i][2]

            if appt_records[i][2]:
                print(appt_records[i][2])
                appt['status'] = False # reserved
            else:
                appt['status'] = True # available
            appts.append(appt)
            print(appt_records[i]) 
       

        conn.close()
        
        return appts, 200, None