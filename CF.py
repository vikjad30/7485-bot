from bs4 import BeautifulSoup
import requests

def getSubmissionCode(cid , sid) :
    try : 
        url = "https://codeforces.com/contest/" + (str)(cid) + "/submission/" + (str)(sid)
        r = requests.get(url)
    except :
        return "Something went wrong !!!"
    htmlContent = r.content
    soup = BeautifulSoup(htmlContent , features="html.parser")
    code = soup.find('pre')
    if code == None : return "Something went wrong !!!"
    return code.text

def validateCFuser(handle) :
    try :
        url = "https://codeforces.com/api/user.info?handles=" + handle
        response = requests.get(url)
        res = response.json()
        if res['status'] != 'OK' :
            return False
        return True
        
    except :
        return False
