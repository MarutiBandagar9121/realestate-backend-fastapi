# create python venev
- python -m venv venv
- pip install -r requirements.txt
- uvicorn main:app --reload

- python -m pip freeze > requirements.txt