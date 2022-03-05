"""
For now, this only works with WhatsApp.
You send a WhatsApp message to your twilio account and in response a MQTT message is sent to your smart door.
"""

# ref.: https://www.twilio.com/blog/build-a-whatsapp-chatbot-with-python-flask-and-twilio

#TODO: whatsappweb + selenium
#           selenium: save cookies
#TODO: use relais to control door strikes
#TODO: make full program via cookiecutter: run, add --name="Gast" --number="491721234567" --expires=+6h
#TODO: add ESP project as submodule
#TODO: translate responses
#TODO: simplify ngrok handling https://github.com/vincenthsu/systemd-ngrok


from open_sesame import helpers as osh


app = Flask(__name__)


@app.route('/', methods=['POST'])
def bot():
    allow_list = osh.load_allow_list() # always read allow_list when receiving new message
    sender = request.values.get('WaId', '').lower()
    print(f"type(sender) = {type(sender)}")
    print(f"sender = {sender}")
    access_granted = osh.is_access_granted(sender, allow_list)
    if access_granted:
        osh.send_open()
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
