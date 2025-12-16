import datetime
import os
import sqlite3

from flask import (Blueprint, Flask, flash, jsonify, redirect, render_template,
                   request, send_file)
from flask_jwt_extended import get_current_user, jwt_required
from pydantic import ValidationError

from app import db
from app.modules.myDBA.schema import UserCreate, UserUpdate
from app.modules.myDBA.service import (delete_all_table_data, export_table_sql,
                                       get_all_table_data, get_all_tables,
                                       import_table_sql)

bp = Blueprint('myDBA', __name__, url_prefix='/myDBA')

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
        return jsonify(list(tables))
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401

@bp.get('/showTable/<string:table_name>')
@jwt_required()
def list_data(table_name):
    user = get_current_user()
    if user.role == "admin":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 10000))
        data = get_all_table_data(db, table_name, skip, limit)
        return jsonify(data)
    else:
        return jsonify({"errors": "UNAUTORIZED"}), 401

@bp.get('/delete/<string:table_name1>')
@jwt_required()
def delete_table_data(table_name1):
    user = get_current_user()
    if user.role == "admin":
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 100))
        data = delete_all_table_data(db, table_name1, skip, limit)
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
@bp.get('/export/<string:table_name>')
@jwt_required()
def export_table(table_name):
    user = get_current_user()
    result = export_table_sql(table_name, db)
    if result:
        response = send_file(
            result,
            as_attachment=True,
            download_name=f"{table_name}.sql",
            mimetype="application/sql"
        )
        return response
    else:
        return jsonify({"error": "Failed to export table"}), 500

 
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
