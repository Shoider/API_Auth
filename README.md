# API_Auth
Autentificador

Ejemplos

Cuenta Nueva:

curl -X POST http://localhost:8001/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "brandon@gmail.com", "passwordInput": "1234"}'

Inicion de Sesion:

curl -X POST http://localhost:8001/api3/auth \
-H "Content-Type: application/json" \
-d '{"emailInput": "brandon", "passwordInput": "1234"}'

Variables de Entorno: (DEBUG)
export MONGODB_USER=admin
;export MONGODB_PASS=pass123
;export MONGODB_HOST=localhost
;export SECRET_KEY=EstaClaveSecreta