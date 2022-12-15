from flask import Blueprint, jsonify
from database import dbcursor
from datetime import datetime

notis = Blueprint("notis",__name__,url_prefix="/api/v1/notis")