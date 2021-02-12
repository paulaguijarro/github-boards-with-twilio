import env
import twilio
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def send_message(text):
  try:
    client = Client(env.ACCOUNT_SID, env.AUTH_TOKEN)
    message = client.messages.create(
      body= text,
      from_= env.TWILIO_PHONE,
      to= env.PHONE
    )
  except TwilioRestException as e:
    print(e)
  return message.sid