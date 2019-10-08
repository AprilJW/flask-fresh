from flask_sqlalchemy import SQLAlchemy
from demo.app import create_app

app = create_app()

db = SQLAlchemy(app)
