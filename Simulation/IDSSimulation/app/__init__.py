from flask import Flask
from flask_redis import FlaskRedis


app = Flask(__name__)
app.config['REDIS_URL'] = "redis://:password@localhost:6379/0"
redis_client = FlaskRedis(app)
from app import routes
