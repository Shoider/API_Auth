from flask import Flask
from logger.logger import Logger
from schemas.schema import Schema
from services.service import Service
from models.model import BDModel
from routes.route import FileGeneratorRoute

#from flask_cors import CORS

app = Flask(__name__)
#CORS(app)

logger = Logger()

# Schema
schema = Schema()

# Model
db_conn = BDModel()
db_conn.connect_to_database()

# Service
service = Service(db_conn)

# Routes
routes = FileGeneratorRoute(service, schema)

#Blueprint
app.register_blueprint(routes)

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", debug=False)
        logger.info("Application started")
    finally:
        db_conn.close_connection()
        logger.info("Application closed")
        logger.info("MongoDB connection closed")