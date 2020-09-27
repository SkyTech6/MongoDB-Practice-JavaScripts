import json
from os import abort
import sys
import getopt
from bson import json_util
from pymongo import MongoClient
from werkzeug.routing import ValidationError

connection = MongoClient('localhost', 27017)
db = connection['city']
collection = db['inspections']


def help_info():
    print('CREATE: milestoneOne -c <business name>')
    print('READ: milestoneOne -g <key> -v <target value> ')
    print('UPDATE: milestoneOne -g <key> -v <target value> -u <update key> -n <new value>')
    print('DELETE: milestoneOne -g <key> -v <target value> -delete')


def insert_document(document):
    try:
        collection.save(document)
        return 'True'
    except ValidationError as ve:
        abort(400, str(ve))
    return 'False'


def find_document(key, value):
    try:
        result = collection.find_one({key: value})
        return result
    except ValidationError as ve:
        abort(400, str(ve))


def update_document(doc, docValue, keyToUpdate, newValue):
    try:
        # returning this result displays the pre-updated document. So instead return a find_one
        collection.find_one_and_update({doc: docValue}, {"$set": {keyToUpdate: newValue}})
        return collection.find_one({doc: docValue})
    except ValidationError as ve:
        abort(400, str(ve))


def delete_document(doc, docValue):
    try:
        collection.delete_one({doc: docValue})
        return 'True'  # Spec says to return json... but the file is deleted? True/False is more appropriate.
    except ValidationError as ve:
        abort(400, str(ve))
    return 'False'


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hc:g:v:u:n:d:", ['business=', "find=", "value=", "update=", "newValue=",
                                                           'delete='])
    except getopt.GetoptError:
        help_info()
        sys.exit(2)

    createBusiness = ''
    findItem = ''
    findValue = ''
    updateItem = ''
    updateValue = ''
    isDeletion = False

    for opt, arg in opts:
        if opt == '-h':
            help_info()
        elif opt in ("-c", "--business"):
            createBusiness = arg
        elif opt in ("-g", "--find"):
            findItem = arg
        elif opt in ("-v", "--value"):
            findValue = arg
        elif opt in ("-u", "--update"):
            updateItem = arg
        elif opt in ("-n", "--newValue"):
            updateValue = arg
        elif opt in ("-d", "--delete"):
            isDeletion = True

    if createBusiness != '':
        myDocument = {"business_name": createBusiness}
        print(insert_document(myDocument))
    elif findItem != '':
        if updateItem != '':
            print(update_document(findItem, findValue, updateItem, updateValue))
        else:
            if isDeletion:
                print(delete_document(findItem, findValue))
            else:
                print(find_document(findItem, findValue))


main(sys.argv[1:])
