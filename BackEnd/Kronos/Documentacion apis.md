# API Documentation

## Introduction
This API provides the information for the frontend to work

## Getting Started
Explain how to get started with the API, including any prerequisites and installation instructions.

    path('login/', LoginView.as_view(), name='login'),
    path('verify-email/<uuid:token>/', verify_email, name='verify-email'),
    path('Register/', RegisterView.as_view(), name='register'),
    path('schools/', SchoolListView.as_view(), name='get_schools'),
    path('create_schools/', SchoolCreateView.as_view(), name='create_school'),
    path('ForgotPassword/', OlvideMiContrasenia.as_view(), name='OlvideMiContrasenia'),
    path('forgot-password/<uuid:token>/', change_password, name='forgot-password')
## Endpoints
1. 127.0.0.1:8000/Kronosapp/Register/
2. 127.0.0.1:8000/Kronosapp/login/
3. 127.0.0.1:8000/Kronosapp/verify-email/<uuid:token>/
4. 127.0.0.1:8000/Kronosapp/schools/
5. 127.0.0.1:8000/Kronosapp/create_schools/
6. 127.0.0.1:8000/Kronosapp/ForgotPassword/
7. 127.0.0.1:8000/Kronosapp/ForgotPassword/<uuid:token>/

### Endpoint 1
- Method: POST
- Path: /Kronosapp/Register/
- body structure: ''' {"username":"teos","email":"dafafs@gmail.com","password":"pepe1234"} '''
- Description: This endpoint register a new user, you can use it to create a teacher too :).

### Endpoint 2
- Method: POST
- Path: /api/endpoint2
- Description: This endpoint creates a new resource on the server.

## Error Handling
Explain how errors are handled by the API, including the error codes and messages returned.

## Rate Limiting
If applicable, describe any rate limiting policies enforced by the API.

## Examples
Provide some examples of how to use the API, including sample requests and responses.

## Conclusion
Wrap up the documentation with any additional information or resources that might be helpful.

