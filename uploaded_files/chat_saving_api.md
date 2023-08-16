
route: /conversation/add_msg    (methods-POST)(authentication required)
    
    -It saves a user query

    -Request: The request must contain a json object with the following perimeter:
        - user_message(The question or query that the user performs on the Ai agent
        - agent_message(The reply of the Agent to the user_message)
        - namespace

    Response: if the authentication is passed, the api will save the query to the database
              should return a response similer to this:
              
                {
                    "data": {
                        "success": "msg saved for the user roni123"
                    },
                    "status_code": 200,
                    "success": true
                }

route: /conversation/get_msg    (methods-POST)(authentication required)

    -It retreives user quiries from the databases.
    
    -Request: the request must have a json object with the following perimeter:
        - pagination(the name speaks for itself)
        - namespace(the name speaks for itself)
    
    -Response: It will try to fetch queries for the given peremiter.
               If it fails to find any conversation for that user it will return a
               402 response like this:

                    {
                        'error': f"no messages with user abc found"
                    }
               Else It will give a response similer to the following:

                    {
                        "data": {
                            "messages": [
                                {
                                    "agent_msg": "Ans1",
                                    "date": "Fri, 11 Aug 2023 04:26:13 GMT",
                                    "is_archived": false,
                                    "namespace": "folder_1",
                                    "user_msg": "Q1"
                                },
                                {
                                    "agent_msg": "Ans2",
                                    "date": "Fri, 11 Aug 2023 04:26:25 GMT",
                                    "is_archived": false,
                                    "namespace": "folder_1",
                                    "user_msg": "Q2"
                                },
                                {
                                    "agent_msg": "Ans3",
                                    "date": "Sun, 13 Aug 2023 23:52:52 GMT",
                                    "is_archived": false,
                                    "namespace": "folder_1",
                                    "user_msg": "Q3"
                                },
                                {
                                    "agent_msg": "Ans344",
                                    "date": "Mon, 14 Aug 2023 00:01:12 GMT",
                                    "is_archived": false,
                                    "namespace": "folder_1",
                                    "user_msg": "Q345"
                                },
                                {
                                    "agent_msg": "Ans344",
                                    "date": "Mon, 14 Aug 2023 00:01:27 GMT",
                                    "is_archived": false,
                                    "namespace": "folder_1",
                                    "user_msg": "Q345"
                                }
                            ]
                        },
                        "status_code": 200,
                        "success": true
                    }
                                                    "date": "Fri, 11 Aug 2023 04:26:13 GMT",

    -Plz notice the datetime format. It follows as:
        - <DAY><comma,space><DATE><space><MONTH><space><YEAR><space><HOUR><colon><MINUTE><colon><SECOND><space><TIMEZONE>

                    