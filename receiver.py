from flask import Flask, request
from flask_restful import Api
import json
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://172.17.0.3:27017/')
#@app.before_first_request
#if __name__ == '__main__':
@app.route('/write', methods=['GET', 'POST'])
def handler():
    req = request.data
    try:
        parsed_req = json.loads(req)
        print(parsed_req)
    except ValueError as e:
        return {"Error!":"Requested information is not a valid json string"}
    start_time = parsed_req['start_time']['$date']
    db_name = parsed_req['user_id']
    col_name = datetime.utcfromtimestamp(start_time/1000).strftime('%Y_%m_%d')
    db = client[db_name][col_name]
    print(db)
    post_id = db.insert_one(parsed_req).inserted_id
    post_id
    return req


#if __name__ == '__main__':
app.run(host='172.31.95.196', port=8090)
