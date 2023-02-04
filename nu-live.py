import requests
from datetime import datetime
from db import DB

db = DB()
ju_server = "https://discord.com/api/webhooks/1063664044759859263/pPYQgv-Mj1f0FHMK68HLDf2Nol1iuYQilgg5BsheasmA10zs-zNReNbLnlbL8FhtINjv"
        
discord_webhook_url = 'https://discord.com/api/webhooks/1063683998007697499/BuufF0Si__WHgASkWRWm3zVgu_MvfebdGz2Yxs6mh7qKQT1yhfQ2TSHGw-UIpvh4c2kC'

# discord_webhook_url = ju_server

def makeEntity(handle , sub):
    TODAY = "http://worldtimeapi.org/api/timezone/Asia/Kolkata"
    TODAY = requests.get(TODAY)
    TODAY = TODAY.json()['datetime']
    temp = TODAY.split('-')
    TODAY = datetime(month=(int)(temp[1]) , year=(int)(temp[0]) , day=(int)(temp[2].split('T')[0]) , hour = (int)(temp[2].split('T')[1].split('.')[0].split(':')[0]) , minute=(int)(temp[2].split('T')[1].split('.')[0].split(':')[1]) , second=(int)(temp[2].split('T')[1].split('.')[0].split(':')[2]))
    print("Today : " , TODAY)
    d = TODAY
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

def CString(s) :
    n = (len)(s)
    s = s + " " * (20 - n)
    return s

def problemLink(cid , pid) :
    return 'https://codeforces.com/contest/' + (str)(cid) + '/problem/' + (str)(pid)

def submissionLink(cid , sid) :
    return 'https://codeforces.com/contest/' + (str)(cid) + '/submission/' + (str)(sid)

def sendMSG(handle , cid , pid , sid , verdict) :
    Message = {
        "content": '```' + '\n' + CString("Handle") + ":   " + handle + '\n' + CString("Problem Link") + ":   " + problemLink(cid , pid) + '\n' + CString("Submission Link") + ":   " + submissionLink(cid , sid) + '\n' + CString("Verdict") + ":   " + verdict + '```'
    }
    requests.post(discord_webhook_url , data=Message)


file = open("nu-cf-handles.txt" , "r")
NU_USERS = []
for each in file.readlines() :
    temp = each.split()
    handle = temp[2]
    if len(handle) >= 5 and handle[:5] == 'India' :
        handle = handle[5:]
    NU_USERS.append(handle) 

dataBaseHandles = db.db['linkedHandles'].find({})
for each in dataBaseHandles : 
    if each['handle'] not in NU_USERS : 
        NU_USERS.append(each['handle'])
        print(each['handle'] , " : added from db")
    
print(NU_USERS)
url = "https://codeforces.com/api/problemset.recentStatus?count=1000"
prevSubmissionId = -1
while True :  
    try :  
        res = requests.get(url)
        res = res.json()
        if res['status'] == 'OK' : 
            newID = -1
            for each in res['result'] :
                if len(each['author']['members']) == 0 :
                    continue
                handle = each['author']['members'][0]['handle']
                if handle in NU_USERS :
                    cid = each['contestId']
                    pid = each['problem']['index']
                    sid = each['id']
                    verdict = each['verdict']
                    
                    if verdict == 'TESTING' :
                        continue
                    
                    if verdict == 'OK' :
                        verdict = 'Accepted'
                    
                    if sid == prevSubmissionId :
                        break
                    
                    if newID == -1 :
                        newID = sid
                    
                    sendMSG(handle=handle , cid=cid , pid=pid , sid=sid , verdict=verdict)
                    
                    makeEntry = makeEntity(handle=handle , sub=each)
                    db.addSubmission(makeEntry)
                    # print(makeEntry)
                    print(handle , sid , cid , pid , verdict)
            if newID != -1 :
                prevSubmissionId = newID
        else :
            print('API error :(')
    except KeyboardInterrupt :
        print("Stopping...")
        break
    except :
        print("Something went wrong.")
