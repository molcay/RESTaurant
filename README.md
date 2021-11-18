# RESTaurant

RESTaurant is a RESTful API for managing the restaurants.

## Instruction to Setup and Run
* You can create a virtual environment.
```shell
python3 -m venv venv
```

* You can activate it the venv.
```shell
. ./venv/bin/activate 
# or in PowerShell
.\venv\Scripts\activate
```

* You can use the `requirements.txt` file to install dependencies.
```shell
pip install -r requirements.txt
```

* Now, you can start the application:
```shell
python manage.py runserver
```
> For easy setup, I include the db.sqlite3 file to easily start application.
> You can pass the `migrate` command

* or, you can run the tests:
```shell
python manage.py test
```
