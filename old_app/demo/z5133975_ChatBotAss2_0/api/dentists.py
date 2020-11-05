# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import sqlite3
from flask import request, g, jsonify

from . import Resource
from .. import schemas


class Dentists(Resource):
    print('heyy')
    def get(self):
        print(g.args)
        print(request.args['expression'])
        dentist_name = request.args['expression']

        dentists = []
        try:
            conn = sqlite3.connect('dentists.db')
            print("connected to db")

            if(dentist_name == ''): # get every dentists on db
                cursor = conn.execute("SELECT name, location, specialization from dentists")
                for row in cursor:
                    dentist_info = {}
                    dentist_info['name'] = row[0]
                    dentist_info['location'] = row[1]
                    dentist_info['specialization'] = row[2]
                    print(dentist_info)
                    dentists.append(dentist_info)
                
            else:

                # cursor = conn.execute("SELECT * FROM dentists WHERE name LIKE '%s'" % dentist_name)
                cursor = conn.execute("SELECT * FROM dentists WHERE name LIKE '%s'" % (dentist_name+'%'))
                details = cursor.fetchall()
                print("Details", details)
                if len(details) == 0:  
                    return "No such dentist found", 403
            
                else:    
                
                # info = {
                #     'name': dentists[0]['name'],
                #     'location': dentists[0]['location'],
                #     'specialization': dentists[0]['specialization']
                #     }
            # print(info)
            conn.close()
            return info, 200, None
        except:
            return "cannot open db", 400
        

        