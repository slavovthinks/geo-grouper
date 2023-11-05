from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from geo_grouper.routes import grouping_router

app = FastAPI()

app.include_router(grouping_router)
app.mount("/static", StaticFiles(directory="static"), name="static")
