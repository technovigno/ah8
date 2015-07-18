from flask import Flask
from flask import g
from flask import Response
from flask import request
import json
import pycps

app = Flask(__name__)

def clusterpoint_connect():
	con = pycps.Connection('tcp://cloud-us-0.clusterpoint.com:9007', 
		                   'shareapp', 
		                   'technovigno@gmail.com', 
		                   'hackathon123', 
		                   '100881')
	return con


# Entities being user, companies, locations and reviews
# Sample jsons:
# user - { 'tim@gmail.com' : {'name': 'Tim Southee', 'location': 'San Francisco, CA' } }
# company - { 'Uber' : { 'type': 'ride sharing' } }
# location - { 'San Francisco, CA' : { 'companies': ['Uber', 'lyft', 'sidecar', 'doordash'] } }
# reviews - { 1: { 'user_id': 'tim@gmail.com', 'comp_id': 'Uber', 'location_id': 'San Francisco, CA', 'review_text': 'Awesome experience!', 'rating': 'love', 'hour_earning': '45' } }
@app.route("/api/load/<entity_id>", methods=['POST'])
def insert_entity_data(entity_id):
	json_data = json.loads(request.data)
	try:
		con = clusterpoint_connect()
		try:
			response = con.retrieve(entity_id)
		except pycps.APIError:
			con.insert({entity_id: json_data})
		con.update({entity_id: json_data})
	except pycps.APIError as e:
		print e

@app.route("/api/find/<entity_id>", methods=['GET'])
def get_entity_data(entity_id):
	try:
		con = clusterpoint_connect()
		response = con.retrieve(entity_id)
	except pycps.APIError as e:
		print e
	return response

@app.route("/api/location/<location_id>", methods=['GET'])
def get_location_reviews_ratings(location_id):
	response = con.search(pycps.query.term(location_id), docs=10, 
		        offset=1, list={'location_id':'yes', 'user_id':'no', 'comp_id':'no'})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	return response

@app.route("/api/company/<comp_id>", methods=['GET'])
def get_company_reviews_ratings(comp_id):
	response = con.search(pycps.query.term(comp_id), docs=10, 
		          offset=1, list={'comp_id':'yes', 'user_id':'no', 'location_id':'no'})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	return response	

@app.route("/api/user/<user_id>", methods=['GET'])
def get_user_reviews_ratings(user_id):
	response = con.search(pycps.query.term(user_id), 
		          docs=10, offset=1, list={'user_id':'yes', 'comp_id':'no', 'location_id':'no'})
	print "Total hits: {0}, returned: {1}".format(response.hits, response.found)
	return response	

def calculate_overall_ratings(company_id):
	con = clusterpoint_connect()

@app.route("/")
def hello():
	return "Hello Hackaton!"

if __name__ == "__main__":
	app.debug = True
	app.run(host="location", port=8080)







