from flask import Flask, render_template, request, Response
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class sampleModel(db.Model):
    __tablename__ = 'Samples'
    sample_id = db.Column(db.Integer, primary_key = True)
    sample_date = db.Column(db.String, nullable = False)
    sample_name = db.Column(db.String(500), nullable = False)
    sample_location_latitude = db.Column(db.Float, nullable = False)
    sample_location_longtitude = db.Column(db.Float, nullable = False)
    sample_type = db.Column(db.String(100), nullable = False)
    sample_element = db.Column(db.String(100), nullable = False)
    sample_lambda = db.Column(db.String(100), nullable = False)
    sample_laserenergy = db.Column(db.String(100), nullable= False)
    sample_spotsize = db.Column(db.String(100), nullable = False)
    sample_size = db.Column(db.String(100), nullable = False)
    sample_timeperiod = db.Column(db.String(100), nullable = False)
    sample_peakvalue = db.Column(db.String(100), nullable = False)
    sample_1byepeakvalue = db.Column(db.String(100), nullable = False)
    sample_lifetime = db.Column(db.String(100), nullable = False)

class sampleReadingsModel(db.Model):
	__tablename__ = "SampleReadings"
	entry_id = db.Column(db.Integer, nullable = False, primary_key	 = True)
	sample_id = db.Column(db.Integer, nullable = False)
	sample_x = db.Column(db.String(100), nullable = False)
	sample_y = db.Column(db.String(100), nullable = False)

# db.create_all()

# Sample POST Arguments
sample_post_args = reqparse.RequestParser()
sample_post_args.add_argument("sample_date", type=str, help="Sample Date is required", required=True)
sample_post_args.add_argument("sample_name", type=str, help="Sample Name is required", required=True)
sample_post_args.add_argument("sample_location_latitude", type=str, help="Sample Location Latitude is required", required=True)
sample_post_args.add_argument("sample_location_longtitude", type=str, help="Sample Location Longitude is required", required=True)
sample_post_args.add_argument("sample_type", type=str, help="Sample Type is required is required", required=True)
sample_post_args.add_argument("sample_element", type=str, help="Sample Element is required", required=True)
sample_post_args.add_argument("sample_lambda", type=str, help="Sample Lambda Value is required", required=True)
sample_post_args.add_argument("sample_laserenergy", type=str, help="Sample Laser Energy is required", required=True)
sample_post_args.add_argument("sample_spotsize", type=str, help="Sample Spot Size is required", required=True)
sample_post_args.add_argument("sample_size", type=str, help="Sample Size is required", required=True)
sample_post_args.add_argument("sample_timeperiod", type=str, help="Sample Time Period is required", required=True)
sample_post_args.add_argument("sample_peakvalue", type=str, help="Sample Peak Value is required", required=True)
sample_post_args.add_argument("sample_1byepeakvalue", type=str, help="Sample 1 by e of Peak Value is required", required=True)
sample_post_args.add_argument("sample_lifetime", type=str, help="Sample Lifetime is required", required=True)


# Sample Reading Post Arguments
samplereading_post_args = reqparse.RequestParser()
samplereading_post_args.add_argument("sample_id", type=int, help= "Sample ID is required", required = True)
samplereading_post_args.add_argument("sample_x", type=str, help= "Sample X is required", required = True)
samplereading_post_args.add_argument("sample_y", type=str, help= "Sample Y is required", required = True)


# Sample Resource Fields
sample_resource_fields = {
	'sample_id':fields.Integer,
	'sample_date':fields.String,
	'sample_name':fields.String,
	'sample_location_latitude':fields.String,
	'sample_location_longtitude':fields.String,
	'sample_type':fields.String,
	'sample_element':fields.String,
	'sample_lambda':fields.String,
	'sample_laserenergy':fields.String,
	'sample_spotsize':fields.String,
	'sample_size':fields.String,
	'sample_timeperiod':fields.String,
	'sample_peakvalue':fields.String,
	'sample_1byepeakvalue':fields.String,
	'sample_lifetime':fields.String
}


# Sample Reading Resource Fields
samplereading_resource_fields = {
	'sample_id':  fields.Integer,
	'sample_x' : fields.String,
	'sample_y' : fields.String	
}

# Sample Resource
class SampleGetPost(Resource):

	# GET all Samples
	@marshal_with(sample_resource_fields)
	def get(self):
		result = sampleModel.query.all()
		return result

	# POST new Sample
	# payload : 
	# 	{
	# "sample_date":"2021-08-11",
	# "sample_name":"K19",
	# "sample_location_latitude":"12.30",
	# "sample_location_longtitude":"32.80",
	# "sample_type":"Temporal",
	# "sample_element":"Potassium",
	# "sample_lambda":"120",
	# "sample_laserenergy":"120mW",
	# "sample_spotsize":"10",
	# "sample_size":"1000",
	# "sample_timeperiod":"1ns",
	# "sample_peakvalue":"1078mV",
	# "sample_1byepeakvalue":"123mV",
	# "sample_lifetime":"100ns"
	# }
	
	@marshal_with(sample_resource_fields)
	def post(self):
		args = sample_post_args.parse_args()
		sample = sampleModel(
			sample_date = args['sample_date'],
			sample_name = args['sample_name'],
			sample_location_latitude = args['sample_location_latitude'],
			sample_location_longtitude =  args['sample_location_longtitude'],
			sample_type =  args['sample_type'],
			sample_element = args['sample_element'],
			sample_lambda = args['sample_lambda'],
			sample_laserenergy = args['sample_laserenergy'],
			sample_spotsize = args['sample_spotsize'],
			sample_size = args['sample_size'],
			sample_timeperiod = args['sample_timeperiod'],
			sample_peakvalue = args['sample_peakvalue'],
			sample_1byepeakvalue = args['sample_1byepeakvalue'],
			sample_lifetime = args['sample_lifetime'])
		db.session.add(sample)
		db.session.commit()
		return sample, 201

# SampleReading Resource
class SampleReadingGetPost(Resource):

	# GET all Sample Readings for Sample ID
	@marshal_with(samplereading_resource_fields)
	def get(self, sampleid):
		result = sampleReadingsModel.query.filter_by(sample_id = sampleid).all()
		return result

	# POST new Sample Reading for Sample ID
	# payload : 
	# 	{
	# "sample_id":1,
	# "sample_x":"1",
	# "sample_y":"12.30"
	# }
	
	@marshal_with(samplereading_resource_fields)
	def post(self, sample_id):
		args = samplereading_post_args.parse_args()
		sampleReading = sampleReadingsModel(
			sample_id = args['sample_id'],
			sample_x = args['sample_x'],
			sample_y = args['sample_y'])
		db.session.add(sampleReading)
		db.session.commit()
		return sampleReading, 201

# Endpoints
api.add_resource(SampleGetPost, "/api/sample/")
api.add_resource(SampleReadingGetPost, "/api/sample/<sampleid>")


if __name__ == "__main__":
	app.run(debug=True)