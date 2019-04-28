from flask.helpers import get_debug_flag

from shorter.app import create_app
from shorter.start.config import DevelopmentConfig, ProductionConfig

APP = create_app(
    DevelopmentConfig if get_debug_flag() else ProductionConfig
)
