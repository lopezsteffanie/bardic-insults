from flask import Flask, jsonify, request
from db import get, create, get_random, delete_insult_by_id

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_insults():
    return get()

@app.route('/random', methods=['GET'])
def get_random_insult():
    return get_random()

@app.route('/add', methods=['POST'])
def add_insult():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    
    create(request.get_json())
    return 'Insult Added'

@app.route('/delete', methods=['DELETE'])
def delete_insult_by_id():
    data = request.get_json()
    if "insult_id" not in data:
        return jsonify({"msg": "Missing 'insult_id' in JSON"}), 400
    
    delete_insult_by_id(data["insult_id"])
    return 'Insult Deleted'




if __name__ == '__main__':
    app.run()