# constants file for BBDN-REST_DEMO-Python

#IDs and Descriptions for create
DSKEXTERNALID = 'BBDN-OBJECTGEN-DSK'
COURSEEXTERNALIDSTEM = 'BBDN-OBJECTGEN-COURSE'
USEREXTERNALIDSTEM = 'BBDN-OBJECTGEN-USER'

DSKDESCRIPTION = 'Data Source used for OBJECTGEN'

MAX_USERS = 150
MAX_COURSES = 100
MAX_MEMBERSHIPS = 1000
MAX_PER_COURSE_MEMBERSHIPS = 25
INDEX = 5000

#URLs
COURSES_PATH = '/learn/api/public/v1/courses' #create(POST)/get(GET)
COURSE_PATH = '/learn/api/public/v1/courses/externalId:'
USERS_PATH = '/learn/api/public/v1/users' #create(POST)/get(GET)
USER_PATH = '/learn/api/public/v1/users/externalId:'
MEMBERSHIPS_PATH = '/learn/api/public/v1/courses/courseId/users' #create(POST)/get(GET)
MEMBERSHIP_PATH = '/learn/api/public/v1/courses/courseId/users/userId'
USER_MEMBERSHIPS_PATH = '/learn/api/public/v1/users/userId/courses'
DATASOURCES_PATH = '/learn/api/public/v1/dataSources' #create(POST)/get(GET)
DATASOURCE_PATH = '/learn/api/public/v1/dataSources/externalId:'

OUTPUT_FILE = "learnObjectGen"
