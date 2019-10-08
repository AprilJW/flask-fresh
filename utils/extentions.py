from flask_sqlalchemy import SQLAlchemy
from demo.app import create_app
from flask_session import Session

app = create_app()

db = SQLAlchemy(app)

Session(app)
