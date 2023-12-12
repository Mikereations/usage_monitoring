# usage_monitoring
This repo is for a server client based resources monitoring software. The server receives http post requests from the clients indicating usage and it stores it in a sqlite database and display it in a portal. 

To run, use : 
flask --app app run

While its running, if you want to test you can in a seperate terminal run send.py. You might need to change the url components if you are not running locally.
