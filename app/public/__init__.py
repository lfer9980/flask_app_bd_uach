from flask import Blueprint

public_bp = Blueprint(name = 'public',
                     import_name = __name__,
                     )

from . import routes