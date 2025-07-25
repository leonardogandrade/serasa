from flask import request, jsonify
from flask_jwt_extended import create_access_token
import os
import io
import csv
from psycopg2 import sql
from db.init_db import get_db_connection

SECRET_KEY = os.getenv("SECRET_KEY")

COLUMNS = [
'nome', 'nome_social', 'email', 'idade', 'cep', 
'numero', 'rua', 'bairro', 'cidade', 'estado', 
'pais', 'profissao'
]

def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400
    
    try:
        stream = io.StringIO(file.stream.read().decode('UTF-8'), newline=None)
        csv_reader = csv.DictReader(stream)
        
        if not all(col in csv_reader.fieldnames for col in COLUMNS):
            return jsonify({'error': 'CSV file is missing required columns'}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        inserted_rows = 0
        
        for row in csv_reader:
            data = [row.get(col) for col in COLUMNS]
            
            insert_query = sql.SQL("""
            INSERT INTO pessoas ({})
            VALUES ({})
            """).format(sql.SQL(', ').join(map(sql.Identifier, COLUMNS)), sql.SQL(', ').join(sql.Placeholder() * len(COLUMNS)))
            
            cur.execute(insert_query, data)
            inserted_rows += 1
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            'message': f'Successfully uploaded and inserted {inserted_rows} rows'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_data():

    nome = request.args.get('nome')
    if not nome:
        return jsonify({'error': 'Nome parameter is required'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        select_query = sql.SQL("""
        SELECT {} FROM pessoas WHERE nome = %s
        """).format(sql.SQL(', ').join(map(sql.Identifier, COLUMNS)))
        
        cur.execute(select_query, (nome,))
        result = cur.fetchone()
        
        cur.close()
        conn.close()
        
        if not result:
            return jsonify({'message': 'No record found with that nome'}), 404
        
        data = dict(zip(COLUMNS, result))
        return jsonify(data), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def update_data():
    nome = request.args.get('nome')
    
    if not nome:
        return jsonify({'error': 'Nome parameter is required'}), 400
    
    update_data = request.json
    if not update_data:
        return jsonify({'error': 'No update data provided'}), 400
    
    valid_updates = {k: v for k, v in update_data.items() if k in COLUMNS and k != 'nome'}
    if not valid_updates:
        return jsonify({'error': 'No valid fields to update'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        update_query = sql.SQL("""
        UPDATE pessoas SET {}
        WHERE nome = %s
        RETURNING {}
        """).format(
            sql.SQL(', ').join(
                sql.SQL("{} = %s").format(sql.Identifier(k)) 
                for k in valid_updates.keys()
            ),
            sql.SQL(', ').join(map(sql.Identifier, COLUMNS))
        )
        
        cur.execute(update_query, list(valid_updates.values()) + [nome])
        updated_record = cur.fetchone()
        
        if not updated_record:
            conn.rollback()
            return jsonify({'message': 'No record found with that nome'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        data = dict(zip(COLUMNS, updated_record))
        return jsonify({
            'message': 'Record updated successfully',
            'data': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def delete_data():
    nome = request.args.get('nome')
    if not nome:
        return jsonify({'error': 'Nome parameter is required'}), 400
    
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        select_query = sql.SQL("""
        SELECT {} FROM pessoas WHERE nome = %s
        """).format(sql.SQL(', ').join(map(sql.Identifier, COLUMNS)))
        
        cur.execute(select_query, (nome,))
        record = cur.fetchone()
        
        if not record:
            return jsonify({'message': 'No record found with that nome'}), 404
        
        delete_query = "DELETE FROM pessoas WHERE nome = %s"
        cur.execute(delete_query, (nome,))
        rows_deleted = cur.rowcount
        
        conn.commit()
        cur.close()
        conn.close()
        
        if rows_deleted == 0:
            return jsonify({'message': 'No record deleted'}), 404
        
        data = dict(zip(COLUMNS, record))
        return jsonify({
            'message': 'Record deleted successfully',
            'deleted_data': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
def authenticate():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username == "admin" and password == "admin":
        access_token = create_access_token(identity="user_id_here")
        return jsonify(access_token=access_token)
    
    return jsonify({"msg": "Bad username or password"}), 401