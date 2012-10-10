#!/usr/bin/env python3

import habr143972_vk_auth_2to3processed

import getpass
import json
import urllib.request, urllib.error, urllib.parse
from urllib.parse import urlencode

def callApi(method, params, token):
    if isinstance(params, list):
        params_list = [kv for kv in params]
    elif isinstance(params, dict):
        params_list = list(params.items())
    else:
        params_list = [params]
    params_list.append(("access_token", token))
    url = "https://api.vk.com/method/%s?%s" % (method, urlencode(params_list)) 
    return json.loads(urllib.request.urlopen(url).read().decode('utf-8'))["response"]

def dumpMessages(f, msgs, startNum = 1):
    i = startNum
    for msg in msgs[1:]:
        f.write(str(i) + ": " + msg.__repr__() + "\n")
        i += 1

if __name__ == "__main__":
    email = input("Email: ")
    password = getpass.getpass()
    token, user_id = habr143972_vk_auth_2to3processed.auth(email, password, "3168778", "messages")
    
    dumpMore = 'y'
    while dumpMore == 'y':
        UID = input("Target user ID: ")
        
        first200 = callApi("messages.getHistory", [("uid", UID), ("count", "200"), ("rev", "1"), ("offset", "0")], token)
        fullCount = int(first200[0])
        
        with open("dump_dialog_%s.txt" % UID, "w") as f:
            f.write("Messages count: %d\n\n" % fullCount)
            dumpMessages(f, first200)
            receivedCount = len(first200) - 1
            while receivedCount < fullCount:
                print("Dumped %d / %d" % (receivedCount, fullCount))
                next200 = callApi("messages.getHistory", [("uid", UID), ("count", "200"), ("rev", "1"), ("offset", str(receivedCount))], token)
                dumpMessages(f, next200, startNum = receivedCount + 1)
                receivedCount += len(next200) - 1
            print("Dumped %d / %d" % (receivedCount, fullCount))
        print("Finished dumping chat with user %s" % UID)
        dumpMore = input("Do you want to dump one more chat? (y/n) ")

    print("Goodbye!")
