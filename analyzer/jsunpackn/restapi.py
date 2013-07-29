#!/usr/bin/env python
#REST API Server for jsunpack-n


import json
import argparse
from jsunpackn_wrapper import *

try:
    from bottle import Bottle, route, run, request, server_names, ServerAdapter, hook, response, HTTPError
except ImportError:
    raise Exception("No bottle.py!")

    


@hook("after_request")
def custom_headers():
    """Set some custom headers across all HTTP responses."""
    response.headers["Server"] = "Machete Server"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Pragma"] = "no-cache"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Expires"] = "0"


@route("/jsunpackn/analyze/<task_url>", method="GET")
def analyze(task_url):
    wrapper = JsunpacknWrapper()
    response = wrapper.analyzeJs(task_url)

    return response


