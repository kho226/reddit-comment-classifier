import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_migrate import Migrate
from flask.ext.redis import FlaskRedis
from config import Config 


db = SQLAlchemy()
migrate = Migrate()
redis = FlaskRedis()

def create_app(config_class=Config): #will not run

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    redis.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    
    return app


from app import models