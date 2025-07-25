from flask import Flask
from db.init_db import create_table
import os
from flask_jwt_extended import JWTManager, jwt_required
from controllers.data import upload_csv, get_data, update_data, delete_data, authenticate

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app)

# Setup
create_table()

@app.route('/')
def hello():
    return 'Hello'

@app.route("/login", methods=["POST"])
def login():
    return authenticate()

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    return upload_csv()

@app.route('/get_data', methods=['GET'])
def fetch_by_name():
    return get_data()

@app.route('/update', methods=['PUT'])
def update_by_name():
    return update_data()

@app.route('/delete', methods=['DELETE'])
def delete():
    return delete_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)