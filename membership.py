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

class Membership():

    def __init__(self, target_url, token):
        self.target_url = target_url
        self.token = token
        self.memberships_Path = MEMBERSHIPS_PATH #'/learn/api/public/v1/courses/courseId/users' #create(POST)/get(GET)
        self.membership_Path = MEMBERSHIP_PATH #'/learn/api/public/v1/courses/courseId/users/userId'
        self.userMembships_Path = USER_MEMBERSHIPS_PATH #'/learn/api/public/v1/users/userId/courses'

    def createMembership(self, course, user, payload, token):
        #"Authorization: Bearer $token"
        authStr = 'Bearer ' + token

        self.PAYLOAD = payload

        session = requests.session()
        session.mount('https://', Tls1Adapter()) # remove for production with commercial cert

        #self.membership_Path = '/learn/api/public/v1/courses/courseId/users/userId'
        replacement = "externalId:"+course
        membership_Path = self.membership_Path
        membership_Path = membership_Path.replace("courseId", replacement)

        replacement = "externalId:" + user
        membership_Path = membership_Path.replace("userId", replacement)
        try:
            #print("[Membership:getMemberships()] PUT Request URL: https://" + self.target_url + membership_Path)
            #print("[Membership:getMemberships()] JSON Payload: " + self.PAYLOAD)
            r = session.put("https://" + self.target_url + membership_Path, data=self.PAYLOAD, headers={'Authorization':authStr, 'Content-Type':'application/json'}, verify=False)
            #print("[Membership:createMembership()] STATUS CODE: " + str(r.status_code) )
            res = json.loads(r.text)
            #print("[Membership:createMembership()] RESPONSE: \n" + json.dumps(res,indent=4, separators=(',', ': ')))
            if r.status_code == 429:
                print("[datasource:getDataSource] Error 429 Too Many Requests. Exiting.")
                sys.exit(2)
        except requests.HTTPError as err:
            if err.code == 400: 
                print("[membership:createMembership] Error 400 The request did not specify valid data.")
            elif err.code == 403: 
                print("[membership:createMembership] Error 403 User has insufficient privileges.")
                sys.exit(2)
            elif err.code == 404:
                print("[membership:createMembership] Error 404 Course not found; or Course-membership not found.")
            elif err.code == LocationParseError:
                print("[membership:createMembership] Error LocationParseError\n")
                sys.exit(2)
        except requests.RequestException:
            print("[membership:createMembership] Error cannot connect to requested server. Exiting.\n")
            sys.exit(2)