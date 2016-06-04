# arientosend
##Connecting to the Amazon EC2 instance:
ssh -i "TestServer.pem" ec2-user@ec2-54-172-241-8.compute-1.amazonaws.com

TestServer.pem is in the shared Google drive folder.

##Changes to files will not be updated until uwsgi is restarted. If uwsgi is running as a background process, it cannot be killed normally.
###Kill all uwsgi processes:  
killall -SIGINT uwsgi

###Start uwsgi in the foreground:
~/arientosend/arientosend/start_uwsgi.sh

###Start uwsgi in the background:
~/arientosend/arientosend/start_uwsgi.sh &

##After adding static files (css, js) to static/ run the collectstatic command so that nginx can see them
sudo python manage.py collectstatic

##Pushing to the git repo from the instance requires a key:
eval `` `ssh-agent -s` ``  
ssh-add ~/.ssh/github

###Restart nginx server:
sudo service nginx restart

###Script to cleanup expired files every minute
~/arientosend/arientosend/cleanup.sh

### Current Ariento users in the database
test@ariento.com  
other@ariento.com  
pirzadaza@gmail.com

