from flask import Flask, request, send_from_directory,render_template
import requests
import os
from flask_cors import CORS
import logging
from spec import generate_spec

# app config
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

# routes
@app.route('/')
def docs():
    return send_from_directory('static', 'index.html')

@app.route('/demo/')
def demo_index():
    return send_from_directory('demo', 'index.html')

@app.route('/demo/<path:filename>')
def demo(filename):
    #print("---------------------------------------------------")
    #print(filename)
    #print("---------------------------------------------------")
    return send_from_directory('demo', filename)

@app.route("/spec")
def getSpec():
    model = os.getenv('ARTIFACT_PATH')
    spec = generate_spec(model)
    return spec

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    print("redirecting to ", "http://localhost:5002/" + path)
    try:
        resp = requests.request(
            method=request.method,
            url=f"http://localhost:5002/{path}",
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            allow_redirects=False)

        headers = [(name, value) for (name, value) in resp.raw.headers.items()]

        response = app.make_response((resp.content, resp.status_code, headers))
        return response

    except requests.exceptions.RequestException:
        return app.make_response(("An error occurred", 500))