from flask import Flask
from app.routes.series_route import db as db_series

def init_app(app: Flask):

    app.register_blueprint(db_series)