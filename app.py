from flask import Flask, Response, request
from flask_cors import CORS
import json
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
from database_services.RDBService import RDBService as RDBService

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return '<u>Hello World!</u>'


@app.route('/imdb/artists/<prefix>')
def get_artists_by_prefix(prefix):
    res = IMDBArtistResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route('/users')
def get_users():
    res = UserResource.get_by_template()
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users/name/<prefix>')
def get_users_by_name(prefix):
    res = UserResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users/<userid>')
def get_users_by_userid(userid):
    res = UserResource.get_by_name_userid(userid)
    res = UserResource.get_links(res)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp

@app.route('/<table_name>', methods=['POST'])
def do_resource_collection(table_name):
    data = request.get_json()
    data['ID'] = UserResource.get_next_id(table_name)
    res = UserResource.create(table_name, data)
    #rsp1 = Response(json.dumps(data), status=200, content_type="application/json")
    rsp = Response("CREATED", status=201, content_type="text/plain")
    return rsp

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
