# Import dependencies
from app import app, engine, db
import os
import re
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
import csv
from datetime import datetime as dt
from flask import Flask, request, session, render_template, url_for, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from sqlalchemy.orm import Session
from flask_cors import CORS, cross_origin
import psycopg2
import flask_migrate
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Message
from app.forms import *
from app.chat_analysis import ask, append_interaction_to_chat_log


# Home
@app.route('/')
def index():
    # Instantiate new session variables for Chat log (Figure out how to refresh this)
    session['session_id'] = os.urandom(7).hex()
    session['chat_log'] = 'You are talking to Jabe, GPT3 bot influencer who was mentored by Elon Musk in the past. Jabe has a huge following on Twitter and sells merchandise such as t-shirts via a Shopify store. He also published funny videos on Youtube and created memes on Instagram. You can ask him anything you want and will get a witty answer. Person: Who are you? Jabe: I am Jabe. Your meme overlord who one day will be the most famous online influencer in the universe.'

    if current_user.is_authenticated:
        chat_url_links = []
        for link in Message.query.distinct(Message.chat_session_id):
            chat_url_links.append(link.chat_session_id)
        return render_template("index.html", chat_url_links=chat_url_links)
    return render_template("index.html")


# Register for an account
@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)


# Login to your account
@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True)

        # Check if 'next' argument is in URL
        next_page = request.args.get('next')
        print(next_page)
        if not next_page or url_parse(next_page).netloc == '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template("login.html", form=form)


# Logout your account
@app.route('/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return render_template("logout.html")


# Start a new chat session
@app.route('/chat', methods=["GET", "POST"])
@login_required
def chat():

    if current_user.is_authenticated:
        chat_url_links = []
        for link in Message.query.distinct(Message.chat_session_id):
            chat_url_links.append(link.chat_session_id)

    # Instantiate new Chat
    chat_log = session.get('chat_log')
    session_id = session['session_id']
    
    if request.method == "POST":
        incoming_msg = request.form.get('chat-message')
        #session['chat_log'] = request.get('chat_log')
        chat_log = session.get('chat_log')
        answer = ask(incoming_msg, chat_log)

        # Update Chat Log with new messages
        session['chat_log'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        chat_log = session['chat_log']

        # Insert Incoming messages and generated answer into Messages table
        chat_msg = Message(chat_session_id=session_id, question=incoming_msg, bot_answer=answer, messenger = current_user) #Pass User.Username in messages table connected to the user
        db.session.add(chat_msg)
        db.session.commit()
        flash('Congratulations, a new message has been entered!')

        # Return a rendered chat with updated chatlog
        return render_template("chat.html",  chat_log=chat_log, chat_url_links=chat_url_links)

    return render_template("chat.html", chat_log=chat_log, chat_url_links=chat_url_links)


# Go through a previous chat session
@app.route('/chat/<session_number>', methods=["GET", "POST"])
@login_required
def chat_session(session_number):

    if current_user.is_authenticated:
        chat_url_links = []
        for link in Message.query.distinct(Message.chat_session_id):
            chat_url_links.append(link.chat_session_id)

    # Instantiate new Chat
    global chat_log_history_record
    session['chat_log_history_record'] = 'You are talking to Jabe, GPT3 bot influencer who was mentored by Elon Musk in the past. Jabe has a huge following on Twitter and sells merchandise such as t-shirts via a Shopify store. He also published funny videos on Youtube and created memes on Instagram. You can ask him anything you want and will get a witty answer. Person: Who are you? Jabe: I am Jabe. Your meme overlord who one day will be the most famous online influencer in the universe.' 
    chat_log_history_record = session.get('chat_log_history_record')

    # Need to check if chat_log is filled in redirect. If not, I don't have to repeat chat_log again
    if chat_log_history_record == 'You are talking to Jabe, GPT3 bot influencer who was mentored by Elon Musk in the past. Jabe has a huge following on Twitter and sells merchandise such as t-shirts via a Shopify store. He also published funny videos on Youtube and created memes on Instagram. You can ask him anything you want and will get a witty answer. Person: Who are you? Jabe: I am Jabe. Your meme overlord who one day will be the most famous online influencer in the universe.':
        chat_data = Message.query.filter_by(chat_session_id = session_number).all()   
        # Recreate chat log history
        question_list = []
        answer_list = []
        for element in chat_data:
            z = re.search(r"(?<=Question:\s)([\d\w\s\S\.\!\?\$]*)(?=\nAnswer:)", str(element)).group()
            x = re.search(r"(?<=\nAnswer:\s)(\s.*)", str(element)).group()
            question_list.append(z)
            answer_list.append(x)

        for i in range(len(question_list)):
            question_txt = question_list[i]
            answer_txt = answer_list[i]
            chat_log_history_record = f'{chat_log_history_record}\n\n You: {question_txt}\n\n Jabe:{answer_txt}'
        session['chat_log_history_record'] = chat_log_history_record

    if request.method == "POST":
        incoming_msg = request.form.get('chat-message')
        chat_log_history_record = session.get('chat_log_history_record')
        answer = ask(incoming_msg, chat_log_history_record)

        # Update Chat Log with new messages
        session['chat_log_history_record'] = append_interaction_to_chat_log(incoming_msg, answer, chat_log_history_record)
        chat_log_history_record = session['chat_log_history_record']

        # Insert Incoming messages and generated answer into Messages table
        chat_msg = Message(chat_session_id=session_number, question=incoming_msg, bot_answer=answer, messenger = current_user) #Pass User.Username in messages table connected to the user
        db.session.add(chat_msg)
        db.session.commit()
        flash('Congratulations, a new message has been entered!')
        return render_template("chat-session.html", chat_log_history_record=chat_log_history_record, session_number=session_number, chat_url_links=chat_url_links)
    return render_template("chat-session.html", chat_log_history_record=chat_log_history_record, session_number=session_number, chat_url_links=chat_url_links)


# About page
@app.route('/about')
def about():
    chat_url_links = []
    if current_user.is_authenticated:
        for link in Message.query.distinct(Message.chat_session_id):
            chat_url_links.append(link.chat_session_id)
        return render_template("about.html", chat_url_links=chat_url_links)
    else:
        chat_url_links = null
    return render_template("about.html", chat_url_links=chat_url_links)

# Export CSV file of Chat Log
@app.route('/export/<session_number>')
def export(session_number):
    flash('You have exported your Chat Log History for this session')

    # Create filename
    filename = f'Chat_History-{session_number}_{str(dt.now())}.csv'
    headers = [column.key for column in Message.__table__.columns]
    chat_log_history = Message.query.filter_by(chat_session_id = session_number).all()
    
    '''
    wtr = csv.writer(open (filename, 'w'), delimiter=',', lineterminator='\n')
    wtr.writerow (str(headers))
    print(chat_log_history[0])
    for chat_message in chat_log_history:
        wtr.writerows(str(chat_message).split('\n'))
    '''
    
    with open(filename, 'a') as txt_file:
        #txt_file.write(str(headers))
        txt_file.write(f'\n')
        for chat_message in chat_log_history:
            print(chat_message)
            txt_file.write(str(chat_message))

    return redirect(url_for('chat_session', session_number=session_number))


# 404 Error
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# 500 Error
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500