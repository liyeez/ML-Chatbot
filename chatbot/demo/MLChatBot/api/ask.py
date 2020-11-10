# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g
import requests
from requests.exceptions import HTTPError

from . import Resource
from .. import schemas

def requestDentist(dentist):
    try:
        # TODO: CHange port number?
        url = 'http://127.0.0.1:8080/dentist_api/dentists?expression=' + dentist
        response  = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')
        dentist_list = response.json()
        print(dentist_list)
        returnStr = 'Our services available are: '
        for d in dentist_list:
            s = ' Dr. '
            s += d.get('name') +' who '
            s += 'specialized in ' + d.get('specialization')
            s += ', located in ' + d.get('location')
            returnStr += s + '. '
            print(d)

        return returnStr


class Ask(Resource):

    def get(self):
        print(g.args)

        query = request.args.get('expression')
        print(query)
        try:
            url = 'https://api.wit.ai/message?v=20201110&q=' + query
            response  = requests.get(
                url,
                headers={'Authorization': 'Bearer YAJKOQ53TWEQEU2PE76RJK2LXMUFP2PF'},
            )
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')
            print(response.json())

            try:
                data = (response.json()).get('intents')
                intent = data[0].get('name')
                keywords = (response.json()).get('entities')
                
                if intent == 'Dentists':
                    # call dentist api to get identified dentist
                    dentist_list = (keywords.get("wit_dentists:wit_dentists"))[0]
                    dentist = dentist_list.get('body')
                    if 'John' in dentist or 'Smith' in dentist:
                        dentist = 'John'
                    elif 'Chang' in dentist or 'Low Ying' in dentist:
                        dentist = 'Chang'
                    elif 'Asman' in dentist or 'Nematallah' in dentist:
                        dentist = 'Asman'
                    else:
                        dentist = ' ' # used by api to retrieve all dentists

                    return requestDentist(dentist), 200
                else:
                    print(intent) # to do fix timeslot api then continue here
            except:
                return "Third Party API error", 400



        
        return None, 200, None