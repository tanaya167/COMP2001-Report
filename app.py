import requests
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import pyodbc
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from functools import wraps
from marshmallow.exceptions import ValidationError
from schemas import DeleteLocationPointSchema
from schemas import UserLoginSchema
from schemas import AdminLoginSchema
from schemas import AddLocationPointSchema



app = Flask(__name__)
api = Api(app)

# FLASK JWT
app.config['JWT_SECRET_KEY'] = '8251ed1fa49ae27f8f76985211ba9735e013fd65cfc85a0e901612a43a1f'  
jwt = JWTManager(app)

# DATABASE CONNECTION
server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_TLai'
username = 'TLai'
password = 'FaiE451*'

def get_db_connection():
    try:
        return pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                               f"SERVER={server}; DATABASE={database}; UID={username}; PWD={password};"
                               f"TrustServerCertificate=yes; Encrypt=yes")
    except Exception as e:
        raise Exception(f"Error connecting to database: {e}")

# SWAGGER UI  
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Trail Service"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Authenticator API URL
AUTH_API_URL = "https://web.socem.plymouth.ac.uk/COMP2001/auth/api/users"

   # POST /admin-login: Admin Login 
@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.get_json()

    schema = AdminLoginSchema()
    try:
        schema.load(data)  
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    if not data or 'Email_Address'not in data:
        return jsonify({"error": "Email_Address is required"}), 400

    email = data['Email_Address']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CW2.[User] WHERE Email_Address = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user is None:
            return jsonify({"error": "User not found"}), 404

        if user[2].lower() != 'admin': 
            return jsonify({"error": "Unauthorized: Admin role required"}), 403

        token = create_access_token(
            identity=email,  
            additional_claims={"role": user[2]},  
            expires_delta=timedelta(minutes=90) 
        )

        return jsonify({'message': 'Login successful', 'token': token}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
     # POST /login: User Login 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    schema = UserLoginSchema()
    try:
        schema.load(data) 
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400 

    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    username =data.get('username')

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    try:
        response = requests.post(AUTH_API_URL, json={"email": email, "password": password})

        print(f"Authenticator API response: {response.json()}")

        if response.status_code != 200:
            return jsonify({"error": "Invalid credentials or authentication failed"}), 401

        user_data = response.json()

        if user_data and len(user_data) > 1 and user_data[1] == "False":
            return jsonify({"error": "Authentication failed"}), 401

        token = create_access_token(
            identity=email, 
            additional_claims={"role": role, "username": username},  
            expires_delta=timedelta(minutes=90)
        )

        return jsonify({"token": token}), 200

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to connect to the Authenticator API: {str(e)}"}), 500


# GET /protected 
@app.route('/protected', methods=['GET'])
@jwt_required() 
def protected():
    current_user = get_jwt_identity()  
    return jsonify({"message": f"Hello, {current_user}!"})

# ROLE-BASED ACCESS CONTROL (RBAC)
def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
          
            jwt_data = get_jwt() 
            if jwt_data.get('role') != required_role:
                return jsonify({"error": "Forbidden: Insufficient privileges"}), 403

            return fn(*args, **kwargs)  

        return wrapper
    return decorator

# TRAIL API ENDPOINTS
    # GET /trails: Fetch all trails   
@app.route('/trails', methods=['GET'])
def getalltrails():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CW2.Trail') 
            rows = cursor.fetchall()

            trails = []
            for row in rows:
                trail = {
                    'TrailID': row.TrailID,
                    'TrailName': row.TrailName,
                    'TrailSummary': row.TrailSummary,
                    'TrailDescription': row.TrailDescription,
                    'Difficulty': row.Difficulty,
                    'Location': row.Location,
                    'Length': row.Length,
                    'ElevationGain': row.ElevationGain,
                    'RouteType': row.RouteType,
                    'OwnerID': row.OwnerID
                }
                trails.append(trail)

            conn.close()
            return jsonify(trails)  

        except Exception as e:
            return jsonify({"error": str(e)}), 500  
        
      # DELETE /trails: Add a new a trail   
@app.route('/trails', methods=['POST'])
@jwt_required()  
@role_required('admin')  
def newtrail():

        jwt_data = get_jwt()  

        print(f"JWT Data: {jwt_data}")  

        if jwt_data.get('role') != 'admin': 
            return jsonify({"error": "Forbidden: Insufficient privileges"}), 403

        data = request.get_json()

        required_fields = ['TrailID', 'TrailName', 'TrailSummary', 'TrailDescription', 
                       'Difficulty', 'Location', 'Length', 'ElevationGain', 'RouteType', 'OwnerID']
    
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO CW2.Trail (TrailID, TrailName, TrailSummary, TrailDescription, Difficulty, 
                    Location, Length, ElevationGain, RouteType, OwnerID) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data['TrailID'], data['TrailName'], data['TrailSummary'], data['TrailDescription'], 
                        data['Difficulty'], data['Location'], data['Length'], data['ElevationGain'], 
                        data['RouteType'], data['OwnerID']))

            conn.commit()
            conn.close()

            return jsonify({"message": "Trail added successfully!"}), 200

        except Exception as e:
            print("Error in POST:", str(e))
            return jsonify({"error": "An error occurred while adding the trail", "details": str(e)}), 500

#TRAIL-DETAIL API ENDPOINTS
    # GET /trails/<id>: Fetch trail by id
@app.route('/trails/<int:trail_id>', methods=['GET'])
@jwt_required()
def gettrailbyid(trail_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CW2.Trail WHERE TrailID = ?', (trail_id,))
            row = cursor.fetchone()

            if row:
                trail = {
                    'TrailID': row.TrailID,
                    'TrailName': row.TrailName,
                    'TrailSummary': row.TrailSummary,
                    'TrailDescription': row.TrailDescription,
                    'Difficulty': row.Difficulty,
                    'Location': row.Location,
                    'Length': row.Length,
                    'ElevationGain': row.ElevationGain,
                    'RouteType': row.RouteType,
                    'OwnerID': row.OwnerID
                }
                conn.close()
                return jsonify(trail)
            else:
                return jsonify({"error": "Trail not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)})
        
   # PUT /trails/<id>: Update a trails' details by id
@app.route('/trails/<int:trail_id>', methods=['PUT'])
@jwt_required() 
@role_required('admin')
def updatetrail(trail_id):
        data = request.get_json()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''UPDATE CW2.Trail SET 
                TrailName = ?, 
                TrailSummary = ?, 
                TrailDescription = ?, 
                Difficulty = ?, 
                Location = ?, 
                Length = ?, 
                ElevationGain = ?, 
                RouteType = ?, 
                OwnerID = ?
                WHERE TrailID = ?''', (
                data['TrailName'],
                data.get('TrailSummary', ''),
                data.get('TrailDescription', ''),
                data.get('Difficulty', ''),
                data.get('Location', ''),
                data.get('Length', 0),
                data.get('ElevationGain', 0),
                data.get('RouteType', ''),
                data.get('OwnerID', 1),  
                trail_id
            ))

            conn.commit()
            conn.close()
            return jsonify({"message": "Trail updated successfully!"})

        except Exception as e:
            return jsonify({"error": str(e)})
        
    # DELETE /trails/<id>: Delete a trail by id
@app.route('/trails/<int:trail_id>', methods=['DELETE'])
@jwt_required() 
@role_required('admin')
def deletetrailbyid(trail_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM CW2.Trail WHERE TrailID = ?', (trail_id,))
            conn.commit()
            conn.close()

            return jsonify({"message": "Trail deleted successfully!"})

        except Exception as e:
            return jsonify({"error": str(e)})

# TRAIL-LOCATIONPOINT API ENDPOINTS
    # GET /trails/<id>/locationpoints: Fetch all location points for a specific trail
@app.route('/trails/<int:trail_id>/locationpoints', methods=['GET'])
def getalllocationpointsfortrail(trail_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''SELECT LP.Location_Point, LP.Latitude, LP.Longitude, LP.Description
                            FROM CW2.Trail_LocationPoint T_LP
                            JOIN CW2.Location_Point LP ON T_LP.Location_Point = LP.Location_Point
                            WHERE T_LP.TrailID = ?''', (trail_id,))
            rows = cursor.fetchall()

            location_points = []
            for row in rows:
                location_point = {
                    'Location_Point': row.Location_Point,
                    'Latitude': row.Latitude,
                    'Longitude': row.Longitude,
                    'Description': row.Description
                }
                location_points.append(location_point)

            conn.close()
            return jsonify(location_points)
        except Exception as e:
            return jsonify({"error": str(e)})

    # POST /trails/<id>/locationpoints: Add a new location point to a trail
@app.route('/trails/<int:trail_id>/locationpoints', methods=['POST'])
@jwt_required() 
@role_required('admin')
def newlocationpoint(trail_id):
        data = request.get_json()

        schema = AddLocationPointSchema()
        try:
            schema.load(data)  
        except ValidationError as err:
            return jsonify({"error": err.messages}), 400
        
        if not data.get('Location_Point'):
            return jsonify({"error": "Location_Point is required"})

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO CW2.Trail_LocationPoint (TrailID, Location_Point, Order_no)
                            VALUES (?, ?, ?)''', (
                trail_id,
                data['Location_Point'],
                data.get('Order_no', 1)  
            ))

            conn.commit()
            conn.close()
            return jsonify({"message": "Location point added successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)})

    # DELETE /trails/<id>/locationpoints/<order_no>: Remove a location point from a trail
@app.route('/trails/<int:trail_id>/locationpoints/<order_no>', methods=['DELETE'])
@jwt_required() 
@role_required('admin')
def deletelocationpoint(trail_id, order_no):
        try:
            
            data = {
            "trail_id": trail_id,
            "order_no": order_no
             }
            
            schema = DeleteLocationPointSchema()
            schema.load(data)

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''DELETE FROM CW2.Trail_LocationPoint WHERE TrailID = ? AND Order_no = ?''', (trail_id, order_no))

            conn.commit()
            conn.close()

            return jsonify({"message": "Location point removed successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)})

# LOCATIONPOINT API ENDPOINTS
    # GET /locationpoints: Fetch all location points 
@app.route('/locationpoints', methods=['GET'])
@jwt_required() 
@role_required('admin')
def getalllocationpoints():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CW2.Location_Point')
            rows = cursor.fetchall()

            location_points = []
            for row in rows:
                location_point = {
                    'Location_Point': row.Location_Point,
                    'Latitude': row.Latitude,
                    'Longitude': row.Longitude,
                    'Description': row.Description
                }
                location_points.append(location_point)

            conn.close()
            return jsonify(location_points)
        except Exception as e:
            return jsonify({"error": str(e)})

# OWNER API ENDPOINTS
    # GET /owners: Fetch all owners 
@app.route('/owners', methods=['GET'])
@jwt_required() 
@role_required('admin')
def getallowners(): 
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CW2.Owner')
            rows = cursor.fetchall()

            owners = []
            for row in rows:
                owner = {
                    'OwnerID': row.OwnerID,
                    'OwnerName': row.OwnerName
                }
                owners.append(owner)

            conn.close()
            return jsonify(owners)
        except Exception as e:
            return jsonify({"error": str(e)})

    # POST /owners: Create a new owner
@app.route('/owners', methods=['POST'])
@jwt_required() 
@role_required('admin')
def newowner():
        data = request.get_json()
        if not data.get('OwnerName'):
            return jsonify({"error": "OwnerName is required"})

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''INSERT INTO CW2.Owner (OwnerID, OwnerName) VALUES (?, ?)''', (data['OwnerID'], data['OwnerName'],))

            conn.commit()
            conn.close()
            return jsonify({"message": "Owner created successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)})
        


    # GET /owners/<id>: Fetch owner details by id
@app.route('/owners/<int:owner_id>', methods=['GET'])
@jwt_required() 
@role_required('admin')
def getownerbyid(owner_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CW2.Owner WHERE OwnerID = ?', (owner_id,))
            row = cursor.fetchone()

            if row:
                owner = {
                    'OwnerID': row.OwnerID,
                    'OwnerName': row.OwnerName
                }
                conn.close()
                return jsonify(owner)
            else:
                return jsonify({"error": "Owner not found"}), 404
        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)







