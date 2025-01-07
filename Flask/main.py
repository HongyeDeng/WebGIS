from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, origins=["http://172.30.43.33:8080"])

db_config = {
    "dbname": "flaskdatabase",
    "user": "postgres",
    "password": "Jacket123123",
    "host": "localhost",  # Or your database host
    "port": 5432          # Default PostgreSQL port
}

@app.route('/cargo-insert', methods=['POST'])
def insert_cargoes():
    try:
        # Get data from the JSON request
        data = request.get_json()
        Info = data.get('Info')  # Extract the string value
        lng = float(data.get('lng'))  # Extract the longitude value
        lat = float(data.get('lat'))  # Extract the latitude value
        CargoesName = data.get('CargoName')
        CargoesType = data.get('CargoType')
        CargoesStatus = data.get('CargoStatus')
        CargoesWeight = float(data.get('CargoWeight'))

        print("Insert Info",CargoesName, CargoesType, CargoesWeight, CargoesStatus, lng, lat, Info)
        # Validate the data
        if not CargoesName or not CargoesType or CargoesWeight is None or not CargoesStatus or lng is None or lat is None:
            return jsonify({"error": "Missing required fields"}), 400
        if not Info:
            return jsonify({"error": "No string provided"}), 400

        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        MyPoint = sql.SQL("ST_SetSRID(ST_MakePoint(%s,%s), 3857)")
        # Define the insert query
        query = sql.SQL("""
            INSERT INTO cargo (cargoname, cargotype, weight, status, cargolocation, description) 
            VALUES (%s, %s, %s, %s, {}, %s)
        """).format(MyPoint)
        cur.execute(query, [CargoesName, CargoesType, CargoesWeight, CargoesStatus, lng, lat, Info])
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Data inserted successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cargo-get-data', methods=['GET'])
def get_all_cargoes():
    try:
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the select query
        query = sql.SQL("SELECT cargo_id, cargoname, cargotype, weight, status, description, ST_X(cargolocation) AS lng, ST_Y(cargolocation) AS lat FROM cargo")
        cur.execute(query)
        
        # Fetch all the results
        results = cur.fetchall()
        formatted_results = [
        {"cargo_id": row[0], "cargoname": row[1], "cargotype": row[2], "cargoweight":float(row[3]), "cargostatus":row[4], "Info":row[5], "lng": float(row[6]), "lat": float(row[7])}
        for row in results
        ]
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"data": formatted_results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/delete-cargoes', methods=['POST'])
def delete_cargoes():
    try:
        # Get data from the JSON request
        data = request.get_json()
        ids = data.get('ids')
        if ids is None:
            return jsonify({"error": "Marker ID is required"}), 400
        
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the delete query
        query = sql.SQL("DELETE FROM cargo WHERE cargo_id = ANY(%s)")
        cur.execute(query, (ids,))
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "All data deleted successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cargo-update', methods=['POST'])
def update_cargoes():
    try:
        # Get data from the JSON request
        data = request.get_json()
        CargoID = data.get('CargoID')  # Extract the cargo ID (required for updating)
        CargoesName = data.get('CargoName')
        CargoesType = data.get('CargoType')
        CargoesStatus = data.get('CargoStatus')
        CargoesWeight = data.get('CargoWeight')
        lng = data.get('lng')  # Longitude
        lat = data.get('lat')  # Latitude
        Info = data.get('Info')  # Description

        print("Update Info", CargoID, CargoesName, CargoesType, CargoesWeight, CargoesStatus, lng, lat, Info)

        # Validate required fields
        if not CargoID:
            return jsonify({"error": "Missing CargoID (required for updating)"}), 400
        if not CargoesName or not CargoesType or CargoesWeight is None or not CargoesStatus or lng is None or lat is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Define the update query with PostGIS geometry
        MyPoint = sql.SQL("ST_SetSRID(ST_MakePoint(%s, %s), 3857)")
        query = sql.SQL("""
            UPDATE cargo 
            SET cargoname = %s, cargotype = %s, weight = %s, status = %s, cargolocation = {}, description = %s
            WHERE cargo_id = %s
        """).format(MyPoint)

        # Execute the update query
        cur.execute(query, [CargoesName, CargoesType, CargoesWeight, CargoesStatus, lng, lat, Info, CargoID])
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Cargo data updated successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/truck-insert', methods=['POST'])
def intsert_truck():
    try:
        # Get data from the JSON request
        data = request.get_json()
        Info = data.get('Info')  # Extract the string value
        lng = float(data.get('lng'))  # Extract the longitude value
        lat = float(data.get('lat'))  # Extract the latitude value
        TruckName = data.get('TruckName')
        TruckType = data.get('TruckType')
        TruckStatus = data.get('TruckStatus')
        TruckWeight = float(data.get('TruckWeight'))

        print("Insert Info",TruckName, TruckType, TruckWeight, TruckStatus, lng, lat, Info)
        # Validate the data
        if not TruckName or not TruckType or TruckWeight is None or not TruckStatus or lng is None or lat is None:
            return jsonify({"error": "Missing required fields"}), 400
        if not Info:
            return jsonify({"error": "No string provided"}), 400

        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        MyPoint = sql.SQL("ST_SetSRID(ST_MakePoint(%s,%s), 3857)")
        # Define the insert query
        query = sql.SQL("""
            INSERT INTO trucks (truckname, trucktype, maximum_weight, status, trucklocation, description) 
            VALUES (%s, %s, %s, %s, {}, %s)
        """).format(MyPoint)
        cur.execute(query, [TruckName, TruckType, TruckWeight, TruckStatus, lng, lat, Info])
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Data inserted successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/truck-update', methods=['POST'])
def update_truck():
    try:
        # Get data from the JSON request
        data = request.get_json()
        Info = data.get('Info')  # Extract the string value
        lng = float(data.get('lng'))  # Extract the longitude value
        lat = float(data.get('lat'))  # Extract the latitude value
        TruckName = data.get('TruckName')
        TruckType = data.get('TruckType')
        TruckStatus = data.get('TruckStatus')
        TruckWeight = float(data.get('TruckWeight'))
        TruckID = data.get('TruckID')

        print("Update Info", TruckID, TruckName, TruckType, TruckWeight, TruckStatus, lng, lat, Info)

        # Validate required fields
        if not TruckID:
            return jsonify({"error": "Missing CargoID (required for updating)"}), 400
        if not TruckName or not TruckType or TruckWeight is None or not TruckStatus or lng is None or lat is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Define the update query with PostGIS geometry
        MyPoint = sql.SQL("ST_SetSRID(ST_MakePoint(%s, %s), 3857)")
        query = sql.SQL("""
            UPDATE trucks 
            SET truckname = %s, trucktype = %s, maximum_weight = %s, status = %s, trucklocation = {}, description = %s
            WHERE truck_id = %s
        """).format(MyPoint)

        # Execute the update query
        cur.execute(query, [TruckName, TruckType, TruckWeight, TruckStatus, lng, lat, Info, TruckID])
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Cargo data updated successfully!"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/truck-get-data', methods=['GET'])
def get_all_trucks():
    try:
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the select query
        query = sql.SQL("SELECT truck_id, truckname, trucktype, maximum_weight, status, description, ST_X(trucklocation) AS lng, ST_Y(trucklocation) AS lat, driver_id, associated_orders_id FROM trucks")
        cur.execute(query)
        
        # Fetch all the results
        results = cur.fetchall()
        formatted_results = [
        {"truck_id": row[0], "truckname": row[1], "trucktype": row[2], "truckweight":float(row[3]), "truckstatus":row[4], "Info":row[5], "lng": float(row[6]), "lat": float(row[7]), "driver_id": row[8], "associated_orders_id": row[9]}
        for row in results
        ]
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"data": formatted_results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/delete-trucks', methods=['POST'])
def delete_trucks():
    try:
        # Get data from the JSON request
        data = request.get_json()
        ids = data.get('ids')
        if ids is None:
            return jsonify({"error": "Marker ID is required"}), 400
        
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the delete query
        query = sql.SQL("DELETE FROM trucks WHERE truck_id = ANY(%s)")
        cur.execute(query, (ids,))
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "All data deleted successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cargo-add-route', methods=['POST'])
def cargo_add_route():
    try:
        # Get data from the JSON request
        data = request.get_json()
        CargoID = data.get('CargoID')
        polyline = data.get('polyline')
        if CargoID is None:
            return jsonify({"error": "Cargo ID is required"}), 400
        
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the delete query
        query = sql.SQL("""
            UPDATE cargo
            SET cargo_route = ST_GeomFromText(%s, 3857)  -- 3857 is the SRID for Web Mercator
            WHERE cargo_id = %s 
        """)
        cur.execute(query, (polyline, CargoID))
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Cargo route add successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cargo-delete-route', methods=['POST'])
def cargo_delete_route():
    try:
        # Get data from the JSON request
        data = request.get_json()
        CargoID = data.get('CargoID')

        if CargoID is None:
            return jsonify({"error": "Cargo ID is required"}), 400

        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()

        # Define the delete query
        query = sql.SQL("""
            UPDATE cargo
            SET cargo_route = NULL  -- Set the cargo_route column to NULL to remove the route
            WHERE cargo_id = %s
        """)
        cur.execute(query, (CargoID,))

        # Check if the CargoID existed and the route was deleted
        if cur.rowcount == 0:
            conn.rollback() # Roll back since nothing was updated
            cur.close()
            conn.close()
            return jsonify({"error": "Cargo ID not found or cargo route already empty"}), 404

        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "Cargo route deleted successfully!"}), 200

    except Exception as e:
        conn.rollback()  # Roll back changes if an error occurs
        return jsonify({"error": str(e)}), 500
    
@app.route("/getallroutes-cargo", methods=['GET'])
def cargo_get_all_route():
    try:
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the select query
        query = sql.SQL("SELECT cargo_id, cargotype, ST_AsGeoJSON(cargo_route) FROM cargo WHERE NOT ST_IsEmpty(cargo_route)")
        cur.execute(query)
        
        # Fetch all the results
        results = cur.fetchall()
        formatted_results = [
        {"cargo_id": row[0], "cargotype":row[1], "route": row[2]}
        for row in results
        ]
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"data": formatted_results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/getallroutes-truck", methods=['GET'])
def truck_get_all_route():
    try:
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the select query
        query = sql.SQL("SELECT truck_id, trucktype, ST_AsGeoJSON(truck_route) FROM trucks WHERE NOT ST_IsEmpty(truck_route)")
        cur.execute(query)
        
        # Fetch all the results
        results = cur.fetchall()
        formatted_results = [
        {"truck_id": row[0], "truck_type":row[1], "route": row[2]}
        for row in results
        ]
        
        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"data": formatted_results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/truck-add-route', methods=['POST'])
def truck_add_route():
    try:
        # Get data from the JSON request
        data = request.get_json()
        TruckID = data.get('TruckID')
        CargoID = data.get('CargoID')
        polyline = data.get('polyline')
        if TruckID is None:
            return jsonify({"error": "Truck ID is required"}), 400
        if CargoID is None:
            return jsonify({"error": "Cargo ID is required"}), 400
        
        # Establish the database connection
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Define the delete query
        query = sql.SQL("""
            UPDATE trucks
            SET cargo_id = %s, truck_route = ST_GeomFromText(%s, 3857)  -- 3857 is the SRID for Web Mercator
            WHERE truck_id = %s 
        """)
        cur.execute(query, (CargoID, polyline, TruckID))

        query = sql.SQL("""
            UPDATE cargo
            SET associated_truck_id = %s
            WHERE cargo_id = %s
        """)
        cur.execute(query, (TruckID, CargoID))

        # Commit changes and close the connection
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({"message": "Truck route add successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)