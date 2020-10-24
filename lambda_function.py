import os
import json
import boto3
import requests

# Create SQS client
sqs = boto3.client('sqs')
queue_url = os.environ['MAILING_QUEUE_URL']


#@getJsonObject()
#method gets User, Class, School, Activity_log json objects from respective API urls
#no return
def getJsonObject():
    try:
        url1 = os.environ['ACTIVITY_LOG_API_URL']
        headers = {"X-API-KEY": os.environ['API_KEY']}
        activity_log = requests.get(url1, headers=headers)
        activity_log = activity_log.json()
        
        url2 = os.environ['USER_API_URL']
        users = requests.get(url2)
        users = users.json()
        
        url3 = os.environ['CLASS_API_URL']
        classes = requests.get(url3)
        classes = classes.json()
        
        url4 = os.environ['SCHOOL_API_URL']
        schools = requests.get(url4)
        schools = schools.json()
        
        
    except requests.exceptions.RequestException as e:
        print(e.response)
    else:
        print("API call success")



#@queryRecord()
#method queries Json objects for:
    #number of visits
    #number of classes added
    #number of students added
#for each school
#and sends result to an Amazon SQS queue

def queryRecord():
    #loop through list of users
    for user in users:
        
        #for each user, loop through list of schools
        for school in schools['data']:
            
            #get name of current school
            curSchool = school['school_name']
            
            #check if current school belongs to current user (by ID)
            if school['user_id'] == user['id']:
            
                #count variable to keep track of number of visits to current school
                countVisit = 0
                
                #count variable to keep track of number of "joins" to current school
                countStuJoin = 0
                
                #count variable to keep track of number of classes added to current school
                countClasAd = 0
                
                #count variable to keep track of number of visits by owner to current school
                ownVisit = 0
                
                #boolean variable to tell if the current school was created this week
                schCreate = False
                
                #for each school(belonging to current user), loop through list of activities for the week
                for activity in activity_log['data']:
                    
                    #check if current activity has an action pertaining to current school
                    if activity['school_id'] == school['school_id']:
                        
                        #check if a "visit" action was performed by a student on current school
                        if ((activity['action']=="Visited")and(activity['user_type']=="Student")):
                            
                            #increment number of student-visits
                            countVisit += 1
                            
                        #check if a "join" action was performed by a student on current school
                        if ((activity['action']=="Joined school")and(activity['user_type']=="student")):
                            
                            #increment number of "joins"
                            countStuJoin += 1
                            
                        #check if a "class added" action was performed by the owner of current school
                        if ((activity['action']=="Added a class")and(activity['user_type']=="Owner")):
                            
                            #increment number of classes added
                            countClasAd += 1
                            
                        #check if a "school create" action was performed by the owner of current school
                        if ((activity['action']=="Created a school")and(activity['user_type']=="Owner")):
                            
                            schCreate = True
                            
                        #check if a "visit" action was performed by the owner of current school
                        if ((activity['action']=="Visited")and(activity['user_type']=="Owner")):
                            
                            #increment number of owner-visits
                            ownVisit += 1
                
                
                templateName = "mail-analytics-template"
                email = user['email']
                templateData = {
                    "name": user['username'],
                    "school": curSchool,
                    "studentVisit": str(countVisit),
                    "classAdded": str(countClasAd),
                    "studentJoin": str(countStuJoin)
                }
                
                message = {
                    "email": email,
                    "templateName": templateName,
                    "templateData": templateData
                }
                
                
                # Send message to SQS queue
                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageAttributes={},
                    MessageBody=json.dumps(message),
                    MessageGroupId="1"
                )
        
                print(response['MessageId'])



def lambda_handler(event, context):
    
    getJsonObject()
    queryRecord()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Done running!')
    }