import os
from flask import Flask, request, jsonify, Response
from markupsafe import escape
from db import init_db, query_db



def init_reservation():

    app = Flask(__name__)


    
    def datify(date):
        """
        Replaces occurrences of '--' with ' ' in a date string.
    
        Args:
            date (str): The input date string.
    
        Returns:
            str: The modified date string.
        """
        return date.replace('--', ' ')
    
    
    @app.route('/tables', methods=['GET'])
    def get_tables():
        """
        Retrieves table information 
    
        Returns:
            Response: JSON representation of the table information.
        """
    
       
        # Query the database to get table information based on the provided time
        results = query_db("SELECT * FROM tische")
        return jsonify(results)
    
    @app.route('/tables/unreserved', methods=['GET'])
    def tables_unreserved():
        time = request.args.get('timestamp')
        if time is None:
            return Response('No timestamp provided', status=400)
        results = query_db("""
SELECT t.tischnummer, t.anzahlPlaetze
FROM tische t
LEFT JOIN reservierungen r ON t.tischnummer = r.tischnummer
WHERE r.tischnummer IS NULL OR r.zeitpunkt != ?;""", (datify(time) , ) )
        return jsonify(results)
            

#Delete route patch / reservation post is missing.
     
    @app.route('/reservation', methods=['GET'])
    def get_reservations():
        """
        Retrieves all reservations from the database.
    
        Returns:
            Response: JSON representation of all reservations.
        """
        results = query_db("SELECT * FROM reservierungen")
        return jsonify(results)
    return app
if __name__ == '__main__':
    app = init_reservation()
    init_db(app)
    app.run()
 
 