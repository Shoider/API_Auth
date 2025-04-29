from flask import Blueprint, request, jsonify, send_file
from datetime import datetime, timedelta
from io import BytesIO
from logger.logger import Logger
from marshmallow import ValidationError

class FileGeneratorRoute(Blueprint):
    """Class to handle the routes for file generation"""

    def __init__(self, service, schema):
        super().__init__("file_generator", __name__)
        self.logger = Logger()
        self.schema = schema
        self.service = service
        self.register_routes()

    def register_routes(self): 
        """Function to register the routes for file generation"""
        self.route("/api3/healthcheck", methods=["GET"])(self.healthcheck)


    def healthcheck(self):
        """Function to check the health of the services API inside the docker container"""
        return jsonify({"status": "Up"}), 200

