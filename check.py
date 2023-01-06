import json
from paho.mqtt import client as mqtt_client

import paho.mqtt.client as paho  		    #mqtt library

import json
import time
from datetime import datetime
from threading import Thread
import threading
import time
import serial
import ast
import re


broker="127.0.0.1"   			    #host name
port=1883 					    #data listening port
ACCESS_TOKEN1 ='ufgVcklJD3yoKTWSBoa9'    #Smart-lighting -VietPro -- Group Led 1
ACCESS_TOKEN2 ='8rQoOpUxcBmUVkkZaVOb'   # viet : group Led 2 
ACCESS_TOKEN3= 'VPsng4Dk3KXh0NTKwhVt'   # Update infor
TELEMETRY = "v1/devices/me/telemetry"
ATTRIBUTE = "v1/devices/me/attributes"
topic = "v1/devices/me/rpc/request/+"

inf = 'inf'
conf = 'conf'
pin = 'pin'

#data_uart = {"TY":2, "ID": 1, "ON":"0", "DI":30, "TI":10, "SE":100}
z1baudrate = 115200
z1port = '/dev/pts/5'  # set the correct port before run it

# >>>>>>>>>>>>>>>>>>>>>>>>>>>> UART

def connect_uart() -> mqtt_client:
    uart = mqtt_client.Client()  
    uart.connect('127.0.0.1', 1884)
    return uart

def pushUpdateConfigureToThingsboard(TY, ON, DI,  TI, SE) :
    payload = init_responce()
    payload = add_json('TY', str(TY), payload)
    payload = add_json('ON', str(ON), payload)
    payload = add_json('DI', str(DI), payload)
    payload = add_json('TI', str(TI), payload)
    payload = add_json('SE', str(SE), payload)
    return payload    

def convertData(data_uart: str) :
    print ('Data received through uart: ' + data_uart)
    result = re.findall(r"\b\w+:\s*\d+\b", data_uart)

    for item in result:
        key, value = item.split(':')
        value = int(value)
        if key == 'TY':
            TY = value
        elif key == 'ID':
            print("ID vo dich")
            ID = value
        elif key == 'ON':
            ON = value
        elif key == 'DI':
            DI = value
        elif key == 'TI':
            TI = value                        
        elif key == 'SE':
            print("SE vo dich")
            SE = value
    
    if 'TY' in locals() and 'ID' in locals() and 'ON' in locals() and 'DI' in locals() and 'TI' in locals() and 'SE' in locals() :
        print('exist')
        payload = pushUpdateConfigureToThingsboard(TY, ON, DI, TI, SE)
        return ID, payload
    else: 
        ID = -102
        payload = init_responce()
        return ID, payload


def run_uart(client) :
    z1serial = serial.Serial(port=z1port, baudrate=z1baudrate)
    z1serial.timeout = 2  # set read timeout

    print ('Serial Opened')  # True for opened
    if z1serial.is_open:
        while True:
            size = z1serial.inWaiting()
            if size:
                data_uart = z1serial.readline(size).decode("utf-8")
                data_uart = json.loads(data_uart)
                print(data_uart["ID"])
                print(data_uart)
                
                if "TY" in z and "EX" in z and "ID" in z :
                    print("ID = 0")
                    print(payload)
                    client[0].publish(TELEMETRY, payload)

                elif ID == 1 :
                    print("ID = 1")                    
                    print(payload)
                    client[1].publish(TELEMETRY, payload)

                elif ID == 2 :
                    print("ID = 2")
                    print(payload)
                    client[2].publish(TELEMETRY, payload)  

                else :
                    print("Data Received Through UART Not Valid")              
            
            else:
                print ('no data')
            time.sleep(1)
    else:
        print ('z1serial not open')



# >>>>>>>>>>>>>>>>>>>>>>>>>>>> JSON

def check_state(fullstring: str, substring: str) :
    if fullstring.find(substring) != -1:
        payload_telemetry =  {"STATE": "ON"}
        payload_telemetry = json.dumps(payload_telemetry)       # return string
        return payload_telemetry
    else:
        payload_telemetry =  {"STATE": "OFF"}
        payload_telemetry = json.dumps(payload_telemetry)       # return string
        return payload_telemetry    

def init_responce() :
    payload = "{}"
    return payload

def add_json(key , value, responce: str):
    json_responce = json.loads(responce)
    json_responce[key] = value
    payload = json.dumps(json_responce)

    return payload

def respond_message(z: str, y: json, responce: str, client: mqtt_client):
    if "TY" in z and "EX" in z and "ID" in z :
        payload = y["params"]
        str_payload = json.dumps(payload)
        print('Set information: ' + str_payload)

    elif z.count(conf) != 0 and "TY" in z and "ID" in z and "ON" in z and "DI" in z and "TI" in z:    
        payload = y["params"]
        str_payload = json.dumps(payload)
        print('Set configuration: ' + str_payload)

    elif z.count(pin) != 0 and "enabled" in z and "Group" in z:           
        payload = init_responce()
        payload = add_json(y["params"]["pin"], y["params"]["enabled"], payload)
        payload_telemetry = check_state(payload, "true")                    #return JSON
        print('Control Pin: ' + payload_telemetry)
        print('payload ' + payload)
        client.publish("v1/devices/me/attributes", payload)
        client.publish(TELEMETRY, payload_telemetry)
        client.publish(responce, payload)

    else :
        payload = init_responce()
        payload = add_json(1, "false", payload)
        payload = add_json(2, "false", payload)
        client.subscribe(topic)
        client.publish(ATTRIBUTE, payload)
        client.publish(responce, payload)     



# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> MQTT


def connect_mqtt(TOKEN: str) -> mqtt_client:
    client = mqtt_client.Client()  
    client.username_pw_set(TOKEN)
    client.connect(broker, port, keepalive=60)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        y = json.loads(msg.payload.decode())                        #convert sang json
        z = json.dumps(y)                                           #convert to string
        repsonTopic = str(msg.topic)
        responce =  repsonTopic.replace("request", "response")
        respond_message(z, y, responce, client)


    print("CALLBACK>>>>>>>>>>>>>>>>>>>>>>>>")
    payload = init_responce()
    payload = add_json(1, "true", payload)
    payload = add_json(2, "true", payload)
    client.on_message = on_message
    client.subscribe(topic)
    client.publish("v1/devices/me/attributes", payload)
    
def run(client: mqtt_client) :
    client.loop_forever()

if __name__ == '__main__':
    client = connect_mqtt(ACCESS_TOKEN1)
    client1 = connect_mqtt(ACCESS_TOKEN2)
    client2 = connect_mqtt(ACCESS_TOKEN3)
    
    subscribe(client)
    subscribe(client1)
    subscribe(client2)

    #uart = connect_uart()
    uart_client = [client, client1, client2]
    # subscribe_uart(uart_client)



    t1 = threading.Thread(target=run, args=(client,))
    t2 = threading.Thread(target=run, args=(client1,))
    t3 = threading.Thread(target=run, args=(client2,))

    t5 = threading.Thread(target=run_uart, args=(uart_client,))
    t1.start()
    t2.start()
    t3.start()

    t5.start()
