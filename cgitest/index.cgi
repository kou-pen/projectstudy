#!/usr/local/bin/python3.7
from wsgiref.handlers import CGIHandler
from main import app
CGIHandler().run(app)