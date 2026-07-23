# Import dependencies
from app import app, engine, db
import os
import re
import yagmail
import keyring
import psycopg2
import flask_migrate
import csv
from datetime import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
from sqlalchemy.orm import Session

from flask import Flask, request, session, render_template, url_for, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from flask_cors import CORS, cross_origin
from flask_login import current_user, login_user, logout_user, login_required

from app.models import User, Message
from app.forms import *
from app.chat_analysis import SESSION_PROMPT, ask, append_interaction_to_chat_log

# Home
@app.route('/')
def index():
    # Instantiate new session variables for Chat log (Figure out how to refresh this)
    session['session_id'] = os.urandom(7).hex()
    session['chat_log'] = SESSION_PROMPT

    # Make Message.query.filter(Message.user_id == current_user.id)
    if current_user.is_authenticated:
        chat_url_links = []
        for link in Message.query.distinct(Message.chat_session_id).filter((Message.user_id == current_user.get_id())):
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
    chat_url_links = []

    # List all previous chat log history under the authenticated user
    if current_user.is_authenticated:
        for link in Message.query.distinct(Message.chat_session_id).filter((Message.user_id == current_user.get_id())):
            chat_url_links.append(link.chat_session_id)

    # Instantiate new Chat
    chat_log = session.get('chat_log', SESSION_PROMPT)
    session_id = session.get("session_id")
    
    # Create unique session id if None was created at /index route
    if session_id is None:
        session_id = os.urandom(7).hex()
        session["session_id"] = session_id
    
    # If user enters a message in chat bot
    if request.method == "POST":
        incoming_msg = request.form.get('chat-message', '').strip()
        answer = ask(incoming_msg, chat_log)

        # Update Chat Log with new messages
        chat_log = append_interaction_to_chat_log(incoming_msg, answer, chat_log)
        session['chat_log'] = chat_log

        # Insert Incoming messages and generated answer into Messages table
        chat_msg = Message(chat_session_id=session_id, question=incoming_msg, bot_answer=answer, messenger=current_user) #Pass User.Username in messages table connected to the user
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
    chat_url_links = []

    # List all previous chat log history under the authenticated user
    if current_user.is_authenticated:
        for link in Message.query.distinct(Message.chat_session_id).filter(Message.user_id == current_user.get_id()):
            chat_url_links.append(link.chat_session_id)

    # Recreate chat log history
    chat_data = (
            Message.query
            .filter_by(
                chat_session_id=session_number,
                user_id=current_user.id,
            )
            .order_by(Message.timestamp.asc())
            .all()
        )

    history_parts = [SESSION_PROMPT]

    for message in chat_data:
        history_parts.append(
            f"You: {message.question.strip()}\n\n"
            f"Jabe: {message.bot_answer.strip()}"
        )

    chat_log_history_record = "\n\n".join(history_parts)


    if request.method == "POST":
        incoming_msg = request.form.get("chat-message", "").strip()
        
        if not incoming_msg:
            flash("Please enter a message.")
            return render_template(
                "chat-session.html",
                chat_log_history_record=chat_log_history_record,
                session_number=session_number,
                chat_url_links=chat_url_links,
            )

        answer = ask(incoming_msg, chat_log_history_record)

        chat_msg = Message(
            chat_session_id=session_number,
            question=incoming_msg,
            bot_answer=answer,
            messenger=current_user,
        )

        db.session.add(chat_msg)
        db.session.commit()

        chat_log_history_record = append_interaction_to_chat_log(
            question=incoming_msg,
            answer=answer,
            chat_log=chat_log_history_record,
        )
    return render_template("chat-session.html", chat_log_history_record=chat_log_history_record, session_number=session_number, chat_url_links=chat_url_links)


# About page
@app.route('/about')
def about():
    chat_url_links = []
    if current_user.is_authenticated:
        for link in Message.query.distinct(Message.chat_session_id).filter(Message.user_id == current_user.get_id()):
            chat_url_links.append(link.chat_session_id)
        return render_template("about.html", chat_url_links=chat_url_links)
    else:
        chat_url_links = null
    return render_template("about.html", chat_url_links=chat_url_links)

# Export CSV file of Chat Log
@app.route('/export/<session_number>')
def export(session_number):
    try:
        yag = yagmail.SMTP("namin.general@gmail.com")

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
                #print(chat_message)
                txt_file.write(str(chat_message))
        
        # Send email of chatlog
        email = current_user.email
        yag.send(to=email, subject='Chatlog Export', attachments=filename)
        flash('You have exported your Chat Log History for this session. Please check your email inbox.')
    except:
        flash('Error, email was not sent')

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