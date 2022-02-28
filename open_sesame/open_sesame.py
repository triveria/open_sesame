"""
For now, this only works with WhatsApp.
You send a WhatsApp message to your twilio account and in response a MQTT message is sent to your smart door.
"""

# ref.: https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio

#TODO: use relais to control door strikes
#TODO: make full program via cookiecutter: run, add --name="Gast" --number="491721234567" --expires=+6h
#TODO: add ESP project as submodule
#TODO: translate responses


from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import yaml
from pathlib import Path
import paho.mqtt.client as mqtt
import time
import configparser


app = Flask(__name__)


def read_yaml(filepath):
    with open(filepath, 'r') as read_file:
        content = yaml.safe_load(read_file)
    return content


def load_allow_list():
    allow_list_filepath = Path("/etc/open_sesame/allow_list.yaml")
    allow_list = read_yaml(allow_list_filepath)
    return allow_list


def is_access_granted(sender, allow_list):
    if sender not in allow_list:
        return False

    valid_from = datetime.strptime(allow_list[sender]['valid_from'], "%Y.%m.%d - %H:%M:%S")
    valid_until = datetime.strptime(allow_list[sender]['valid_until'], "%Y.%m.%d - %H:%M:%S")
    now = datetime.now()

    if (valid_from <= now) and (now <= valid_until):
        return True
    else:
        return False


def load_ini():
    ini_filepath = Path("/etc/open_sesame/open_sesame.ini")
    ini = configparser.ConfigParser()
    ini.read(ini_filepath)
    return ini


def load_mqtt_config():
    ini = load_ini()
    client_name = ini['MQTT']['clientName']
    broker_ip   = ini['MQTT']['brokerIP']
    topic       = ini['MQTT']['topic']
    message     = ini['MQTT']['message']
    return (client_name, broker_ip, topic, message)


def send_open():
    (client_name, broker_ip, topic, message) = load_mqtt_config()
    client = mqtt.Client(client_name)
    client.connect(broker_ip)
    client.publish(topic, message)


@app.route('/', methods=['POST'])
def bot():
    allow_list = load_allow_list() # always read allow_list when receiving new message
    sender = request.values.get('WaId', '').lower()
    print(f"type(sender) = {type(sender)}")
    print(f"sender = {sender}")
    access_granted = is_access_granted(sender, allow_list)
    if access_granted:
        send_open()
        response = "you may enter"
    else:
        response = "you shall not pass"
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(f'{response}')
    return str(resp)


def main():
    app.run()
