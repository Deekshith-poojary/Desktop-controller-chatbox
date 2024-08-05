import requests
import subprocess
import os
import time,sys
import json,getpass
# URL of the server endpoint where you want to send the data
url = 'http://127.0.0.1:8000/api/data'
lpin=1

def setup():
    requests.post('http://127.0.0.1:8000/api/setup')

def login():
    username=input('enter username: ')
    password=getpass.getpass(prompt='enter password: ')
    #input('enter password')
    login_data={'username':username,'password':password}
    status=requests.post('http://127.0.0.1:8000/system_login',data=login_data).json()['login']
    if status==0:
        print('invalid username or password')
        sys.exit(0)
    
login()
setup()
while True:
    command_dir=requests.post('http://127.0.0.1:8000/api/send').json()
    command=command_dir["cmd"]
    pin=command_dir['pin']
    if lpin==pin:
        result = subprocess.run(command, capture_output=True, text=True,shell=True)
        lpin+=1
    if result.stdout:
        send_out=result.stdout
    elif result.stderr:
        send_out=result.stderr
    else:
        send_out='command executed'

    data = {
        'output': send_out,
        'pin': lpin-1
    }

    # Send POST request
    response = requests.post(url, data=data)

    # Print the response from server (status code and response body)
    print(f"Response status code: {response.status_code}")
    print(f"Response text: {response.text}")
    time.sleep(3)
