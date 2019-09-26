import certifi
import config
from datetime import datetime
from faker import Faker
from flask import Flask
from flask import jsonify
from flask import request
import json
import logging
import os
import random
import requests
import sys
import threading
import time
import uuid

from azure.eventhub import EventHubClient, Sender, EventData

logger = logging.getLogger("azure")

# Define app
app = Flask(__name__)

# set up brands
brands = ['Samsung','Nokia','Apple','Huawei','Blackberry','OnePlus','Sony']
urls = ['http://www.site1.com/abc','http://www.site2.com/abc','http://www.site3.com/abc','http://www.site4.com/abc','http://www.site5.com/abc','http://www.site6.com/abc','http://www.site7.com/abc','http://www.site8.com/abc','http://www.site9.com/abc','http://www.site10.com/abc']

# event builders
def create_advert_event(brands):
	brand = random.choice(brands)
	return(str([{"EntityType":"Adverts", "createdDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "advertID": random.randint(1,100), "brand": brand}]))

def create_impression_event(urls):
	fake = Faker('en_GB')
	name = fake.name().split()
	url = random.choice(urls)
	return(str([{"EntityType":"Impressions", "impressionDate": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "advertID": random.randint(1,100), "impressionURL": url, "firstName":name[0],"lastName":name[1], "sessionID": str(uuid.uuid4())}]))

# Address can be in either of these formats:
# "amqps://<URL-encoded-SAS-policy>:<URL-encoded-SAS-key>@<mynamespace>.servicebus.windows.net/myeventhub"
# "amqps://<mynamespace>.servicebus.windows.net/myeventhub"
# For example:
#ADDRESS = "amqps://streaming-etl-eh.servicebus.windows.net/streaming-etl-eh"

# SAS policy and key are not required if they are encoded in the URL
#USER = "kafka-manage"
#KEY = "noL290HOsrP9cWhhry8x9KsjVFf0b48jk/LHlPDniFk="


@app.before_first_request
def json_generator():
    def run_job():
        # Create Event Hubs client
        client = EventHubClient(config.ADDRESS, debug=False, username=config.USER, password=config.KEY)
        sender = client.add_sender(partition="0")
        client.run()
        while True:
            try:
                messages = [create_advert_event(brands), create_impression_event(urls)]
                for message in messages:
                    print('Sending message to Event Hubs: ' + str(message))
                    sender.send(EventData(message))
                    time.sleep(1)
            except:
                raise
    thread = threading.Thread(target=run_job)
    thread.start()

@app.route('/')
def hello():
    return "<h1>Hello World!</h1><h2>Welcome to the streaming-etl-producer server</h2><p><ul><li>The application is now sending data to your kafka endpoint.</li><li>Monitor stdout to view messages being output from the app.</li></ul></p>"


def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://127.0.0.1:5000/')
                if r.status_code == 200:
                    print('Server started, quiting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
        time.sleep(2)
    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()

if __name__ == '__main__':
    start_runner()
    app.run()