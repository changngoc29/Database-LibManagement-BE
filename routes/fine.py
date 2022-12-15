from flask import Blueprint, jsonify
from database import dbcursor
from datetime import datetime

fines = Blueprint("fines",__name__,url_prefix="/api/v1/fines")