# API_Auth
Autentificador

Ejemplos

Cuenta Nueva:

curl -X POST http://localhost:8001/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "brandon@gmail.com", "passwordInput": "1234"}'

Inicion de Sesion:

curl -X POST http://localhost:8001/api3/auth \
-H "Content-Type: application/json" \
-d '{"emailInput": "brandon@gmail.com", "passwordInput": "1234"}'

curl -X POST http://localhost:8006/api3/validar_privilegios \
-H "Content-Type: application/json" \


Variables de Entorno: (DEBUG)
export MONGODB_USER=admin
;export MONGODB_PASS=pass123
;export MONGODB_HOST=localhost

curl -X POST http://localhost:8006/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "jesus.torres", "passwordInput": "zJg890oLNVky", "privilegesInput" : "rfc"}'
{"message":"Cuenta agregada exitosamente"}

cuenta:
jesus.torres
contraseña:
zJg890oLNVky

curl -X POST http://localhost:8006/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "raul.romero", "passwordInput": "gNj6vUj988Rz", "privilegesInput" : "vpn"}'

---DNS en servidor de desarrollo
curl -X POST http://localhost:8006/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "cuenta.dns", "passwordInput": "gNj8vUj98ERz", "privilegesInput" : "dns"}'

cuenta:
cuenta.dns
contraseña:
gNj8vUj98ERz

---ABC en servidor de desarrollo
curl -X POST http://localhost:8006/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "cuenta.abc", "passwordInput": "gNj8vUj98ER3", "privilegesInput" : "abc"}'

cuenta:
cuenta.abc
contraseña:
gNj8vUj98ER3

cuenta:
raul.romero
contraseña:
gNj6vUj988Rz

curl -X POST http://localhost:8006/api3/generate -H "Content-Type: application/json" -d '{"emailInput": "cuentaPrueba", "passwordInput": "Pru3B4", "privilegesInput" : "admin"}'