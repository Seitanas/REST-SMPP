# REST SMPP 
  
Application runs as REST service. It allows user to send SMS via SMPP protocol.


**INSTALLATION**


    mkdir sms
    virtualenv --python=python3 sms/
    souce sms/bin/activate
    git clone https://github.com/Seitanas/REST-SMPP
    cd REST-SMPP/
    pip install gunicorn smpplib2 falcon mysql-connector
    apt-get install mariadb-server

Create DB from sms/sms.sql  
Configure sms.cfg file


Start web service:

    gunicorn run:smsApp


You should create user first:

    ./user_manager username password

In order to authenticate, you must post JSON formatted array to http://yourserver:8000/auth

    curl -H "Content-Type: application/json" -X POST -d '{"auth": {"username":"username","password":"password"}}' http://localhost:8000/auth

This should provide an authentication token:

    {"token": {"id": "c9529864cef4121c4b1fd1c804", "expires_at": "2017-11-14 15:05:41", "created_at": "2017-11-13 15:05:41"}}

To send SMS you should post JSON formated array to http://yourserver:8000/sms and include `X-Auth-Token` in header:

     curl  -H "X-Auth-Token: c9529864cef4121c4b1fd1c804" -H "Content-Type: application/json" -XPOST -d '{"sendsms": {"number":"+4234","text":"testas"}}' http://localhost:8000/sms

**Service code is still under development.**