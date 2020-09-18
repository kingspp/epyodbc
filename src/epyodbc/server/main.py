# -*- coding: utf-8 -*-
"""
| **@created on:** 9/17/20,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** 
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="/Users/prathyushsp/Git/arl/adhesives/epyodbc/src/epyodbc/server/assets/", html=True), name="static")

# templates = Jinja2Templates(directory="assets")


@app.get("/render/{data.xml}", response_class=HTMLResponse)
def root(xml:str):
    logger.info("hello")
    return xml

#
# @app.get("/", response_class=HTMLResponse)
# async def root(request, graph:str="abc"):
#     print(graph)
#     return templates.TemplateResponse("index.html", {"request": request})
