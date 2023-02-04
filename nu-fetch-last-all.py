import requests
from datetime import datetime
from db import DB

db = DB()
def makeEntity(handle , sub):
    d = datetime.fromtimestamp(sub['creationTimeSeconds'])
    _date = d.day
    _month = d.month
    _year = d.year
    _hour = d.hour
    _min = d.minute
    _sec = d.second
    if 'rating' in sub['problem'].keys() :
        rating = sub['problem']['rating']
    else :
        rating = "None"
        
    if 'contestId' in sub.keys() :
        contestId = sub['contestId']
    else :
        contestId = "None"
    return {
        "handle" : handle,
        "contestId" : contestId,
        "index" : sub['problem']['index'],
        "name" : sub['problem']['name'],
        "rating" : rating,
        "tags" : (str)(sub['problem']['tags']),
        "second" : _sec,
        "minute" : _min,
        "hour" : _hour,
        "date" : _date,
        "month" : _month,
        "year" : _year,
        "submissionId" : sub['id'],
        "programmingLanguage" : sub['programmingLanguage'],
        "verdict" : sub['verdict'],
        "submissionLink" : "https://codeforces.com/contest/" + (str)(contestId) + "/submission/" + (str)(sub['id'])
    }
file = open("nu-cf-handles.txt" , "r")
NU_USERS = []
for each in file.readlines() :
    temp = each.split()
    handle = temp[2]
    if len(handle) >= 5 and handle[:5] == 'India' :
        handle = handle[5:]
    NU_USERS.append(handle) 

doneUsers = 0
data = []

# NU_USERS = ['persevere_07']
for handle in NU_USERS :
    doneUsers += 1
    try : 
        url = "https://codeforces.com/api/user.status?handle=" + handle
        response = requests.get(url)
        res = response.json()
        if res['status'] != 'OK' :
            print(handle + " -> failed !!!")
            continue
        res = res['result']
        n = len(res)
        for i in range(len(res)) :
            sub = res[i]
            data.append(makeEntity(handle=handle , sub=sub))
            # if (i + 1) % 100 == 0 :
                # print(handle + " (" + (str)(doneUsers) + "/" + (str)(len(NU_USERS)) + ") : " + (str)(i + 1) + " Added to db. (" + (str)(i + 1) + "/" + (str)(n) + ")")
        
        print(handle + " (" + (str)(doneUsers) + "/" + (str)(len(NU_USERS)) + ")")
        
    except KeyboardInterrupt :
        break
    
    except :
        print(handle + "-> failed !!!")
        
print("total : " , len(data))
db.addSubmissionAll(data=data)
print("Done :)")