import datetime
import pytz
 
# defining the object
obj = datetime.datetime(2001, 11, 15, 1, 20, 25)
 
# defining the timezone
tz = pytz.timezone('Asia/Kolkata')
 
# localising the datetime object
# to the timezone
aware_obj = tz.localize(obj)
 
# checking timezone information
print(aware_obj.tzinfo)
print(aware_obj)
print(type(aware_obj))