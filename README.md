# Heimdall

Heimdall is a gatekeeper app, aimed at simple auth-as-a-service.

It uses django's built in auth system and exposes REST APIs for the same.

### Goal

- Simple auth service, without any riff-raff.
- Should handle exceptions, like unique username, email validation, password hashing, unique phone_number
- Works flawlessly out of the box.
- Future extensibility of modules for complex auth workflows should be possible.

### To Do
- logout
- Reset password feature
- Change email for account 
- Change username?
- phone/email verification

### Setup

- Clone repo

Using, django local
- in venv, run
    ```shell
    pip3 install -r heimdall/requirements.txt
    ```
- now, run
    ```shell
     python manage.py migrate
    ```
  This should create a new db.sqlite3
- and then,

    ```shell
     python manage.py runserver
    ```
- Et voila! a working auth service with a minimal user model is available now

alternatively

```shell
docker-compose up --build --force-recreate --remove-orphans
```
can be used to run the same in a docker container.


### docs
16 Oct, 21
There are currently 3 APIs available

- Signup
    ```json
      {
        "username" : "username",
        "email": "email",
        "password": "password"    
  
      }
    ```
    All three are mandatory fields and username and email should be unique.
    A Response with set-cookie header is sent to the client
  
- login

    ```json
      {
        "username" : "username",
        "password" : "password"
      } 
    ```

- validate

    we use django's session based auth. So, when a user makes a request, the session can be validated
  by sending a request with the session id
  
    ```json
      {
        "session" : "session_token"
        
      }  
    
    ```
