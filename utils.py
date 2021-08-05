from bson import json_util
import json

def simplify_id(obj):
    obj['_id'] = obj['_id']['$oid']
    return obj

def mongres_to_json(mongres):
    return json.loads(json_util.dumps(mongres))