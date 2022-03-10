"""
Set up your VoIP provider to call a webhook on incoming calls.
The webhook e.g. can be a ngrok address, which in turn passes a POST request to this server.
"""

#TODO: use relais to control door strikes
#TODO: make full program via cookiecutter: run, add --name="Gast" --number="491721234567" --expires=+6h
#TODO: add ESP project as submodule
#TODO: translate responses
#TODO: simplify ngrok handling https://github.com/vincenthsu/systemd-ngrok

from flask import Flask, request
from open_sesame import helpers as osh


app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():
    allow_list = osh.load_allow_list() # always read allow_list when receiving new message
    sender = request.values.get('from', '').lower()
    print(f"type(sender) = {type(sender)}")
    print(f"sender = {sender}")
    access_granted = osh.is_access_granted(sender, allow_list)
    if access_granted:
        osh.open_door()
        response = "you may enter"
    else:
        response = "you shall not pass"
    print(response)
    return ""


def main():
    app.run()
