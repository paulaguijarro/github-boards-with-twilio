import env
import twilio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_message(text):
  try:
    client = Client(env.account_sid, env.auth_token)
    message = client.messages.create(
      body= text,
      from_= env.twilio_phone,
      to= env.phone
    )
  except TwilioRestException as e:
    print(e)
  return message.sid