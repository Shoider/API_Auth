from datetime import datetime, timedelta
from flask import jsonify
from pymongo import ReturnDocument
from logger.logger import Logger

class Service:
    """Service class to that implements the logic of the CRUD operations for tickets"""

    def __init__(self, db_conn):
        self.logger = Logger()
        self.db_conn = db_conn
    
    def add_account(self, new_account):
        """Function to add a account register to the database"""
        try:
            self.db_conn.db.auth.insert_one(new_account)
            return 201
        except Exception as e:
            self.logger.error(f"Error adding new Account to database: {e}")
            return jsonify({"error": f"Error adding new Account to database: {e}"}), 500
    