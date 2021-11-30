from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.models import Business, Category, Customer, BusinessOwner
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title= "Home")


@app.route('/shops')
def shops():
    shops = Business.query.all()
    return render_template('shops.html', shops=shops)


@app.route('/categories')
def categories():
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)


# @app.route('/add_business')
# @login_required
# def add_business():


@app.route('/shops/<name>')
def business(name):
    business = Business.query.filter_by(name=name).first()
    category_list = []
    for cat in business.b2c:
        category_list.append(cat.category.name)

#
# @app.route('/reviews')
# def reviews():

# @app.route('/add_review')
# @login_required
# def add_review():


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/populate_db')
def populate_db():
    b1 = Business(name="Ithaca Outdoor Store", description="We sell a variety of outdoor equipment and apparel", location="Commons")
    b2 = Business(name="Autumn Leaves", description= "Used bookstore", location="Commons")
    b3 = Business(name="Alphabet Soup", description= "Children's toy shop", location= "Commons")

    db.session.add_all([b1, b2, b3])
    db.session.commit()

    c1 = Customer(username="dberman")
    c2 = Customer(username="jsmith")
    c3 = Customer(username="segner")

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    ca1 = Category(name="Books")
    ca2 = Category(name="Restaurant")
    ca3 = Category(name="Crafts")

    db.session.add_all([ca1, ca2, ca3])
    db.session.commit()

    flash("database has been populated")
    return render_template('base.html', title='Home')

@app.route('/reset_db')
def reset_db():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()
    return render_template('base.html', title='Home')



# @app.route('/profile')
# @login_required
# def profile():
