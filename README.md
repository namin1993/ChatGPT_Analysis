## ChatGPT App

### Table of Contents
* Description
* Installation
* Instructions for use
* Featured packages
* General Sources
* Webpage design source
* Database design source
* Additional features to include
* Notes
* Website

### Description:
Create a Web App that creates and validates user accounts, uses ChatGPT API to talk to a chat bot, and allows the user to export any chatlog message from their account.


### Installation:
Enter commands in terminal to create Pipenv virtual environment:<br />
```
python3 -m pipenv install
python3 -m pipenv shell
export FLASK_APP='chat_analysis.py'
flask run
```
To exit Pipenv virtual environment:<br />
```
exit
```

### Instructions for use:
    1.) Click "Register New Account" in order to create a new user account.
    2.) Enter unique Username, Password, and email address.
    3.) Go to "Login" and enter Username and Password.
    4.) Select "New Chat" on the side navigation bar for a new chat session. Or click on the dropdown menu "Chat Log History" and select a previous chat session to continue.
    5.) Select "Export" if you want to download the current chat log history of the current chat session selected.


### Featured Packages:
openai

## Requirements

- Python 3.9+
- PostgreSQL
- Pipenv
- An OpenAI API account with active API billing

## Environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env

### Sources:
Call Python Functions to javascript code: https://stackoverflow.com/questions/13175510/call-python-function-from-javascript-code

Regex Expressions: https://regexr.com/

Use Chatbot: https://jman4190.medium.com/how-to-build-a-gpt-3-chatbot-with-python-7b83e55805e6

Environment Variable Configuration: https://www.doppler.com/blog/environment-variables-in-python

Exporting Table Column Names: https://stackoverflow.com/questions/24959589/get-table-columns-from-sqlalchemy-table-model

Setting up email with YAGmail: https://yagmail.readthedocs.io/en/latest/usage.html

### Webpage Design:
Template Source: https://dev.to/codeply/bootstrap-5-sidebar-examples-38pb

Flask tutorial: https://blog.miguelgrinberg.com/

### Database Design:
Database Join: https://hackersandslackers.com/sqlalchemy-data-models/

SA_Instance Error: https://stackoverflow.com/questions/16151729/attributeerror-int-object-has-no-attribute-sa-instance-state

### Additional features to include:
* Delete option for chat session
* Delete option individual chat message
* Visual on how "positive" or "negative" an entire chat session is compared to other chat sessions (machine learning algorithm to apply here?)

### Notes:
    - replaced deprecated `davinci`;
    - migrated to the modern OpenAI Responses API;
    - updated OpenAI SDK;
    - added Python 3.9-compatible type annotations;
    - improved chat formatting;
    - improved responsive/mobile presentation;
    - updated database migrations and dependency files.

### Website:

View application here: https://flask-chatgpt-v01.herokuapp.com/
