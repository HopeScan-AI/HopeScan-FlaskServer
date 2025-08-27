# routes/myDBA_routes.py
import datetime
from flask import Blueprint, flash, redirect, request, jsonify, render_template
from pydantic import ValidationError
from .schema import UserCreate, UserUpdate
from app import db
from .service import get_all_tables, get_all_table_data, delete_all_table_data, export_table_sql, import_table_sql
from flask_jwt_extended import jwt_required, get_current_user
from flask import Flask, request, jsonify, send_file
import sqlite3
import os


bp = Blueprint('myDBA', __name__, url_prefix='/myDBA')


# @bp.get("/page")
# @jwt_required()
# def serve_users_page():
#     user = get_current_user()
#     if user.role == "admin":
#         return render_template("myDBA.html", role=user.role)
#     else:
#         return jsonify({"errors": "UNAUTORIZED"}), 401
    
# @bp.get("/show/<string:table_name1>")
# @jwt_required()
# def serve_table_page(table_name1):
#     user = get_current_user()
#     if user.role == "admin":
#         return render_template("myDBATable.html", role=user.role, table_name = table_name1)
#     else:
#         return jsonify({"errors": "UNAUTORIZED"}), 401

'''@bp.post('/')
@jwt_required()
def create_user():
    try:
        user = get_current_user()
        if user.role == "admin":
            user_data = UserCreate(**request.json)
            saved_user = create(user_data, db, provider="email")
            return jsonify(saved_user.as_dict()), 201
        else:
            return jsonify({"errors": "UNAUTORIZED"}), 401
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
'''
@bp.get('/')
@jwt_required()
def list_users():
    user = get_current_user()
    if user.role == "admin":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        tables = get_all_tables(db, skip, limit)
        #print(tables)
        return jsonify(list(tables))
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401

@bp.get('/showTable/<string:table_name>')
@jwt_required()
def list_data(table_name):
    #print(table_name)
    user = get_current_user()
    if user.role == "admin":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        data = get_all_table_data(db, table_name, skip, limit)
        #row_dicts = [dict(row) for row in data]
        #return render_template("myDBA.html", role=user.role)
        return jsonify(data)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401

@bp.get('/delete/<string:table_name1>')
@jwt_required()
def delete_table_data(table_name1):
    #print(table_name)
    user = get_current_user()
    if user.role == "admin":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        data = delete_all_table_data(db, table_name1, skip, limit)
        #row_dicts = [dict(row) for row in data]
        #return render_template("myDBA.html", role=user.role)
        #return jsonify(data)
        return  jsonify({"siccess": "table deleted"}),200,
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401


'''@bp.get('/<int:user_id>')
@jwt_required()
def get_user(user_id):
    user = get_current_user()
    if user.role == "admin":
        db_user = get_one_user(user_id, db)
        return jsonify(db_user.as_dict())
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
'''
'''
@bp.put('/<int:user_id>')
@jwt_required()
def update_user(user_id):
    user = get_current_user()
    if user.role == "admin":
        user_data = UserUpdate(**request.json)
        db_user = update(user_id, user_data, db)
        return jsonify(db_user.as_dict())
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
'''
'''   
@bp.delete('/<int:user_id>')
@jwt_required()
def delete_user(user_id):
    user = get_current_user()
    if user.role == "admin":
        db_user = delete(user_id, db)
        return jsonify({"message": "User deleted", "user": db_user.as_dict()})
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
'''    
### API to Export a Table as SQL ###
@bp.get('/export/<string:table_name>')
@jwt_required()
def export_table(table_name):
    user = get_current_user()
    result = export_table_sql(table_name, db)
    #print("The Result:")
    #print(result)
    if result:
        response = send_file(
            result,
            as_attachment=True,
            download_name=f"{table_name}.sql",
            mimetype="application/sql"
        )
        # Delete the file after sending it
        # os.remove(result)
        return response
    else:
        return jsonify({"error": "Failed to export table"}), 500

 
# API to Import an SQL File ###
@bp.post('/import')
@jwt_required()
def import_table():
    user = get_current_user()
    if user.role == "admin":
        result = import_table_sql(request, db)
        if result:
            return jsonify({"succes": "Table Imported Successfully"}), 200
        else:
            return jsonify({"error": "Failed to export table"}), 500
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401
