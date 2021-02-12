import env
import requests

API_ENDPOINT = "https://api.github.com"
USER_PROJECTS = API_ENDPOINT + "/users/{}/projects"
PROJECT_COLUMNS = API_ENDPOINT + "/projects/{}/columns"
COLUMN_CARDS = API_ENDPOINT + "/projects/columns/{}/cards"
COLUMN_CARD = API_ENDPOINT + "/projects/columns/cards/{}"

headers = {
  "Accept": "application/vnd.github.inertia-preview+json",
  "Authorization": "token {}".format(env.GITHUB_TOKEN)
}

def error_log(message):
  print("ERROR: " + message)

def cards_to_string(data):
  cards_string = ""
  try:
    for item in data:
      string = "- " + item["note"] + '\n'
      cards_string += string
    return cards_string
  except TypeError as e:
    error_log("card_to_string - {}".format(e))
    raise Exception("Error")

def get_data(url): #SENDS GET REQUESTS TO URL
  try:
    response = requests.request("GET",url,headers=headers)
    if response.status_code == 200:
      responseJson = response.json()
      return responseJson
    else:
      error_log("get_data - {}".format(response))
      raise Exception("Error")
  except requests.exceptions.RequestException as e: 
    error_log("get_data - {}".format(e))
    raise Exception("Error")

def config(): #CALLED BEFORE APP RUNS TO SET PROJECT AND COLUMNS VARIABLES
  if not env.GITHUB_PROJECT:
    url = USER_PROJECTS.format(env.GITHUB_USERNAME)
    data = get_data(url)
    for item in data:
      if item["name"] == env.GITHUB_PROJECT_NAME:
        env.GITHUB_PROJECT = item["id"]
  if not env.COLUMNS:
    url = PROJECT_COLUMNS.format(env.GITHUB_PROJECT)
    data = get_data(url)
    for item in data:
      env.COLUMNS[item["name"].lower()] = item["id"]
    env.BACKLOG_COLUMN = data[0]["id"]
    env.DONE_COLUMN = data[-1]["id"]

def get_cards(column): #GET CARDS IN SELECTED COLUMN
  url = COLUMN_CARDS.format(env.COLUMNS.get(column))
  data = get_data(url)
  cards_string = cards_to_string(data)
  return cards_string

def add_card(body): #ADD CARD TO FIRST COLUMN
  url = COLUMN_CARDS.format(env.BACKLOG_COLUMN)
  body_json = {
    "note": body
  }
  try:
    response = requests.request("POST", url, headers = headers, json = body_json)
    if response.status_code == 201:
      return "New card added!"
    else:
      error_log("add_card - {}".format(response))
      raise Exception("Error")
  except requests.exceptions.RequestException as e: 
    error_log("add_card - {}".format(e))
    raise Exception("Error")

def archive_done(): #ARCHIVE CARDS IN DONE COLUMN
    url = COLUMN_CARDS.format(env.DONE_COLUMN)
    data = get_data(url)
    body_json={
      "archived": True
    }
    for item in data:
      card = item["id"]
      url_card = COLUMN_CARD.format(card)
      try:
        requests.patch(url_card, headers=headers, json=body_json)
      except requests.exceptions.RequestException as e: 
        error_log("archive_done - {}".format(e))
        raise Exception("Error")