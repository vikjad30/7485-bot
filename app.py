import discord
import os
from dotenv import load_dotenv
from datetime import date, datetime
import requests
from db import DB
import pytz

db = DB()
BLOCKED_USERS = ['Dhru08#8877']
ME = 'Urvik#2249'
TODAY = datetime.now()
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def compare_two_dates(d1 , d2) :
    return d1.day == d2.day and d1.month == d2.month and d1.year == d2.year
def prev_day(d) :
    d = datetime(year=d.year , month=d.month , day=d.day)
    return datetime.fromtimestamp(datetime.timestamp(d) - SEC_PER_DAY)
def next_day(d) :
    d = datetime(year=d.year , month=d.month , day=d.day)
    return datetime.fromtimestamp(datetime.timestamp(d) + SEC_PER_DAY)

def update_today() :
    try : 
        TODAY = "http://worldtimeapi.org/api/timezone/Asia/Kolkata"
        TODAY = requests.get(TODAY)
        TODAY = TODAY.json()['datetime']
        temp = TODAY.split('-')
        
        # temp_obj = datetime.now()
        time_zone = pytz.timezone('Asia/Kolkata')
        # update_today()
        TODAY = datetime(month=(int)(temp[1]) , year=(int)(temp[0]) , day=(int)(temp[2].split('T')[0]) , hour = (int)(temp[2].split('T')[1].split('.')[0].split(':')[0]) , minute=(int)(temp[2].split('T')[1].split('.')[0].split(':')[1]) , second=(int)(temp[2].split('T')[1].split('.')[0].split(':')[2]))
        TODAY = time_zone.localize(TODAY)
        print("Today : " , TODAY)
        p = next_day(TODAY)
        for i in range(7) :
            p = prev_day(p)
            LAST_SEVEN_DAYS.append(p)
    except :
        print("Today error")
        
@client.event
async def on_ready() :
    
    # try : 
    
    # except :
    #     print("Bot main function crashed.")
    #     pass
    update_today()
    print("Ready to serve....")
    # while True : 
    #     pass
    
@client.event
async def on_message(m) :
    username = str(m.author)
    msg = str(m.content)
    channel = str(m.channel.name)
    Channel = m.channel
    
    if username == 'HopeBot#1332' :
        return
    
    try :
        currentTime = "http://worldtimeapi.org/api/timezone/Asia/Kolkata"
        currentTime = requests.get(currentTime)
        print(currentTime.json())
        currentTime = currentTime.json()['datetime']
        print(currentTime)
    except :
        currentTime = -1
        print("problem in fetching current time.")
    await db.addDB(msg=msg , author=username , channel=channel , time=currentTime)
    
    if username in BLOCKED_USERS :
        await m.delete()
        return 
    
    print("username : " , username)
    print("message : " , msg)
    print("channel : " , channel)
    
    # await m.reply('working')
    
    msg = msg.split(' ')
    print(msg)
    
    try :
        if len(msg) == 0 :
            return
        
        if msg[0][0] == '>' :
            command = msg[0][1:]
            print(command)
            
            if command == 'alive' :
                await m.reply("Yes :grinning: ! Thank you for asking. :blush: ")
            
            if command == 'done' :
                await m.reply(":blush: ")
            
            elif command == 'help' :
                embed=discord.Embed(title="HopeBot command list", description="Enjoy the bot." , color=0x49fdfa)
                embed.add_field(name='>alive' , value='Check whether the bot is live or not' , inline=False)
                embed.add_field(name='>code' , value='Get submission link of any problem solved by provided user' , inline=False)
                embed.add_field(name='>help' , value='List of commands' , inline=False)
                embed.add_field(name='>identify' , value='Link your cf handle with your discord account for further use related to bot commands' , inline=False)
                embed.add_field(name='>info' , value='CF profile information about entered user' , inline=False)
                embed.add_field(name='>todaystat' , value='Submission statistics of all nirmaties' , inline=False)
                embed.add_field(name='>ranking' , value='Contest standing for NU users' , inline=False)
                embed.add_field(name='>me' , value='CF profile information of you' , inline=False)
                await m.reply(embed=embed)
            
            elif command == "magic" : 
                try :
                    if username != ME :
                        await m.reply("You are not allowed to use this command")
                        return
                    
                    n = (int)(msg[1])
                    dn = 0
                    while n > 0 :
                        n -= 1
                        msg1 = await discord.utils.get(m.channel.history(), author__name='Urvik')
                        if msg1 == None : 
                            await m.channel.send("All deleted")
                            return
                        await msg1.delete()
                        dn += 1
                        if dn % 5 == 0 :
                            await m.channel.send((str)(dn) +  " messages deleted.")
                except :
                    await m.reply("Something went wrong.")
                    
            elif command == "ranking" :
                try :
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
                        
                    cid = msg[1]
                    url = "https://codeforces.com/api/contest.standings?contestId="+(str)(cid) +"&showUnofficial=false"
                    print("Fetching of contest ranking started...")
                    send_me = ""
                    res = requests.get(url)
                    res = res.json()
                    heading = True
                    if res['status'] == 'OK' :
                        print(NU_USERS)
                        headString = "Rank".ljust(6) + "|" + "Handle".ljust(15) + "|";
                        for prob in res['result']['problems'] :
                            if 'points' in prob :
                                pt = prob['points']
                            else :
                                pt = 1
                            baseString = prob['index'] + ' ' + (str)((int)(pt))
                            headString += baseString.center(7) + "|"
                        headString += '\n'
                        headString += "".join(['-' for i in range(len(headString))]) + '\n'
                        send_me += headString
                        res = res['result']['rows']
                        for r in res :
                            rank = r['rank']
                            handle = r['party']['members'][0]['handle']
                            if handle in NU_USERS :
                                if len(handle) > 15 :
                                    handle = handle[:15]
                                print(handle)
                                entity = (str)(rank).ljust(6) + "|" + (str)(handle).ljust(15) + "|";
                                for prob in r['problemResults'] :
                                    if 'points' in prob :
                                        pt = prob['points']
                                    else :
                                        pt = 1
                                    entity += (str)((int)(pt)).center(7) + "|";
                                entity += '\n'
                                if len(send_me) + len(entity) < 1900 :
                                    send_me += entity;
                                else :
                                    await m.channel.send('```' + send_me + '```')
                                    send_me = entity
                    
                    if len(send_me) > 0 : await m.channel.send('```' + send_me + '```')
                    print("Fetching of contest ranking finished...")
                except :
                    await m.channel.send("Something went wrong :(")
            
            elif command == 'db' :
                if username != ME :
                    await m.reply("You are not allowed to view the details.")
                else :
                    temp = db.db['liveSubmission'].find()
                    cnt = 0
                    for each in temp :
                        cnt += 1
                    await m.reply("Total entries : " + (str)(cnt))
            
            elif command == 'solvedby' :
                try :
                    if len(msg) != 3 :
                        await m.reply("Invalid command. Use '>solvedby conetst-id problem-index'")
                    else :
                        cid = (int)(msg[1])
                        pid = msg[2]
                        print("cid : " , cid , "pid : " , pid)
                        temp = db.db['liveSubmission'].find({
                            "contestId" : cid,
                            "index" : pid
                        })
                        
                        when = {}
                        subids = {}
                        sublinks = {}
                        for each in temp :
                            handle = each['handle']
                            verdict = each['verdict']
                            sid = each['submissionId']
                            sublink = 'https://codeforces.com/contest/' + (str)(cid) + '/submission/' + (str)(sid)
                            day = (str)(each['date'])
                            day = "0"*(2-len(day)) + day
                            month = (str)(each['month'])
                            month = "0"*(2-len(month)) + month
                            year = (str)(each['year'])
                            hour = (str)(each['hour'])
                            hour = "0"*(2-len(hour)) + hour
                            min = (str)(each['minute'])
                            min = "0"*(2-len(min)) + min
                            sec = (str)(each['second'])
                            sec = "0"*(2-len(sec)) + sec
                            time = day + "-" + month + "-" + year + "   " + hour + ":" + min + ":" + sec
                                                        
                            if verdict != 'OK' :
                                continue
                            
                            if handle not in when.keys() :
                                when[handle] = time
                                subids[handle] = (int)(sid)
                                sublinks[handle] = sublink
                            
                            elif subids[handle] < (int)(sid) :
                                when[handle] = time
                                subids[handle] = (int)(sid)
                                sublinks[handle] = sublink
                        
                        embed=discord.Embed(title="Problem : " + (str)(cid) + (str)(pid) + " solved by" , color=0xffde38)
                        subids = sorted(subids.items(), key=lambda x:x[1])
                        print(subids)
                        for each in reversed(subids) :
                            print(each)
                            handle = each[0]
                            embed.add_field(name=when[handle] + "         " + handle, value=sublinks[handle] , inline=False)
                            
                        await m.reply(embed=embed)
                        
                except :
                    await m.reply("Something went wrong.")
                
            elif command == 'todaystat' :
                try :
                    TODAY = "http://worldtimeapi.org/api/timezone/Asia/Kolkata"
                    TODAY = requests.get(TODAY)
                    TODAY = TODAY.json()['datetime']
                    temp = TODAY.split('-')
                    
                    # temp_obj = datetime.now()
                    time_zone = pytz.timezone('Asia/Kolkata')
                    # update_today()
                    TODAY = datetime(month=(int)(temp[1]) , year=(int)(temp[0]) , day=(int)(temp[2].split('T')[0]) , hour = (int)(temp[2].split('T')[1].split('.')[0].split(':')[0]) , minute=(int)(temp[2].split('T')[1].split('.')[0].split(':')[1]) , second=(int)(temp[2].split('T')[1].split('.')[0].split(':')[2]))
                    TODAY = time_zone.localize(TODAY)
                    print("Today -> " , TODAY)
                    temp = db.db['liveSubmission'].find({
                        "date" : TODAY.day,
                        "month" : TODAY.month,
                        "year" : TODAY.year
                    })
                    dir = {}
                    accepted = {}
                    
                    for each in temp :
                        if each['handle'] not in dir.keys() :
                            dir[each['handle']] = 0
                            accepted[each['handle']] = 0
                        if each['verdict'] == 'OK':
                            accepted[each['handle']] += 1
                        dir[each['handle']] += 1 
                        
                    dir = sorted(dir.items(), key=lambda x:x[1])
                    today = (str)(TODAY)
                    today = " ".join(today.split('.')[0].split('T'))
                    # await m.channel.send(today)
                    embed=discord.Embed(title="Submission Count Leaderboard", color=0x49fdfa)
                    for each in reversed(dir) :
                        embed.add_field(name=each[0], value="Submission Count : " + (str)(each[1]) + "\t\t\t|\t\t\tAccepted : " + (str)(accepted[each[0]]), inline=False)
                        
                    await m.reply(embed=embed)
                    
                except :
                    await m.reply("Something went wrong.")
                    
            elif command == 'identify' :
                try :
                    if len(msg)  != 2 :
                        await m.reply("Invalid command : Use '>identify cf-handle'")
                        return
                    handle = msg[1]
                    respond = db.addHandle(dcUser=username , handle=handle)
                    await m.reply(respond)
                except :
                    await m.reply("Something went wrong.")
            
            elif command == 'me' :
                try :
                    temp = db.db['linkedHandles'].find_one({"dcUser" : username})
                    if temp == None :
                        await m.reply("You have not added your handle :smiling_face_with_tear: \nUse command '>identify handle' to link your account.:thumbsup: ")
                    else :
                        handle = temp['handle']
                        await m.reply(embed=fetch_user(handle))
                        
                except :
                    await m.reply("Something went wrong.")
                
            elif command == 'info' :
                if len(msg) != 2 :
                    await m.reply("Invalid command : Use '>info username'")
                    return
                
                handle = msg[1]
                print(handle)
                await m.reply(embed=fetch_user(handle))
                
            elif command == 'code' :
                # code , handle , contest id , problem id
                if len(msg) != 4 :
                    await m.reply("Invalid command : Use '>code handle contest-id problem-index'")
                    return
            
                await m.reply(getCode(handle=msg[1] , cid=msg[2] , pid=msg[3]))
    except :
        print("Main thread error happened.")
        return
            
            

            
    

def getCode(handle , cid , pid) :
    try : 
        cid = (int)(cid)
        url = "https://codeforces.com/api/user.status?handle=" + handle
        response = requests.get(url)
        res = response.json()
        reply = "-1"
        if res['status'] != 'OK' :
            reply = "Something went wrong."
        else :
            res = res['result']
            
            subids = []
            problem_name = ""
            for sub in res :
                if 'verdict' not in sub or 'contestId' not in sub or 'problem' not in sub: continue # BUG 1
                if sub['verdict'] != 'OK' or sub['contestId'] != cid or sub['problem']['index'] != pid: continue
                problem_name = sub['problem']['name']
                subids.append(sub['id'])
            
            if len(subids) == 0 :
                reply = "This problem is not solved by " + handle
            
            else :
                reply = "Problem : " + (str)(pid) + " . " + problem_name + '\n'
                reply += "Handle : " + handle + '\n'
                reply += "Total " + (str)(len(subids)) + " accepted solutions\n\n";
                
                for i in range(len(subids)) :
                    url = "https://codeforces.com/contest/" + (str)(cid) + "/submission/" + (str)(subids[i])
                    reply += (str)(i + 1) + ". " + url + '\n'
    except :
        reply = "Something went wrong."
    
    print(reply)
    return reply
        
    
    # await m.delete()







SEC_PER_DAY = 24 * 60 * 60
LAST_SEVEN_DAYS = []



def fetch_user(handle) :
    print('fetching user : ' , handle)
    url = "https://codeforces.com/api/user.info?handles=" + handle
    response = requests.get(url)
    res = response.json()
    if res['status'] != 'OK' :
        return discord.Embed(title="Something went wrong.")
    res = res['result'][0];
    if 'rating' in res.keys() :
        rating = str(res['rating']) + " " + res['rank'] + " (Max Rating : " + (str)(res['maxRating']) + " " + res['maxRank'] + ")"  
    else :
        rating = "unrated"
        
    dp = res['avatar']
    if 'firstName' in res.keys() :
        fname = res['firstName']
    else :
        fname = ""
    
    if 'lastName' in res.keys() :
        lname = res['lastName']
    else :
        lname = ""
    desc = fname + " " + lname
    statistics = problem_count(handle=handle)
    if statistics == -1 :
        return discord.Embed(title="Something went wrong :(")
    print("after function")
    print(response)
    print(type(response.content))
    print(response.content)
    prof_url = "https://codeforces.com/profile/" + handle
    embed=discord.Embed(title=handle, url=prof_url, description=desc, color=0x98f5fb)
    embed.set_thumbnail(url=dp)
    embed.add_field(name="Rating", value=rating, inline=False)
    # embed.add_field(name="Current strikes", value=statistics['current_strike'], inline=True)
    # embed.add_field(name="Max strikes", value=statistics['max_strike'], inline=True)
    embed.add_field(name="Total submission", value=statistics['total_submission'], inline=False)
    # embed.add_field(name="AC", value=statistics['AC'], inline=True)
    # embed.add_field(name="WA", value=statistics['WA'], inline=True)
    # embed.add_field(name="RE", value=statistics['RE'], inline=True)
    # embed.add_field(name="TLE", value=statistics['TLE'], inline=True)
    # embed.add_field(name="MLE", value=statistics['MLE'], inline=True)
    
    embed.add_field(name="Problem solved", value=statistics['total_solved'], inline=False)
    embed.add_field(name="Solved in last month", value=statistics['last_month_count'], inline=True)
    embed.add_field(name="Solved in last 7 days", value=statistics['last_seven_days_count'], inline=True)
    return embed


def problem_count(handle) :
    print("Problem count of : " , handle)
    url = "https://codeforces.com/api/user.status?handle=" + handle
    response = requests.get(url)
    res = response.json()
    if res['status'] != 'OK' :
        return -1
    res = res['result'];
    a = 0
    problems = set()
    dates = []
    today_solved_count = 0
    today_solved = []
    last_week_count = 0
    last_month_count = 0
    last_seven_days_count = 0
    submission_verdict = {
        "OK" : 0 ,
        "WRONG_ANSWER" : 0 ,
        "RUNTIME_ERROR" : 0 ,
        "TIME_LIMIT_EXCEEDED" : 0 ,
        "MEMORY_LIMIT_EXCEEDED" : 0
    }
    for sub in res :
        if 'verdict' not in sub : continue # BUG 1
        if sub['verdict'] not in submission_verdict :
            submission_verdict[sub['verdict']] = 0
        submission_verdict[sub['verdict']] += 1
        
        if sub['verdict'] == 'OK' :
            sub_date = datetime.fromtimestamp(int(sub['creationTimeSeconds']))
            if str(sub['problem']) not in problems :
                if compare_two_dates(TODAY , sub_date) :
                    print("Today submission")
                    today_solved.append(sub['problem'])
                    today_solved_count += 1
                if prev_day(next_day(sub_date)) in LAST_SEVEN_DAYS :
                    last_seven_days_count += 1
                if sub_date.month == TODAY.month and sub_date.year == TODAY.year :
                    last_month_count += 1
            # if sub_date.month == TODAY.month and sub_date.year == TODAY.year:
            #     print(sub['problem']['name'] , " : ")
            dates.append(sub_date)
            if a==0 :
                a=1
                datetime_obj = sub_date
                tt = compare_two_dates(datetime.now() , datetime_obj)
                print(tt)
            prob = str(sub['problem'])
            problems.add(prob)
    
    print(submission_verdict)
    p_solved = len(problems)
    return {
        "all_solved" : problems ,
        "total_submission" : len(res),
        "AC" : submission_verdict['OK'],
        "WA" : submission_verdict['WRONG_ANSWER'],
        "RE" : submission_verdict['RUNTIME_ERROR'],
        "TLE" : submission_verdict['TIME_LIMIT_EXCEEDED'],
        "MLE" : submission_verdict['MEMORY_LIMIT_EXCEEDED'],
        "total_solved" : p_solved,
        "last_month_count" : last_month_count,
        "today_solved_count" : today_solved_count,
        "today_solved" : today_solved,
        "last_seven_days_count" : last_seven_days_count
    }


if __name__ == "__main__" :
    client.run(BOT_TOKEN)
    #done done