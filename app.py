import os
import datetime 
from datetime import timedelta
import pytz
from flask import Flask, jsonify, url_for, redirect, request, render_template
from flask_pymongo import PyMongo
from flask_restful import Api, Resource


"""
	MongoDB configurations
"""

MONGO_URL = os.environ.get('MONGODB_URI')

if not MONGO_URL:
	MONGO_URL = 'mongodb://127.0.0.1:27017/ad_db';




app = Flask(__name__)

app.config["MONGO_URI"] = MONGO_URL


mongo = PyMongo(app, config_prefix='MONGO')

utc=pytz.UTC


class PartnerPost (Resource):

	def post(self):
		data = request.get_json()

		post_data = {}
		ad_post_time = datetime.datetime.now()
		
		
		

		if not data:
			data = {"response": "Error"}
			return jsonify(data)

		else:
			partner_id = data.get('partner_id')
			duration = data.get('duration')
			ad_content = data.get('ad_content')

			#convert ad_duration to integer value
			seconds = int(duration)
			ad_duration =timedelta(seconds =seconds)

			expiration = ad_post_time + ad_duration
			
			print ad_duration

			if data.has_key('partner_id') and data.has_key('duration') and data.has_key('ad_content'):
				if mongo.db.partner_id.find_one({"partner_id": partner_id}):
					return {"response": "partner already has ad running"}
				
				else:
					post_data['partner_id'] = str(partner_id)
					post_data['duration'] = int(duration)
					post_data['ad_content'] = str(ad_content)
					post_data['expiration'] = expiration
					mongo.db.partner_id.insert(post_data)
					return {"response": "post data sucessfuly!"}
					del post_data
			else:
				return {"response": "value missing || incorrect data format"}
		return redirect(url_for("partner_id"))

class PartnerGet (Resource):
	def get(self, id):

		data = []

		cursor = mongo.db.partner_id.find({"partner_id":str(id)}, {"_id": 0}).limit(1)

		if cursor.count() == 0:
			return {"response": "partner id does not exits"}

		else:
			for partner_id in cursor:
				if utc.localize(datetime.datetime.now()) < partner_id['expiration']:

					#print partner_id['expiration']
					del partner_id['expiration']
					data.append(partner_id)
					del cursor
				else:
					return {"response": "Ad expired for partner_id = " + str(partner_id['partner_id'])}
			
			return jsonify({"response": data})
class PartnerList(Resource):
	def get(self):
		return [x for x in mongo.db.partner_id.find({}, {"_id": 0, "expiration": 0}).limit(10)]



api = Api(app)
api.add_resource(PartnerList, "/", endpoint="list")
api.add_resource(PartnerPost, "/ad", endpoint="partner_id")
api.add_resource(PartnerGet, "/ad/<string:id>", endpoint = "id")



if __name__ == "__main__":
    app.run(debug=True, port=3000)