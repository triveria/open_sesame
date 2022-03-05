from datetime import datetime
import yaml
from pathlib import Path
import paho.mqtt.client as mqtt
import time
import configparser


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


def open_door():
    (client_name, broker_ip, topic, message) = load_mqtt_config()
    client = mqtt.Client(client_name)
    client.connect(broker_ip)
    client.publish(topic, message)