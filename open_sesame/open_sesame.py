"""
For now, this only works with WhatsApp.
You send any WhatsApp message to your twilio account and in response a MQTT message is sent to your door.
"""

# ref.: https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio

#TODO: how to control house door via telephone?? => without it, project is useless
#       => is there DC available? Can MOSFETS pass AC?
#       => design + 3D print box for custom electronics
#TODO: make ESP an MQTT client
#TODO: make full program via cookiecutter: run, run --config=/etc/myConf.yaml, add --name="Gast" --number="491721234567" --expires=+6h
#TODO: convert into systemd service
#TODO: send MQTT message to broker
#TODO: make ESP raise pin-voltage for 5s
#TODO: add Arduino project as submodule


from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
import yaml
from pathlib import Path


app = Flask(__name__)


def read_yaml(filepath):
    with open(filepath, 'r') as read_file:
        content = yaml.safe_load(read_file)
    return content


def load_allow_list(allow_list_filepath):
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


@app.route('/', methods=['POST'])
def bot():
    allow_list_filepath = app.config['allow_list_filepath']
    allow_list = load_allow_list(allow_list_filepath) # always read allow_list when receiving new message
    sender = request.values.get('WaId', '').lower()
    print(f"type(sender) = {type(sender)}")
    print(f"sender = {sender}")
    access_granted = is_access_granted(sender, allow_list)
    if access_granted:
        response = "you may enter"
    else:
        response = "you shall not pass"
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(f'{response}')
    return str(resp)


def main(allow_list_filepath):
    app.config['allow_list_filepath'] = allow_list_filepath
    app.run()


if __name__ in ['__main__', '__console__']:
    sender = "49172123456"
    allow_list_filepath = Path(__file__).absolute().parent.parent / "resources" / "allow_list.yaml"
    allow_list = load_allow_list(allow_list_filepath)
    access_granted = is_access_granted(sender, allow_list)
    if access_granted:
        response = "you may enter"
    else:
        response = "you shall not pass"
    print(response)
