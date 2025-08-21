from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from logger.logger import Logger
from marshmallow import ValidationError
import hashlib
import jwt  # Importa PyJWT
import os

secret_key = os.getenv("SECRET_KEY", "mi_clave_secreta")

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
        self.route("/api3/auth", methods=["POST"])(self.auth)
        self.route("/api3/validar_token", methods=["POST"])(self.validar_token)
        self.route("/api3/protected", methods=["POST"])(self.protected_route)
        self.route("/api3/generate", methods=["POST"])(self.generate_user)

    def validar_token(self):
        """Endpoint para validar el token"""
        try:
            # Obtener el token del cuerpo de la solicitud
            data = request.get_json()
            if not data or "token" not in data:
                return jsonify({"error": "Token no proporcionado"}), 400

            token = data["token"]

            # Decodificar y validar el token
            try:
                decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
                return jsonify({"message": "Token válido", "usuario": decoded_token["usuario"]}), 210
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expirado"}), 211
            except jwt.InvalidTokenError:
                return jsonify({"error": "Token inválido"}), 212

        except Exception as e:
            self.logger.error(f"Error validando el token: {e}")
            return jsonify({"error": "Error interno del servidor"}), 401

    def protected_route(self):
        """Function to handle a protected route"""
        data = request.get_json()
        token = data.get("token")

        self.logger.debug("Token recibido: ", token)

        if not token:
            self.logger.debug("Token no proporcionado, 201")
            return jsonify({"error": "Token no proporcionado"}), 201

        # Validar el token
        validacion = self.validar_token(token)
        self.logger.debug("Token que se mando a validar: ", token, "Con resultado: ", validacion)
        if "error" in validacion:
            self.logger.debug("Error de validacion 401: ", validacion)
            return jsonify(validacion), 401
        
        self.logger.debug("message: Acceso permitido usuario: ", validacion["usuario"], " Codigo: 200")

        return jsonify({"message": "Acceso permitido", "usuario": validacion["usuario", "token": token]}), 200

    def generate_user(self):
        """Function to register users"""
        try:
            # Get the data from the request
            data = request.get_json()

            if not data:
                return jsonify({"error": "Invalid data"}), 400

            # Validacion
            validated_data = self.schema.load(data)

            hashed_password = hashlib.sha256(validated_data.get("passwordInput").encode('utf-8')).hexdigest()

            # Cuenta creada
            cuentaNueva = {
                "usuario": validated_data.get("emailInput"),
                "password": hashed_password,
                #Crear los privilegios según el usuario
                "privilegios": validated_data.get("privilegesInput"),
                "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                #Cambiar la fecha de expiración, dependiendo lo que se necesita
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
        
    def auth(self):
        """Function to authenticate users"""
        try:
            self.logger.info("Iniciando autenticación...")

            # Obtener los datos de la solicitud
            data = request.get_json()
            self.logger.info(f"Datos recibidos: {data}")
            

            if not data:
                self.logger.error("No se recibieron datos en la solicitud.")
                return jsonify({"error": "Invalid data"}), 400

            # Validación
            validated_data = self.schema.load(data)
            self.logger.info(f"Datos validados: {validated_data}")

            hashed_password = hashlib.sha256(validated_data.get("passwordInput").encode('utf-8')).hexdigest()
            self.logger.info(f"Contraseña encriptada: {hashed_password}")

            # Cuenta ingresada
            cuenta = {
                "usuario": validated_data.get("emailInput"),
                "password": hashed_password,
            }
            self.logger.info(f"Cuenta ingresada: {cuenta}")

            # Revisión de cuenta
            status_code = self.service.get_account(cuenta)
            self.logger.info(f"Status code: {status_code}")
            
            if status_code == 201:
            #if status_code["status"] == 201:
                self.logger.info("Cuenta correcta. Generando token JWT...")

                # Generar un token JWT válido por 10 minutos
                payload = {
                    "usuario": cuenta["usuario"],
                    "exp": datetime.utcnow() + timedelta(minutes=10),  # Fecha de expiración
                    "iat": datetime.utcnow(),  # Fecha de emisión
                }
                token = jwt.encode(payload, secret_key, algorithm="HS256")
                self.logger.info(f"Token generado: {token}")

                #privilegios = status_code["tipoUsuario"]
                return jsonify({
                    "message": "Cuenta correcta",
                    "token": token,
                    #"tipoUsuario":status_code["tipoUsuario"]
                }), 201

            elif status_code == 202:
                self.logger.info("Contraseña incorrecta.")
                return jsonify({"message": "Contraseña incorrecta"}), 202
            elif status_code == 203:
                self.logger.info("Cuenta no encontrada.")
                return jsonify({"message": "Cuenta no encontrada"}), 203

        except ValidationError as err:
            self.logger.error(f"Validation error: {err.messages}")
            return jsonify({"error": "Invalid input"}), 400

        except Exception as e:
            self.logger.error(f"Error de cuenta: {e}")
            return jsonify({"error": "Error de cuenta"}), 500  
    
    def healthcheck(self):
        """Function to check the health of the services API inside the docker container"""
        return jsonify({"status": "Up"}), 200

