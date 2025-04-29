from datetime import datetime, timedelta
from flask import jsonify
from pymongo import ReturnDocument
from logger.logger import Logger
from bson import ObjectId

class Service:
    """Service class to that implements the logic of the CRUD operations for tickets"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn
    
    