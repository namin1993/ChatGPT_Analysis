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
conda deactivate (*if you also have Conda active)
SET FLASK_APP='chat_analysis.py'
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

### Sources:
Call Python Functions to javascript code: https://stackoverflow.com/questions/13175510/call-python-function-from-javascript-code

Regex Expressions: https://regexr.com/

Use Chatbot: https://jman4190.medium.com/how-to-build-a-gpt-3-chatbot-with-python-7b83e55805e6

Environment Variable Configuration: https://www.doppler.com/blog/environment-variables-in-python

Exporting Table Column Names: https://stackoverflow.com/questions/24959589/get-table-columns-from-sqlalchemy-table-model

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
* Fix lines 67-71 in routes.py login() route. Variable next_page is null for some reason.
* Fix how new lines/line breaks are represented for incoming messages and chat bot answers. So far, there are no line breaks for quesitions and answers.

### Website:


