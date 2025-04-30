from flask import Blueprint, request, jsonify, send_file
from datetime import datetime, timedelta
from logger.logger import Logger
from marshmallow import ValidationError
import hashlib

class FileGeneratorRoute(Blueprint):
    """Class to handle the routes for file generation"""

    def __init__(self, service, schema):
        super().__init__("Auth_Api", __name__)
        self.logger = Logger()
        self.schema = schema
        self.service = service
        self.register_routes()

    def register_routes(self): 
        """Function to register the routes for file generation"""
        self.route("/api3/healthcheck", methods=["GET"])(self.healthcheck)
        self.route("/api3/generate", methods=["POST"])(self.generate_user)

    def generate_user(self):
        """Function to register users"""
        try:
            # Get the data from the request
            data = request.get_json()

            if not data:
                return jsonify({"error": "Invalid data"}), 400

            # Validacion
            validated_data = self.schema.load(data)

            password = validated_data.get("passwordInput")

            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            # Cuenta creada
            cuentaNueva = {
                "usuario": validated_data.get("emailInput"),
                "contrasena": hashed_password,
                "privilegios": "administrador",
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fecha_expiracion": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S"),
                "estado": "activo"
            }

            # Guardar en BD
            status_code = self.service.add_account(cuentaNueva)
            self.logger.info(f"Status code: {status_code}")
            if status_code == 201:
                return jsonify({"message": "Cuenta agregada exitosamente"}), 201

        except ValidationError as err:
            self.logger.error(f"Validation error: {err.messages}")
            return jsonify({"error": "Invalid input"}), 400
        
        except Exception as e:
            self.logger.error(f"Error agregando cuenta: {e}")
            return jsonify({"error": "Error agregando cuenta"}), 500


    def healthcheck(self):
        """Function to check the health of the services API inside the docker container"""
        return jsonify({"status": "Up"}), 200

