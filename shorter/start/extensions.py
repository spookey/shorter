from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

CSRF_PROTECT = CSRFProtect()
DB = SQLAlchemy()
