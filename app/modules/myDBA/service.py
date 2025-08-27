import datetime
from flask import abort, jsonify
from app.models import User
from app.utils import hash_password
from .schema import UserCreate
from app import jwt
from sqlalchemy import inspect, text
from sqlalchemy import Table, MetaData
import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename


@jwt.user_identity_loader
def user_identity_lookup(user):
    return str(user.id)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
'''
def create(user: UserCreate, db, provider):
    db_user = User(
        name=user.name,
        email=user.email,
        role=user.role,
        is_verified=user.is_verified,
        password=hash_password(user.password),
        provider=provider
    )
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user
'''

def get_all_tables(db, skip, limit):
    #return db.session.query(User).offset(skip).limit(limit).all()
    inspector = inspect(db.engine)
    #table_names = inspector.get_table_names()

    tables_info = []  # List to store all table details

    for table_name in inspector.get_table_names():
        table_details = {
            "table_name": table_name,
            "columns": [],
            "foreign_keys": [],
            "indexes": []
        }
        
        # Get column details
        for column in inspector.get_columns(table_name):
            table_details["columns"].append({
                "name": column["name"],
                "type": str(column["type"]),
                "nullable": column["nullable"],
                "default": column.get("default")
            })

        # Get foreign key details
        for fk in inspector.get_foreign_keys(table_name):
            table_details["foreign_keys"].append({
                "column": fk["constrained_columns"],
                "references": f"{fk['referred_table']}({fk['referred_columns']})"
            })

        # Get index details
        for index in inspector.get_indexes(table_name):
            table_details["indexes"].append({
                "name": index["name"],
                "columns": index["column_names"],
                "unique": index.get("unique", False)
            })

        # Append to the list
        tables_info.append(table_details)
    return tables_info

def get_all_table_data(db, table_name, skip, limit):
    tables_info = []  # List to store all table details
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=db.engine)
    table_details = {
            "columns": [],
            "rows": []
        }
    # Get column names
    column_names = [col.name for col in table.columns]
    
    table_details["columns"] = column_names
    query = db.session.query(table).offset(skip).limit(limit)
    result = [dict(row._mapping) for row in query]  # Convert result to dictionary
    
    table_details["rows"] = result

    #print(table_details)
    return table_details

def delete_all_table_data(db, table_name, skip, limit):
    metadata = MetaData()
    
    try:
        table = Table(table_name, metadata, autoload_with=db.engine)
    except Exception:
        return {"error": f"Table '{table_name}' not found"}, 404

    # Perform the deletion
    db.session.execute(table.delete())
    db.session.commit()
    return {"message": f"All data deleted from {table_name}"}
'''
def get_one_user(user_id, db):
    db_user = db.session.query(User).filter(User.id == user_id).first()
    if db_user is None:
        abort(404, description="User not found")
    return db_user
'''
'''
def get_user_by_email(email, db):
    db_user = db.session.query(User).filter(User.email == email).first()
    return db_user
'''
'''
def set_verification_code(email, code, db):
    db_user = get_user_by_email(email, db)
    if db_user:
        db_user.verification_code = code
        db.session.commit()
        db.session.refresh(db_user)
'''
'''
def get_verification_code(email, db):
    db_user = get_user_by_email(email, db)
    if db_user:
        return db_user.verification_code
    return None
'''
'''
def verify_account(email, db):
    db_user = get_user_by_email(email, db)
    if db_user:
        db_user.is_verified = True
        db.session.commit()
        db.session.refresh(db_user)
'''
'''
def update(user_id, user_data, db):
    db_user = db.session.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_data.name:
            db_user.name = user_data.name
        if user_data.email:
            db_user.email = user_data.email
        if user_data.role:
            db_user.role = user_data.role
        if user_data.is_verified is not None:
            db_user.is_verified = user_data.is_verified
        if user_data.password:
            db_user.password = hash_password(user_data.password)
        db.session.commit()
        db.session.refresh(db_user)
    else:
        abort(404, description="User not found")
    return db_user
'''
'''
def delete(user_id, db):
    db_user = db.session.query(User).filter(User.id == user_id).first()
    if db_user:
        db.session.delete(db_user)
        db.session.commit()
        return db_user
    else:
        abort(404, description="User not found")
'''
def export_table_sql(table_name, db):
    EXPORT_FOLDER = "app/exports"
    
    # Create the export folder if it doesn't exist
    if not os.path.exists(EXPORT_FOLDER):
        os.makedirs(EXPORT_FOLDER)
        
    try:
        # Initialize Metadata without the 'bind' argument
        metadata = MetaData()
        
        # Reflect the table using autoload_with
        table = Table(table_name, metadata, autoload_with=db.engine)
        
        # Generate the CREATE TABLE DDL
        table_ddl = str(CreateTable(table).compile(db.engine)).rstrip() + ";"
        
        # Define the output file path
        output_file = os.path.join(EXPORT_FOLDER, f"{table_name}.sql")
        # print('###########', output_file)
        # Open the output file and write SQL commands
        with open(output_file, 'w', encoding='utf-8') as f:
            # Write DROP TABLE IF EXISTS
            f.write(f"DROP TABLE IF EXISTS {table_name};\n\n")
            
            # Write CREATE TABLE statement
            f.write(f"{table_ddl}\n\n")
            
            # Fetch all rows from the table
            Session = sessionmaker(bind=db.engine)
            session = Session()
            results = session.query(table).all()
            
            # Get column names
            column_names = [column.name for column in table.columns]
            
           # Write INSERT statements for each row
            for row in results:
                values = ', '.join(
                    "NULL" if getattr(row, col) is None
                    else f"'{str(getattr(row, col))}'" if isinstance(getattr(row, col), str)
                    else f"'{getattr(row, col)}'" if isinstance(getattr(row, col), (datetime.date, datetime.datetime))
                    else str(getattr(row, col))
                    for col in column_names
                )
                insert_stmt = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({values});\n"
                f.write(insert_stmt)
                
        EXPORT_FOLDER = "exports"  
        output_file = os.path.join(EXPORT_FOLDER, f"{table_name}.sql")
        # print('@@@@@@@@@@@', output_file)

        print(f"SQL file '{output_file}' has been created successfully.")
        return output_file  # Return the path to the exported SQL file
    
    except Exception as e:
        print(f"Error exporting table {table_name}: {e}")
        return None  # Return None in case of failure

def import_table_sql(request, db):
    UPLOAD_FOLDER = "app/uploads"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'sql'}

    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    # Check if the file is empty
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Only .sql files are allowed"}), 400
    
    # Save the file securely
    # UPLOAD_FOLDER = "uploads"
    #file_path = os.path.exists(UPLOAD_FOLDER)
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    try:
        # Read and execute the SQL file
        with open(file_path, 'r', encoding='utf-8') as f:
            sql_commands = f.read()
        #print("file_path:",file_path)
        # Split the SQL commands by semicolon (to handle multiple statements)
        commands = [cmd.strip() for cmd in sql_commands.split(';') if cmd.strip()]
        
        # Execute each command using the database engine
        #with db.engine.connect() as connection:
        for cmd in commands:
            db.session.execute(text(cmd))
            db.session.commit()
            # print(cmd)
        
        # Optionally, delete the uploaded file after processing
        # os.remove(file_path)
        
        return jsonify({"message": "SQL file imported successfully"}), 200
    
    except Exception as e:
        # Log the error and return a response
        print(f"Error importing SQL file: {e}")
        return jsonify({"error": f"Failed to import SQL file: {str(e)}"}), 500

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'sql'}
