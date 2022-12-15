from flask import Blueprint, jsonify
from database import dbcursor
from datetime import datetime

payments = Blueprint("payments",__name__,url_prefix="/api/v1/payments")