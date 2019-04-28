from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from shorter.start.environment import MIGR_DIR

CSRF_PROTECT = CSRFProtect()
DB = SQLAlchemy()
MIGRATE = Migrate(directory=MIGR_DIR)
