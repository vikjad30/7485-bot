from pymongo import MongoClient
class DB :
    def __init__(self) :
        CONNECTION_STRING = "mongodb+srv://ju:ju@cluster0.lvmcxvm.mongodb.net/test"
        self.client = MongoClient(CONNECTION_STRING)
        self.db = self.client['test']
        
    async def addDB(self , author , msg , channel , time) :
        self.db['test'].insert_one({
            "author" : author,
            "message" : msg,
            "channel" : channel,
            "time" : time
        })
    
    def addSubmission(self , details) :
        try :
            temp = self.db['liveSubmission'].find_one({"submissionId" : details['submissionId']})
            if temp == None :
                self.db['liveSubmission'].insert_one(details)
                print("Submission added")
            else :
                print("Submission already exist")
        except :
            print("Add submission error.")
            
    def addSubmissionAll(self , data) :
        try :
            self.db['liveSubmission'].insert_many(data)
            print("Added successfully")
        except : 
            print("Error at dbSubmissionAll")
            pass
        
    def addHandle(self , dcUser , handle) :
        try : 
            temp = self.db['linkedHandles'].find_one({"dcUser" : dcUser})
            msg = ""
            if temp == None :
                print("New user")
                self.db['linkedHandles'].insert_one({
                    "dcUser" : dcUser ,
                    "handle" : handle
                })
                print(handle , " Added successfully !!!")
                msg = handle + " Added !! :white_check_mark: "
            
            else :
                print(handle , " already exist")
                msg = "Prev linked handle : " + temp['handle'] + '\n'
                self.db['linkedHandles'].update_one({"dcUser" : dcUser} , { "$set": { 
                    "dcUser" : dcUser ,
                    "handle" : handle
                } })
                print(handle , " Added successfully !!!")
                msg += handle + " updated !! :white_check_mark: "
        except :
            msg = "Something went wrong. Try again.";
        return msg
            
        
        
        
# db = DB()

# alreadyExist = {}
# temp = db.db['liveSubmission'].find()

# cnt = 0
# deleted = 0

# unique = []
# for each in temp :
#     cnt += 1
#     subid = each['submissionId']
#     if subid in alreadyExist.keys() :
#         deleted += 1
#         db.db['liveSubmission'].delete_one({"submissionId" : subid})
#         print("deleted : " , deleted)
#     else :
#         alreadyExist[subid] = True    
    
#     if cnt % 10000 == 0 :
#         print(cnt , "done")
        
# # print("Duplicate : " , duplicate)
# # db.db['liveSubmission'].delete_many({})
# # print("All data gone.")
# # db.db['liveSubmission'].insert_many(unique)
# # print("All unique data added")

# # print('done')
# # # db.addSubmission({
# #     "submissionId": 1,
# # })

# # print('done')
# # db.addHandle('me' , 'JUBHAI')

# # temp = db.db.find({})
# # for x in temp :
# #     print(x)
# # print(temp)
# # db.addHandle(dcUser="me" , handle="JUBHAI")