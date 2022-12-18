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

    client = mqtt_client.Client()  #ko co id
    client.username_pw_set(ACCESS_TOKEN)
    client.connect(broker,port,keepalive=60)
    return client

def init_responce() :
    payload = "{}"
    return payload

def add_json(key , value, responce: str):
    json_responce = json.loads(responce)
    json_responce[key] = value
    return json.dumps(json_responce)


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        y = json.loads(msg.payload.decode())                        #convert sang json
        z = json.dumps(y)                                           #convert to string
        repsonTopic = str(msg.topic)
        responce =  repsonTopic.replace("request", "response")

        if z.count('pin') != 0 :           
            payload = init_responce()
            payload = add_json(y["params"]["pin"], y["params"]["enabled"], payload)
            payload = payload.replace("\"true\"", "true")
            payload = payload.replace("\"false\"", "false")
            print("PARSE SUCCESSFULLY..................")
            print(payload)
            client.publish("v1/devices/me/attributes", payload)
            client.publish(responce, payload)

        else :
            payload = init_responce()
            payload = add_json(1, "false", payload)
            payload = add_json(2, "false", payload)
            client.subscribe(topic)
            client.publish("v1/devices/me/attributes", payload)
            client.publish(responce, payload)


    print("CALLBACK>>>>>>>>>>>>>>>>>>>>>>>>")
    payload = init_responce()
    payload = add_json(1, "true", payload)
    payload = add_json(2, "true", payload)
    client.on_message = on_message
    client.subscribe(topic)
    client.publish("v1/devices/me/attributes", payload)
    
def run() :
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()




if __name__ == '__main__':
    run()