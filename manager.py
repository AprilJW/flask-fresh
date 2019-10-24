from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app import create_app
from utils import extentions, script

app = create_app()
manager = Manager(app)

Migrate(app, extentions.db)
manager.add_command('admin', script.manager)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
