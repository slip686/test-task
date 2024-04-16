TEST-TASK API

Building and running docker container

- git pull repository https://github.com/slip686/test-task
- Before building image, specify environment vars in .env file
to configure DB connection
- run "docker build -t test_task ." to build docker image file
- run "docker run -d -p 5473:80 test_task" to start container. Specify docker port if necessary. 
API using postgres driver, DB must have postgis extension.
All tables will be created automatically. Docs will be available by "/docs" endpoint

Flush data to DB

- git pull repository https://github.com/slip686/points
- run "pip install -r requirements.txt"
- specify environment vars in .env file to configure DB connection
- From repository "points" run "loader.py" to flush data to DB. Provide path to .xlsx file to upload_data() function
