from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import AddBusinessForm, LoginForm, CustomerRegistrationForm, OwnerRegistrationForm
from app.models import Business, Category, Customer, BusinessOwner, BusinesstoCategory
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title= "Home")


@app.route('/shops')
def shops():
    shops = Business.query.all()
    shop = {'name': shops}
    my_shops = []
    for shop in shops:
        my_shops.append(shop)

    return render_template('shops.html', shops=shops, shop = shop, my_shops = my_shops)


@app.route('/categories')
def categories():
    categories = Category.query.all()
    category= {'name': categories}
    my_categories = []
    for category in categories:
        my_categories.append(category)
    return render_template('categories.html', categories=categories, category= category, my_categories= my_categories)

@app.route('/categories/<name>')
def category(name):
    cat = Category.query.filter_by(name=name).first()
    b2c = BusinesstoCategory.query.all()
    businessID= {'businessID': b2c}
    businesses= []
    for businessID in b2c:
        if businessID.categoryID == cat.id:
            businesses.append(businessID)
    shops= Business.query.all()
    #shop= {'name': shops}
    my_shops= []
    for shop in shops:
        for business in businesses:
            if shop.id == business.id:
                my_shops.append(shop)
    return render_template('category.html', my_shops=my_shops, category=cat)



@app.route('/add_business')
@login_required
def add_business():
    form = AddBusinessForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]
    if form.validate_on_submit():
        flash('{} added to list of businesses'.format(form.name.data))
        new_business = Business(name=form.name.data, category=form.category.data, description=form.description.data, location=form.location.data, top_items=form.top_items.data)
        db.session.add(new_business)
        db.session.commit()
        for category in form.category.data:
            b2c = BusinesstoCategory(businessID=new_business.id, categoryID=category)
            db.session.add(b2c)
        db.session.commit()
        return render_template('business.html', title='Business')
    return render_template('add_business.html', title='Add Business', form=form)


@app.route('/shops/<name>')
def business(name):
    business = Business.query.filter_by(name=name).first()
    category_list = []
#    for cat in business.b2c:
 #       category_list.append(cat.category.name)
    return render_template('business.html', business=business)

#
# @app.route('/reviews')
# def reviews():

# @app.route('/add_review')
# @login_required
# def add_review():


@app.route('/customer_login', methods=['GET', 'POST'])
def customer_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Customer.query.filter_by(username=form.username.data).first()
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


@app.route('/owner_login', methods=['GET', 'POST'])
def owner_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = BusinessOwner.query.filter_by(username=form.username.data).first()
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


@app.route('/customer_register', methods=['GET', 'POST'])
def customer_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        user = Customer(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)


@app.route('/owner_register', methods=['GET', 'POST'])
def owner_register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = OwnerRegistrationForm()
    if form.validate_on_submit():
        user = BusinessOwner(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/populate_db')
def populate_db():

    ca1 = Category(name="Sporting Goods")
    ca2 = Category(name="Books")
    ca3 = Category(name="Toys")

    db.session.add_all([ca1, ca2, ca3])
    db.session.commit()

    b1 = Business(name="Ithaca Outdoor Store", description="We sell a variety of outdoor equipment and apparel", location="Commons")
    b2 = Business(name="Autumn Leaves",  description= "Used bookstore", location="Commons")
    b3 = Business(name="Alphabet Soup",  description= "Children's toy shop", location= "Commons")

    db.session.add_all([b1, b2, b3])
    db.session.commit()


    c1 = Customer(username="dberman")
    c2 = Customer(username="jsmith")
    c3 = Customer(username="segner")

    db.session.add_all([c1, c2, c3])
    db.session.commit()

    b2c1= BusinesstoCategory(businessID= b2.id, categoryID= ca1.id)
    b2c2= BusinesstoCategory(businessID= b1.id, categoryID= ca2.id)
    b2c3= BusinesstoCategory(businessID= b3.id, categoryID= ca3.id)

    db.session.add_all([b2c1, b2c2, b2c3])
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
