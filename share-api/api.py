from flask import Flask
from flask import g
from flask import Response
from flask import request
from flask import jsonify
import json
import pycps
import uuid

app = Flask(__name__)

def clusterpoint_connect():
	con = pycps.Connection('tcp://cloud-us-0.clusterpoint.com:9007', 
		                   'shareapp', 
		                   'technovigno@gmail.com', 
		                   'hackathon123', 
		                   '100881')
	return con


def ret_json(json_data):
	return Response(response=json_data, status=200, mimetype="application/json")

# Entities being user, companies, locations and reviews
# Sample jsons:
# user - { 'tim@gmail.com' : {'name': 'Tim Southee', 'location': 'San Francisco, CA' } }
# company - { 'Uber' : { 'type': 'ride sharing' } }
# location - { 'San Francisco, CA' : { 'companies': ['Uber', 'lyft', 'sidecar', 'doordash'] } }
# reviews - { 1: { 'user_id': 'tim@gmail.com', 'comp_id': 'Uber', 'location_id': 'San Francisco, CA', 'review_text': 'Awesome experience!', 'rating': 'love', 'hour_earning': '45' } }
@app.route("/api/load/<entity_id>", methods=['POST'])
def insert_entity_data(entity_id):
	if entity_id == 'ref':
		entity_id = uuid.uuid4()
	entity_id = str(entity_id).lower()
	entity_id = entity_id.replace('_', ' ')
	print request.data
	json_data = json.loads("{ \""+ entity_id + "\": " + request.data + "}")
	print json_data
	try:
		con = clusterpoint_connect()
		try:
			response = con.retrieve(entity_id)
			con.update(json_data)
		except pycps.APIError:
			con.insert(json_data)
	except pycps.APIError as e:
		print e
	return Response(status=200)

@app.route("/api/find/<entity_id>", methods=['GET'])
def get_entity_data(entity_id):
	entity_id = str(entity_id).lower()
	entity_id = entity_id.replace('_', ' ')
	try:
		con = clusterpoint_connect()
		response = con.retrieve(entity_id)
	except pycps.APIError as e:
		print e
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	result = []
	if response.hits:
		for iid, item in response.get_documents().items():
			result.append(item)
	json_r = jsonify(res=result)
	return json_r

@app.route("/api/location/<location_id>", methods=['GET'])
def get_location_reviews_ratings(location_id):
	location_id = location_id.replace("_", " ")
	con = clusterpoint_connect()
	response = con.search(pycps.query.term(location_id, 'location_id'), docs=10, 
		        offset=0, list = {})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	result = []
	if response.hits:
		for iid, item in response.get_documents().items():
			result.append(item)
	json_r = jsonify(res=result)
	return json_r

@app.route("/api/company/<comp_id>", methods=['GET'])
def get_company_reviews_ratings(comp_id):
	con = clusterpoint_connect()
	response = con.search(pycps.query.term(comp_id, 'comp_id'), docs=10, 
		          offset=0, list={})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	result = []
	if response.hits:
		for iid, item in response.get_documents().items():
			result.append(item)
	json_r = jsonify(res=result)
	return json_r

@app.route("/api/user/<user_id>", methods=['GET'])
def get_user_reviews_ratings(user_id):
	con = clusterpoint_connect()
	response = con.search(pycps.query.term(user_id, 'user_id'), docs=10, 
		           offset=0, list={})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	result = []
	if response.hits:
		for iid, item in response.get_documents().items():
			result.append(item)
	json_r = jsonify(res=result)
	return json_r

@app.route("/api/allreviews", methods=['GET'])
def get_allreviews():
	con = clusterpoint_connect()
	response = con.search(pycps.query.term('reviews', 'type'), docs=10, 
		          offset=0, list={})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	result = []
	if response.hits:
		for iid, item in response.get_documents().items():
			result.append(item)
	json_r = jsonify(res=result)
	return json_r

def calculate_overall_ratings(company_id):
	con = clusterpoint_connect()

@app.route("/")
def hello():
	return "Hello Hackaton!"

if __name__ == "__main__":
	app.debug = True
	app.run(host="li1184-50.members.linode.com", port=8081)

