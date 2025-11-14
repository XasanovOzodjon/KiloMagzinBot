from . import errors
from .users import start, help, echo, debug
from .groups import joined, lefted
from . import groups
from . import channels

def register_handlers(dp):
    start.register_handlers(dp)
    help.register_handlers(dp)
    debug.register_handlers(dp)
    # echo.register_handlers(dp)
    joined.register_handlers(dp)
    # Error handler ni ham qo'shamiz
    dp.add_error_handler(errors.error_handler.error_handler)
    lefted.register_handlers(dp)