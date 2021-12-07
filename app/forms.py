from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Customer, BusinessOwner, Category


class AddBusinessForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = SelectField('Category', validators=[DataRequired()], coerce=int)
    new_category = StringField("Don't see your category? Add another:")
    description = TextAreaField('Description', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    top_items = TextAreaField('Top Items', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def edit_category(request, id):
        category = Category.query.get(id)
        form = AddBusinessForm(request.POST, obj=category)
        form.category.choices = [(c.id, c.name) for c in Category.query.order_by('name')]


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class CustomerRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = Customer.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class OwnerRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = BusinessOwner.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
