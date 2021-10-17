# AUTOMATING MY TASKS USING GITHUB & TWILIO

This is a simple app to automatically organize tasks on a Kanban board. You can use it when sharing a collaborative board with other people or to keep track of your own personal tasks.
You can add simple cards to the 'to do' column wherever you are thanks to Twilio Programmable SMS.  
You will also receive a weekly summary on your phone with the tasks you have completed and these will be archived to clear the board.

This has been made using:

- Github Boards
- Twilio Programmable SMS
- Python & Flask

## GITHUB BOARDS

For my Kanban board I'm using a private project board: [GitHub Project Boards](https://docs.github.com/en/free-pro-team@latest/github/managing-your-work-on-github/about-project-boards) configured as "basic kanban".  
You can configure the columns you need, bearing in mind that the application will take the first one to add cards received by SMS, and the last one will be from which it sends the weekly digest notification.

### Configure Github Project

Within your github account, you just have to go to the projects tab and click on the "create project" button, then you can choose:

- A name for your project board that you will later include in a variable called "GITHUB_PROJECT_NAME" within the "env" file.
- Your preferred template: In my case it will be a "basic kanban"
- The visibility for your project: as my board will be for personal tasks and not for sharing with a team, I will choose the "private" option.

## TWILIO PROGRAMMABLE SMS

To be able to add cards from anywhere by sending an SMS and to receive weekly notifications, we will be using Twilio.  
You can sign up for a free trial account and request a Twilio number. Twilio gives you some credit to start with: [Twilio Trial Account](https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account)  
For more information about how Twilio works, you can check its [documentation](https://www.twilio.com/docs/sms) and try the [Python helper library](https://www.twilio.com/docs/libraries/python).

## PYTHON & FLASK

The app is developed using Python and Flask, it will make requests to the Github API to manage cards, and Twilio library will be used to send and receive SMS's.  
Once you have cloned this repository, there are some things that you will need to configure to get the application up and running: 

### App configuration

First you will need to create a configuration file for the application with the same content of the env.example file included in the repository.

```text
cp .env.example .env
```

You will need to fill in the specified variables with your own data:

```text
ACCOUNT_SID
AUTH_TOKEN
TWILIO_PHONE
PHONE
GITHUB_TOKEN
GITHUB_USERNAME
GITHUB_PROJECT_NAME
```

The rest of the variables, although they must be included in the env file, you can leave them blank because they will be configured when the application starts.
Once you have configured these variables, you can start the app:

```text
python3 -m pip install -r requirements.txt
python3 app.py
```

As I don't have the application deployed in a public url that Twilio has access to. I'll also be using [Ngrok](https://ngrok.com) to expose a public url where Twilio can send a webhook.  
Ngrok exposes local servers behind NATs and firewalls to the public internet over secure tunnels.  
If you have the app deployed in your local, you can use ngrok tool as follows:

```text
./ngrok http 5000
```

Finally, you will need to add ngrok generated url to [Twilio console](https://www.twilio.com/console/phone-numbers/) inside messaging section and displaying the webhook option.

### Usage

Now you can send a SMS to the Twilio number as follows:

```text
Usage:
    Send your message starting with the keyword for your desired action:
    ADD <Text for the task> //for adding a new card to the Github board
    GET <Exact column name> //for get cards in a column
```

Twilio number will automatically respond to incoming SMS sending a confirmation message for a new card added or with the list of cards for the selected column.

### Cron Job

Add a cron job to receive an SMS with the weekly digest of completed cards (in done column) and to move them to archived:
#### Configure cron job in linux

To edit a cron job:

```text
crontab -e
````

Configure cron to send notifications once a week, e.g., on Fridays at 15:00:

```text
0 15 * * 5 cd /path/to/app && /usr/bin/python3 -c "import app; app.send_weekly_digest()"
```
