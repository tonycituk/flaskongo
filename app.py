# IMPORTS
from flask import Flask, Response, request
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
from utils import simplify_id
from utils import mongres_to_json as mtj

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://flaskonger:flaskongerpass@localhost:27017/flaskongo-db"
mongo = PyMongo(app)

#mongo.db.flaskongos.insert_one({
#   'message': 'im another flaskongo'
#})


@app.route("/flaskongos/", methods=['GET'])
def get_allFlaskongos():
    # BSON to JSONstr to JSONobj
    flaskongos_obj = mtj(mongo.db.flaskongos.find())
    flaskongos_obj_clean = [simplify_id(flaskongo_obj)
                            for flaskongo_obj in flaskongos_obj]
    # JSONobj to JSONstr again
    flaskongos_clean = json_util.dumps(flaskongos_obj_clean)
    return Response(flaskongos_clean, mimetype='application/json')
# Another implementation to swap _id for $oid
# flaskongos_obj_clean.append({
#    'id': flaskongo_obj['_id']['$oid'],
#    'message': flaskongo_obj['message']
# })
# Simplify _id
    # for flaskongo_obj in flaskongos_obj:
    #    flaskongo_obj['_id'] = flaskongo_obj['_id']['$oid']
    #    flaskongos_obj_clean.append(flaskongo_obj)


@app.route("/flaskongo/<id>", methods=['GET'])
def get_flaskongo(id):
    flaskongo = mtj(mongo.db.flaskongos.find_one_or_404({'_id': ObjectId(id)}))
    flaskongo_clean = json_util.dumps(simplify_id(flaskongo))
    return Response(flaskongo_clean, mimetype='application/json')

@app.route("/flaskongo/<id>", methods=['DELETE'])
def delete_flaskongo(id):
    flaskongo = mtj(mongo.db.flaskongos.find_one_or_404({'_id': ObjectId(id)}))
    if flaskongo:
        print("deleted: ", flaskongo)
    mongo.db.flaskongos.delete_one({'_id': ObjectId(id)})
    flaskongo_clean = json_util.dumps(simplify_id(flaskongo))
    return Response(flaskongo_clean, mimetype='application/json')

@app.route("/flaskongo/", methods=['POST'])
def add_flaskongo():
    new_flaskongo = request.get_json()
    mongo.db.flaskongos.insert_one(new_flaskongo)
    new_clean_flaskongo = json_util.dumps(simplify_id(mtj(new_flaskongo)))
    print("added: ", new_flaskongo)
    return Response(new_clean_flaskongo, mimetype='application/json')

@app.route("/flaskongo/<id>", methods=['PUT'])
def update_flaskongo(id):
    message = request.get_json()['message']
    mongo.db.flaskongos.find_one_or_404({'_id': ObjectId(id)})
    mongo.db.flaskongos.update_one({'_id': ObjectId(id)}, { "$set": { "message": message } })
    updated_flaskongo = simplify_id(mtj(mongo.db.flaskongos.find_one_or_404({'_id': ObjectId(id)})))
    print("updated: ", updated_flaskongo)
    clean_updated_flaskongo = json_util.dumps(updated_flaskongo)
    return Response(clean_updated_flaskongo, mimetype='application/json')