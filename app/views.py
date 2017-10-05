from flask import render_template, flash, redirect, request
from app import app
from .database import Database
from .forms import LoginForm

from .validations import *

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Paulips'}  # usuario Test fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
                          
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if(request.method == 'POST'):
        error = None
        print("Hay un post :D")
        if(validRegisterForm(request.form)):
            createUser(request.form)
            status = "Cuenta registrada exitosamente"
        else:
            status = "El email ya fue registrado, prueba con una cuenta de correo diferente"
        print(status)            
        return render_template('registerResult.html',
                            title = 'Registro',
                            status = status)
        
            
            
    return render_template('registro.html',
                            title='Registro')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', 
                           title='Iniciar Sesión'
                           )
                           

@app.route('/balance')
def balance():
    return render_template('balance.html',
                            title='Balance')


@app.route('/gasto')
def gasto():
    return render_template('gasto.html',
                            title='Ingreso de gasto')                            
                           
                         
@app.route('/crearCategoria')
def crearCategoria():
    return render_template('crearCategoria.html',
                            title='Crear categoría')
