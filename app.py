from chalice import Chalice, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from dotenv import load_dotenv
import os

app = Chalice(app_name='auction_service')
app.debug = True

load_dotenv()
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri,tlsAllowInvalidCertificates=True)
db = client['auction_service_db']
trays_collection = db.trays

@app.route('/api/auctions', methods=['GET'])
def index():
    return {'hello': 'world'}



@app.route('/api/trays/{tray_id}', methods=['DELETE'])
def delete_tray(tray_id):
    try:
        oid = ObjectId(tray_id)
    except InvalidId:
        return Response(body={'status': 'failure', 'message': 'Invalid tray ID format'}, status_code=400)

    result = trays_collection.delete_one({'_id': oid})
    if result.deleted_count > 0:
        return {'status': 'success', 'message': f'Tray {tray_id} deleted successfully'}
    else:
        return Response(body={'status': 'failure', 'message': 'Tray not found'}, status_code=404)
@app.route('/api/trays/{tray_id}', methods=['PUT'])
def update_tray(tray_id):
    try:
        oid = ObjectId(tray_id)
    except InvalidId:
        return Response(body={'status': 'failure', 'message': 'Invalid tray ID format'}, status_code=400)

    request = app.current_request
    tray_data = request.json_body

    result = trays_collection.update_one(
        {'_id': oid},
        {'$set': tray_data}
    )
    if result.matched_count > 0:
        updated_tray = trays_collection.find_one({'_id': oid})
        updated_tray['_id'] = str(updated_tray['_id'])
        return {'status': 'success', 'message': f'Tray {tray_id} updated successfully', 'updatedTray': updated_tray}
    else:
        return Response(body={'status': 'failure', 'message': 'Tray not found'}, status_code=404)

@app.route('/api/trays/{tray_id}', methods=['GET'])
def get_tray(tray_id):
    try:
        oid = ObjectId(tray_id)
    except bson.errors.InvalidId:
        return Response(body={'status': 'failure', 'message': 'Invalid tray ID format'}, status_code=400)

    tray = trays_collection.find_one({'_id': oid})
    if tray:
        tray['_id'] = str(tray['_id'])  #  ObjectId conversion back to string for print
        return {'status': 'success', 'tray': tray}
    else:
        return Response(body={'status': 'failure', 'message': 'Tray not found'}, status_code=404)
@app.route('/api/trays', methods=['POST'])
def add_tray():
    tray_data = app.current_request.json_body

    result = trays_collection.insert_one(tray_data)
    if result.inserted_id:
        return {'status': 'success', 'message': 'Tray added successfully', 'tray_id': str(result.inserted_id)}
    else:
        return Response(body={'status': 'failure', 'message': 'Failed to add tray'}, status_code=400)