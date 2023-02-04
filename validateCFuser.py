import requests

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
