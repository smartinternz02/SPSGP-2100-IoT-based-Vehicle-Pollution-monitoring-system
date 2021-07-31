import wiotp.sdk.device
import time
import requests
import random

from ibmcloudant.cloudant_v1 import CloudantV1
from ibmcloudant import CouchDbSessionAuthenticator
from ibm_cloud_sdk_core.authenticators import BasicAuthenticator

authenticator = BasicAuthenticator('apikey-v2-2fqwiwoufz8etrfmviwgkcgaqvxhc3fl19lakdoaj6hy', 'ae6d4b9928b96a0f78dc2a0c30d506de') #username, password

service = CloudantV1(authenticator=authenticator)

service.set_service_url('https://apikey-v2-2fqwiwoufz8etrfmviwgkcgaqvxhc3fl19lakdoaj6hy:ae6d4b9928b96a0f78dc2a0c30d506de@fd2a1a55-2bdb-4741-848e-851a2d88b7da-bluemix.cloudantnosqldb.appdomain.cloud')

myConfig = { 
    "identity": {
        "orgId": "1cidqc",
        "typeId": "mydevice",
        "deviceId":"789456123"
    },
    "auth": {
        "token": "123123123"
    }
}



client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()

def thresh(smoke, air_quality, harmful_gases):
    url = "https://www.fast2sms.com/dev/bulkV2?authorization=6lqAVKLc5i9vgnf3PsRDrTMwpC2aHj0Od81ZUkXuFWt4YhxGIb4X0HaVZtSdIjQbhlz57vDOCcE6BWxN&route=v3&sender_id=TXTIND&message=Hey,%20some%20aspects%20of%20your%20vehicle%20exhaust%20exceeded%20the%20Thresholds.%20Please%20check&language=english&flash=0&numbers=9505155234,"
    if smoke>85:
        sen = requests.get(url)
        print(sen.text)  
    if air_quality<15:
        sen = requests.get(url)
        print(sen.text)  
    if harmful_gases>80:
        sen = requests.get(url)
        print(sen.text)  
    
    
while True:
    smoke = random.randint(0, 100)
    air_quality = random.randint(0, 100)
    harmful_gases = random.randint(0, 100)
    lat = random.randint(-90, 90)
    lon = random.randint(-180, 180)
    
    thresh(smoke, air_quality, harmful_gases)

    myData={'smoke':smoke, 'air_quality':air_quality, 'harmful_gases':harmful_gases, 'latitude': lat, 'longitude': lon}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
    print("Published data Successfully: %s", myData)
    
    products_dc = {'smoke':smoke, 'air_quality':air_quality, 'harmful_gases':harmful_gases, 'latitude': lat, 'longitude': lon}

    response = service.post_document(db='noderedhzbna20210721', document=products_dc).get_result() #db = database name
    print(response)
    time.sleep(2)
    
client.disconnect()

