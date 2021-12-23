from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, date, timezone, timedelta
import sys
import os
from os import abort
from flask import current_app as app
# from app import app, bcrypt #  import current_app
import pytz



@app.route('/')
def index():
    return render_template('index.html')




