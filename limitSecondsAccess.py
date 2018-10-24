#!/usr/bin/python
# coding:utf-8

import time
import datetime
import cgi
import os
from pathlib import Path
import re
import sys
import inspect
import traceback
import json

# Definition
def limitSecondsAccess():
    try:
        # Init
        ## Access Timestamp Build
        sec_usec_timestamp = time.time()
        sec_timestamp = int(sec_usec_timestamp)

        ## Access Limit Default Value
        ### Depends on Specifications: For Example 10
        access_limit = 10

        ## Roots Build
        ### Depends on Environment: For Example '/tmp'
        tmp_root = '/tmp'
        access_root = os.path.join(tmp_root, 'access')

        ## Auth Key
        ### Depends on Specifications: For Example 'app_id'
        auth_key = 'app_id'

        ## Response Content-Type
        ### Depends on Specifications: For Example JSON and UTF-8
        response_content_type = 'Content-Type: application/json; charset=utf-8'

        ### Response Bodies Build
        ### Depends on Design
        response_bodies = {}

        # Authorized Key Check
        query = cgi.FieldStorage()
        auth_id = query.getvalue(auth_key)
        if not auth_id:
            raise Exception('Unauthorized', 401)
    
        # The Auth Root Build
        auth_root = os.path.join(access_root, auth_id)

        # The Auth Root Check
        if not os.path.isdir(auth_root):
            # The Auth Root Creation
            os.makedirs(auth_root, exist_ok=True)

        # A Access File Creation Using Micro Timestamp
        ## For example, other data resources such as memory cache or RDB transaction.
        ## In the case of this sample code, it is lightweight because it does not require file locking and transaction processing.
        ## However, in the case of a cluster configuration, file system synchronization is required.
        access_file_path = os.path.join(auth_root, str(sec_usec_timestamp))
        path = Path(access_file_path)
        path.touch()

        # The Access Counts Check
        access_counts = 0
        for base_name in os.listdir(auth_root):
            ## A Access File Path Build
            file_path = os.path.join(auth_root, base_name)

            ## Not File Type
            if not os.path.isfile(file_path):
                continue

            ## The Base Name Data Type Casting
            base_name_sec_usec_timestamp = float(base_name)
            base_name_sec_timestamp = int(base_name_sec_usec_timestamp)

            ## Same Seconds Stampstamp
            if sec_timestamp == base_name_sec_timestamp:

                ### A Overtaken Processing
                if sec_usec_timestamp < base_name_sec_usec_timestamp:
                    continue

                ### Access Counts Increment
                access_counts += 1

                ### Too Many Requests
                if access_counts > access_limit:
                    raise Exception('Too Many Requests', 429)

                continue

            ## Past Access Files Garbage Collection
            if sec_timestamp > base_name_sec_timestamp:
                os.remove(file_path)

    except Exception as e:
        # Exception Tuple to HTTP Status Code
        http_status = e.args[0]
        http_code = e.args[1]

        # 4xx
        if http_code >= 400 and http_code <= 499:
            # logging
            ## snip...
        # 5xx
        elif http_code >= 500:
            # logging
            # snip...

            ## The Exception Message to HTTP Status
            http_status = 'foo'
        else:
            # Logging
            ## snip...

            # HTTP Status Code for The Response
            http_status = 'Internal Server Error'
            http_code = 500

        # Response Headers Feed
        print('Status: ' + str(http_code) + ' ' + http_status)
        print(response_content_type + "\n\n")

        # A Response Body Build
        response_bodies['message'] = http_status
        response_body = json.dumps(response_bodies)

        # The Response Body Feed
        print(response_body)

# Excecution
limitSecondsAccess()
