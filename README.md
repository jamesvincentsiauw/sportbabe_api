# Sportbabe API with Flask
### How to run

```bash
# clone the repository
$ git clone https://github.com/jamesvincentsiauw/sportbabe_api.git

# create virtual environment
$ python -m venv venv

# activate virtual environment
$ venv\scripts\activate

# install dependencies
(venv) $ pip install -r requirements.txt

# configure environment variable
(venv) $ cp .env.example .env

# change DB_URI in .env file to your DB URI

# run project
(venv) $ python app.py

# deactivate virtual environment
(venv) $ deactivate

# open in browser at http://127.0.0.1:5000/
```