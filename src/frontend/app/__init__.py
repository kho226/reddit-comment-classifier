import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from elasticsearch import Elasticsearch
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from config import Config 


db = SQLAlchemy()
migrate = Migrate()
redis_store = FlaskRedis()

def create_app(config_class=Config): #will not run

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    redis_store.init_app(app)

    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    app.redis_store = redis_store
    
    
    return app


from app import models