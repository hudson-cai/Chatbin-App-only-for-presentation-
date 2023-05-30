from app import app, db
from app.models import User, Message

# This decorator registers the function as a shell context function
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Message': Message}