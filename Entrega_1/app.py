from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:d0p4m1n3Ru135!@localhost/dopamine_v2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)



class Usuario(db.Model):
	idUsuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
	NombreUsuario = db.Column(db.String(45), nullable=False)
	Email = db.Column(db.String(45), nullable=False)
	Pais = db.Column(db.String(45), nullable=False)
	PasswordHash = db.Column(db.String(100), nullable=False)
	DT = db.Column(db.TIMESTAMP, nullable=False)

	def __init__(self, NombreUsuario, Email, Pais, PasswordHash, DT):
		self.NombreUsuario = NombreUsuario
		self.Email = Email
		self.Pais = Pais
		self.PasswordHash = PasswordHash
		self.DT = DT

db.create_all()

class UserSchema(ma.Schema):
	class Meta:
		fields = ('idUsuario', 'NombreUsuario', 'Email', 'Pais', 'PasswordHash', 'DT')
user_schema = UserSchema()
users_schema = UserSchema(many=True)


##Ruta post
@app.route('/Usuario', methods=['POST'])
def create_user():
	NombreUsuario = request.json['NombreUsuario']
	Email = request.json['Email']
	Pais = request.json['Pais']
	PasswordHash = request.json['PasswordHash']
	DT = request.json['DT']
	new_user = Usuario(NombreUsuario,Email,Pais, PasswordHash, DT)
	db.session.add(new_user)
	db.session.commit()
	JUser = user_schema.jsonify(new_user)
	return jsonify({"Server Message":"User has been created sucessfully!", "test":str(new_user)})

##Ruta GET

# GET ALL
@app.route('/Usuario', methods=['GET'])  ##metodo get se incluye por defecto
def get_data():
	 all_users = Usuario.query.all()
	 result = users_schema.dump(all_users)
	 return jsonify({"message": "all users registered", "Usuarios": result})

#GET by id
@app.route('/Usuario/<id>', methods=['GET'])
def get_by_id(id):
	 user = Usuario.query.get(id)
	 return user_schema.jsonify(user)

#UPDATE by ID
@app.route("/Usuario/<id>", methods=['PUT'])
def update_user(id):
	user = Usuario.query.get(id)
	user.NombreUsuario = request.json["NombreUsuario"]
	user.Email =request.json["Email"]
	user.Pais = request.json["Pais"]
	user.PasswordHash = request.json["PasswordHash"]
	user.DT = request.json["DT"]
	db.session.commit()
	return jsonify({"message": "User has been updated sucessfully"})



#DELETE route
@app.route('/Usuario/<id>', methods=['DELETE'])
def delete_user(id):
  user = Usuario.query.get(id)
  db.session.delete(user)
  db.session.commit()

  all_users = Usuario.query.all()
  result = users_schema.dump(all_users)

  c = 0
  for user in all_users:
	  c+=1
  if c == 0:
	  return jsonify({"message": "No hay usuarios registrados"})
  return jsonify({"message": "User has been deleted sucessfully", "Users":result})


if __name__ == "__main__":


	app.run(debug=True)
