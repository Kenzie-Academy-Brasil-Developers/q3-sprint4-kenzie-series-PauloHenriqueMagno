from flask import Blueprint
from app.controllers import series_controller

db = Blueprint("series", __name__, url_prefix="/series")

db.get("")(series_controller.series)
db.get("<id>")(series_controller.select_by_id)
db.post("")(series_controller.create)