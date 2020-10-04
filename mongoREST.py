import json
from bson import json_util
from flask import Flask
from flask import request, abort
from pymongo import MongoClient
from werkzeug.routing import ValidationError

app = Flask(__name__)
connection = MongoClient('localhost', 27017)
db = connection['city']
collection = db['inspections']


@app.route('/hello')
def hello_world():
    name = request.args.get('name')

    try:
        if name:
            return '{hello: \"' + name + '\"}'
        else:
            abort(404)
    except NameError:
        abort(404)


@app.route('/strings')
def get_strings():
    first = request.args.get('string1')
    second = request.args.get('string2')

    try:
        if first and second:
            return '{first: \"' + first + '\", second: \"' + second + '\"}'
        else:
            abort(404)
    except NameError:
        abort(404)


@app.route('/create', methods=['POST'])
def create_business():
    content = request.get_json(silent=True)

    try:
        myDocument = {
            "business_name": content["business_name"],
            "certificate_number": content["certificate_number"],
            "date": content["date"],
            "id": content["id"],
            "sector": content["sector"]
        }
        collection.save(myDocument)
        return json.dumps(myDocument, default=json_util.default)
    except ValidationError:
        abort(404)
    except NameError:
        abort(404)


@app.route('/read')
def get_business():
    name = request.args.get('business_name')

    try:
        result = collection.find_one({'business_name': name})
        if result:
            return json.dumps(result, default=json_util.default)
        else:
            abort(404)
    except ValidationError as ve:
        abort(404)
    except NameError:
        abort(404)

    return abort(404)


@app.route('/update')
def update_business():
    bizID = request.args.get("id")
    newValue = request.args.get("result")

    try:
        collection.find_one_and_update({"id": bizID}, {"$set": {"result": newValue}})
        updatedDoc = collection.find_one({"id": bizID})

        if updatedDoc:
            return json.dumps(updatedDoc, default=json_util.default)
        else:
            abort(404)

    except ValidationError:
        abort(404)
    except NameError:
        abort(404)

    return abort(404)


@app.route('/delete')
def delete_business():
    bizID = request.args.get("id")

    try:
        collection.delete_one({"id": bizID})
        return 'True'
    except ValidationError:
        abort(400)
    except NameError:
        abort(400)

    return 'False'

