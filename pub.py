import paho.mqtt.client as paho  		    #mqtt library
import os
import json
import time
from datetime import datetime

ACCESS_TOKEN='ufgVcklJD3yoKTWSBoa9'                 #Token of your device
broker="127.0.0.1"   			    #host name
port=1883 					    #data listening port

# def on_publish(client,userdata,result):             #create function for callback
#     print("data published to thingsboard \n")
#     pass
# client1= paho.Client("control1")                    #create client object
# client1.on_publish = on_publish                     #assign function to callback
# client1.username_pw_set(ACCESS_TOKEN)               #access token from thingsboard device
# client1.connect(broker,port,keepalive=60)           #establish connection
# print("HAHAHAHAHAHAH")

def on_message(client, userdata, msg):
  print ('Incoming message\nTopic: ' + msg.topic + '\nMessage: ' + str(msg.payload))
  if msg.topic.startswith('v1/devices/me/rpc/request/+'):
    #    print ('This is a Two-way RPC call. Going to reply now!')
    #    responseMsg = "{\"rpcReceived\":\"OK\"}"
    #    print ('Sending a response message: ' + responseMsg)
    #    client.publish('tb/mqtt-integration-tutorial/sensors/SN-001/rx/response', responseMsg)
    #    print ('Sent a response message: ' + responseMsg)
       return
    print("KAKAKAKKAKA")

while True:
  
   payload="{"
   payload+="\"1\":true,"; 
   payload+="\"2\":false"; 
   payload+="}"
   ret= client1.subscribe("v1/devices/me/rpc/request/+") #topic-v1/devices/me/telemetry
   client1.publish("v1/devices/me/attributes", payload);
   print("Please check LATEST TELEMETRY field of your device")
   print(payload);
   print("Pub done*************************")
   time.sleep(5)