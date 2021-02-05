from flask import Flask, request
import env, request_github, send_message
from twilio.twiml.messaging_response import Message, MessagingResponse

request_github.config() # Configure github project and column names variables 
app = Flask(__name__)

@app.route('/message', methods=['POST'])
def message_received():
  body = request.form['Body']
  response = user_action(body)
  resp = MessagingResponse()
  resp.message(response)
  return str(resp)

def user_action(body):
  usage = '''
    Usage:
    Send your message starting with the keyword for your desired action:
    ADD <TEXT> for adding a new card to the Github board
    GET <COLUMN_NAME> for get cards in a column
    '''
  try:
    action = body[:4].lower()
    if action == "get ":
      column = body[4:].strip().lower()
      response = request_github.get_cards(column)
    elif action == "add ":
      response = request_github.add_card(body[4:])
    else:
      response = usage
    if response:
      return response
    else:
      return "There are no cards in the requested column"
  except:
    return usage
  
# Sends a weekly notification to the user (configured by a cron job) with the tasks completed (last column of the board)
def send_weekly_digest():
  done_name = (list(env.columns.keys())[list(env.columns.values()).index(env.done_column)])
  text = request_github.get_cards(done_name)
  if text:
    weekly_digest = "Your completed tasks for this week:\n\n" + text
  else:
    weekly_digest = "No cards were completed this week!"
  send_message.send_message(weekly_digest)
  # Once sent the weekly digest, done tasks are archived:
  request_github.archive_done()

if __name__ == '__main__':
  app.run(debug=True)