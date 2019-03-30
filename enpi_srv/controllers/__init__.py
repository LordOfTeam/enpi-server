from flask import Blueprint

core_blueprint = Blueprint(
    'core',
    __name__,
    url_prefix="/core",
)
