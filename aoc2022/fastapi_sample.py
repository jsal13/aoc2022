import random

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """Read root in API."""
    return {"Hello": "World"}


@app.get("/roll")
def roll():
    """Return a random number from 1 to 6."""
    return {"data": random.randint(1, 6)}
