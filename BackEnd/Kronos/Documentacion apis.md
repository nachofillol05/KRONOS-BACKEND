# KRONOS API Documentation

## Introduction
This API provides the information for the frontend to work

## Getting Started
This API uses DRF. To consume it you have:
- While testing: Point to the URL: 
  localhost:8000/Kronosapp/YourRoute/
- while production: Point to the URL:
  Kronosapp.com.ar/Kronosapp/YourRoute/

## Endpoints
1. 127.0.0.1:8000/Kronosapp/Register/
2. 127.0.0.1:8000/Kronosapp/login/
3. 127.0.0.1:8000/Kronosapp/verify-email/<uuid:token>/
4. 127.0.0.1:8000/Kronosapp/schools/
5. 127.0.0.1:8000/Kronosapp/create_schools/
6. 127.0.0.1:8000/Kronosapp/ForgotPassword/
7. 127.0.0.1:8000/Kronosapp/ForgotPassword/<uuid:token>/
***
## Endpoint 1: Register
  ### Method: 
  POST
### Path: 
  /Kronosapp/Register/
### body structure:
    {
        "username":"teos",
        "email":"dafafs@gmail.com",
        "password":"pepe1234"
    } 
### Description: 
This endpoint register a new user, you can use it to create a teacher too :).
  ### Output:
- HTTPstatus=200
  Response:
  ``` Json
  {
    "token": "354b333cfb962cfc4df0e8105e21275ad55e5450",
    "mensaje": "Correo electrónico enviado con éxito"
  }
- HTTPstatus=400
  Response:
    ```
    "Nombre de usuario ya en uso"
- HTTPstatus=400
  Response:
    ```
    "mail ya en uso"
***

### Endpoint 2
  ### Method: 
  POST
### Path: 
  /Kronosapp/login/
### body structure:
    {
        "username": "teos",
        "password": "pepe1234"
    }
### Description: 
Este endpoint permite a un usuario existente iniciar sesión en el sistema.
  ### Output:
- HTTPstatus=200
  Response:
  ``` Json
  {
      "Token": "a18a0428a4d6cb797ba5923eb7315af9b8f182ad",
      "message": "Login exitoso"
  }
- HTTPstatus=401
  Response:
  ``` Json
    {
        "message": "El usuario o contraseña son incorrectos"
    }

***



### Endpoint 3
  ### Method: 
  GET
### Path: 
  /Kronosapp/verify-email/<uuid:token>/
### Parámetro URL:
<uuid:token>: Token único enviado por email para verificar la cuenta del usuario.
### Description: 
Este endpoint permite a un usuario verificar su dirección de correo electrónico haciendo clic en un enlace enviado por email después del registro.
### Output: 
- HTTPstatus=200
  Response:
  ``` Json
    'Correo electrónico verificado con éxito'
- HTTPstatus=400
  Response:
  ``` Json
    'Correo electrónico ya verificado'
- HTTPstatus=404
  Response:
  ``` Json
    'Token de verificación no válido'

***



### Endpoint 4
  ### Method: 
  GET
### Path: 
  /Kronosapp/schools/
### Description: 
Este endpoint devuelve una lista de todas las escuelas del sistema.
### Output: 
- HTTPstatus=200
  Response:
  ``` Json
    {
        COMPLETA ORE
    }
***

### Endpoint 5
  ### Method: 
  POST
### Path: 
  /Kronosapp/create_schools/
### body structure:
    {
        "name": "Escuela XYZ",
        "address": "Calle 123",
        "city": "Córdoba",
        "state": "Córdoba",
        "country": "Argentina"
        COMPLETAAAAAAAAAAAAAAAAAA
    }
### Description: 
Descripción: Este endpoint permite a un usuario con permisos de administrador crear una nueva escuela en el sistema.
### Output: 
COMPLETAAAA
***

### Endpoint 6
  ### Method: 
  POST
### Path: 
  /Kronosapp/ForgotPassword/
### body structure:
    {
        "token": "xxxx"
    }
### Description: 
 Este endpoint permite a un usuario solicitar un enlace para restablecer su contraseña. El token es el enviado desde el Front para identificar el usuario.
### Output: 
- HTTPstatus=200
  Response:
  ``` Json
    {
        "Correo enviado con exito"
    }
- HTTPstatus=400
  Response:
  ``` Json
    {
        "Error al enviar el correo"
    }
***

### Endpoint 7
  ### Method: 
  POST
### Path: 
  /Kronosapp/ForgotPassword/<uuid:token>/
### Parámetro URL:
<uuid:token>: Token único enviado por email para restablecer la contraseña del usuario.
### body structure:
    
    {
        "new_password": "nueva_contraseña"
    }
### Description: 
 Este endpoint permite a un usuario restablecer su contraseña utilizando el token enviado por email.
### Output: 
- HTTPstatus=200
  Response:
  ``` Json
    {
        "Contraseña cambiada"
    }
- HTTPstatus=400
  Response:
  ``` Json
    {
        "El correo no esta verificado"
    }
- HTTPstatus=404
  Response:
  ``` Json
    {
        "Token de verificación no válido"
    }
***
## Error Handling
The errors will be handed by the HTTP Status 400, There you have to show to the user had an error in what he was doing.

## Examples
Provide some examples of how to use the API, including sample requests and responses.

## Conclusion
Use this API if you need information about the app Kronos

