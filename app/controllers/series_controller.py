from flask import jsonify, request
from app.models.series_model import Serie
from app.models import DatabaseConnector
from psycopg2.errors import UniqueViolation, NullValueNotAllowed

VALUE_NAMES = ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]
VALUE_TYPES = {"serie": str, "seasons": int, "released_date": str, "genre": str, "imdb_rating": float}

def series():
    db = DatabaseConnector()
    db.create_table()

    db.get_conn_cur()
    
    query = """
        SELECT
            id, serie, seasons, to_char(released_date, 'DD/MM/YYYY') as released_date, genre, imdb_rating
        FROM
            ka_series;
    """
    
    db.cur.execute(query)
    
    series = db.cur.fetchall()
    
    formatted = []

    for row in series:
        formatted.append(dict(zip(VALUE_NAMES, row)))

    db.commit_and_close()


    return jsonify({"data": formatted}), 200

def select_by_id(id: int):
    try:
        id = int(id)

        db = DatabaseConnector()
        db.create_table()

        db.get_conn_cur()

        query = """
            SELECT
                id, serie, seasons, to_char(released_date, 'DD/MM/YYYY') as released_date, genre, imdb_rating
            FROM 
                ka_series
            WHERE
                id = %s
        """

        db.cur.execute(query, [id])

        response = db.cur.fetchone()
        formatted = dict(zip(VALUE_NAMES, response))

        db.commit_and_close()

        return jsonify({"data": formatted}), 200
    except TypeError:
        return jsonify({"error": "Not found"}), 404

def create():
    try:
        data = request.json

        for value in VALUE_NAMES:
            if not data.get(value) and value != "id":
                raise NullValueNotAllowed(f"{value} is necessary")

        invalid_values = {
            "invalid_values": {},
            "correct_values_type": {},
            "is_ok": True
        }

        for value in VALUE_NAMES:
            if value != "id" and not type(data[value]) == VALUE_TYPES[value]:
                invalid_values["invalid_values"][value] = data[value]
                invalid_values["correct_values_type"][value] = str(VALUE_TYPES[value])[8:-2]
                invalid_values["is_ok"] = False

        if not invalid_values["is_ok"]:
            del invalid_values["is_ok"]
            raise TypeError(invalid_values)

        serie = Serie(**data)

        serie.save_serie()

        print(serie.__dict__)

        return jsonify(serie.__dict__), 201

    except UniqueViolation as err:
        error_message =  {
            "error": err.args[0].split("=")[1].replace("\n", "")
        }

        return jsonify(error_message), 409

    except NullValueNotAllowed as err:
        return jsonify({"error": err.args[0]}), 400
    
    except TypeError as err:
        return jsonify(err.args[0]), 400