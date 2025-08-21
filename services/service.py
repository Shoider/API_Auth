from flask import jsonify
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
        
    def get_account(self, account):
        """Function to get a account register from the database"""
        try:
            accountFound = self.db_conn.db.auth.find_one({"usuario": account.get("usuario")})
            self.logger.info(f"Account find: {account}")
            self.logger.info(f"Account found: {accountFound}")

            # Cuenta No existe
            if not accountFound:
                self.logger.error("Account not found")
                return 203
            
            # Check the password
            if account.get("password") == accountFound.get("password"):
                tipoUsuario = accountFound.get("privilegios")
                self.logger.info(tipoUsuario)
                #return {"status": 201, "tipoUsuario": tipoUsuario}   
                return 201          
            else:
                self.logger.error("Invalid password")
                return 202           
            
            
        except Exception as e:
            self.logger.error(f"Error getting Account from database: {e}")
            return jsonify({"error": "Error de cuenta"}), 500
    