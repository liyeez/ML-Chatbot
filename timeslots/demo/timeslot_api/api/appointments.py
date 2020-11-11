# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
import sqlite3
import datetime as DT
from datetime import time, timedelta
import re
from . import Resource
from .. import schemas

# find first weekday given a date 'd'
# d = datetime.date(2011, 7, 2)
# next_monday = next_weekday(d, 0) # 0 = Monday, 1=Tuesday, 2=Wednesday...
def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

# accumulates records from past until 7 days from now
# need to ensure db is alrdy created with the correct schema table created
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

                timeslot_chang = (None,'Chang Low Ying', None, day.strftime("%A"), time(start_time, 00, 00).strftime("%H:%M%p"), day.strftime("%Y-%m-%d"), True)
                timeslot_asman = (None,'Asman Nematallah', None, day.strftime("%A"), time(start_time, 00, 00).strftime("%H:%M%p"), day.strftime("%Y-%m-%d"), True)
                timeslot_john = (None,'John Smith', None, day.strftime("%A"), time(start_time, 00, 00).strftime("%H:%M%p"), day.strftime("%Y-%m-%d"), True)
                    
                cursor.execute('INSERT INTO timeslots VALUES (?,?,?,?,?,?,?);' , timeslot_chang)
                cursor.execute('INSERT INTO timeslots VALUES (?,?,?,?,?,?,?);' , timeslot_asman)
                cursor.execute('INSERT INTO timeslots VALUES (?,?,?,?,?,?,?);' , timeslot_john)
                start_time += 1
        
    conn.commit()
    conn.close()

class Appointments(Resource):

    def get(self):
        try:
            dentist_name = g.args['dentist_name']
        except:
            dentist_name = ''

        try:
            day_of_week = g.args['day_of_week']
        except:
            day_of_week = '%'

        try:
            time_of_day = g.args['time_of_day']
        except:
            time_of_day = '%'
        
        configDB()

        conn = sqlite3.connect('timeslots.db')
        # filter by day of week, dentist name and time of the day
        # need to ensure filter format is correct, assumed correct format is passed from chatbot api
        cursor = conn.execute("SELECT * FROM timeslots WHERE day_of_week like ? and dentist_name like ? and time_of_day like ?", (day_of_week, '%'+dentist_name+'%', time_of_day))
        appt_records = cursor.fetchall()

        appts = []
        for i in range(len(appt_records)): 
            appt = {}
            appt['day_of_week'] = appt_records[i][3]
            appt['dentist_name'] = appt_records[i][1]
            appt['patient_name'] = appt_records[i][2]
            
            # False = reserved, True = available
            appt['status'] = appt_records[i][6]
            appt['time_of_day'] = appt_records[i][4]

            appts.append(appt)
            print(appt_records[i]) 
       

        conn.close()
    
        links = user_links('get_request')
        
        return {'appointments': appts, 'links': links}, 200, None

    def post(self):
        appt = {}
        try:
            reservation = request.json
            conn = sqlite3.connect('timeslots.db')
            cursor = conn.execute("SELECT * FROM timeslots WHERE day_of_week like ? and dentist_name like ? and time_of_day like ?", (reservation['day_of_week'], '%'+reservation['dentist_name']+'%', reservation['time_of_day']))
            appt_records = cursor.fetchall()

            if not len(appt_records) == 1:
                print(appt_records)
                return 'Fields not specified enough', 400
            else:
                
                if appt_records[0][6] == False: # already reserved
                    return "Appointment time already reserved.", 400
                else:
                    tuple_id = appt_records[0][0]
                    # update database to store the status of reservation as false as well as the patient_name
                    conn.execute("UPDATE timeslots SET status=0, patient_name=? WHERE id=?", (reservation['patient_name'], appt_records[0][0]))
                    # get the appointment again from db
                    conn.commit()
                    
                    #cursor = conn.execute("SELECT * FROM timeslots WHERE id=?", (tuple_id))
                    #appt_records = cursor.fetchall()
                    
                    
                    appt['day_of_week'] = appt_records[0][3]
                    appt['dentist_name'] = appt_records[0][1]
                    #appt['patient_name'] = appt_records[0][2]
                    appt['patient_name'] = reservation['patient_name']
                    # # appt['status'] = appt_records[0][6]
                    appt['status'] = False
                    appt['time_of_day'] = appt_records[0][4]

                
                    links = user_links('post_request')
               
                    return {'appointment': appt, 'links': links }, 201, None
            
        except:
            return 'Fields not satisfied: Is booking time within 7 days?', 400

def user_links(type_of_links):
    objs = []
    obj_a = {}
    obj_b = {}

    print(type_of_links)

    if type_of_links == 'post_request':
        obj_a['description'] = 'Book an Appointment by providing [day_of_week], [dentist_name], [patient_name], [status] of availability and [time_of_day] in hh:mm AM/PM format'
        obj_a['href'] = 'http://127.0.0.1:5000/appointments'
        obj_a['rel'] = 'self'
        obj_a['request'] = 'POST'

        obj_b['description'] = 'Cancel an Appointment by providing [day_of_week], [dentist_name], [patient_name], [status] of availability and [time_of_day] in hh:mm AM/PM format'
        obj_b['href'] = 'http://127.0.0.1:5000/appointments/cancel'
        obj_b['rel'] = 'next'
        obj_b['request'] = 'POST'

        objs.append(obj_a)
        objs.append(obj_b)

    elif type_of_links == 'get_request':

        obj_a['description'] = 'Get Appointment info, filters available for [day_of_week], [dentist_name] and [time_of_day] in hh:mm AM/PM format'
        obj_a['href'] = 'http://127.0.0.1:5000/appointments'
        obj_a['rel'] = 'self'
        obj_a['request'] = 'GET'

        obj_b['description'] = 'Book an Appointment by providing [day_of_week], [dentist_name], [patient_name], [status] of availability and [time_of_day] in hh:mm AM/PM format'
        obj_b['href'] = 'http://127.0.0.1:5000/appointments'
        obj_b['rel'] = 'next'
        obj_b['request'] = 'POST'

        objs.append(obj_a)
        objs.append(obj_b)
    
    else:
        return []

    return objs


    # description*	string
    # href*	string
    # rel*	string
    # request*