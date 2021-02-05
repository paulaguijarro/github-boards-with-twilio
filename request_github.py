import env
import requests

API_ENDPOINT = "https://api.github.com"
USER_PROJECTS = API_ENDPOINT + "/users/{}/projects"
PROJECT_COLUMNS = API_ENDPOINT + "/projects/{}/columns"
COLUMN_CARDS = API_ENDPOINT + "/projects/columns/{}/cards"
COLUMN_CARD = API_ENDPOINT + "/projects/columns/cards/{}"

headers = {
  "Accept": "application/vnd.github.inertia-preview+json",
  "Authorization": "token {}".format(env.github_token)
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
  if not env.github_project:
    url = USER_PROJECTS.format(env.github_username)
    data = get_data(url)
    for item in data:
      if item["name"] == env.github_project_name:
        env.github_project = item["id"]
  if not env.columns:
    url = PROJECT_COLUMNS.format(env.github_project)
    data = get_data(url)
    for item in data:
      env.columns[item["name"].lower()] = item["id"]
    env.backlog_column = data[0]["id"]
    env.done_column = data[-1]["id"]

def get_cards(column): #GET CARDS IN SELECTED COLUMN
  url = COLUMN_CARDS.format(env.columns.get(column))
  data = get_data(url)
  cards_string = cards_to_string(data)
  return cards_string

def add_card(body): #ADD CARD TO FIRST COLUMN
  url = COLUMN_CARDS.format(env.backlog_column)
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
    url = COLUMN_CARDS.format(env.done_column)
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

