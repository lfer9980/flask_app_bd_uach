import uuid
import hashlib
from app import db
from app import models
from . import admin_bp
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from app.models import User,Data
from app import login_manager
from flask_login import login_required
from flask_login import logout_user
from flask_login import current_user

from app import admin


""" obtener nombre usuario """
def get_current_username():
    current_id = current_user.id
    current_user_data = User.query.filter_by(id = current_id).first()
    current_name = current_user_data.username.capitalize()

    return current_name


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(str(user_id))

@admin_bp.route('/admin/home', methods=['GET'])
@login_required
def home():

    current_name = get_current_username()
    
    try:
        
        data =  Data.query.with_entities(Data.temp, Data.hum, Data.datetime).all()
    
    except Exception as e:
        
        print(e)
        
        flash("Error al conectarse en la base de datos", "error")
        
        return redirect(url_for('admin.home'), code = 302)
    else:
        
        if len(data):
            
            
            labels = [f'{d.datetime}' for d in data]
            
            temp = [f'{d[0]}' for d in data]
            
            hum = [f'{d[1]}' for d in data]
            
            print(hum, temp)
            
            return render_template('admin/home.html',
                           nombre = current_name,
                           marcador = True,
                           labels = labels,
                           temdata = temp,
                           humdata = hum
                           )
        
        else:
            
            
            return render_template('admin/home.html',
                           nombre = current_name,
                           marcador = False)

@admin_bp.route('/admin/registro', methods=['GET'])
@login_required
def registrar():
    current_name = get_current_username()
    
    return render_template('admin/registro.html', nombre = current_name)

@admin_bp.route('/admin/editar', methods=['GET'])
@login_required
def editar():
    current_name = get_current_username()
    return render_template('admin/editar.html', nombre = current_name)

@admin_bp.route('/api/v1/admin/registro', methods=['POST'])
def registro():
    
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    if username and password and email:
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        
        id = str(uuid.uuid4())
        
        user = models.User(id, username, email, hashed_password)
        
        try:
            
            db.session.add(user)
            
            db.session.commit()
            
        except:
            
            flash("Usuario ya registrado, intente otros datos", "error")
        
            return redirect(url_for('admin.home'), code = 302)
        
        else:
            
            flash('Usuario registrado correctamente', 'success')
            
            return redirect(url_for('admin.home'), code = 302)
    else:
        
        flash('Datos incompletos', 'warning')
        
        return redirect(url_for('admin.home'), code = 302)


@admin_bp.route("/api/v1/auth/admin/logout",  methods=['GET'])
@login_required
def logout():
    
    logout_user()
    
    return redirect(url_for('public.index'), code = 302)
