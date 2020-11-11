# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
import sqlite3
from . import Resource
from .. import schemas



class AppointmentsCancel(Resource):

    def post(self):

        try:
            reservation = request.json
            try:
                time_of_day = reservation['time_of_day']
            except:
                return "time_of_day field not found", 400
            
            try:
                day_of_week = reservation['day_of_week']
            except:
                return "day_of_week field not found", 400
            
            try:
                dentist_name = reservation['dentist_name']
            except:
                return "dentist_name field not found", 400

            try:
                patient_name = reservation['patient_name']
            except:
                return "patient_name field not found", 400

            try:
                status = reservation['status']
            except:
                return "status field not found", 400
        

            conn = sqlite3.connect('timeslots.db')
            cursor = conn.execute("SELECT * FROM timeslots WHERE day_of_week like ? and dentist_name like ? and time_of_day like ?", (reservation['day_of_week'], '%'+reservation['dentist_name']+'%', reservation['time_of_day']))
            appt_records = cursor.fetchall()

            if not len(appt_records) == 1: # if more than one tuples are returned 
                print(appt_records)
                conn.close()
                return 'Fields not specified enough', 400
            
            elif appt_records[0][2] != reservation['patient_name']:
                return ('Patient_name does not match, recorded patient is: ', appt_records[0][2]), 400
            else:
                if appt_records[0][6] == True or appt_records[0][2] == None: # already reserved or have no name
                    return "Appointment fields are already deprecated.", 400
                else:
                    try:
                        conn.execute("UPDATE timeslots SET status=1, patient_name=? WHERE id=?", (None, appt_records[0][0]))
                        conn.commit()
                        conn.close()
                        print('Canceled!')
                    except:
                        conn.close()
                        return "Failed to cancel appointment in db", 400
            return {'links': user_links()}, 202, None
        except:
            return 'Unable to cancel appointment', 400

def user_links():
    objs = []
    obj_a = {}
    obj_b = {}
    obj_c = {}
   
    obj_a['description'] = 'Get Appointment info, filters available for [day_of_week], [dentist_name] and [time_of_day] in hh:mm AM/PM format'
    obj_a['href'] = 'http://127.0.0.1:5000/appointments'
    obj_a['rel'] = 'next'
    obj_a['request'] = 'GET'

    obj_b['description'] = 'Book an Appointment by providing [day_of_week], [dentist_name], [patient_name], [status] of availability and [time_of_day] in hh:mm AM/PM format'
    obj_b['href'] = 'http://127.0.0.1:5000/appointments'
    obj_b['rel'] = 'next'
    obj_b['request'] = 'POST'

    obj_c['description'] = 'Cancel an Appointment by providing [day_of_week], [dentist_name], [patient_name], [status] of availability and [time_of_day] in hh:mm AM/PM format'
    obj_c['href'] = 'http://127.0.0.1:5000/appointments/cancel'
    obj_c['rel'] = 'next'
    obj_c['request'] = 'POST'

    objs.append(obj_a)
    objs.append(obj_b)  
    objs.append(obj_c)  

    return objs