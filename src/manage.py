import os

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

from app import create_app, db, models
from config import BASE_DIR


app = create_app(os.getenv('APP_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('shell',
                    Shell(make_context=lambda: dict(app=app, db=db),
                          use_ipython=True,
                          use_ptpython=True))

manager.add_command('db', MigrateCommand)


@manager.command
def db_create():
    db.create_all()


@manager.option('-t', '--test-path', default=os.path.join(BASE_DIR, 'tests'))
def test(tests_path):
    try:
        import pytest
        args = ['-x', tests_path, 'rsx']
        pytest.main(args)
    except ImportError:
        print('You need install py.test package to run test commnad')


if __name__ == '__main__':
    manager.run()
