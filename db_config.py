import os

db_config = {
    "host":"localhost",
    "user":"root",
    "password":os.environ.get("DB_PASSWORD"),
    "database": "assigment"
}