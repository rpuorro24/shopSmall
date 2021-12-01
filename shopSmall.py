from app import app, db
from app.models import Business, BusinessOwner, Category, Customer


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Business': Business, 'BusinessOwner': BusinessOwner, 'Category': Category, 'Customer': Customer}