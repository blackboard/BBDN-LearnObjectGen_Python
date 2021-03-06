# BBDN-LearnObjectGen-Python
This project is a Python app for generating test User, Course, and Membership objects in Blackboard Learn.
It writes Snapshot Flat Files and optionally uses the Blackboard Learn REST APIs to update your developer/test instance.

This sample code was built with Python 3.7.0 and the latest Developer AMI.

### Project at a glance:
- Target: Blackboard Learn SaaS and Q2 2016 Release 3000.1.0 minimum
- Source Release: v1.1
- Release Date  2020-12-28
- Author: shurrey

- Target: Blackboard Learn SaaS and Q2 2016 Release 3000.1.0 minimum
- Source Release: v1.0
- Release Date  2016-04-29
- Author: moneil

### Requirements:
- Python  3.7.0
- Developer account - register at https://developer.blackboard.com
- Test instance


### Setting Up Your Development Environment
#### Python development tools
You will first need to install Python 3.7.0. You can use tools like brew or ports to install, or run the installation manually.

You may also install Python tools for your IDE or use a text editor and terminal to run the python code.


### Included Files
file | description
--- | ---
learnObjectGen.py | this is the main script.<br/>
constants.py | this file contains constants used by the application.<br/>
auth.py | this script contains the code for authenticating the application and managing tokens<br/>
datasource.py | this script creates or gets the datasource for the generated data.<br/>
course.py | this script contains REST source for creating Courses in Learn<br/>
user.py | this script contains REST source for creating Users in Learn<br/>
membership.py | this script contains REST source for creating User's course memberships (enrollments)


### What it does
Having a test environment is great - having a test environment with data is <i>awesome</i>! 
The learnObjectGenerator creates Snapshot Flat Files for Courses, Users, and Memberships. 
User course memberships are randomly distributed across the created courses to simulate an
SIS populated environment - not all courses will end up with members, and not all users will 
end up in courses.

In addition to creating one Snapshot Flat File for each of the objects created (which are 
useful for removing the test objects), the application also optionally utilizes the REST APIs
 to create the objects in Learn.
 
Two additional files are created - one which presents the courses created which did not receive memberships 
and one which presents users which were created but were not placed in courses.

 
This script demonstrates authenticating a REST application, use of the authorization token, 
creating supported Learn objects, and writing files

<i><b>NOTE:</b> Before running the example code you must register a developer account and application as described on the Developer Docs <a href="https://docs.blackboard.com/learn/rest/getting-started/registry">REST Registration</a> and <a href="https://docs.blackboard.com/learn/rest/getting-started/rest-and-learn">Managing REST Integrations in Learn: The REST Integrations Tool for System Administrators</a> pages. You must also configure the script as outlined in the below Configure the Script section.</i>

When run the script will in the following order:<br/>
1. Authenticate<br/>
2. Create the specified or maximum allowed Courses for the Developer AMI using the specified or default starting index.<br/>

The application does not support deleting created objects - you are responsible for system cleanup using the generated snapshot files.

e.g.:
```
$ python learnObjectGen.py -i|--index <start index> [-t|--target_url] [-f|--output_file]  [-o|--object <Courses|Users|Memberships>] [-n|--number]
            -t|--target_url : (Optional) Target URL - required to update with REST. If left blank output will be written to a the file specified by -f
            -i|--index : (Optional) Starting index for object ids. e.g.: 1000
            -n|--number : (Optional) Number of objects to create. e.g.: 10
            -f|--output_file : (Optional) Snapshot Flat File prefix. Default: learnObjectGen
         You have to minimally provide either the target (-t) or index (-i)
         Providing only the index arg writes Snapshot Flat Files for all objects (max count).
         Providing only the target arg writes Snapshot Flat Files for all objects (max count) AND uses REST to create the objects on the target system.
         Max Counts: 100 Courses, 150 Users, 1000 Memberships
         NOTE: Snapshot flat files are created to assist in managing created objects. These may be regenerated using the same index
         and count arguments as when you created the objects and running without the -t argument.
         Note: When creating memberships this tool will randomly distribute memberships, emulating a real world environment.
         Not all courses will have enrollments, not all Users will have enrollments. Regenerated membership files will not align with previously generated 
         membership snapshot files.

```

For example:
```
$ python learnObjectGen.py -i 1000 
```
<i>Creates the maximum developer license supported number of all objects starting with the index (-i) of 1000. 100 Courses, 150 Users, 1000 Memberships
</i>
<br/><br/>

```
$ python learnObjectGen.py -t localhost:9877
```
<i>Uses REST to create the maximum developer license supported number of all objects starting with the default index of 5000.<br/>
Writes Snapshot files to learnObjectGen
</i>
<br/><br/>

```
$ python learnObjectGen.py -t localhost:9877 -i 2000
```
<i>Uses REST to create the maximum developer license supported number of all objects starting with the index of 2000. </i>
<br/><br/>

```
$ python learnObjectGen.py -t localhost:9877 -i 2000 -n 10
```
<i>Uses REST to create 10 of all objects starting with the index of 2000. </i>
<br/><br/>

```
$ python learnObjectGen.py -t localhost:9877 -i 2000 -n 10 -f myoutput
```
<i>Uses REST to create 10 of all objects starting with the index of 2000 and creates snapshot files with the prefix "myoutput".<br/>
E.g.: myoutput_COURSES-20160427-171504.txt</i>
<br/><br/>


## Running the Demo!
### Setup Your Test Server
To run the demo if you have not already done so you must as outlined above register the application via the Developer Portal and add the application to your test environment using the REST API Integration tool.


### Configuring the Script
Before executing the script to run against your test server you must configure it with your registered application's Key and Secret.

1. Open auth.py and edit lines 33 and 34.<br/>
2. On line 33 replace "insert_your_application_key_here" with the key issued when you registered your application.<br/>
3. On line 34 replace "insert_your_application_secret_here" with the secret issued when you registered your application.

Once you have setup your test server and changed auth.py to reflect your application's key and secret you may run the command line tools as outlined above or via your IDE.
