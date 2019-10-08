from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from demo.app import create_app
from script import utils, db
from utils.core import import_modules

app = create_app()
manager = Manager(app)

Migrate(app, db.db)
manager.add_command('admin', utils.manager)
manager.add_command('db', MigrateCommand)

import_modules()

if __name__ == '__main__':
    manager.run()
