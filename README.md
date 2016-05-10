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

##Pushing to the git repo from the instance requires a key:
eval `ssh-agent -s'  
ssh-add ~/.ssh/github

##Restart nginx server:
sudo service nginx restart
