from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
cors = CORS(app)

def db_connection(database, starttime):
    client = MongoClient('172.17.0.3', 27017)
    #collection = datetime.utcnow().strftime('%Y_%m_%d')
    #collection = '2022_11_27'
    col = client[database][starttime]
    return col

def make_response(target, datapoints):
    response_object = { 
            "target": target,
            "datapoints": datapoints,
        }
    
    return response_object


def r_table2(target, cursor):
    datapoints = []
    response = []

    pipeline = [{ "$unwind": "$windows" }, { "$project": { "_id": 0, "title": "$windows"}}]
    tmp_datapoints = list(cursor.aggregate(pipeline))
    most_active_window = []
    for datapoint in tmp_datapoints:
        for key, value in datapoint['title'].items():
            tmp_most_active_window_value = value
            most_active_window = [key, value]
            if value > tmp_most_active_window_value:
                most_active_window = [key, value]
        for doc in cursor.find({}):
            datapoints.append([key,doc['start_time']['$date'],doc['end_time']['$date']])

    print("!!!!!!!!!!!!!!!!!!!!!!")
    response = make_response(target, datapoints)
    response = json.loads(str(response).replace("\'",'"'))
    print(response)
    response = [
        {
        "columns":[
        {"text":"Nome do programa","type":"string"},
        {"text":"Data inicial","type":"number"},
        {"text":"Data Final","type":"number"},
    ],
    "rows": datapoints,
        "type":"table"
        }
    ]
    return response

def r_graph(target, cursor, values):
    datapoints = []
    response = []

    for value in values:
        for doc in cursor.find({}):
            datapoints.append([doc[value],doc['start_time']['$date']])
        datapoints = json.loads(str(datapoints).replace("\'",""))
        print(datapoints)
        response.append(make_response(target, datapoints))
    print("!!!!!!!!!!!!!!!!!!!!!!")

    print(response)

    return response

def r_bar(target, cursor):

    datapoints = []
    for doc in cursor.find({}):
        datapoints.append( [doc['activity_score'],doc['start_time']['$date']])
    print("!!!!!!!!!!!!!!!!!!!!!!")
    datapoints = json.loads(str(datapoints).replace("\'",""))
    print(datapoints)

    response = [
        {
            "target": target,
            "datapoints": datapoints, 
        }
    ]
    print(response)
    return response

def r_table(target, cursor):
    #pipeline = [{ "$unwind": "$windows" }, { "$project": { "_id": 0, "title": "$windows"}}]
    pipeline = [ { "$project": { "_id": 0, "windows": "$windows"}},{ "$unwind": "$windows" },{ "$addFields": { "window": { "$objectToArray": "$windows"} } }, { "$unwind": "$window"},{ "$group": { "_id": { "id": "$_id", "k": "$window.k"}, "v": {"$sum": "$window.v"}} },{ "$group": {"_id": "$_id.id","windows": { "$push": {"k": "$_id.k", "v": "$v"}}} },{ "$project": {"windows": {"$arrayToObject": "$windows"} } } ]
    datapoints = []

    tmp_datapoints = list(cursor.aggregate(pipeline))
    print("!!!!!!!!!!!!!!!!!!!!!!")
    for datapoint in tmp_datapoints:
        for key, value in datapoint['windows'].items():
            datapoints.append([key,value])

    response = [
        {
        "columns":[
        {"text":"Nome do programa","type":"string"},
        {"text":"Rank de uso","type":"number"},
    ],
    "rows": datapoints,
        "type":"table"
        }
    ]
    print(response)
    return response


def r_gauge(target, cursor):

    datapoints = 0
    for doc in cursor.find({}):
        datapoints+=( doc['activity_score'])
    print("!!!!!!!!!!!!!!!!!!!!!!")
    print(datapoints)
    
    response = [
        {
            "target": target,
            "datapoints": [ [datapoints/3600]],
        }
    ]
    print(response)
    return response

@app.route('/query', methods=['GET', 'POST'])
def r_query():

    req = request.json
    target = req["targets"][0]["target"]
    print(str(req["range"]["from"]).split('T')[0])
    short_date = str(req["range"]["from"]).split('T')[0]
    starttime = datetime.strptime(short_date, "%Y-%m-%d").strftime('%Y_%m_%d')
    print(starttime)
    panel = target.split("/")[-1]
    database = target.split("/")[-2]

    mongo_cursor = db_connection(database, starttime)
    print(mongo_cursor)
    values = target.split("&")
    for v in values[1:]:
        print(v)
    if(panel == "bar"):
        return jsonify(r_bar(target, mongo_cursor))
    if('graph' in panel):
        return jsonify(r_graph(target, mongo_cursor, values[1:]))
    if(panel == "gauge"):
         return jsonify(r_gauge(target, mongo_cursor))
    if(panel == "table"):
         return jsonify(r_table(target, mongo_cursor))
    if(panel == "table2"):
         return jsonify(r_table2(target, mongo_cursor))
    return ""

if __name__ == '__main__':
    app.run(host='172.31.95.196', port=8091)
