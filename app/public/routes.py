import os
import uuid
import hashlib
from app import db
from app import models
from . import public_bp
from flask import request
from flask import jsonify
from flask import flash
from flask import render_template
from flask import redirect
from flask import url_for
from app import login_manager 
from datetime import datetime
from flask_login import login_user



@public_bp.before_app_first_request
def create_db():

    db.create_all()
    
    if not models.User.query.first():
        
        id = str(uuid.uuid4())

        admin = models.User(id = id,
                            username = os.environ.get("ADMIN_USER"),
                            password = hashlib.sha256(os.environ.get("ADMIN_PSS").encode('utf-8')).hexdigest(),
                            email = os.environ.get("EMAIL_ADMIN")
                            )

        db.session.add(admin)
        db.session.commit()
    
    id = str(uuid.uuid4())
    hum = 80
    temp = 25
    date = datetime.now()
    
    jeje = models.Data(id = id,
                       hum = hum,
                       temp = temp,
                       datetime = date)
    
    db.session.add(jeje)
    db.session.commit()
        
        
@public_bp.route('/', methods=['GET'])
def index():
    
    message = {'message': 'Proyecto de base de datos, control de un sistema de riego',
               'login': '/api/v1/login',
               'datos': '/api/v1/datos',
               'formato': 'json',
               'integrantes': 'Jessy Garcia, Luis Fernandez, Melanie Delgado, Jesus Hernandez, Miguel Barrera',
               'grupo': '7IB1',
               'Materia': 'Base de datos'}
    
    return render_template('index.html', message=message)


@public_bp.route('/registro', methods=['GET'])
def registro_get():
    
    return render_template('registro.html')

@public_bp.route('/api/v1/public/login', methods=['POST'])
def login():
    
    usuario = request.form['username']
    password = request.form['password']

    if usuario and password:
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        user = models.User.query.filter_by(username = usuario,
                                           password = hashed_password).first()
        
        if user:
            
            
            login_user(user)
            
            return redirect(url_for('admin.home'), code = 302)
        
        else:
            
            flash("Usuario o password incorrectos", "error")
            
            return redirect(url_for('public.index'), code = 302)
    
    else:
        
        flash("Datos incompletos", "warning")
            
        return redirect(url_for('public.index'), code = 302)

@public_bp.route('/api/v1/public/datos', methods=['POST'])
def data():
    
    try:
        id = str(uuid.uuid4())
        temp = float(request.form['temp'])
        hum = float(request.form['hum'])
        time = datetime.now()
    
    except:
        
        message = {'message': 'Datos incompletos o incorrectos',
                   'code': 200,
                   'status': 'False'}
        
        return jsonify(message)
        
    else:  
          
        data = {
            'id': id,
            'temp': temp,
            'hum': hum,
            'datetime': time
        }
        
        data = models.Data(**data)
        
        try:
            
            db.session.add(data)
            
        except:
            
            message = {'message': 'Error al guardar los datos',
                       'code': 502,
                       'status': 'Error'}
            
            return jsonify(message)
        
        else:
            
            db.session.commit()
            
            message = {'message': 'Datos guardados correctamente',
                       'code': 200,
                       'status': 'True'}
            
            return jsonify(message)
        
@login_manager.user_loader
def load_user(user_id):

    return models.User.query.get(str(user_id))