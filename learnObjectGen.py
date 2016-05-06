"""
Copyright (C) 2016, Blackboard Inc.
All rights reserved.
Redistribution and use in source and binary forms, with or without modification, are permitted provided
that the following conditions are met:
Redistributions of source code must retain the above copyright notice, this list of conditions and the
following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the name of Blackboard Inc. nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY BLACKBOARD INC ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL BLACKBOARD INC. BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
import getopt
import datetime
import time
import json
import random


from auth import AuthToken
from datasource import DataSource
from course import Course
from user import User
from membership import Membership

from constants import *


authorized_session = None


def process_all(req_number, index, output_file, rest):
    indx = int(index)
    n = int(req_number)
    req_num = int(req_number)
    if req_num == 0:
        n = MAX_COURSES
    process_courses(n, index, output_file, rest)
    if req_num == 0:
        n = MAX_USERS
    process_users(n, index, output_file, rest)
    if req_num == 0:
        n = MAX_MEMBERSHIPS
    process_memberships(n, index, output_file, rest)

def process_courses(req_number, index, output_file, rest):
    print ("PROCESSING COURSES")
    indx = int(index)
    if rest:
        print("WRITING DATA FILE and PROCESSING via REST, this will take a minute or so...")
    else:
        print("WRITING DATA FILE ONLY - you must process via SIS Framework...")
    with open(output_file+"_COURSES-"+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+".txt", "w") as text_file:
        text_file.write("\n##### DELETE THIS LINE....THE FOLLOWING IS A COURSE SNAPSHOT FLAT FILE FOR STORE OR DELETE #####\n")
        text_file.write("##### DELETE THIS LINE.... DATASOURCEKEY %s #####\n" % DSKEXTERNALID)
        text_file.write("COURSE_ID|EXTERNAL_COURSE_KEY|COURSE_NAME\n")
        for num in range( 0, int(req_number)):
            json_payload = {}
            externalId = "%s_%d" % (COURSEEXTERNALIDSTEM, indx)
            text_file.write("%s|%s|%s\n" % (externalId, externalId, externalId))
            if rest:
                externalId = "%s_%d" % (COURSEEXTERNALIDSTEM, indx)
                dataSourceId = "externalId:%s" % DSKEXTERNALID
                courseId = "%s_%d" % (COURSEEXTERNALIDSTEM, indx)
                name = "%s_%d" % (COURSEEXTERNALIDSTEM, indx)
                description = "Course created by LearnObjGen"
                allowGuests = "true"
                readOnly = "false"
                availability = { "duration":"continuous"}

                json_payload["externalId"] = externalId
                json_payload["dataSourceId"] = dataSourceId
                json_payload["courseId"] = courseId
                json_payload["name"] = name
                json_payload["description"] = description
                json_payload["allowGuests"] = allowGuests
                json_payload["readOnly"] = readOnly
                json_payload["availability"] = availability

                #print (json.dumps(json_payload, indent=4, separators=(',', ': ')))
                global authorized_session
                course_session = Course(rest, authorized_session.getToken())
                course_session.createCourse(DSKEXTERNALID, json.dumps(json_payload), authorized_session.getToken())

            indx = indx+1




def process_users(req_number, index, output_file, rest):
    print ("PROCESSING USERS...")
    indx = int(index)
    if rest:
        print("WRITING DATA FILE and PROCESSING via REST, this will take a minute or so...")
    else:
        print("WRITING DATA FILE ONLY - you must process via SIS Framework...")
    with open(output_file+"_USERS-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt", "w") as text_file:
        text_file.write("\n##### DELETE THIS LINE....THE FOLLOWING IS A USER SNAPSHOT FLAT FILE FOR STORE OR DELETE #####\n")
        text_file.write("##### DELETE THIS LINE.... DATASOURCEKEY %s #####\n" % DSKEXTERNALID)
        text_file.write("EXTERNAL_PERSON_KEY|USER_ID|SYSTEM_ROLE|FIRSTNAME|LASTNAME|EMAIL|INSTITUTION_ROLE|PASSWORD\n")
        for num in range( 0, int(req_number)):
            json_payload = {}
            externalId = "%s_%d" % (USEREXTERNALIDSTEM, indx)
            userName = "%s_%d" % (USEREXTERNALIDSTEM, indx)
            password = "python_%d" % indx


            text_file.write("%s|%s|none|%s|%d|%s_%d@erehwon.edu|Student|%s\n" % (externalId, userName, USEREXTERNALIDSTEM, indx, USEREXTERNALIDSTEM,  indx, password))
            if rest:
                #externalId = "%s_%d" % (USEREXTERNALIDSTEM, indx)
                dataSourceId = "externalId:%s" % DSKEXTERNALID
                #userName = "%s_%d" % (USEREXTERNALIDSTEM_, indx)
                #password = "python_%d" % indx
                availability = { "available":"Yes"}
                name = { "given": "%s" % USEREXTERNALIDSTEM, "family": "%d" % indx }
                contact = { "email" : "%s@erehwon.edu" % userName }

                json_payload["externalId"] = externalId
                json_payload["dataSourceId"] = dataSourceId
                json_payload["userName"] = userName
                json_payload["password"] = password
                json_payload["availability"] = availability
                json_payload["name"] = name
                json_payload["contact"] = contact

                #print (json.dumps(json_payload, indent=4, separators=(',', ': ')))
                global authorized_session
                user_session = User(rest, authorized_session.getToken())
                user_session.createUser(DSKEXTERNALID, json.dumps(json_payload), authorized_session.getToken())
            indx = indx+1

def process_memberships(req_number_memberships, index, output_file, rest):
# randomizing n memberships for n users into n courses can be tricky -
# if you have a better way of doing this let me know - mark.oneil@blackboard.com
    print ("PROCESSING MEMBERSHIPS...")

    indx = int(index) #starting index for courses and users
    memberships_count = 0
    full = set()
    course_memberships = {}
    courses = set()
    users = set()
    courses_with_members = set()
    users_in_courses = set()


    #req_number is the required number of memberships - user entered or constant max of 1000
    if int(req_number_memberships) == 1000:
        req_number_users = 150
        req_number_courses = 100
    else:
        req_number_users = req_number_memberships
        req_number_courses = req_number_memberships

    print ("number memberships in: %d" % req_number_memberships)
    print ("number users in: %d" % req_number_users)
    print ("number courses in: %d" % req_number_courses)

    #build membership lists for courses
    #create arrays containing memberships randomly associated with courses until
    #req_number_memberships is met.
    #Since membership count is the control:
    #    all courses may not have memberships
    #    all users may not have memberships
    while memberships_count < req_number_memberships:
        user_set = set()
        userID = USEREXTERNALIDSTEM + "_" + str(random.randint(int(index), int(index)+int(req_number_users)-1))
        #print ("userID %d" % userID)
        courseID = COURSEEXTERNALIDSTEM + "_" + str(random.randint(int(index), int(index)+int(req_number_courses)-1))
        #print ("courseID %d" % courseID)
        if courseID in course_memberships and courseID not in full:
            user_set = set(course_memberships[courseID])

        #print ("%s is not full - adding membership" % courseID)
        user_set.add(userID)
        course_memberships[courseID] = list(user_set)
        courses_with_members.add("%s_%s" % (COURSEEXTERNALIDSTEM, courseID))
        users_in_courses.add("%s_%s" % (USEREXTERNALIDSTEM, userID))
        memberships_count += 1
        #check if full add to full set.
        if len(user_set) >= MAX_PER_COURSE_MEMBERSHIPS:
            #print ("%s is full." % courseID)
            full.add(courseID)

    #what courses did not get members?
    all_courses = []
    for num in range( indx, indx+int(req_number_courses)-1):
        all_courses.append("%s_%d" % (COURSEEXTERNALIDSTEM, num))
    with open(output_file + "Courses_with_no_enrollments-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt", "w") as text_file:
        text_file.write("\n##### This file contains the list of courses not given enrollments #####\n")
        text_file.write(str(set(all_courses) - courses_with_members))
    print ("COURSES WITH NO ENROLLMENTS FILE WRITTEN")

    #what users did not get into courses?
    all_users = []
    for num in range( indx, indx+int(req_number_users)-1):
        all_users.append("%s_%d" % (USEREXTERNALIDSTEM, num))
    #print (all_courses)
    with open(output_file + "Users_with_no_enrollments-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt", "w") as text_file:
        text_file.write("\n##### This file contains the list of users not enrolled in a course #####\n")
        text_file.write(str(set(all_users) - users_in_courses))
    print ("USERS WITH NO ENROLLMENTS FILE WRITTEN")
    #print (set(all_users) - users_in_courses)

    if rest:
        print("WRITING DATA FILE and PROCESSING via REST, this will take a minute or so...")
    else:
        print("WRITING DATA FILE ONLY - you must process via SIS Framework...")

    with open(output_file+"_MEMBERSHIPS-"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".txt", "w") as text_file:
        text_file.write("\n##### DELETE THIS LINE....THE FOLLOWING IS A MEMBERSHIP SNAPSHOT FLAT FILE FOR STORE OR DELETE #####\n")
        text_file.write("##### DELETE THIS LINE.... DATASOURCEKEY %s #####\n" % DSKEXTERNALID)
        text_file.write("EXTERNAL_COURSE_KEY|EXTERNAL_PERSON_KEY|ROLE\n")

        if rest:
            print("WRITING DATA FILE and PROCESSING via REST, this will take a minute or so...")
            extId = "externalId:%s" % DSKEXTERNALID
            #same payload used for all membership requests
            json_payload = {
                "dataSourceId": extId,
                "availability": {
                    "available":"Yes"
                },
                "courseRoleId":"Student"
            }
        else:
            print("WRITING DATA FILE ONLY - you must process via SIS Framework...")
        counter = 0

        # take the above course_memberships dictionary,
        # iterate through the keys,
        # the values are the list of userIDs by index
        # write the snapshot file and
        # if REST send the request payload

        for key in course_memberships:
            courseID = key
            userID_list = course_memberships[key]

            for user in userID_list:
                text_file.write("%s|%s|Student\n" % (key, user))
                if rest:
                    global authorized_session
                    membership_session = Membership(rest, authorized_session.getToken())
                    membership_session.createMembership(courseID, user, json.dumps(json_payload), authorized_session.getToken())

def main(argv):

    target_url = ''
    output_file = 'LearnObjectGen'
    object = 'all'
    index = 5000
    req_number = 0
    req_max = False

    usageStr = "$ python learnObjectGen.py -i|--index <start index> [-t|--target_url] [-f|--output_file]  [-o|--object <Courses|Users|Memberships>] [-n|--number]"
    usageStr += "\n\t-t|--target_url : (Optional) Target URL - required to update with REST. If left blank output will be written to a the file specified by -f"
    usageStr += "\n\t-i|--index : (Optional) Starting index for object ids. e.g.: 1000"
    usageStr += "\n\t-n|--number : (Optional) Number of objects to create. e.g.: 10"
    usageStr += "\n\t-f|--output_file : (Optional) Snapshot Flat File prefix. Default: learnObjectGen"
    usageStr += "\nYou have to minimally provide either the target (-t) or index (-i)"
    usageStr += "\nProviding only the index arg writes Snapshot Flat Files for all objects (max count)."
    usageStr += "\nProviding only the target arg writes Snapshot Flat Files for all objects (max count) AND uses REST to create the objects on the target system."
    usageStr += "\n\tMax Counts: 100 Courses, 150 Users, 1000 Memberships"
    usageStr += "\nNOTE: Snapshot flat files are created to assist in managing created objects. These may be regenerated using the same index "
    usageStr += "and count arguments as when you created the objects and running without the -t argument.\n"
    usageStr += "Note: When creating memberships this tool will randomly distribute memberships, emulating a real world environment."
    usageStr += "Not all courses will have enrollments, not all Users will have enrollments.  Regenerated membership files will not align with previously generated "
    usageStr += "membership snapshot files.\n"

    if len(sys.argv) > 1: #there are command line arguments
        try:
            opts, args = getopt.getopt(argv,"ht:f:o:i:n:",["target=","output_file=","object=","index=","number="])
        except getopt.GetoptError as err:
            print (err)
            print (usageStr)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print (usageStr)
                sys.exit()
            elif opt in ("-t", "--target_url"):
                target_url = arg
            elif opt in ("-f", "--output_file"):
                output_file = arg
            elif opt in ("-i", "--index"):
                index = arg
            elif opt in ("-o", "--object"):
                object = arg
            elif opt in ("-n", "--number"):
                req_number = arg
            else:
                object = "all"


        if (req_number == 0):
            req_max = True
        if not output_file:
            output_file = OUTPUT_FILE
        if not index:
            index = INDEX

        print ('[main] Object is:', object)
        print ('[main] Index is:', index)
        print ('[main] req_number is:', req_number)
        print ('[main] req_max is:', req_max)

        if req_max:
            if object == 'all':
                print ("Creating ", MAX_COURSES, " Courses, ", MAX_USERS, " Users, and ", MAX_MEMBERSHIPS, " Memberships.\n")
            elif object != 'all':
                print ("Creating max number of " + object + "\n")
        else:
            if object == 'all':
                print ("Creating ", req_number, " Courses, ", req_number, " Users, and ", req_number, " Memberships.\n")
            elif object != 'all':
                print ("Creating ", req_number, " " + object + "\n")
    else:
        print(usageStr)
        sys.exit(2)

    start_time = datetime.datetime.now()

    if target_url:
        print ('[main] Using REST APIs - Acquiring auth token...\n')
        global authorized_session
        authorized_session = AuthToken(target_url)
        authorized_session.setToken()
        print ('[main] Returned token: ' + authorized_session.getToken() + '\n')
        print ('[main] Checking DataSource and creating if necessary...\n')
        global datasource_session
        datasource_session = DataSource(target_url, authorized_session.getToken())
        datasource_session.getDataSource(authorized_session.getToken())
        if not datasource_session.datasource_PK1:
            datasource_session.createDataSource(authorized_session.getToken())
            print ("[main] Data Source not found - created new Data Source\n")
        else:
            print ("[main] Data Source found.")
    else:
        print ("[main] Writing snapshot flat file: {}".format(output_file))


#depending on all or individual objects iterate through and process the specified object
    if "all" in object:
        print("Processing All Objects")
        process_all(req_number, index, output_file, target_url)
    elif "courses" in object:
        print("Processing Courses")
        process_courses(req_number, index, output_file, target_url)
    elif "users" in object:
        print("Processing Users")
        if req_number == 0: req_number = MAX_USERS
        process_users(req_number, index, output_file, target_url)
    elif "memberships" in object:
        print("Processing Memberships")
        process_memberships(req_number, index, output_file, target_url)

    end_time = datetime.datetime.now()

    total_time = (end_time - start_time)

    print ("Total Processing time: %s" % str(total_time))


if __name__ == '__main__':
    main(sys.argv[1:])
