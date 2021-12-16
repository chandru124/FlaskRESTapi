from datetime import datetime
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, json_response, as_json, jsonify
import json
import random, string
from flask import Flask, abort


app = Flask(__name__)
FlaskJSON(app)

class Counter:
	def __init__(self, id, name, value):
		self.id = id
		self.name = name
		self.value = value

	def to_json(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

counters = {}

@app.route('/areyoualive')
def get_time():
    now = datetime.utcnow()
    res = { "success" : True, "date": now}
    return jsonify(res)

@app.route('/counters', methods = ['GET'])
def get_counters():
	res = []
	for k, v in counters.items():
		res.append(json.loads(v.to_json()))
	return jsonify(res)

@app.route('/counters', methods = ['POST'])
def create_counter():
	try:
		req_json = request.get_json(force=True)
	except Exception as e:
		print("Data:", request, format(e))
		abort(400, "Invalid request body")

	print("Request", req_json)
	id = get_id()
	res = Counter(id, req_json['name'], 0)
	counters[id] = res
	return res.to_json()

def get_id():
	
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route('/counters/<string:id>', methods = ['PUT'])
def increment(id):
	# counters { "id1" : CounterObj1, "id2": CounterObj}
	body=request.get_json(force=True)
	# Fetch based on id.
	# If not found, return 404
	# increment and return
	if id not in counters:
		print("something")
		return 404
	else:
		counter = counters[id]
		counter.value = body["increment_by"] + counter.value
		print("something")
		return counter.to_json()

@app.route('/counters/<string:id>',methods = ['GET'])
def get_odj(id):
	if id not in counters:
		return 404
	else:
		result=counters[id]
		return result.to_json()

@app.route('/counters/<string:id>',methods = ['DELETE'])
def delt(id):
	if id not in counters:
		return "not in data"
	else:
		del counters[id]
		return "done"


if __name__ == '__main__':
	app.run(debug = True)



