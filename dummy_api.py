import json


#dummy json object for Pledre users (school owners and class owners)
users = {
        "data":[
        {
            "user_id":"1",
            "user_name":"Some Name",
            "user_email":"somename@email.mail"
        },
        {
            "user_id":"2",
            "user_name":"Adifferent Name",
            "user_email":"adifferentname@email.mail"
        },
        {
            "user_id":"3" ,
            "user_name":"Yetanother Name",
            "user_email":"yetanothername@email.mail"
        }
    ]
}

#dummy json object for classes on Pledre
classes = {
    "data":[
        {
            "class_id":"1",
            "school_id":"1",
            "class_name":"Design & Prints",
            "user_id":"1",
            "students":50
        },
        {
            "class_id":"2",
            "school_id":"1",
            "class_name":"Photography",
            "user_id":"1",
            "students":54
        },
        {
            "class_id":"3",
            "school_id":"2",
            "class_name":"Fishery",
            "user_id":"2",
            "students":504
        },
        {
            "class_id":"4",
            "school_id":"none",
            "class_name":"Standalone Class",
            "user_id":"3",
            "students":501
        },
        {
            "class_id":"5",
            "school_id":"3",
            "class_name":"Pastries & Bakes",
            "user_id":"3",
            "students":503
        }
    ]
}


#dummy json object for schools on pledre
schools = {
    "data":[
        {
            "school_id":"1",
            "school_name":"School of Arts and Photography",
            "user_id":"1",
            "teachers":20
        },
        {
            "school_id":"2",
            "school_name":"Fish School",
            "user_id":"2",
            "teachers":10
        },
        {
            "school_id":"3",
            "school_name":"Culinary Skills",
            "user_id":"3",
            "teachers":13
        }
    ]
}


#dummy json object for activity log of Pledre users (student, class owners & school owners)
#get request returns json object for activity log over 1 week
activity_log = {
    "data":[
        {
            "user_id":"1",
            "user_type":"owner",
            "class_id":"1",
            "school_id":"1",
            "action":"created a school"
        },
        {
            "user_id":"001123",
            "user_type":"student",
            "class_id":"1",
            "school_id":"3",
            "action":"visit"
        },
        {
            "user_id":"001128",
            "user_type":"student",
            "class_id":"2",
            "school_id":"1",
            "action":"visit"
        },
        {
            "user_id":"001129",
            "user_type":"student",
            "class_id":"2",
            "school_id":"1",
            "action":"joined school"
        },
        {
            "user_id":"001158",
            "user_type":"student",
            "class_id":"1",
            "school_id":"3",
            "action":"joined school"
        },
        {
            "user_id":"3",
            "user_type":"owner",
            "class_id":"5",
            "school_id":"3",
            "action":"added a class"
        },
        {
            "user_id":"1",
            "user_type":"owner",
            "class_id":"4",
            "school_id":"1",
            "action":"added a class"
        }
    ]
}



#@queryRecord()
#method queries Json objects for:
    #number of visits
    #number of classes added
    #number of students added
#for each school
#and outputs result on the console

def queryRecord():
    #loop through list of users
    for user in users['data']:
        
        #for each user, loop through list of schools
        for school in schools['data']:
            
            #get name of current school
            curSchool = school['school_name']
            
            #check if current school belongs to current user (by ID)
            if school['user_id'] == user['user_id']:
            
                #count variable to keep track of number of visits to current school
                countVisit = 0
                
                #count variable to keep track of number of "joins" to current school
                countStuJoin = 0
                
                #count variable to keep track of number of classes added to current school
                countClasAd = 0
                
                #for each school(belonging to current user), loop through list of activities for the week
                for activity in activity_log['data']:
                    
                    #check if current activity has an action pertaining to current school
                    if activity['school_id'] == school['school_id']:
                        
                        #check if a "visit" action was performed by a student on current school
                        if ((activity['action']=="visit")and(activity['user_type']=="student")):
                            
                            #increment number of visits
                            countVisit += 1
                            
                        #check if a "join" action was performed by a student on current school
                        if ((activity['action']=="joined school")and(activity['user_type']=="student")):
                            
                            #increment number of "joins"
                            countStuJoin += 1
                            
                         #check if a "class added" action was performed by the owner of current school
                        if ((activity['action']=="added a class")and(activity['user_type']=="owner")):
                            
                            #increment number of "joins"
                            countClasAd += 1
                            
                #output results for each school owner
                print ("School Owner " + user['user_name'] + " has had " + str(countVisit) + " visit(s),")
                print (str(countVisit) + " class(es) added,")
                print ("and " + str(countStuJoin) + " student(s) added to the school, " + curSchool + ", this week\n")



def handler(event, context):
    
    queryRecord()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Done running!')
    }