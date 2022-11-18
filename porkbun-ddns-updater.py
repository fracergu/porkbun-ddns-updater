#!/bin/python3
import sys
import time
import requests
import json

SECRET_API_KEY = ""
API_KEY = ""
DOMAIN = ""

#########################################
# Check for --sleep and --ttl options
#########################################

for i in range(len(sys.argv)):
    if sys.argv[i] == "--sleep":
        time.sleep(int(sys.argv[i+1]))
        break

for i in range(len(sys.argv)):
    if sys.argv[i] == "--ttl":
        ttl = int(sys.argv[i+1])
        break
    else:
        ttl = 600

#########################################
# Check for mode flags
#########################################

if '--all' in sys.argv and '--records' in sys.argv:
    print('You can only use one of --all or --records')
    sys.exit(1)
if '--all' not in sys.argv and '--records' not in sys.argv:
    print('You must use one of --all or --records')
    sys.exit(1)


#########################################
# Function definitions
#########################################

def updateRecord(record):
    if record['content'] == ip:
        print('Record ' + record['name'] + ' is already up to date')
        return
    deleteRecord(record)
    createRecord('' if record['name'] ==
                 DOMAIN else record['name'].replace(DOMAIN, ''))
    print('Record ' + record['name'] + ' updated to ' + ip)


def deleteRecord(record):
    requests.post('https://porkbun.com/api/json/v3/dns/delete/'+DOMAIN+'/' +
                  record['id'], json={'secretapikey': SECRET_API_KEY, 'apikey': API_KEY})


def createRecord(recordName):
    requests.post('https://porkbun.com/api/json/v3/dns/create/'+DOMAIN, json={'secretapikey': SECRET_API_KEY, 'apikey': API_KEY,
                  'name': DOMAIN if recordName == '' else recordName.replace(DOMAIN, ''), 'type': 'A', 'content': ip, 'ttl': ttl})


#########################################
# Get current IP
#########################################


ip = requests.get('https://api.ipify.org').text

#########################################
# Fetch A type records from domain
#########################################

records = json.loads(json.dumps([r for r in requests.post('https://porkbun.com/api/json/v3/dns/retrieve/'+DOMAIN,
                     json={'secretapikey': SECRET_API_KEY, 'apikey': API_KEY}).json()['records'] if r['type'] == 'A']))


#########################################
# All mode, just update all A records
#########################################

if sys.argv[1] == '--all':
    if len(records) == 0:
        print('No records found')
        sys.exit(1)
    for record in records:
        updateRecord(record)
    sys.exit(0)

#########################################
# Records mode, update specific records
# or create them if they don't exist
#########################################

if sys.argv[1] == '--records':
    inputRecords = sys.argv[2].split(',')
    for ir in inputRecords:
        found = True if len([r for r in records if r['name'] == (
            DOMAIN if ir == '' else ir+'.'+DOMAIN)]) > 0 else False

        if found:
            updateRecord([r for r in records if r['name'] == (
                DOMAIN if ir == '' else ir+'.'+DOMAIN)][0])
        else:
            print('Record ' + ir+'.'+DOMAIN + ' not found, creating')
            createRecord(ir)
    sys.exit(0)
