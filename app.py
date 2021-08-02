from flask import Flask,jsonify,request
from werkzeug.utils import secure_filename
import os

Media = "./database"
app = Flask(__name__)

database = []

# endpoint to get data on all
@app.route("/",methods = ['GET'])
def get():
	return jsonify({'database':database})
	
# endpoint to get data on a specific pic
@app.route("/get/<int:id>",methods = ['GET'])
def get_one_item(id):
	pic = database[id]
	return jsonify({'pic':pic})

# endpoint to post a pic
# pic is saved to file "Media" in same firectory as app
# create the file called "database" to save pic
@app.route("/",methods = ['POST'])
def create():
	name = request.form.get('name')
	id = request.form.get('id')
	pic = request.files['pic']
	file_name = secure_filename(pic.filename)
	file_location = os.path.join(Media, file_name)
	pic.save(file_location)
	new_pic = {'name':name,'file_name':file_name,'file_location':file_location,
				'id':id}
	database.append(new_pic)
	return jsonify(database),200

# endpoint to update and change a pic
@app.route("/<int:id>",methods = ['PUT'])
def update(id):
	name = request.form.get('name')
	NewPic = request.files['pic']
	new_file_name = secure_filename(NewPic.filename)
	new_file_location = os.path.join(Media, new_file_name)
	NewPic.save(new_file_location)
	database[id]['file_name'] = new_file_name
	database[id]['file_location'] = new_file_location
	return jsonify({name:database[id]}),200


# endpoint to get delete a specific pic
@app.route("/pic/<int:id>",methods = ['DELETE'])
def item_delete(id):
	try:	
		database.pop(id)
		return jsonify(database)
	except:
		return'error deleting'
	

if __name__ == "__main__":
	app.run(debug =True)