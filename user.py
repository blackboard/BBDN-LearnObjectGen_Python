"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl
import sys
from constants import *

requests.packages.urllib3.disable_warnings()

#Tls1Adapter allows for connection to sites with non-CA/self-signed
#  certificates e.g.: Learn Dev VM
class Tls1Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)

class User():

    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        #self.users_Path = '/learn/api/public/v1/users' #create(POST)/get(GET)
        #self.user_Path = '/learn/api/public/v1/users/externalId:'
        self.users_Path = USERS_PATH #create(POST)/get(GET)
        self.user_Path = USER_PATH   #update(PATCH)/delete


    def createUser(self, dsk, payload, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        self.PAYLOAD = payload

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert
        try:
            #print("[User:createUser()] POST Request URL: https://" + self.target_url + self.users_Path)
            #print("[User:createUser()] JSON Payload: " + self.PAYLOAD)
            r = session.post("https://" + self.target_url + self.users_Path, data=self.PAYLOAD, headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)
            #print("[User:createUser()] STATUS CODE: " + str(r.status_code) )
            res = json.loads(r.text)
            #print("[User:createUser()] RESPONSE: \n" + json.dumps(res, indent=4, separators=(',', ': ')))
            if r.status_code == 429:
                print("[datasource:getDataSource] Error 429 Too Many Requests. Exiting.")
                sys.exit(2)
        except requests.HTTPError as err:
            if err.code == 400: 
                print("[user:createUser] Error 400 The request did not specify valid data.")
            elif err.code == 403: 
                print("[user:createUser] Error 403 User has insufficient privileges. Exiting.")
                sys.exit(2)
            elif err.code == 409:
                print("[user:createUser] Error 409 A user with the same userName or externalId already exists.")
            elif err.code == LocationParseError:
                print("[user:createUser] Error LocationParseError. Exiting.\n")
                sys.exit(2)
        except requests.RequestException:
            print("[user:createUser] Error cannot connect to requested server. Exiting.\n")
            sys.exit(2)