import random
import json
from paho.mqtt import client as mqtt_client

import paho.mqtt.client as paho  		    #mqtt library
import os
import json
import time
from datetime import datetime

broker = '127.0.0.1'
port = 1883
topic = "v1/devices/me/rpc/request/+"
broker="127.0.0.1"   			    #host name
port=1883 					    #data listening port
ACCESS_TOKEN='ufgVcklJD3yoKTWSBoa9'    
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'

state1 = "false"
state2 = "false"

def connect_mqtt() -> mqtt_client:

    client = mqtt_client.Client(client_id)
    client.connect(broker, port)
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(broker,port,keepalive=60)
    return client

def convert():
    payload="{"
    payload+="\"1\":"
    payload+=state1
    payload+="," 
    payload+="\"2\":"
    payload+=state2
    payload+="}"
    print(payload)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("HJAHAHAHAHAH")
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        print(msg.payload.decode())
        y = json.loads(msg.payload.decode())

        if y["params"]["pin"] == True :
            state = str(y["params"]["enabled"])
            payload="{"
            payload+="\"1\":"
            payload+=state
            payload+="}"
            print("PARSE SUCCESSFULLY..................")
            print(payload)
        else :
            state = str(y["params"]["enabled"])
            payload="{"
            payload+="\"2\":"
            payload+=state
            payload+="}"    
            print("PARSE SUCCESSFULLY..................")
            print(payload)
        

        client.publish("v1/devices/me/attributes", payload)
    
    payload="{"
    payload+="\"1\":"
    payload+=state1
    payload+="," 
    payload+="\"2\":"
    payload+=state2
    payload+="}"

    client.publish("v1/devices/me/attributes", payload)
    client.subscribe(topic)
    client.on_message = on_message


def run() :
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()




if __name__ == '__main__':
    run()