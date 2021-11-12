from flask import render_template, flash, redirect, url_for, request
from app import app
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/shops')
def shops():


@app.route('/categories')
def categories():


@app.route('/add_business')
@login_required
def add_business():


@app.route('/business')
def business():


@app.route('/reviews')
def reviews():


@app.route('/add_review')
@login_required
def add_review():


@app.route('/login', methods=['GET', 'POST'])
def login():


@app.route('/logout')
def logout():


@app.route('/register', methods=['GET', 'POST'])
def register():


@app.route('/profile')
@login_required
def profile():


@app.route('populate_db')
def populate_db():
