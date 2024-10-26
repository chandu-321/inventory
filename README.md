
# Inventory Management System - User Guide

## User Registration and Authentication

1. **Registering a New User**:
   - Before using the API, you need to register a new user.
   - Send a **POST** request to `/register/` with the following JSON body:
     ```json
     {
         "username": "your_username",
         "password": "your_password"
     }
     ```

2. **Logging In**:
   - After registration, you can log in to obtain your JSON Web Token (JWT).
   - Send a **POST** request to `/login/` with the following JSON body:
     ```json
     {
         "username": "your_username",
         "password": "your_password"
     }
     ```
   - If successful, you will receive a JWT token in the response, which will be used for authenticating future requests.

3. **Using the JWT Token**:
   - Include the JWT token in the `Authorization` header for all subsequent requests to access protected endpoints:
     ```
     Authorization: Bearer your_jwt_token
     ```

## Accessing Other Endpoints

- After logging in and obtaining the JWT token, ensure to include the `Authorization` header in your requests to access other endpoints (e.g., creating, retrieving, updating, or deleting inventory items).
- Example request to create a new inventory item:
  ```http
  POST /items/
  Authorization: Bearer your_jwt_token

  {
      "name": "New Item",
      "quantity": 5,
      "description": "Description of the item.",
      "price": 20.99
  }
  ```

## Database and Redis Configuration

### Update `settings.py`

To configure the database and Redis server, you need to modify the `settings.py` file in your Django project. Here are the necessary changes:

1. **Database Configuration**:
   - Locate the `DATABASES` setting in `settings.py`.
   - Replace the default SQLite configuration with your desired database settings. For example, if you are using PostgreSQL, it might look like this:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'your_database_name',
             'USER': 'your_database_user',
             'PASSWORD': 'your_database_password',
             'HOST': 'localhost',  # Or your database server address
             'PORT': '5432',       # Default PostgreSQL port
         }
     }
     ```

2. **Redis Cache Configuration**:
   - To enable caching, you must set up Redis in the `CACHES` setting:
     ```python
     CACHES = {
         'default': {
             'BACKEND': 'django_redis.cache.RedisCache',
             'LOCATION': 'redis://127.0.0.1:6379/1',  # Change this to your Redis server location
             'OPTIONS': {
                 'CLIENT_CLASS': 'django_redis.client.DefaultClient',
             }
         }
     }
     ```

### Summary

- Ensure you **register** first before trying to **log in**.
- After logging in, use the provided JWT token in the `Authorization` header for all requests to access other endpoints.
- Make necessary changes to `settings.py` for database and Redis server configurations before running the application.

For any questions or further assistance, feel free to reach out or refer to the Django and Django REST Framework documentation.
