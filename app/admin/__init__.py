from flask import Blueprint

admin_bp = Blueprint('admin', 
                     import_name = __name__)

from . import (routes)