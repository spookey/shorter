from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from shorter.environment import MIGR_DIR

# from flask_migrate import Migrate

CSRF_PROTECT = CSRFProtect()
DB = SQLAlchemy()
MIGRATE = Migrate(directory=MIGR_DIR)
