import flask
from flask import Flask, redirect, url_for
from flask_prometheus_metrics import register_metrics
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

app = Flask(__name__)

@app.route('/admin')  # decorator for route(argument) functions
def hello_admin():  # binding to hello_admin call
    return 'Hello Admin'


@app.route('/guest/<guest>')
def hello_guest(guest):  # binding to hello_guest call
    return 'Hello %s as Guest' % guest


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':  # dynamic binding of URL to function
        return redirect(url_for('hello_admin'))

    else:
        return redirect(url_for('hello_guest', guest=name))

# provide app's version and deploy environment/config name to set a gauge metric
register_metrics(app, app_version="v0.1.2", app_config="staging")

# Plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

run_simple(hostname="0.0.0.0", port=5000, application=dispatcher)
