import os
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import pyodbc




app = Flask(__name__)
api = Api(app)


server = 'dist-6-505.uopnet.plymouth.ac.uk'
database = 'COMP2001_TLai'
username = 'TLai'
password = 'FaiE451*'



def get_db_connection():
    try:
        return pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={server}; DATABASE={database}; UID={username}; PWD={password};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=yes")
    except Exception as e:
        raise Exception(f"Error connecting to database: {e}")
    
print("Connection successful!")


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Trail Service"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#TRAIL API ENDPOINTS
class Trail(Resource):
    def get(self):
        """Fetch all trails from the database"""
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
            return jsonify({"error": str(e)})


class TrailDetail(Resource):
    def get(self, trail_id):
        """Fetch a specific trail by its ID"""
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

    def put(self, trail_id):
        """Update an existing trail by its ID"""
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

    def delete(self, trail_id):
        """Delete a trail by its ID"""
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM CW2.Trail WHERE TrailID = ?', (trail_id,))
            conn.commit()
            conn.close()

            return jsonify({"message": "Trail deleted successfully!"})

        except Exception as e:
            return jsonify({"error": str(e)})


 

#TRAIL-LOCATIONPOINT API ENDPOINTS
class TrailLocationPoint(Resource):
    # GET /trails/<id>/locationpoints: Fetch all location points for a specific trail
    def get(self, trail_id):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                SELECT LP.LocationPoint, LP.Latitude, LP.Longitude, LP.Description
                FROM CW2.TrailLocationPoint TLP
                JOIN CW2.LocationPoint LP ON TLP.LocationPoint = LP.LocationPoint
                WHERE TLP.TrailID = ?
            ''', (trail_id,))
            rows = cursor.fetchall()

            location_points = []
            for row in rows:
                location_point = {
                    'LocationPoint': row.LocationPoint,
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
    def post(self, trail_id):
        data = request.get_json()
        if not data.get('LocationPoint'):
            return jsonify({"error": "LocationPoint is required"})

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO CW2.TrailLocationPoint (TrailID, LocationPoint, OrderNo)
                VALUES (?, ?, ?)
            ''', (
                trail_id,
                data['LocationPoint'],
                data.get('OrderNo', 1)  
            ))

            conn.commit()
            conn.close()
            return jsonify({"message": "Location point added successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)})

    # DELETE /trails/<id>/locationpoints/<order_no>: Remove a location point from a trail
    def delete(self, trail_id, order_no):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM CW2.TrailLocationPoint WHERE TrailID = ? AND OrderNo = ?
            ''', (trail_id, order_no))

            conn.commit()
            conn.close()

            return jsonify({"message": "Location point removed successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)})


#LOCATIONPOINT API ENDPOINTS
class LocationPoint(Resource):
    # GET /locationpoints: Fetch all location points (admin functionality)
    def get(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM CW2.LocationPoint')
            rows = cursor.fetchall()

            location_points = []
            for row in rows:
                location_point = {
                    'LocationPoint': row.LocationPoint,
                    'Latitude': row.Latitude,
                    'Longitude': row.Longitude,
                    'Description': row.Description
                }
                location_points.append(location_point)

            conn.close()
            return jsonify(location_points)
        except Exception as e:
            return jsonify({"error": str(e)})
        


#OWNER API ENDPOINTS
class Owner(Resource):
    # GET /owners: Fetch all owners (admin functionality)
    def get(self):
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
    def post(self):
        data = request.get_json()
        if not data.get('OwnerName'):
            return jsonify({"error": "OwnerName is required"})

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO CW2.Owner (OwnerName)
                VALUES (?)
            ''', (data['OwnerName'],))

            conn.commit()
            conn.close()
            return jsonify({"message": "Owner created successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)})

    # GET /owners/<id>: Fetch owner details by ID
    def get(self, owner_id):
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
                return jsonify(owner)
            else:
                return jsonify({"error": "Owner not found"})
        except Exception as e:
            return jsonify({"error": str(e)})

api.add_resource(Trail, '/trails', endpoint="trails")
api.add_resource(TrailDetail, '/trails/<int:trail_id>', endpoint="traildetail")
api.add_resource(TrailLocationPoint, '/trails/<int:trail_id>/locationpoints', '/trails/<int:trail_id>/locationpoints/<int:order_no>')
api.add_resource(LocationPoint, '/locationpoints')
api.add_resource(Owner, '/owners', '/owners/<int:owner_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)



