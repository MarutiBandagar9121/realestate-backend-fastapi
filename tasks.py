from invoke import task

@task
def freezereq(c):
    c.run("python -m pip freeze > requirements.txt")

@task
def dev(c):
    c.run("uvicorn main:app --reload --port 8000")

@task
def migrate(c, msg):
    c.run(f'alembic revision --autogenerate -m "{msg}"')

@task
def upgrade(c):
    c.run("alembic upgrade head")