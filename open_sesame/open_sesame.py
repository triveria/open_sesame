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
#TODO: load allow_list / deny-list
#TODO: send MQTT message to broker
#TODO: make ESP raise pin-voltage for 5s
#TODO: add Arduino project as submodule


from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)


allow_list = ["49172123456789"]


@app.route('/', methods=['POST'])
def bot():
    sender = request.values.get('WaId', '').lower()
    print(f"type(sender) = {type(sender)}")
    print(f"sender = {sender}")
    if sender in allow_list:
        prefix = "you may enter"
    else:
        prefix = "you shall not pass"
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(f"{prefix} \n {quote}")
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body(f'{prefix} \n I only know about famous quotes and cats, sorry!')
    return str(resp)


if __name__ in ['__main__', '__console__']:
    app.run()
